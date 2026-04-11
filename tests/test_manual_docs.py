import json
from pathlib import Path


def _extract_first_json_block(text: str) -> str:
    marker = "```json\n"
    start = text.index(marker) + len(marker)
    end = text.index("\n```", start)
    return text[start:end]


def test_api_reference_examples_are_consistent_and_valid_json():
    text = Path("manual/api-reference.md").read_text(encoding="utf-8")
    assert "#### Python 클라이언트 예제 (requests)" in text
    payload = json.loads(_extract_first_json_block(text))
    assert payload["pages"][0]["articles"][0]["images"][0]["bbox"]["x0"] == 120.0


def test_development_doc_uses_tree_wording():
    text = Path("manual/development.md").read_text(encoding="utf-8")
    assert "트리 구조의 DOM" in text


def test_installation_doc_uses_uv_first_setup_and_verification_commands():
    text = Path("manual/installation.md").read_text(encoding="utf-8")
    assert "Required: `>=3.10, <3.14`" in text
    assert "uv sync --frozen --all-extras" in text
    assert 'uv pip install --python .venv/bin/python "mineru[pipeline]==3.0.9"' in text
    assert "uv run pytest" in text
    assert "python3.10 -m venv .venv" not in text
    assert 'pip install -e ".[dev]"' not in text


def test_installation_doc_includes_manual_api_healthcheck_commands():
    text = Path("manual/installation.md").read_text(encoding="utf-8")
    assert (
        "uv run uvicorn --app-dir src newsdom_api.main:app --host 0.0.0.0 --port 8000 --reload"
        in text
    )
    assert "curl -sS http://127.0.0.1:8000/health" in text
    assert "HTTP 200" in text


def test_api_reference_uses_uv_run_server_command():
    text = Path("manual/api-reference.md").read_text(encoding="utf-8")
    assert "uv run uvicorn --app-dir src newsdom_api.main:app --reload" in text
    assert "가상환경을 활성화한 상태" not in text


def test_installation_doc_notes_windows_uv_python_path_equivalent():
    text = Path("manual/installation.md").read_text(encoding="utf-8")
    assert ".venv\\Scripts\\python.exe" in text
