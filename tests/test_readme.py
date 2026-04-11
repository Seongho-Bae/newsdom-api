from pathlib import Path


def test_readme_points_to_user_and_maintainer_docs():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "fixtures and provenance" in text.lower()
    assert "contributing.md" in text.lower()
    assert "docs/workflow/git-flow.md" in text


def test_readme_includes_scorecard_badge():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "securityscorecards.dev" in text


def test_contributing_mentions_develop_branch():
    text = Path("CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "develop" in text


def test_readme_quotes_dev_extra_install_command():
    text = Path("README.md").read_text(encoding="utf-8")
    assert 'pip install -e ".[dev]"' in text


def test_readme_mentions_linux_amd64_only_nvidia_path_once():
    text = Path("README.md").read_text(encoding="utf-8")
    assert text.count("`linux/amd64`-only") == 1


def test_contributing_quotes_dev_extra_install_command():
    text = Path("CONTRIBUTING.md").read_text(encoding="utf-8")
    assert 'pip install -e ".[dev]"' in text


def test_pull_request_template_exists():
    assert Path(".github/pull_request_template.md").exists()


def test_security_workflows_exist():
    assert Path(".github/workflows/scorecards.yml").exists()
    assert Path(".github/workflows/codeql.yml").exists()
    assert Path(".github/workflows/dependency-review.yml").exists()


def test_quality_gate_workflow_exists():
    assert Path(".github/workflows/quality-gate.yml").exists()
