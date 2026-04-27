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


def test_readme_uses_uv_sync_for_repo_setup():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "uv sync --frozen --all-extras" in text
    assert 'pip install -e ".[dev]"' not in text
    assert "python3.10 -m venv .venv" not in text


def test_contributing_uses_uv_sync_for_repo_setup():
    text = Path("CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "uv sync --frozen --all-extras" in text
    assert 'pip install -e ".[dev]"' not in text


def test_readme_documents_uv_run_entrypoints():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "uv run uvicorn --app-dir src newsdom_api.main:app --reload" in text
    assert "uv run pytest" in text
    assert (
        "uv run python fuzzers/dom_builder_fuzzer.py --smoke tests/fixtures/mineru_sample.json"
        in text
    )


def test_repo_docs_note_windows_uv_python_path_equivalent():
    text = Path("CONTRIBUTING.md").read_text(encoding="utf-8")
    assert ".venv\\Scripts\\python.exe" in text


def test_repo_docs_describe_live_mineru_install_as_optional_follow_up():
    for path in [Path("README.md"), Path("CONTRIBUTING.md")]:
        text = path.read_text(encoding="utf-8")
        assert 'uv sync --frozen --all-extras' in text
    assert 'uv pip install --python .venv/bin/python "mineru[pipeline]==3.0.9"' in Path(
        "CONTRIBUTING.md"
    ).read_text(encoding="utf-8")
    assert 'uv pip install --python .venv/bin/python "mineru[pipeline]==3.0.9"' not in Path(
        "README.md"
    ).read_text(encoding="utf-8")


def test_repo_docs_explain_live_mineru_install_is_optional_security_isolation():
    for path in [Path("README.md"), Path("CONTRIBUTING.md")]:
        text = path.read_text(encoding="utf-8")
        assert "optional" in text.lower()
        assert "separate" in text.lower() or "separately" in text.lower()


def test_readme_describes_default_container_as_api_only_runtime():
    text = Path("README.md").read_text(encoding="utf-8")

    assert "ships the API service only" in text
    assert "does not bundle the MinerU runtime" in text


def test_pull_request_template_exists():
    assert Path(".github/pull_request_template.md").exists()


def test_security_workflows_exist():
    assert Path(".github/workflows/scorecards.yml").exists()
    assert Path(".github/workflows/codeql.yml").exists()
    assert Path(".github/workflows/dependency-review.yml").exists()


def test_quality_gate_workflow_exists():
    assert Path(".github/workflows/quality-gate.yml").exists()
