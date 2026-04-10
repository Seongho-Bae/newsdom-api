import re
from pathlib import Path

import yaml

INTEGRATION_MARK_RE = re.compile(
    r"(^|\n)\s*(?:@pytest\.mark\.integration|pytestmark\s*=\s*pytest\.mark\.integration)",
    re.MULTILINE,
)


def _integration_marked_test_exists() -> bool:
    for test_path in Path("tests").glob("test_*.py"):
        if test_path.name == Path(__file__).name:
            continue
        text = test_path.read_text(encoding="utf-8")
        if INTEGRATION_MARK_RE.search(text):
            return True
    return False


def test_installation_manual_does_not_reference_empty_integration_marker() -> None:
    text = Path("manual/installation.md").read_text(encoding="utf-8")
    mentions_marker = (
        'pytest -m "integration"' in text or "pytest -m integration" in text
    )
    assert not mentions_marker or _integration_marked_test_exists()


def test_gh_pages_workflow_targets_supported_branches_only() -> None:
    workflow = yaml.safe_load(
        Path(".github/workflows/gh-pages.yml").read_text(encoding="utf-8")
    )
    triggers = workflow.get("on", workflow.get(True))
    branches = triggers["push"]["branches"]
    assert set(branches) == {"main", "develop"}


def test_security_gate_docs_use_current_codeql_check_name() -> None:
    paths = [
        Path("docs/plans/2026-04-08-security-gates.md"),
        Path("docs/plans/2026-04-08-security-gates-design.md"),
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "codeql (python, actions)" in text
        assert "codeql (python)" not in text


def test_adr_follow_up_drops_stale_issue_references() -> None:
    text = Path("docs/adr/0001-openssf-best-practices-badge.md").read_text(
        encoding="utf-8"
    )
    assert "#8" not in text
    assert "#10" not in text
