from pathlib import Path


def test_javascript_actions_are_forced_to_node24():
    workflow_paths = sorted(Path(".github/workflows").glob("*.yml")) + sorted(
        Path(".github/workflows").glob("*.yaml")
    )
    for workflow_path in workflow_paths:
        text = workflow_path.read_text(encoding="utf-8")
        assert "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true" in text, workflow_path
