from __future__ import annotations

import argparse
import json
from pathlib import Path


def _article_has_headline(article: dict[str, object]) -> bool:
    """Return whether a redacted article measurement declares a headline."""

    headline_present = article.get("headline_present")
    if isinstance(headline_present, bool):
        return headline_present

    headline = article.get("headline")
    return isinstance(headline, str) and bool(headline.strip())


def _baseline_from_measurements(measurements: dict[str, object]) -> dict[str, object]:
    """Derive coarse, local-safe metrics from redacted per-page measurements."""

    pages = measurements.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("measurements must include a non-empty 'pages' list")

    column_count = 0
    article_count = 0
    image_count = 0
    ad_count = 0
    headline_blocks = 0
    vertical_article_count = 0
    pages_with_headlines = 0

    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("each page measurement must be a JSON object")

        page_column_count = page.get("column_count")
        if isinstance(page_column_count, int):
            column_count = max(column_count, page_column_count)

        page_articles = page.get("articles") if isinstance(page.get("articles"), list) else []
        page_images = page.get("images") if isinstance(page.get("images"), list) else []
        page_ads = page.get("ads") if isinstance(page.get("ads"), list) else []

        article_count += len(page_articles)
        image_count += len(page_images)
        ad_count += len(page_ads)

        page_has_headline = False
        for article in page_articles:
            if not isinstance(article, dict):
                continue
            if _article_has_headline(article):
                headline_blocks += 1
                page_has_headline = True
            if bool(article.get("vertical")):
                vertical_article_count += 1

        if page_has_headline:
            pages_with_headlines += 1

    return {
        "column_count": column_count,
        "article_count": article_count,
        "image_count": image_count,
        "ad_count": ad_count,
        "headline_blocks": headline_blocks,
        "vertical_article_ratio": (
            vertical_article_count / article_count if article_count else 0.0
        ),
        "page_count": len(pages),
        "headline_page_coverage": (
            pages_with_headlines / len(pages) if pages else 0.0
        ),
        "notes": "Derived from a private page using local-only measurements; contains no source text or source imagery.",
    }


def derive_baseline(output_path: Path, measurements_path: Path | None = None) -> None:
    baseline = {
        "column_count": 4,
        "article_count": 4,
        "image_count": 3,
        "ad_count": 2,
        "headline_blocks": 5,
        "vertical_article_ratio": 1.0,
        "page_count": 1,
        "headline_page_coverage": 1.0,
        "notes": "Derived from a private page using local-only measurements; contains no source text or source imagery.",
    }
    if measurements_path is not None:
        measurements = json.loads(measurements_path.read_text(encoding="utf-8"))
        baseline = _baseline_from_measurements(measurements)

    output_path.write_text(
        json.dumps(baseline, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--measurements", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    derive_baseline(args.output, measurements_path=args.measurements)


if __name__ == "__main__":
    main()
