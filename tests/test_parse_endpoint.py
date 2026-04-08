from fastapi.testclient import TestClient

from newsdom_api.main import app


def test_parse_endpoint_requires_pdf_file():
    client = TestClient(app)
    response = client.post("/parse")
    assert response.status_code == 422
