from pathlib import Path

import yaml


def _workflow_paths() -> list[Path]:
    return sorted(Path(".github/workflows").glob("*.yml")) + sorted(
        Path(".github/workflows").glob("*.yaml")
    )


def test_each_workflow_job_forces_javascript_actions_to_node24():
    for workflow_path in _workflow_paths():
        data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        for job_name, job_data in data["jobs"].items():
            assert job_data["env"]["FORCE_JAVASCRIPT_ACTIONS_TO_NODE24"] is True, (
                workflow_path,
                job_name,
            )


def test_workflows_do_not_use_top_level_env_blocks():
    for workflow_path in _workflow_paths():
        text = workflow_path.read_text(encoding="utf-8")
        assert not text.startswith("env:\n")
        assert "\nenv:\n" not in text.split("jobs:", 1)[0], workflow_path
