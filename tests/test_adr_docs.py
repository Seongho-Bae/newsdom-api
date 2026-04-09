from pathlib import Path


def test_best_practices_decision_adr_exists_and_documents_deferral():
    path = Path("docs/adr/0001-openssf-best-practices-badge.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Status" in text
    assert "Accepted" in text
    assert "defer" in text.lower()
    assert "first tagged release" in text.lower()
    assert "external reviewer" in text.lower()
