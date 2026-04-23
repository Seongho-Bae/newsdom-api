import json
import subprocess
import sys
from pathlib import Path


def test_derive_private_baseline_derives_page_aware_metrics_from_measurements(
    tmp_path: Path,
):
    measurements_path = tmp_path / "measurements.json"
    output_path = tmp_path / "baseline.json"
    measurements_path.write_text(
        json.dumps(
            {
                "pages": [
                    {
                        "column_count": 4,
                        "articles": [
                            {"headline_present": True, "vertical": True},
                            {"headline_present": False, "vertical": True},
                        ],
                        "images": [{}, {}],
                        "ads": [{}],
                    },
                    {
                        "column_count": 3,
                        "articles": [{"headline_present": False, "vertical": False}],
                        "images": [{}],
                        "ads": [],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            "tools/derive_private_baseline.py",
            "--measurements",
            str(measurements_path),
            str(output_path),
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
    )

    baseline = json.loads(output_path.read_text(encoding="utf-8"))
    assert baseline["column_count"] == 4
    assert baseline["article_count"] == 3
    assert baseline["image_count"] == 3
    assert baseline["ad_count"] == 1
    assert baseline["headline_blocks"] == 1
    assert baseline["vertical_article_ratio"] == 2 / 3
    assert baseline["page_count"] == 2
    assert baseline["headline_page_coverage"] == 0.5


def test_derive_private_baseline_rejects_missing_pages_measurements(tmp_path: Path):
    measurements_path = tmp_path / "measurements.json"
    output_path = tmp_path / "baseline.json"
    measurements_path.write_text(json.dumps({"pages": []}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "tools/derive_private_baseline.py",
            "--measurements",
            str(measurements_path),
            str(output_path),
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "pages" in result.stderr
