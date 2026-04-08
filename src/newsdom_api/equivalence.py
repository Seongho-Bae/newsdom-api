"""Compare synthetic fixture metrics against the committed structural baseline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_metrics(path: Path) -> dict[str, Any]:
    """Load a JSON metrics file from disk using UTF-8 encoding."""

    return json.loads(path.read_text(encoding="utf-8"))


def compare_fixture_to_baseline(
    truth_path: Path, baseline: dict[str, Any]
) -> dict[str, Any]:
    """Compare a synthetic fixture metrics file against the committed baseline."""

    truth = load_metrics(truth_path)
    failures: list[str] = []

    checks = {
        "column_count": abs(truth["column_count"] - baseline["column_count"]) <= 1,
        "article_count": abs(truth["article_count"] - baseline["article_count"]) <= 1,
        "image_count": abs(truth["image_count"] - baseline["image_count"]) <= 1,
        "ad_count": abs(truth["ad_count"] - baseline["ad_count"]) <= 1,
        "headline_blocks": abs(truth["headline_blocks"] - baseline["headline_blocks"])
        <= 2,
        "vertical_article_ratio": abs(
            truth["vertical_article_ratio"] - baseline["vertical_article_ratio"]
        )
        <= 0.2,
    }

    for key, passed in checks.items():
        if not passed:
            failures.append(key)

    return {"equivalent": not failures, "failures": failures, "checks": checks}
