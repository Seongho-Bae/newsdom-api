# NewsDOM API

NewsDOM API parses scanned Japanese newspaper PDFs into DOM-like article trees.

## Primary parser

- Primary engine: `MinerU` pipeline backend
- Service wrapper: FastAPI
- Output: canonical JSON with pages, articles, headlines, body blocks, images, captions, and quality metadata

## Copyright-safe testing

This repository does **not** include the original copyrighted newspaper PDF used during local validation.

Instead, it ships:

- a fully **synthetic** newspaper-like PDF generator
- a synthetic ground-truth JSON sidecar
- an **equivalence** test against private-page-derived structural metrics only

The committed baseline contains only non-expressive numeric layout metrics and no copyrighted text or imagery.

## Install

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

To enable real parsing with MinerU:

```bash
pip install -e .[parser]
```

## Run

```bash
uvicorn newsdom_api.main:app --reload
```

## Tests

```bash
pytest
```

## Local-only baseline derivation

If you have a private reference page and want to refresh structural baselines locally:

```bash
python tools/derive_private_baseline.py tests/fixtures/private_page_baseline.json
```

Do not commit copyrighted source PDFs or source-derived OCR text.
