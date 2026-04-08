from pathlib import Path


def test_committed_synthetic_fixture_exists():
    assert Path("tests/fixtures/synthetic_reference.pdf").exists()
    assert Path("tests/fixtures/synthetic_reference.json").exists()
