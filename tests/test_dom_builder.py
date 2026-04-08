import json
from pathlib import Path

from newsdom_api.dom_builder import _bbox_from_values, build_dom


def test_build_dom_extracts_articles_from_mineru_sample():
    sample = json.loads(
        Path("tests/fixtures/mineru_sample.json").read_text(encoding="utf-8")
    )
    dom = build_dom(sample, document_id="doc1")
    assert len(dom.pages) == 1
    assert len(dom.pages[0].articles) >= 2
    assert dom.pages[0].articles[0].headline == "次世代電池材料"


def test_bbox_helper_returns_none_for_invalid_values():
    assert _bbox_from_values(None) is None
    assert _bbox_from_values([1, 2, 3]) is None


def test_build_dom_handles_non_headline_paths():
    dom = build_dom(
        [
            {
                "type": "text",
                "text": "ignore me",
                "bbox": [0, 0, 10, 10],
                "role": "header",
            },
            {"type": "ad", "text": "buy now", "bbox": [1, 1, 2, 2]},
            {"type": "text", "text": "", "bbox": [1, 1, 2, 2]},
            {
                "type": "image",
                "img_path": "img.png",
                "bbox": [1, 1, 2, 2],
                "image_caption": ["caption"],
            },
            {"type": "table", "table_body": "<table></table>", "bbox": [1, 1, 2, 2]},
            {"type": "text", "text": "body text", "bbox": [1, 1, 2, 2]},
        ],
        document_id="doc2",
    )
    page = dom.pages[0]
    assert page.headers == ["ignore me"]
    assert page.ads == ["buy now"]
    assert page.articles[0].headline == "(untitled)"
    assert page.articles[0].images[0].captions[0].text == "caption"
    assert "<table></table>" in page.articles[0].body_blocks
    assert "body text" in page.articles[0].body_blocks


def test_build_dom_creates_table_article_when_needed():
    dom = build_dom(
        [{"type": "table", "table_body": "<table></table>", "bbox": [1, 1, 2, 2]}],
        document_id="doc3",
    )
    assert dom.pages[0].articles[0].headline == "(table-block)"


def test_build_dom_creates_untitled_article_for_plain_text():
    dom = build_dom(
        [{"type": "text", "text": "plain body", "bbox": [1, 1, 2, 2]}],
        document_id="doc4",
    )
    assert dom.pages[0].articles[0].headline == "(untitled)"
