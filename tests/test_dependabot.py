import re
from pathlib import Path


def test_dependabot_configuration_exists_for_pip_and_actions():
    text = Path(".github/dependabot.yml").read_text(encoding="utf-8")
    assert re.search(r'package-ecosystem:\s*"?github-actions"?', text)
    assert re.search(r'package-ecosystem:\s*"?pip"?', text)
