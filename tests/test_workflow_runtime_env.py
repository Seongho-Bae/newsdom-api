from pathlib import Path


def test_javascript_actions_are_forced_to_node24():
    for workflow_path in sorted(Path(".github/workflows").glob("*.yml")):
        text = workflow_path.read_text(encoding="utf-8")
        assert "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true" in text, workflow_path
