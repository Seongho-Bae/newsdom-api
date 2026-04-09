from pathlib import Path


def test_scorecards_push_runs_only_on_default_branch():
    text = Path(".github/workflows/scorecards.yml").read_text(encoding="utf-8")
    push_section = text.split("pull_request:", 1)[0]
    assert "branches: [develop]" in push_section
    assert "branches: [main, develop]" not in push_section


def test_scorecards_pull_requests_cover_main_and_develop():
    text = Path(".github/workflows/scorecards.yml").read_text(encoding="utf-8")
    assert "pull_request:" in text
    pull_request_section = text.split("pull_request:", 1)[1].split("schedule:", 1)[0]
    assert "branches:" not in pull_request_section


def test_scorecards_workflow_supports_optional_repo_token_for_branch_protection():
    text = Path(".github/workflows/scorecards.yml").read_text(encoding="utf-8")
    assert "repo_token: ${{ secrets.SCORECARD_TOKEN || github.token }}" in text
