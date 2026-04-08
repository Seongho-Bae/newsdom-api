from __future__ import annotations

from fastapi import FastAPI, File, UploadFile

from .schemas import ParseResponse
from .service import parse_pdf_bytes

app = FastAPI(title="NewsDOM API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse", response_model=ParseResponse)
async def parse(file: UploadFile = File(...)) -> ParseResponse:
    return parse_pdf_bytes(await file.read(), filename=file.filename or "upload.pdf")
