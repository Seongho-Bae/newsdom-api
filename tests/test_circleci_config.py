from pathlib import Path


def test_circleci_config_exists_and_uses_uv_quality_gate():
    text = Path(".circleci/config.yml").read_text(encoding="utf-8")
    assert "version: 2.1" in text
    assert "cimg/python:3.10" in text
    assert "UV_UNMANAGED_INSTALL=1" in text
    assert "UV_NO_MODIFY_PATH=1" in text
    assert "https://astral.sh/uv/0.11.3/install.sh" in text
    assert "curl -LsSf -o /tmp/uv-install.sh" in text
    assert "sh /tmp/uv-install.sh" in text
    assert "curl -LsSf https://astral.sh/uv/install.sh | sh" not in text
    assert "uv sync --locked --extra dev" in text
    assert "PYTHONWARNINGS=error uv run pytest" in text
    assert (
        "uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100"
        in text
    )
