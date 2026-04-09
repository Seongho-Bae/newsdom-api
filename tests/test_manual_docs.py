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


def test_installation_doc_uses_quoted_extras_and_clear_python_wording():
    text = Path("manual/installation.md").read_text(encoding="utf-8")
    assert "Required: `>=3.10, <3.14`" in text
    assert "Recommended: `python3.10`" in text
    assert "python3.10 -m venv .venv" in text
    assert 'pip install -e ".[dev]"' in text
    assert 'pip install "mineru[pipeline]==3.0.9"' in text
