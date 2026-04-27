import hashlib
import json
import subprocess
from pathlib import Path
import re
from typing import Any, cast

import pytest
import yaml


def _release_workflow() -> dict[str, Any]:
    return yaml.safe_load(Path(".github/workflows/release.yml").read_text(encoding="utf-8"))


def _release_workflow_steps(job_name: str) -> list[dict[str, Any]]:
    return _release_workflow()["jobs"][job_name]["steps"]


def _find_step_by_uses(steps: list[dict[str, Any]], uses: str) -> dict[str, Any]:
    match = next(
        (
            step
            for step in steps
            if re.match(rf"{re.escape(uses)}@[0-9a-fA-F]{{40}}", step.get("uses", ""))
        ),
        None,
    )
    assert match is not None, f"missing workflow step for uses={uses!r}"
    return match


def test_release_workflow_exists():
    assert Path(".github/workflows/release.yml").exists()


def test_release_workflow_mentions_attestation_and_checksums():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "uses: actions/attest-build-provenance@" in text
    assert re.search(r"sha256sum dist/\* > dist/SHA256SUMS.txt", text)
    assert (
        'python scripts/release/export_release_attestations.py dist "${GITHUB_REPOSITORY}"'
        in text
    )


def test_release_manifest_script_exists():
    assert Path("scripts/release/build_release_manifest.py").exists()


def test_release_attestation_export_script_exists():
    assert Path("scripts/release/export_release_attestations.py").exists()


def test_release_manifest_script_outputs_json(tmp_path: Path):
    from scripts.release.build_release_manifest import build_manifest

    dist = tmp_path / "dist"
    dist.mkdir()
    artifact = dist / "demo.txt"
    artifact.write_text("demo", encoding="utf-8")
    manifest_path = dist / "release-manifest.json"
    manifest_path.write_text("{}", encoding="utf-8")
    manifest = build_manifest(dist)
    artifacts = cast(list[dict[str, Any]], manifest["artifacts"])
    expected_sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
    assert len(artifacts) == 1
    assert artifacts[0]["name"] == "demo.txt"
    assert artifacts[0]["size"] == artifact.stat().st_size
    assert artifacts[0]["sha256"] == expected_sha
    assert all(item["name"] != "release-manifest.json" for item in artifacts)
    json.loads(json.dumps(manifest))


def test_release_manifest_script_excludes_explicit_output_path(tmp_path: Path):
    from scripts.release.build_release_manifest import build_manifest

    dist = tmp_path / "dist"
    dist.mkdir()
    artifact = dist / "demo.txt"
    artifact.write_text("demo", encoding="utf-8")
    output_path = dist / "custom-manifest.json"
    output_path.write_text("{}", encoding="utf-8")

    manifest = build_manifest(dist, exclude={output_path})
    artifacts = cast(list[dict[str, Any]], manifest["artifacts"])

    assert [item["name"] for item in artifacts] == ["demo.txt"]


def test_release_workflow_publish_step_is_idempotent():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert 'gh release view "${GITHUB_REF_NAME}"' in text
    assert 'gh release upload "${GITHUB_REF_NAME}" dist/* --clobber' in text
    assert 'gh release create "${GITHUB_REF_NAME}" dist/* --generate-notes' in text


def test_release_workflow_pins_uv_version():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "astral-sh/setup-uv@" in text
    assert "version: '0.11.3'" in text


def test_release_workflow_splits_build_and_publish_permissions():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    workflow_header, _jobs_section = text.split("jobs:", 1)
    workflow = _release_workflow()

    assert "contents: read" in workflow_header
    assert "contents: write" not in workflow_header

    build_job = workflow["jobs"]["build-release"]
    publish_job = workflow["jobs"]["publish-release"]

    assert build_job["permissions"] == {
        "contents": "read",
        "attestations": "write",
        "id-token": "write",
    }
    assert publish_job["permissions"] == {
        "contents": "write",
        "actions": "read",
    }
    assert publish_job["needs"] == "build-release"


