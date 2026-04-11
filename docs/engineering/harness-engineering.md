# Harness engineering

This repository relies on durable verification harnesses instead of
informal spot checks.

## Local verification harnesses

- `uv run pytest` for full regression coverage
- `uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100`
- `uv run mkdocs build --strict` for the published manual
- targeted smoke entrypoints such as:
  - `uv run python fuzzers/dom_builder_fuzzer.py --smoke tests/fixtures/mineru_sample.json`
  - local container smoke against `/health`

## Live verification harnesses

- GitHub state via `gh pr view`, `gh issue view`, `gh api`, and
  workflow runs
- Playwright or equivalent browser capture when manual screenshots or
  localhost UI/API console evidence changes
- release artifact verification through GitHub Releases and exported
  `*.intoto.jsonl` bundles

## Evidence policy

- Prefer checked-in tests, screenshots in `manual/assets/`, ADRs,
  plan docs, and PR comments.
- Do not leave durable evidence only in `tmp/`.
- If logs are needed for deployment or workflow debugging, store or
  upload them somewhere durable and redact secrets.
