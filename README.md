# NewsDOM API

[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/Seongho-Bae/newsdom-api/badge)](https://securityscorecards.dev/viewer/?uri=github.com/Seongho-Bae/newsdom-api)

NewsDOM API parses scanned Japanese newspaper PDFs into DOM-like article trees.

## Features

- Primary engine: `MinerU` pipeline backend
- Service wrapper: FastAPI
- Output: canonical JSON with pages, articles, headlines, body blocks, images, captions, and quality metadata

## Quickstart

### Install

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

To enable real parsing with MinerU:

```bash
pip install -e .[parser]
```

### Run

```bash
uvicorn newsdom_api.main:app --reload
```

### Parse a PDF

```bash
curl -F "file=@sample.pdf" http://127.0.0.1:8000/parse
```

### Run tests

```bash
pytest
```

The repository also enforces a `quality-gate` workflow with 100% source coverage and docstring audit coverage.

## Fixtures and provenance

This repository ships only synthetic test fixtures and derived structural baselines. For fixture provenance and regeneration notes, see `tests/fixtures/README.md`.

## Development

Development setup, fixture handling rules, and local-only baseline maintenance are documented in `CONTRIBUTING.md`.

Security reporting guidance is documented in `SECURITY.md`.

Repository branch workflow is documented in `docs/workflow/git-flow.md`.

## Repository layout

- `src/newsdom_api/`: API, MinerU wrapper, DOM builder, synthetic fixture generator
- `tests/`: unit tests and committed synthetic fixtures
- `tools/`: local maintenance utilities