def test_release_workflow_uploads_intoto_assets_with_release_artifacts():
    upload_step = next(
        step
        for step in _release_workflow_steps("build-release")
        if step.get("name") == "Upload release artifacts"
    )

    assert "dist/*.intoto.jsonl" in upload_step["with"]["path"]


def test_release_workflow_exports_attestations_before_uploading_artifacts():
    step_names = [step.get("name") for step in _release_workflow_steps("build-release")]
    assert step_names.index("Export release attestation bundles") < step_names.index(
        "Upload release artifacts"
    )


def test_release_workflow_downloads_artifacts_before_publish_step():
    step_names = [step.get("name") for step in _release_workflow_steps("publish-release")]

    assert step_names.index("Download release artifacts") < step_names.index(
        "Publish GitHub release"
    )


def test_release_workflow_uses_pinned_download_artifact_action_for_publish_job():
    publish_steps = _release_workflow_steps("publish-release")
    download_step = _find_step_by_uses(publish_steps, "actions/download-artifact")

    assert download_step["with"]["name"] == "release-artifacts"
    assert download_step["with"]["path"] == "dist"


def test_release_attestation_export_script_hashes_artifacts_in_chunks(tmp_path: Path):
    from scripts.release.export_release_attestations import _sha256_file

    artifact = tmp_path / "demo.bin"
    artifact.write_bytes(b"newsdom-" * 4096)

    assert _sha256_file(artifact) == hashlib.sha256(artifact.read_bytes()).hexdigest()


def test_release_attestation_export_script_writes_named_intoto_files(
    tmp_path: Path, monkeypatch
):
    from scripts.release.export_release_attestations import (
        ATTESTATION_DOWNLOAD_TIMEOUT_SECONDS,
        export_attestations,
    )

    dist = tmp_path / "dist"
    dist.mkdir()
    artifact = dist / "demo.whl"
    artifact.write_text("demo", encoding="utf-8")

    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    downloaded = tmp_path / f"sha256:{digest}.jsonl"
    downloaded.write_text('{"bundle": true}', encoding="utf-8")

    calls: list[tuple[list[str], Path, int]] = []
    monkeypatch.setattr(
        "scripts.release.export_release_attestations.shutil.which",
        lambda name: "/usr/bin/gh" if name == "gh" else None,
    )

    def fake_run(cmd, check, cwd, timeout):
        calls.append((cmd, cwd, timeout))
        assert check is True
        assert cwd == tmp_path
        assert timeout == ATTESTATION_DOWNLOAD_TIMEOUT_SECONDS

    monkeypatch.setattr(
        "scripts.release.export_release_attestations.subprocess.run", fake_run
    )

    export_attestations(dist, "Seongho-Bae/newsdom-api", working_dir=tmp_path)

    assert calls == [
        (
            [
                "/usr/bin/gh",
                "attestation",
                "download",
                str(artifact.resolve()),
                "-R",
                "Seongho-Bae/newsdom-api",
            ],
            tmp_path,
            ATTESTATION_DOWNLOAD_TIMEOUT_SECONDS,
        )
    ]
    assert (dist / "demo.whl.intoto.jsonl").read_text(
        encoding="utf-8"
    ) == '{"bundle": true}'


def test_release_attestation_export_script_fails_fast_on_download_timeout(
    tmp_path: Path, monkeypatch
):
    from scripts.release.export_release_attestations import export_attestations

    dist = tmp_path / "dist"
    dist.mkdir()
    artifact = dist / "demo.whl"
    artifact.write_text("demo", encoding="utf-8")

    monkeypatch.setattr(
        "scripts.release.export_release_attestations.shutil.which",
        lambda name: "/usr/bin/gh" if name == "gh" else None,
    )

    def fake_run(cmd, check, cwd, timeout):
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=timeout)

    monkeypatch.setattr(
        "scripts.release.export_release_attestations.subprocess.run", fake_run
    )

    with pytest.raises(RuntimeError, match=r"demo\.whl"):
        export_attestations(dist, "Seongho-Bae/newsdom-api", working_dir=tmp_path)
