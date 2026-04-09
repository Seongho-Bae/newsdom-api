from pathlib import Path


def test_changelog_exists_and_uses_keep_a_changelog_format():
    text = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert text.startswith("# Changelog")
    assert "Keep a Changelog" in text
    assert "## [Unreleased]" in text
    assert "Semantic Versioning" in text
