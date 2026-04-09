import json
from pathlib import Path


def test_release_workflow_exists():
    assert Path(".github/workflows/release.yml").exists()


def test_release_workflow_mentions_attestation_and_checksums():
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "attest-build-provenance" in text
    assert "sha256sum" in text


def test_release_manifest_script_exists():
    assert Path("scripts/release/build_release_manifest.py").exists()


def test_release_manifest_script_outputs_json(tmp_path: Path):
    from scripts.release.build_release_manifest import build_manifest

    dist = tmp_path / "dist"
    dist.mkdir()
    artifact = dist / "demo.txt"
    artifact.write_text("demo", encoding="utf-8")
    manifest = build_manifest(dist)
    assert manifest["artifacts"][0]["name"] == "demo.txt"
    assert manifest["artifacts"][0]["sha256"]
    json.loads(json.dumps(manifest))
