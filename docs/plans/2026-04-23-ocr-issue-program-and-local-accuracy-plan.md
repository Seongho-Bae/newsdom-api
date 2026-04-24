# OCR issue program and local accuracy implementation plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Repair OCR GitHub continuity and implement the smallest page-aware/local-only accuracy slice on top of current `develop`.

**Architecture:** First update issue hierarchy so the OCR program’s execution order matches current code reality. Then pass MinerU `model` end-to-end and extend DOM/equivalence logic just enough to preserve multi-page structure and generate richer redacted metrics without storing private content.

**Tech Stack:** Python 3.13 via uv, FastAPI, MinerU CLI, pytest, GitHub CLI.

---

### Task 1: Repair GitHub OCR hierarchy and issue bodies

**Files / surfaces:**
- Modify issue bodies: `#61`, `#60`, `#63`, `#64`, `#66`, `#67`, `#68`
- GitHub hierarchy: sub-issue wiring under `#61` / `#66`

**Step 1: Re-read current issue bodies and hierarchy**

Run:

```bash
gh api graphql -f query='query { repository(owner:"Seongho-Bae", name:"newsdom-api") { issue61: issue(number:61) { number title id subIssues(first:20) { nodes { id number title } } } issue66: issue(number:66) { number title id subIssues(first:20) { nodes { id number title } } } issue68: issue(number:68) { number title id } } }'
```

Expected: `#68` is not yet wired under `#66` or `#61`.

**Step 2: Update issue bodies to current-code language**

- Ensure `#61` names `#62` + `#67` as highest-priority implementation/measurement tracks.
- Ensure `#60` explicitly follows `#62` and `#67`.
- Ensure `#63` consumes outputs from `#67`.
- Ensure `#64` stays runtime/Kubernetes-specific.
- Ensure `#66` owns warning/runtime harness stabilization.
- Ensure `#68` is described as the bounded runtime child slice.

**Step 3: Wire missing native subissue**

Add `#68` under `#66`.

**Step 4: Verify hierarchy**

Run the GraphQL query again and confirm `#68` appears under `#66`.

---

### Task 2: Add failing tests for page-aware DOM and model propagation

**Files:**
- Modify: `tests/test_dom_builder.py`
- Modify: `tests/test_service.py`

**Step 1: Write failing DOM tests**

Add tests that prove:
- `build_dom(..., model=...)` accepts optional model input
- `page_idx` and/or model `page_info` produce multiple `PageNode`s
- no false page-divergence warning is emitted when no model exists

**Step 2: Run failing DOM tests**

Run:

```bash
uv run pytest tests/test_dom_builder.py -q
```

Expected: failure because `build_dom` lacks `model` support and multi-page behavior.

**Step 3: Write failing service test**

Add/adjust a test proving `parse_pdf_bytes()` forwards `mineru_output["model"]` into `build_dom(...)`.

**Step 4: Run failing service test**

Run:

```bash
uv run pytest tests/test_service.py -q
```

Expected: failure because `service.py` drops the `model` payload.

---

### Task 3: Implement minimal page-aware model propagation

**Files:**
- Modify: `src/newsdom_api/service.py`
- Modify: `src/newsdom_api/dom_builder.py`

**Step 1: Extend builder signature minimally**

- Accept `model: list[dict[str, Any]] | None = None`
- Keep backward compatibility for existing single-page callers/tests.

**Step 2: Preserve multi-page structure**

- Group blocks by `page_idx` when present.
- Use model `page_info` for page number/size when available.
- Keep the existing article/ad/header/image heuristics scoped per page.

**Step 3: Thread `model` through service**

- Pass `mineru_output.get("model")` into `build_dom(...)`.

**Step 4: Run targeted tests**

Run:

```bash
uv run pytest tests/test_dom_builder.py tests/test_service.py -q
```

Expected: green.

---

### Task 4: Add failing tests for richer redacted structural metrics

**Files:**
- Modify: `tests/test_fixture_equivalence.py`
- Add/modify tests near `equivalence.py` if needed

**Step 1: Write failing metric/equivalence tests**

Add tests that prove:
- baseline comparison can include page count or page-structure-sensitive metrics
- results remain non-expressive and numeric only

**Step 2: Run failing tests**

Run:

```bash
uv run pytest tests/test_fixture_equivalence.py -q
```

Expected: failure until richer metric support is implemented.

---

### Task 5: Implement minimal richer redacted metric support

**Files:**
- Modify: `src/newsdom_api/equivalence.py`
- Modify: `tools/derive_private_baseline.py`
- Possibly update: `tests/fixtures/private_page_baseline.json`

**Step 1: Add one or two page-aware structural metrics only**

Examples:
- `page_count`
- `headline_page_coverage` or similar strictly numeric ratio

Do not add expressive text artifacts.

**Step 2: Keep derivation script durable and local-safe**

- Ensure generated JSON stays structural/numeric only.

**Step 3: Run targeted tests**

Run:

```bash
uv run pytest tests/test_fixture_equivalence.py -q
```

Expected: green.

---

### Task 6: Refresh docs for local-only evidence workflow if contract changed

**Files:**
- Modify as needed: `tests/fixtures/README.md`
- Modify as needed: `manual/development.md`

**Step 1: Update docs only if metric contract changed**

- Document newly allowed redacted numeric/structural metrics.
- Re-state forbidden classes (private text, filenames, raw OCR output).

**Step 2: Build docs strictly**

Run:

```bash
uv run mkdocs build --strict
```

Expected: success.

---

### Task 7: Full verification and delivery continuity

**Files / surfaces:**
- Whole repo verification
- GitHub PR continuity

**Step 1: Run full tests**

```bash
uv run pytest
```

**Step 2: Run full coverage gate**

```bash
uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100
```

**Step 3: Re-check PR continuity before opening/updating PR**

```bash
gh pr list --head "feature/ocr-accuracy-program-followthrough-8" --json number,url,state
```

Expected: no duplicate PR for this branch.

**Step 4: Push and open draft PR if none exists**

- Target `develop`
- Link `#61`, `#62`, `#67`, and any issue-body updates landed in Task 1.

**Step 5: Continue through merge path**

- If branch is behind, update branch.
- If checks are green and robot review gate is satisfied, continue toward merge.
- If externally blocked, leave durable blocker evidence and keep moving on adjacent OCR follow-up work.
