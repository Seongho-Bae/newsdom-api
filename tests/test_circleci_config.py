from pathlib import Path


def test_circleci_config_exists_and_uses_uv_quality_gate():
    text = Path(".circleci/config.yml").read_text(encoding="utf-8")
    assert "version: 2.1" in text
    assert "cimg/python:3.10" in text
    assert "uv sync --locked --extra dev" in text
    assert "PYTHONWARNINGS=error uv run pytest" in text
    assert (
        "uv run pytest --cov=src/newsdom_api --cov-report=term-missing --cov-fail-under=100"
        in text
    )
