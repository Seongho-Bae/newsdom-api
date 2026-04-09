from pathlib import Path

from PIL import Image, ImageDraw

from newsdom_api import synthetic


def test_load_font_falls_back_to_default(monkeypatch):
    sentinel = object()
    monkeypatch.setattr(synthetic, "_font_candidates", lambda: ["/does/not/exist.ttf"])
    monkeypatch.setattr(synthetic.Path, "exists", lambda self: False)
    monkeypatch.setattr(synthetic.ImageFont, "load_default", lambda: sentinel)
    font = synthetic._load_font(12)
    assert font is sentinel


def test_load_font_uses_first_existing_candidate(monkeypatch):
    sentinel = object()
    called = {}
    monkeypatch.setattr(synthetic, "_font_candidates", lambda: ["/pretend/font.ttf"])
    monkeypatch.setattr(synthetic.Path, "exists", lambda self: True)

    def fake_truetype(candidate, size):
        called["candidate"] = candidate
        called["size"] = size
        return sentinel

    monkeypatch.setattr(synthetic.ImageFont, "truetype", fake_truetype)
    assert synthetic._load_font(14) is sentinel
    assert called == {"candidate": "/pretend/font.ttf", "size": 14}


def test_draw_vertical_columns_stops_when_width_exhausted(monkeypatch):
    x_calls = []
    image = Image.new("L", (100, 100), color=255)
    draw = ImageDraw.Draw(image)
    monkeypatch.setattr(synthetic, "_split_vertical", lambda *_: ["A"] * 50)
    monkeypatch.setattr(
        synthetic,
        "_draw_vertical_text",
        lambda draw, text, x, y, font, line_height: x_calls.append(x),
    )

    class Font:
        size = 24

    synthetic._draw_vertical_columns(draw, (0, 0, 40, 120), "ABCDEFGHIJKL", Font())
    assert x_calls == [16]


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
