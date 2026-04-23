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
    ParseQuality,
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


def _build_page_dom(
    content_list: list[dict[str, Any]],
    *,
    page_number: int,
    article_seq: count,
    width: float | None = None,
    height: float | None = None,
) -> PageNode:
    """Normalize MinerU-style content blocks into a canonical NewsDOM page."""

    page = PageNode(page_number=page_number, width=width, height=height)
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

    return page


def _page_number_from_info(page_info: dict[str, Any], fallback: int) -> int:
    """Resolve page numbering from MinerU page metadata."""

    page_number = page_info.get("page_number")
    if isinstance(page_number, int):
        return page_number

    page_no = page_info.get("page_no")
    if isinstance(page_no, int):
        return page_no + 1

    return fallback


def build_dom(
    content_list: list[dict[str, Any]],
    document_id: str,
    model: list[dict[str, Any]] | None = None,
) -> ParseResponse:
    """Normalize MinerU-style content blocks into the canonical NewsDOM schema."""

    page_info_by_idx: dict[int, dict[str, Any]] = {}
    quality_warnings: list[str] = []
    if model:
        for index, page_model in enumerate(model):
            page_info = page_model.get("page_info") or {}
            page_info_by_idx[index] = page_info

    has_page_idx = any(isinstance(block.get("page_idx"), int) for block in content_list)
    if not has_page_idx:
        article_seq = count(1)
        if len(page_info_by_idx) > 1:
            quality_warnings.append(
                "Some blocks are missing page_idx; content was assigned to page_idx 0 while preserving model-declared page count."
            )
            pages = []
            for page_idx in sorted(page_info_by_idx):
                page_info = page_info_by_idx.get(page_idx, {})
                pages.append(
                    _build_page_dom(
                        content_list if page_idx == 0 else [],
                        page_number=_page_number_from_info(page_info, page_idx + 1),
                        article_seq=article_seq,
                        width=page_info.get("width"),
                        height=page_info.get("height"),
                    )
                )
            return ParseResponse(
                document_id=document_id,
                pages=pages,
                quality=ParseQuality(warnings=quality_warnings),
            )

        page_info = page_info_by_idx.get(0, {})
        return ParseResponse(
            document_id=document_id,
            pages=[
                _build_page_dom(
                    content_list,
                    page_number=_page_number_from_info(page_info, 1),
                    article_seq=article_seq,
                    width=page_info.get("width"),
                    height=page_info.get("height"),
                )
            ],
        )

    has_missing_page_idx = any(not isinstance(block.get("page_idx"), int) for block in content_list)
    if has_missing_page_idx and len(page_info_by_idx) > 1:
        quality_warnings.append(
            "Some blocks are missing page_idx; untagged blocks were assigned to page_idx 0 for deterministic grouping."
        )

    blocks_by_page_idx: dict[int, list[dict[str, Any]]] = {}
    for block in content_list:
        page_idx = block.get("page_idx")
        normalized_page_idx = page_idx if isinstance(page_idx, int) else 0
        blocks_by_page_idx.setdefault(normalized_page_idx, []).append(block)

    pages = []
    article_seq = count(1)
    for page_idx in sorted(blocks_by_page_idx):
        page_info = page_info_by_idx.get(page_idx, {})
        pages.append(
            _build_page_dom(
                blocks_by_page_idx[page_idx],
                page_number=_page_number_from_info(page_info, page_idx + 1),
                article_seq=article_seq,
                width=page_info.get("width"),
                height=page_info.get("height"),
            )
        )

    return ParseResponse(
        document_id=document_id,
        pages=pages,
        quality=ParseQuality(warnings=quality_warnings),
    )
