from __future__ import annotations

import tempfile
from pathlib import Path

from .dom_builder import build_dom
from .mineru_runner import run_mineru
from .schemas import ParseResponse


def parse_pdf_bytes(data: bytes, filename: str = "upload.pdf") -> ParseResponse:
    with tempfile.TemporaryDirectory(prefix="newsdom-upload-") as tempdir:
        pdf_path = Path(tempdir) / filename
        pdf_path.write_bytes(data)
        mineru_output = run_mineru(pdf_path)
        response = build_dom(mineru_output["content_list"], document_id=pdf_path.stem)
        return response
