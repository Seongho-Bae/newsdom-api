from pathlib import Path


def test_security_policy_file_exists():
    assert Path("SECURITY.md").exists()


def test_security_policy_covers_reporting_and_supported_branches():
    text = Path("SECURITY.md").read_text(encoding="utf-8")
    assert "report a vulnerability" in text.lower()
    assert "develop" in text
    assert "main" in text


def test_readme_and_contributing_link_security_policy():
    assert "SECURITY.md" in Path("README.md").read_text(encoding="utf-8")
    assert "SECURITY.md" in Path("CONTRIBUTING.md").read_text(encoding="utf-8")
