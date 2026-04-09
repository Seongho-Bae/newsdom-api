# Contributing

## Development setup

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Install the parser stack only when you need live MinerU execution:

```bash
pip install "mineru[pipeline]==3.0.9"
```

## Test commands

```bash
pytest
PYTHONWARNINGS=error pytest
pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100
```

CI installs dependencies from `uv.lock`, and workflow actions are pinned by immutable commit SHA. Keep both policies intact when editing `.github/` automation.

CircleCI parity is defined in `.circleci/config.yml` and mirrors the same uv-locked warnings-as-errors and 100% coverage quality gate.

## Documentation build

The GitHub Pages workflow installs documentation tooling from `uv.lock` via the optional `docs` extra. For local maintainer work, sync all extras so the docs build does not drop the test toolchain from the active environment.

```bash
uv sync --frozen --all-extras
uv run mkdocs build --strict
```

Tagged releases use `.github/workflows/release.yml` to build artifacts, generate SHA256 checksums, emit a JSON manifest, and publish a GitHub Release with provenance attestation.

## Fixture policy

This project intentionally separates public test artifacts from private validation material.

Allowed in the repository:

- synthetic PDFs
- synthetic sidecar JSON
- derived, non-expressive structural metrics

Not allowed in the repository:

- copyrighted source newspaper PDFs
- OCR text copied from private reference pages
- image crops extracted from private reference pages

## Private baseline refresh

If you maintain a private reference page locally, refresh only the derived structural baseline:

```bash
python tools/derive_private_baseline.py tests/fixtures/private_page_baseline.json
```

The source page must remain local.

## Documentation split

- `README.md`: user-facing overview and quickstart
- `CONTRIBUTING.md`: maintainer workflow and safety rules
- `SECURITY.md`: vulnerability reporting and supported-branch policy
- `docs/workflow/git-flow.md`: canonical branch workflow
- `tests/fixtures/README.md`: fixture provenance and regeneration notes
- `docs/plans/`: design and implementation planning notes

## Branch workflow

This repository uses a manual Git Flow model.

- Branch normal work from `develop`
- Open feature/fix/chore pull requests into `develop`
- Use `release/*` and `hotfix/*` only when stabilizing or patching production history

See `docs/workflow/git-flow.md` for the full branch model.
