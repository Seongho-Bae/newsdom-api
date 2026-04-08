# Fixture provenance

This directory contains only redistributable synthetic artifacts and non-expressive derived metrics.

## Files

- `synthetic_reference.pdf`: synthetic newspaper-style test page
- `synthetic_reference.png`: rasterized image used to build the synthetic PDF
- `synthetic_reference.json`: synthetic ground-truth structure used by equivalence tests
- `private_page_baseline.json`: numeric layout targets derived from a private reference page
- `mineru_sample.json`: small hand-authored MinerU-like sample for unit tests

## Provenance model

The synthetic reference fixture is generated from original, fictional content and synthetic layout logic. It is designed to be structurally similar to a private reference page without reproducing that page’s protected expression.

`private_page_baseline.json` contains only coarse structural measurements such as block counts and ratios. It must not contain source text, source imagery, or OCR output from the private reference page.

## Regeneration

Regenerate the synthetic fixture with:

```bash
python - <<'PY'
from pathlib import Path
from newsdom_api.synthetic import generate_fixture
generate_fixture(Path('tests/fixtures'), seed=7)
PY
```

Refresh the private structural baseline locally with:

```bash
python tools/derive_private_baseline.py tests/fixtures/private_page_baseline.json
```

The private source page itself must never be committed.
