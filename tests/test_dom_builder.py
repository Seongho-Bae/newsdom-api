import json
from pathlib import Path

from newsdom_api.dom_builder import build_dom


def test_build_dom_extracts_articles_from_mineru_sample():
    sample = json.loads(
        Path("tests/fixtures/mineru_sample.json").read_text(encoding="utf-8")
    )
    dom = build_dom(sample, document_id="doc1")
    assert len(dom.pages) == 1
    assert len(dom.pages[0].articles) >= 2
    assert dom.pages[0].articles[0].headline == "次世代電池材料"
