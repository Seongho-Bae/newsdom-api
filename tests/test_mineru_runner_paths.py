import json
from pathlib import Path

import pytest

from newsdom_api import mineru_runner


class _FakeTempDir:
    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.path.mkdir(parents=True, exist_ok=True)
        return str(self.path)

    def __exit__(self, exc_type, exc, tb):
        return False


def test_resolve_mineru_bin_prefers_env(monkeypatch):
    monkeypatch.setenv("NEWSDOM_MINERU_BIN", "/opt/mineru")
    assert mineru_runner._resolve_mineru_bin() == "/opt/mineru"


def test_resolve_mineru_bin_raises_when_not_found(monkeypatch):
    monkeypatch.delenv("NEWSDOM_MINERU_BIN", raising=False)
    monkeypatch.setattr(mineru_runner.shutil, "which", lambda name: None)
    with pytest.raises(FileNotFoundError):
        mineru_runner._resolve_mineru_bin()


def test_find_output_dir_raises_when_missing(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        mineru_runner._find_output_dir(tmp_path)


def test_run_mineru_reads_generated_json(monkeypatch, tmp_path: Path):
    tempdir = tmp_path / "temp"
    ocr_dir = tempdir / "sample" / "ocr"
    ocr_dir.mkdir(parents=True)
    (ocr_dir / "alt_content_list.json").write_text(
        json.dumps([{"type": "text", "text": "ok"}]), encoding="utf-8"
    )
    (ocr_dir / "alt_model.json").write_text(
        json.dumps([{"layout_dets": []}]), encoding="utf-8"
    )

    monkeypatch.setattr(mineru_runner.shutil, "which", lambda name: "/usr/bin/mineru")
    monkeypatch.setattr(
        mineru_runner.tempfile,
        "TemporaryDirectory",
        lambda prefix: _FakeTempDir(tempdir),
    )

    called = {}

    def fake_run(cmd, check, capture_output, text, timeout=None):
        assert check is True
        assert capture_output is True
        assert text is True
        assert timeout is not None
        called["cmd"] = cmd

        class Result:
            stdout = "stdout"
            stderr = "stderr"

        return Result()

    monkeypatch.setattr(mineru_runner.subprocess, "run", fake_run)

    result = mineru_runner.run_mineru(Path("sample.pdf"))
    assert called["cmd"][0] == "/usr/bin/mineru"
    assert result["content_list"][0]["text"] == "ok"
    assert result["stderr"] == "stderr"


def test_run_mineru_prefers_exact_stem_content_json(monkeypatch, tmp_path: Path):
    tempdir = tmp_path / "temp"
    ocr_dir = tempdir / "sample" / "ocr"
    ocr_dir.mkdir(parents=True)
    (ocr_dir / "sample_content_list.json").write_text(
        json.dumps([{"type": "text", "text": "exact"}]), encoding="utf-8"
    )
    (ocr_dir / "alt_content_list.json").write_text(
        json.dumps([{"type": "text", "text": "fallback"}]), encoding="utf-8"
    )
    (ocr_dir / "alt_model.json").write_text(
        json.dumps([{"layout_dets": []}]), encoding="utf-8"
    )

    monkeypatch.setattr(mineru_runner.shutil, "which", lambda name: "/usr/bin/mineru")
    monkeypatch.setattr(
        mineru_runner.tempfile,
        "TemporaryDirectory",
        lambda prefix: _FakeTempDir(tempdir),
    )

    def fake_run(cmd, check, capture_output, text, timeout=None):
        assert check is True
        assert capture_output is True
        assert text is True
        assert timeout is not None

        class Result:
            stdout = "stdout"
            stderr = "stderr"

        return Result()

    monkeypatch.setattr(mineru_runner.subprocess, "run", fake_run)

    result = mineru_runner.run_mineru(Path("sample.pdf"))
    assert result["content_list"][0]["text"] == "exact"


def test_run_mineru_raises_when_content_json_missing(monkeypatch, tmp_path: Path):
    tempdir = tmp_path / "temp"
    ocr_dir = tempdir / "sample" / "ocr"
    ocr_dir.mkdir(parents=True)
    (ocr_dir / "alt_model.json").write_text(
        json.dumps([{"layout_dets": []}]), encoding="utf-8"
    )

    monkeypatch.setattr(mineru_runner.shutil, "which", lambda name: "/usr/bin/mineru")
    monkeypatch.setattr(
        mineru_runner.tempfile,
        "TemporaryDirectory",
        lambda prefix: _FakeTempDir(tempdir),
    )

    def fake_run(cmd, check, capture_output, text, timeout=None):
        assert check is True
        assert capture_output is True
        assert text is True
        assert timeout is not None

        class Result:
            stdout = ""
            stderr = ""

        return Result()

    monkeypatch.setattr(mineru_runner.subprocess, "run", fake_run)

    with pytest.raises(FileNotFoundError):
        mineru_runner.run_mineru(Path("sample.pdf"))


def test_run_mineru_raises_when_model_json_missing(monkeypatch, tmp_path: Path):
    tempdir = tmp_path / "temp"
    ocr_dir = tempdir / "sample" / "ocr"
    ocr_dir.mkdir(parents=True)
    (ocr_dir / "alt_content_list.json").write_text(
        json.dumps([{"type": "text", "text": "ok"}]), encoding="utf-8"
    )

    monkeypatch.setattr(mineru_runner.shutil, "which", lambda name: "/usr/bin/mineru")
    monkeypatch.setattr(
        mineru_runner.tempfile,
        "TemporaryDirectory",
        lambda prefix: _FakeTempDir(tempdir),
    )

    def fake_run(cmd, check, capture_output, text, timeout=None):
        assert check is True
        assert capture_output is True
        assert text is True
        assert timeout is not None

        class Result:
            stdout = ""
            stderr = ""

        return Result()

    monkeypatch.setattr(mineru_runner.subprocess, "run", fake_run)

    with pytest.raises(FileNotFoundError):
        mineru_runner.run_mineru(Path("sample.pdf"))
