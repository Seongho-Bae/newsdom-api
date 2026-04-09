import json
from pathlib import Path

from newsdom_api.equivalence import compare_fixture_to_baseline, load_metrics


def test_load_metrics_reads_json(tmp_path: Path):
    path = tmp_path / "metrics.json"
    path.write_text(json.dumps({"column_count": 1}), encoding="utf-8")
    assert load_metrics(path)["column_count"] == 1


def test_compare_fixture_to_baseline_reports_failures(tmp_path: Path):
    truth_path = tmp_path / "truth.json"
    truth_path.write_text(
        json.dumps(
            {
                "column_count": 10,
                "article_count": 10,
                "image_count": 10,
                "ad_count": 10,
                "headline_blocks": 10,
                "vertical_article_ratio": 0.0,
            }
        ),
        encoding="utf-8",
    )
    baseline = {
        "column_count": 1,
        "article_count": 1,
        "image_count": 1,
        "ad_count": 1,
        "headline_blocks": 1,
        "vertical_article_ratio": 1.0,
    }
    result = compare_fixture_to_baseline(truth_path, baseline)
    assert result["equivalent"] is False
    assert set(result["failures"]) == {
        "column_count",
        "article_count",
        "image_count",
        "ad_count",
        "headline_blocks",
        "vertical_article_ratio",
    }
