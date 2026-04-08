import json
from pathlib import Path

from newsdom_api.equivalence import compare_fixture_to_baseline


def test_synthetic_fixture_matches_private_baseline():
    truth_path = Path("tests/fixtures/synthetic_reference.json")
    baseline = json.loads(
        Path("tests/fixtures/private_page_baseline.json").read_text(encoding="utf-8")
    )
    result = compare_fixture_to_baseline(truth_path, baseline)
    assert result["equivalent"] is True
