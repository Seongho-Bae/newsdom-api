# Quality Gate Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a repository quality gate for 100% line coverage and 100% source docstring coverage, then make the codebase satisfy it.

**Architecture:** Use `pytest-cov` for line coverage and a repo-local AST-based docstring audit test for source modules. Backfill tests and docstrings until both local execution and CI can enforce the baseline.

**Tech Stack:** Python 3.10, pytest, pytest-cov, GitHub Actions.

---

### Task 1: Add failing docstring audit test

**Files:**
- Create: `tests/test_docstrings.py`

**Step 1: Write the failing test**
- Audit every source module/class/function in `src/newsdom_api`.
- Fail if any object lacks a docstring.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_docstrings.py -v`

**Step 3: Add minimal code changes**
- Backfill docstrings.

### Task 2: Add coverage tooling and failing coverage measurement

**Files:**
- Modify: `pyproject.toml`

**Step 1: Add `pytest-cov` to dev dependencies**

**Step 2: Run coverage command to measure current gap**

Run: `pytest --cov=src/newsdom_api --cov-report=term-missing --cov-fail-under=100`

Expected: FAIL before additional tests are written.

### Task 3: Backfill tests to 100% line coverage

**Files:**
- Create/modify targeted tests under `tests/`

**Step 1: Add tests for uncovered branches in**
- `mineru_runner.py`
- `service.py`
- `synthetic.py`
- `equivalence.py`
- `dom_builder.py`

**Step 2: Re-run full suite with 100% threshold**

### Task 4: Add CI workflow and required check

**Files:**
- Create: `.github/workflows/quality-gate.yml`
- Modify: branch protection required checks

**Step 1: Add workflow job named `quality-gate`**

**Step 2: Verify YAML, tests, and coverage locally**

**Step 3: Update branch protection to require `quality-gate` on `main` and `develop`
