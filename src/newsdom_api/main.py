"""FastAPI entrypoints for the NewsDOM service."""

from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, File, UploadFile

from .schemas import ParseResponse
from .service import parse_pdf_bytes

app = FastAPI(title="NewsDOM API")


@app.get("/health")
def health() -> dict[str, str]:
    """Return a minimal liveness response for health checks."""

    return {"status": "ok"}


@app.post("/parse", response_model=ParseResponse)
async def parse(file: Annotated[UploadFile, File(...)]) -> ParseResponse:
    """Parse an uploaded PDF into the canonical DOM response model."""

    return parse_pdf_bytes(await file.read(), filename=file.filename or "upload.pdf")
