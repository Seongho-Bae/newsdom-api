from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def build_mineru_command(
    input_pdf: Path, output_dir: Path, mineru_bin: str = "mineru"
) -> list[str]:
    return [
        mineru_bin,
        "-p",
        str(input_pdf),
        "-o",
        str(output_dir),
        "-b",
        "pipeline",
        "-m",
        "ocr",
        "-l",
        "japan",
    ]


def _resolve_mineru_bin() -> str:
    configured = os.environ.get("NEWSDOM_MINERU_BIN")
    if configured:
        return configured
    return shutil.which("mineru") or "mineru"


def _find_output_dir(base_output_dir: Path) -> Path:
    candidates = list(base_output_dir.glob("*/ocr"))
    if not candidates:
        raise FileNotFoundError(f"No MinerU OCR output found under {base_output_dir}")
    return candidates[0]


def run_mineru(input_pdf: Path) -> dict[str, Any]:
    mineru_bin = _resolve_mineru_bin()
    with tempfile.TemporaryDirectory(prefix="newsdom-mineru-") as tempdir:
        output_dir = Path(tempdir)
        cmd = build_mineru_command(input_pdf, output_dir, mineru_bin=mineru_bin)
        completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
        ocr_dir = _find_output_dir(output_dir)
        content_path = ocr_dir / f"{input_pdf.stem}_content_list.json"
        if not content_path.exists():
            json_candidates = sorted(ocr_dir.glob("*_content_list.json"))
            if not json_candidates:
                raise FileNotFoundError("MinerU content list JSON was not produced")
            content_path = json_candidates[0]
        model_candidates = sorted(ocr_dir.glob("*_model.json"))
        if not model_candidates:
            raise FileNotFoundError("MinerU model JSON was not produced")
        return {
            "content_list": json.loads(content_path.read_text(encoding="utf-8")),
            "model": json.loads(model_candidates[0].read_text(encoding="utf-8")),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
