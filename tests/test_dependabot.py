from pathlib import Path


def test_dependabot_configuration_exists_for_pip_and_actions():
    text = Path(".github/dependabot.yml").read_text(encoding="utf-8")
    assert "package-ecosystem: github-actions" in text
    assert 'package-ecosystem: "pip"' in text
