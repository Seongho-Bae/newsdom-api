from pathlib import Path

import yaml


def test_codeowners_exists_and_covers_repository() -> None:
    codeowners_path = Path(".github/CODEOWNERS")
    assert codeowners_path.exists()
    rules: dict[str, set[str]] = {}
    for raw_line in codeowners_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        pattern, *owners = line.split()
        rules[pattern] = set(owners)

    assert "@Seongho-Bae" in rules["*"]
    assert "@Seongho-Bae" in rules[".github/"]
    assert "@Seongho-Bae" in rules["docs/"]
    assert "@Seongho-Bae" in rules["manual/"]


def test_codeql_scans_python_and_actions() -> None:
    workflow = yaml.safe_load(
        Path(".github/workflows/codeql.yml").read_text(encoding="utf-8")
    )
    analyze_steps = workflow["jobs"]["analyze"]["steps"]
    init_step = next(
        step
        for step in analyze_steps
        if step.get("uses", "").startswith("github/codeql-action/init@")
    )
    languages = init_step["with"]["languages"]
    if isinstance(languages, str):
        normalized_languages = {
            language.strip().lower()
            for language in languages.split(",")
            if language.strip()
        }
    else:
        normalized_languages = {
            str(language).strip().lower()
            for language in languages
            if str(language).strip()
        }

    assert "python" in normalized_languages
    assert "actions" in normalized_languages


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


def test_development_manual_documents_single_maintainer_review_exception() -> None:
    manual_text = Path("manual/development.md").read_text(encoding="utf-8")
    for expected in (
        "단일 유지보수자",
        "필수 상태 체크",
        "리뷰어 용량이 확보되면",
        "비작성자 승인",
        "CODEOWNERS",
    ):
        assert expected in manual_text


def test_gitignore_excludes_generated_runtime_artifacts() -> None:
    gitignore_text = Path(".gitignore").read_text(encoding="utf-8")
    active_lines = {
        line.strip()
        for line in gitignore_text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    for pattern in ("site/", "registered_agents.json", "task_agent_mapping.json"):
        assert pattern in active_lines
