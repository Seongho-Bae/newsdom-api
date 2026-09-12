from fastapi.testclient import TestClient
from newsdom_api.main import app, MAX_PARSE_UPLOAD_BYTES

def test_multipart_payload_over_part_size_is_rejected(monkeypatch):
    monkeypatch.setattr("newsdom_api.main._validate_pdf_structure", lambda _: None)
    monkeypatch.setattr("newsdom_api.main.parse_pdf", lambda *a, **kw: {"document_id": "test", "pages": []})

    client = TestClient(app)

    large_payload = b"%PDF-" + (b"x" * (MAX_PARSE_UPLOAD_BYTES - 4))

    response = client.post(
        "/parse",
        files={"file": ("fixture.pdf", large_payload, "application/pdf")},
    )

    assert response.status_code == 413
