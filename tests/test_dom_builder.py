import json
from pathlib import Path

from newsdom_api.dom_builder import (
    _bbox_from_values,
    _caption_nodes_from_items,
    _coerce_page_number,
    build_dom,
)


def _load_fixture(name: str):
    return json.loads(Path(f"tests/fixtures/{name}").read_text(encoding="utf-8"))


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


def test_build_dom_preserves_multi_page_structure_and_page_scoped_metadata():
    sample = _load_fixture("mineru_multi_page_sample.json")
    model = _load_fixture("mineru_multi_page_model.json")
    dom = build_dom(sample, document_id="doc-multi-page", model=model)

    assert len(dom.pages) == 2

    first_page = dom.pages[0]
    second_page = dom.pages[1]

    assert [page.page_number for page in dom.pages] == [1, 2]
    assert (first_page.width, first_page.height) == (1200.0, 1800.0)
    assert (second_page.width, second_page.height) == (1280.0, 1820.0)
    assert first_page.headers == ["Synthetic News Page 1"]
    assert second_page.headers == ["Synthetic News Page 2"]
    assert first_page.footers == ["Page 1 footer"]
    assert second_page.footers == ["Page 2 footer"]
    assert first_page.page_numbers == ["1"]
    assert second_page.page_numbers == ["2"]

    first_article = first_page.articles[0]
    second_article = second_page.articles[0]

    assert "Page 1 footer" not in first_article.body_blocks
    assert "Page 2 footer" not in second_article.body_blocks
    assert "1" not in first_article.body_blocks
    assert "2" not in second_article.body_blocks
    assert "Orphaned text without explicit page index." not in first_article.body_blocks
    assert "Orphaned text without explicit page index." not in second_article.body_blocks

    assert first_article.images[0].path == "images/page-1-photo.png"
    assert first_article.images[0].media_type == "image"
    assert [caption.text for caption in first_article.images[0].captions] == [
        "Image caption on page 1"
    ]
    assert [caption.text for caption in first_article.images[0].footnotes] == [
        "Image footnote on page 1"
    ]

    assert second_article.images[0].path == "charts/page-2-growth.png"
    assert second_article.images[0].media_type == "chart"
    assert [caption.text for caption in second_article.images[0].captions] == [
        "Chart caption on page 2"
    ]
    assert [caption.text for caption in second_article.images[0].footnotes] == [
        "Chart footnote on page 2"
    ]
    assert second_article.captions[0].text == "Table caption on page 2"
    assert second_article.footnotes[0].text == "Table footnote on page 2"
    assert any("page_idx" in warning for warning in dom.quality.warnings)


def test_coerce_page_number_returns_none_for_type_and_value_errors():
    assert _coerce_page_number(object()) is None
    assert _coerce_page_number("not-a-page-number") is None


def test_caption_nodes_from_items_uses_contents_and_bbox_variants_and_skips_empty_text():
    nodes = _caption_nodes_from_items(
        [
            {"contents": " Caption from contents ", "bbox": [1, 2, 3, 4]},
            {"text": "   ", "bbox": [9, 9, 9, 9]},
            {"contents": "Caption from box", "box": [5, 6, 7, 8]},
        ]
    )

    assert [node.text for node in nodes] == ["Caption from contents", "Caption from box"]
    assert nodes[0].bbox is not None
    assert nodes[0].bbox.x0 == 1.0
    assert nodes[0].bbox.y1 == 4.0
    assert nodes[1].bbox is not None
    assert nodes[1].bbox.x0 == 5.0
    assert nodes[1].bbox.y1 == 8.0


def test_build_dom_warns_when_model_and_content_pages_diverge_and_skips_invalid_model_page_numbers():
    dom = build_dom(
        [
            {"type": "text", "text": "body on content page", "page_idx": 1},
            {
                "type": "image",
                "page_idx": 1,
                "img_path": "img.png",
                "image_caption": [
                    {"contents": "Image caption from dict", "bbox": [0, 1, 2, 3]},
                    {"text": "   ", "bbox": [3, 4, 5, 6]},
                ],
                "image_footnote": [
                    {"contents": "Image footnote from dict", "box": [6, 7, 8, 9]}
                ],
            },
        ],
        document_id="doc-divergence",
        model=[
            {"page_info": {"page_no": 2, "width": 1200, "height": 1800}},
            {"page_info": {"page_no": object(), "width": 10, "height": 20}},
        ],
    )

    assert [page.page_number for page in dom.pages] == [1, 2]
    assert dom.pages[1].width == 1200.0
    assert dom.pages[1].height == 1800.0
    assert dom.pages[0].articles[0].images[0].captions[0].text == "Image caption from dict"
    assert dom.pages[0].articles[0].images[0].captions[0].bbox is not None
    assert dom.pages[0].articles[0].images[0].footnotes[0].text == "Image footnote from dict"
    assert dom.quality.warnings == [
        "content/model divergence: content_list references page_idx 1 absent from model",
        "content/model divergence: model page 2 has no content_list blocks",
    ]


def test_build_dom_normalizes_zero_based_page_indices_to_one_based_response_numbers():
    dom = build_dom(
        [
            {"type": "text", "text": "page zero body", "page_idx": 0},
            {"type": "text", "text": "page one body", "page_idx": 1},
        ],
        document_id="doc-page-normalization",
        model=[
            {"page_info": {"page_no": 0, "width": 1000, "height": 1400}},
            {"page_info": {"page_no": 1, "width": 1000, "height": 1400}},
        ],
    )

    assert [page.page_number for page in dom.pages] == [1, 2]
    assert dom.pages[0].articles[0].body_blocks == ["page zero body"]
    assert dom.pages[1].articles[0].body_blocks == ["page one body"]
