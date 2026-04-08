from __future__ import annotations

import argparse
import json
from pathlib import Path


def derive_baseline(output_path: Path) -> None:
    baseline = {
        "column_count": 4,
        "article_count": 4,
        "image_count": 3,
        "ad_count": 2,
        "headline_blocks": 5,
        "vertical_article_ratio": 1.0,
        "notes": "Derived from a private page using local-only measurements; contains no source text or source imagery.",
    }
    output_path.write_text(
        json.dumps(baseline, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    derive_baseline(args.output)


if __name__ == "__main__":
    main()
