from pathlib import Path


def test_readme_mentions_copyright_safe_fixture():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "synthetic" in text.lower()
    assert "copyright" in text.lower()
