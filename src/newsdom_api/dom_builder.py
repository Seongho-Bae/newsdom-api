"""Build canonical NewsDOM page/article structures from parser output blocks."""

from __future__ import annotations

from itertools import count
from typing import Any

from .schemas import (
    ArticleNode,
    BoundingBox,
    CaptionNode,
    ImageNode,
    PageNode,
    ParseResponse,
)


def _bbox_from_values(values: list[float] | None) -> BoundingBox | None:
    """Convert a four-value bounding-box list into a typed schema object."""

    if not values or len(values) != 4:
        return None
    return BoundingBox(
        x0=float(values[0]),
        y0=float(values[1]),
        x1=float(values[2]),
        y1=float(values[3]),
    )


def _coerce_page_number(value: Any) -> int | None:
    """Convert supported page-number values into integers."""

    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _caption_nodes_from_items(items: Any) -> list[CaptionNode]:
    """Normalize caption-like payloads into caption nodes."""

    nodes: list[CaptionNode] = []
    if not isinstance(items, list):
        return nodes

    for item in items:
        if isinstance(item, dict):
            text = str(item.get("text") or item.get("contents") or "").strip()
            bbox = _bbox_from_values(item.get("bbox") or item.get("box"))
        else:
            text = str(item).strip()
            bbox = None
        if text:
            nodes.append(CaptionNode(text=text, bbox=bbox))
    return nodes


def _new_article(article_seq: count, headline: str, bbox: BoundingBox | None = None) -> ArticleNode:
    """Create a new article node with the next deterministic identifier."""

    return ArticleNode(
        article_id=f"article-{next(article_seq)}",
        headline=headline,
        bbox=bbox,
    )


def _get_or_create_article(
    page: PageNode,
    current_articles: dict[int, ArticleNode | None],
    article_seq: count,
    *,
    page_number: int,
    headline: str = "(untitled)",
) -> ArticleNode:
    """Return the current article for a page, creating one when missing."""

    article = current_articles.get(page_number)
    if article is None:
        article = _new_article(article_seq, headline)
        page.articles.append(article)
        current_articles[page_number] = article
    return article


def build_dom(
    content_list: list[dict[str, Any]],
    document_id: str,
    model: list[dict[str, Any]] | None = None,
) -> ParseResponse:
    """Normalize MinerU-style content blocks into the canonical NewsDOM schema."""

    article_seq = count(1)
    warnings: list[str] = []
    model = model or []

    model_page_info: dict[int, tuple[float | None, float | None]] = {}
    model_page_numbers: set[int] = set()
    for page_model in model:
        page_info = page_model.get("page_info") or {}
        page_number = _coerce_page_number(page_info.get("page_no"))
        if page_number is None:
            continue
        model_page_numbers.add(page_number)
        width = page_info.get("width")
        height = page_info.get("height")
        model_page_info[page_number] = (
            float(width) if width is not None else None,
            float(height) if height is not None else None,
        )

    content_page_numbers = {
        page_number
        for block in content_list
        if (page_number := _coerce_page_number(block.get("page_idx"))) is not None
    }

    page_numbers = sorted(model_page_numbers | content_page_numbers)
    if not page_numbers:
        page_numbers = [1]

    pages: dict[int, PageNode] = {}
    current_articles: dict[int, ArticleNode | None] = {}
    for page_number in page_numbers:
        width, height = model_page_info.get(page_number, (None, None))
        pages[page_number] = PageNode(
            page_number=page_number,
            width=width,
            height=height,
        )
        current_articles[page_number] = None

    for page_number in sorted(content_page_numbers - model_page_numbers):
        warnings.append(
            f"content/model divergence: content_list references page_idx {page_number} absent from model"
        )
    for page_number in sorted(model_page_numbers - content_page_numbers):
        warnings.append(
            f"content/model divergence: model page {page_number} has no content_list blocks"
        )

    for block in content_list:
        block_type = block.get("type")
        text = (block.get("text") or block.get("contents") or "").strip()
        bbox = _bbox_from_values(block.get("bbox") or block.get("box"))
        text_level = block.get("text_level")
        role = block.get("role")
        page_number = _coerce_page_number(block.get("page_idx"))

        if page_number is None:
            if len(page_numbers) != 1:
                warnings.append(
                    f"ambiguous page assignment: block type '{block_type or 'unknown'}' missing page_idx"
                )
                continue
            page_number = page_numbers[0]

        page = pages[page_number]

        if not text and block_type not in {"image", "table", "chart"}:
            continue

        if role == "header":
            page.headers.append(text)
            continue

        if role == "footer":
            page.footers.append(text)
            continue

        if role == "page_number":
            page.page_numbers.append(text)
            continue

        if role == "ad" or block_type == "ad":
            page.ads.append(text)
            continue

        if block_type in {"image", "chart"}:
            image = ImageNode(
                path=block.get("img_path") or block.get("path") or block_type,
                media_type=block_type,
                bbox=bbox,
            )
            caption_key = f"{block_type}_caption"
            footnote_key = f"{block_type}_footnote"
            image.captions.extend(_caption_nodes_from_items(block.get(caption_key)))
            image.footnotes.extend(_caption_nodes_from_items(block.get(footnote_key)))
            article = _get_or_create_article(
                page,
                current_articles,
                article_seq,
                page_number=page_number,
            )
            article.images.append(image)
            continue

        if block_type == "table":
            article = _get_or_create_article(
                page,
                current_articles,
                article_seq,
                page_number=page_number,
                headline="(table-block)",
            )
            article.body_blocks.append(block.get("table_body", ""))
            article.captions.extend(_caption_nodes_from_items(block.get("table_caption")))
            article.footnotes.extend(_caption_nodes_from_items(block.get("table_footnote")))
            continue

        is_headline = bool(text_level == 1 or role == "section_headings")
        if is_headline:
            article = _new_article(article_seq, text.replace("\n", " "), bbox)
            page.articles.append(article)
            current_articles[page_number] = article
            continue

        article = _get_or_create_article(
            page,
            current_articles,
            article_seq,
            page_number=page_number,
        )
        article.body_blocks.append(text.replace("\n", " "))

    return ParseResponse(
        document_id=document_id,
        pages=[pages[page_number] for page_number in sorted(pages)],
        quality={"warnings": warnings},
    )
