# Contributing

## Development setup

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Install the parser stack only when you need live MinerU execution:

```bash
pip install -e .[parser]
```

## Test commands

```bash
pytest
PYTHONWARNINGS=error pytest
```

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
