# Truth Source Alignment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use
> superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restore repository docs and workflow metadata so manuals, ADR
follow-ups, and planning docs reflect the actual verification and branch state.

**Architecture:** Add one focused regression test module for truth-source
drift, then make the minimal file edits needed to satisfy those tests. Keep
the task documentation-only except for removing the dead `master` GitHub Pages
trigger.

**Tech Stack:** Pytest, PyYAML, Markdown docs, GitHub Actions YAML.

---

## Task 1: Guard installation manual and Pages branch trigger drift

**Files:**

- Modify: `tests/test_truth_source_alignment.py`
- Modify: `manual/installation.md`
- Modify: `.github/workflows/gh-pages.yml`

### Task 1 / Step 1: Write the failing test

Add tests that fail when:

- `manual/installation.md` advertises `pytest -m "integration"` without any
  integration-marked tests in `tests/`
- `.github/workflows/gh-pages.yml` still includes `master` in its push branch
  trigger list

### Task 1 / Step 2: Run test to verify it fails

Run: `uv run pytest tests/test_truth_source_alignment.py -q`
Expected: FAIL on the installation manual and GitHub Pages trigger assertions.

### Task 1 / Step 3: Write minimal implementation

- Update `manual/installation.md` to document only real verification commands.
- Remove `master` from `.github/workflows/gh-pages.yml`.

### Task 1 / Step 4: Run test to verify it passes

Run:

```bash
TEST_FILE="tests/test_truth_source_alignment.py"
TEST_ONE="test_installation_manual_does_not_reference_empty_integration_marker"
TEST_TWO="test_gh_pages_workflow_targets_supported_branches_only"
uv run pytest \
  "$TEST_FILE::$TEST_ONE" \
  -q
uv run pytest \
  "$TEST_FILE::$TEST_TWO" \
  -q
```

Expected: PASS.

### Task 1 / Step 5: Commit

```bash
git add tests/test_truth_source_alignment.py manual/installation.md .github/workflows/gh-pages.yml
git commit -m "docs: align installation and Pages workflow contracts"
```

## Task 2: Guard stale security-plan and ADR references

**Files:**

- Modify: `tests/test_truth_source_alignment.py`
- Modify: `docs/adr/0001-openssf-best-practices-badge.md`
- Modify: `docs/plans/2026-04-08-security-gates.md`
- Modify: `docs/plans/2026-04-08-security-gates-design.md`

### Task 2 / Step 1: Write the failing test

Add tests that fail when:

- the security-gates plan docs still reference `codeql (python)` instead of
  `codeql (python, actions)`
- ADR-0001 still mentions stale issue references `#8` / `#10`

### Task 2 / Step 2: Run test to verify it fails

Run: `uv run pytest tests/test_truth_source_alignment.py -q`
Expected: FAIL on stale CodeQL naming and stale ADR follow-up references.

### Task 2 / Step 3: Write minimal implementation

- Update both security-gates docs to reflect the current required check name.
- Rewrite the ADR follow-up section to condition-based language without stale
  issue references.

### Task 2 / Step 4: Run test to verify it passes

Run: `uv run pytest tests/test_truth_source_alignment.py -q`
Expected: PASS.

### Task 2 / Step 5: Commit

```bash
git add tests/test_truth_source_alignment.py \
  docs/adr/0001-openssf-best-practices-badge.md \
  docs/plans/2026-04-08-security-gates*.md
git commit -m "docs: remove stale governance planning references"
```

## Task 3: Full verification

**Files:**

- No new files.

### Task 3 / Step 1: Run focused lint

Run: `uvx ruff check tests/test_truth_source_alignment.py`

### Task 3 / Step 2: Run full test suite

Run: `uv run pytest -q`

### Task 3 / Step 3: Capture git status

Run: `git status --short --branch`

### Task 3 / Step 4: Commit

```bash
git add .
git commit -m "docs: restore truth-source alignment for workflow and manual"
```
