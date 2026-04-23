# OCR issue program and local accuracy investigation design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Re-anchor the OCR issue program around current `develop`, repair missing GitHub hierarchy/continuity, and land the smallest root-cause code slice that improves real local-only OCR accuracy interpretation without exposing copyrighted inputs.

**Architecture:** Treat the active OCR work as a coordinated program rooted at issue `#61`, with local-only measurement, normalization, runtime/Kubernetes, and evidence tracks separated into explicit child issues. In code, preserve the full MinerU artifact contract (`content_list` + `model`) through service/builder boundaries so page-aware normalization and redacted local-only metrics can become accurate and repeatable.

**Tech Stack:** FastAPI, Pydantic, MinerU CLI, pytest, GitHub Issues/PRs via `gh`, uv-managed Python environment.

---

## Current-code findings

- Fresh `origin/develop` baseline in the new worktree passes locally after `uv sync --frozen --all-extras` and `uv run pytest -q` (`160 passed`).
- Local-only copyrighted OCR fixture directory exists outside the repo and contains **5 PDFs**; no durable OCR text or filenames may be committed.
- MinerU is available in the worktree venv (`.venv/bin/mineru`).
- Canonical OCR program remains rooted at **issue `#61`** with milestone **`v0.2.0 OCR accuracy and runtime readiness`**.
- GitHub-native subissues under `#61` currently include `#60`, `#62`, `#63`, `#64`, `#66`, `#67`.
- **`#68` is milestone-linked but not wired as a subissue** even though its body makes it a child of `#66` / `#61`.
- Canonical active OCR PR is **`#65`**, but it is blocked by review state (`reviewDecision=CHANGES_REQUESTED`) despite green checks and mergeable head.
- Current OCR accuracy bottleneck is not just engine OCR itself: `service.py` drops `model`, `dom_builder.py` collapses everything into one page, and `equivalence.py` / `derive_private_baseline.py` are too coarse for local-only structural accuracy measurement.

## Root-cause frame

1. **Normalization contract loss**
   - `run_mineru()` returns `model`, but `parse_pdf_bytes()` discards it.
   - `build_dom()` only builds a single page and ignores `page_idx` / model page info.
2. **Accuracy evidence is too coarse**
   - `private_page_baseline.json` and `equivalence.py` measure only a few counts/ratios.
   - This can make real recognition loss and post-processing loss indistinguishable.
3. **Issue program continuity is partially stale**
   - `#68` needs native subissue wiring.
   - `#60/#63/#64/#66/#67` need clearer blocked-by / follow-up structure in bodies.
4. **Kubernetes/runtime track must remain explicit**
   - OCR-capable runtime contract (`#64`) remains separate from measurement and normalization.

## Proposed execution order

1. Repair GitHub issue hierarchy and bodies to reflect current code and blockers.
2. Land the smallest code slice that preserves MinerU `model` through service and builder and reconstructs multi-page output.
3. Tighten redacted structural metrics / baseline derivation for local-only measurement.
4. Re-run tests/coverage/docs; then push, open or attach to canonical PR, and continue follow-through.

## Guardrails

- Do not print or persist copyrighted OCR text, raw filenames, or absolute private paths.
- Keep durable evidence to structural counts, page counts, ratios, runtime metadata, sanitized warnings.
- Any warning/deprecation/linter/security issue found in the touched slice must be root-caused and fixed, or moved into a durable issue/skill if broader.
- Treat human review as non-authoritative for planning; use repo-local PR continuity and current-head robot review evidence for merge readiness.
