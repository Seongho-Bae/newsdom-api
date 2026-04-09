from pathlib import Path

import yaml


def test_coderabbit_configuration_file_exists():
    assert Path(".coderabbit.yaml").exists()


def test_coderabbit_request_changes_workflow_is_enabled():
    data = yaml.safe_load(Path(".coderabbit.yaml").read_text(encoding="utf-8"))
    assert data["reviews"]["request_changes_workflow"] is True
