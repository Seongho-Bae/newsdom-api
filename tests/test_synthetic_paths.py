from pathlib import Path

from PIL import ImageFont

from newsdom_api import synthetic


def test_load_font_falls_back_to_default(monkeypatch):
    sentinel = object()
    monkeypatch.setattr(synthetic, "_font_candidates", lambda: ["/does/not/exist.ttf"])
    monkeypatch.setattr(synthetic.ImageFont, "load_default", lambda: sentinel)
    font = synthetic._load_font(12)
    assert font is sentinel


def test_generate_fixture_supports_horizontal_article_branch(
    monkeypatch, tmp_path: Path
):
    original_ground_truth = synthetic._ground_truth

    def fake_truth():
        data = original_ground_truth()
        data["articles"][0]["vertical"] = False
        return data

    monkeypatch.setattr(synthetic, "_ground_truth", fake_truth)
    pdf_path, truth_path = synthetic.generate_fixture(tmp_path, seed=9)
    assert pdf_path.exists()
    assert truth_path.exists()
