from pathlib import Path

from newsdom_api.schemas import ParseResponse
from newsdom_api.service import parse_pdf_bytes


def test_parse_pdf_bytes_writes_temp_file_and_builds_dom(monkeypatch):
    observed = {}

    def fake_run_mineru(path: Path):
        observed["path_name"] = path.name
        observed["bytes"] = path.read_bytes()
        return {
            "content_list": [
                {
                    "type": "text",
                    "text": "headline",
                    "text_level": 1,
                    "bbox": [0, 0, 1, 1],
                }
            ]
        }

    def fake_build_dom(content_list, document_id: str) -> ParseResponse:
        observed["document_id"] = document_id
        observed["content_list"] = content_list
        return ParseResponse(document_id=document_id, pages=[])

    monkeypatch.setattr("newsdom_api.service.run_mineru", fake_run_mineru)
    monkeypatch.setattr("newsdom_api.service.build_dom", fake_build_dom)

    result = parse_pdf_bytes(b"pdf-bytes", filename="fixture.pdf")
    assert observed["path_name"] == "fixture.pdf"
    assert observed["bytes"] == b"pdf-bytes"
    assert observed["document_id"] == "fixture"
    assert result.document_id == "fixture"


def test_parse_pdf_bytes_sanitizes_client_filename(monkeypatch):
    observed = {}

    def fake_run_mineru(path: Path):
        observed["path_name"] = path.name
        return {
            "content_list": [
                {
                    "type": "text",
                    "text": "headline",
                    "text_level": 1,
                    "bbox": [0, 0, 1, 1],
                }
            ]
        }

    monkeypatch.setattr("newsdom_api.service.run_mineru", fake_run_mineru)
    result = parse_pdf_bytes(b"pdf-bytes", filename="../../nested/unsafe.pdf")
    assert observed["path_name"] == "unsafe.pdf"
    assert result.document_id == "unsafe"
