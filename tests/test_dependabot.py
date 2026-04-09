from pathlib import Path

import yaml


def _dependabot_package_ecosystems() -> set[str]:
    data = yaml.safe_load(Path(".github/dependabot.yml").read_text(encoding="utf-8"))
    return {
        update["package-ecosystem"]
        for update in data.get("updates", [])
        if "package-ecosystem" in update
    }


def test_dependabot_configuration_exists_for_pip_and_actions():
    assert _dependabot_package_ecosystems() == {"github-actions", "pip"}


def test_dependabot_package_ecosystems_are_loaded_structurally():
    data = yaml.safe_load(Path(".github/dependabot.yml").read_text(encoding="utf-8"))
    assert isinstance(data.get("updates"), list)
