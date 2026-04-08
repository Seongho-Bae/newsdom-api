import re
from pathlib import Path


PINNED_ACTION_RE = re.compile(r"uses:\s+[\w./-]+@[0-9a-f]{40}\b")


def test_workflow_actions_are_pinned_by_sha():
    for workflow_path in sorted(Path(".github/workflows").glob("*.yml")):
        text = workflow_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("uses:"):
                assert PINNED_ACTION_RE.search(stripped), (
                    f"unpinned action in {workflow_path}: {stripped}"
                )


def test_ci_workflows_do_not_use_pip_install_commands():
    for workflow_name in ["tests.yml", "quality-gate.yml"]:
        text = Path(f".github/workflows/{workflow_name}").read_text(encoding="utf-8")
        assert "pip install" not in text


def test_uv_lock_exists_for_ci_reproducibility():
    assert Path("uv.lock").exists()
