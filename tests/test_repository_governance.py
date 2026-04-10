from pathlib import Path


def test_codeowners_exists_and_covers_repository() -> None:
    codeowners_path = Path(".github/CODEOWNERS")
    assert codeowners_path.exists()
    rules = {
        tuple(line.split())
        for line in codeowners_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert ("*", "@Seongho-Bae") in rules
    assert (".github/", "@Seongho-Bae") in rules
    assert ("docs/", "@Seongho-Bae") in rules
    assert ("manual/", "@Seongho-Bae") in rules


def test_codeql_scans_python_and_actions() -> None:
    workflow_text = Path(".github/workflows/codeql.yml").read_text(encoding="utf-8")
    assert "github/codeql-action/init@" in workflow_text
    assert "languages: python, actions" in workflow_text


def test_api_manual_references_screenshot_assets() -> None:
    manual_text = Path("manual/api-reference.md").read_text(encoding="utf-8")
    swagger_path = Path("manual/assets/swagger-ui.png")
    redoc_path = Path("manual/assets/redoc.png")
    assert swagger_path.exists()
    assert redoc_path.exists()
    assert swagger_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert redoc_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert (
        "manual/assets/swagger-ui.png" in manual_text
        or "assets/swagger-ui.png" in manual_text
    )
    assert "manual/assets/redoc.png" in manual_text or "assets/redoc.png" in manual_text


def test_development_manual_documents_review_gates() -> None:
    manual_text = Path("manual/development.md").read_text(encoding="utf-8")
    expected_phrases = [
        "2명의 승인",
        "CODEOWNERS",
        "마지막 푸시",
        "pytest",
        "scorecard",
        "codeql (python, actions)",
        "dependency-review",
        "quality-gate",
    ]
    for phrase in expected_phrases:
        assert phrase in manual_text


def test_gitignore_excludes_generated_runtime_artifacts() -> None:
    gitignore_text = Path(".gitignore").read_text(encoding="utf-8")
    for pattern in ("site/", "registered_agents.json", "task_agent_mapping.json"):
        assert pattern in gitignore_text
