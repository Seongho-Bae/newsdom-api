import hashlib
import json
from pathlib import Path
import re


def test_release_workflow_exists():
    assert Path(".github/workflows/release.yml").exists()


def test_release_workflow_mentions_attestation_and_checksums():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "uses: actions/attest-build-provenance@" in text
    assert re.search(r"sha256sum dist/\* > dist/SHA256SUMS.txt", text)


def test_release_manifest_script_exists():
    assert Path("scripts/release/build_release_manifest.py").exists()


def test_release_manifest_script_outputs_json(tmp_path: Path):
    from scripts.release.build_release_manifest import build_manifest

    dist = tmp_path / "dist"
    dist.mkdir()
    artifact = dist / "demo.txt"
    artifact.write_text("demo", encoding="utf-8")
    manifest_path = dist / "release-manifest.json"
    manifest_path.write_text("{}", encoding="utf-8")
    manifest = build_manifest(dist)
    expected_sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
    assert len(manifest["artifacts"]) == 1
    assert manifest["artifacts"][0]["name"] == "demo.txt"
    assert manifest["artifacts"][0]["size"] == artifact.stat().st_size
    assert manifest["artifacts"][0]["sha256"] == expected_sha
    assert all(
        item["name"] != "release-manifest.json" for item in manifest["artifacts"]
    )
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

    assert [item["name"] for item in manifest["artifacts"]] == ["demo.txt"]


def test_release_workflow_publish_step_is_idempotent():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert 'gh release view "${GITHUB_REF_NAME}"' in text
    assert 'gh release upload "${GITHUB_REF_NAME}" dist/* --clobber' in text
    assert 'gh release create "${GITHUB_REF_NAME}" dist/* --generate-notes' in text


def test_release_workflow_pins_uv_version():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "astral-sh/setup-uv@" in text
    assert "version: '0.11.3'" in text


def test_release_workflow_scopes_write_permissions_to_job_level():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "contents: read" in text.split("jobs:", 1)[0]
    assert "contents: write" not in text.split("jobs:", 1)[0]
    assert "contents: write" in text.split("jobs:", 1)[1]
    assert "attestations: write" in text.split("jobs:", 1)[1]
    assert "id-token: write" in text.split("jobs:", 1)[1]
