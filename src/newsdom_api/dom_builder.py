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


def build_dom(content_list: list[dict[str, Any]], document_id: str) -> ParseResponse:
    """Normalize MinerU-style content blocks into the canonical NewsDOM schema."""

    page = PageNode(page_number=1)
    article_seq = count(1)
    current_article: ArticleNode | None = None

    for block in content_list:
        block_type = block.get("type")
        text = (block.get("text") or block.get("contents") or "").strip()
        bbox = _bbox_from_values(block.get("bbox") or block.get("box"))
        text_level = block.get("text_level")
        role = block.get("role")

        if not text and block_type not in {"image", "table"}:
            continue

        if role == "header":
            page.headers.append(text)
            continue

        if role == "ad" or block_type == "ad":
            page.ads.append(text)
            continue

        if block_type == "image":
            image = ImageNode(
                path=block.get("img_path") or block.get("path") or "image", bbox=bbox
            )
            for caption in block.get("image_caption", []):
                image.captions.append(CaptionNode(text=str(caption)))
            if current_article is None:
                current_article = ArticleNode(
                    article_id=f"article-{next(article_seq)}", headline="(untitled)"
                )
                page.articles.append(current_article)
            current_article.images.append(image)
            continue

        if block_type == "table":
            if current_article is None:
                current_article = ArticleNode(
                    article_id=f"article-{next(article_seq)}", headline="(table-block)"
                )
                page.articles.append(current_article)
            current_article.body_blocks.append(block.get("table_body", ""))
            continue

        is_headline = bool(text_level == 1 or role == "section_headings")
        if is_headline:
            current_article = ArticleNode(
                article_id=f"article-{next(article_seq)}",
                headline=text.replace("\n", " "),
                bbox=bbox,
            )
            page.articles.append(current_article)
            continue

        if current_article is None:
            current_article = ArticleNode(
                article_id=f"article-{next(article_seq)}", headline="(untitled)"
            )
            page.articles.append(current_article)
        current_article.body_blocks.append(text.replace("\n", " "))

    return ParseResponse(document_id=document_id, pages=[page])
