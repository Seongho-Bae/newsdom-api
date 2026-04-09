import re
from pathlib import Path


PINNED_ACTION_RE = re.compile(r"uses:\s+[\w./-]+@[0-9a-f]{40}\b")
PULL_REQUEST_BRANCH_FILTER_RE = re.compile(
    r"pull_request:\s*\n\s+branches:", re.MULTILINE
)


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


def test_ci_workflows_run_pytest_through_uv():
    tests_text = Path(".github/workflows/tests.yml").read_text(encoding="utf-8")
    quality_text = Path(".github/workflows/quality-gate.yml").read_text(
        encoding="utf-8"
    )
    assert "uv run pytest" in tests_text
    assert (
        "uv run pytest --cov=src/newsdom_api --cov-report=term-missing --cov-fail-under=100"
        in quality_text
    )


def test_uv_lock_exists_for_ci_reproducibility():
    assert Path("uv.lock").exists()


def test_ci_workflows_run_for_all_pull_requests():
    for workflow_path in sorted(Path(".github/workflows").glob("*.yml")):
        text = workflow_path.read_text(encoding="utf-8")
        assert not PULL_REQUEST_BRANCH_FILTER_RE.search(text), (
            f"pull_request branch filter blocks stacked PR checks in {workflow_path}"
        )
