from pathlib import Path

from newsdom_api.mineru_runner import build_mineru_command


def test_build_mineru_command_uses_pipeline_backend(tmp_path: Path):
    cmd = build_mineru_command(Path("input.pdf"), tmp_path)
    assert "pipeline" in cmd
    assert "ocr" in cmd
    assert "japan" in cmd
