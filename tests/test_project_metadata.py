from pathlib import Path


def test_project_metadata_does_not_bundle_mineru_extra():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert "mineru[pipeline]" not in text
