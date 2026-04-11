# Security Gates Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add OpenSSF Scorecard and adjacent security workflows, then make them required checks on `main` and `develop`.

**Architecture:** Extend GitHub Actions with three lightweight security workflows—Scorecard, CodeQL, and Dependency Review—using explicit job names so branch protection can require them deterministically.

**Tech Stack:** GitHub Actions, OpenSSF Scorecard Action, GitHub CodeQL, Dependency Review Action.

---

### Task 1: Add security workflows

**Files:**
- Create: `.github/workflows/scorecards.yml`
- Create: `.github/workflows/codeql.yml`
- Create: `.github/workflows/dependency-review.yml`

**Step 1: Write the failing test**

Add a repo test that asserts these workflow files exist.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_readme.py -v`
Expected: FAIL until the files are added and referenced.

**Step 3: Write minimal implementation**

Add the workflows with explicit job names:
- `scorecard`
- `codeql (python, actions)`
- `dependency-review`

**Step 4: Run test to verify it passes**

Run: `pytest`
Expected: PASS.

**Step 5: Commit**

```bash
git add .github/workflows/*.yml tests/
git commit -m "ci: add security workflows"
```

### Task 2: Add minimal documentation signal

**Files:**
- Modify: `README.md`

**Step 1: Write the failing test**

Add a doc test that checks for the Scorecard badge URL or text.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_readme.py -v`
Expected: FAIL until README is updated.

**Step 3: Write minimal implementation**

Add a single Scorecard badge near the title.

**Step 4: Run test to verify it passes**

Run: `pytest`
Expected: PASS.

### Task 3: Verify workflow syntax and tests

**Files:**
- No new files.

**Step 1: Run unit tests**

Run: `pytest`

**Step 2: Run warnings-as-errors tests**

Run: `PYTHONWARNINGS=error pytest`

**Step 3: Validate workflow files structurally**

Run a YAML parser or equivalent check against `.github/workflows/*.yml`.

### Task 4: Update branch protections

**Files:**
- No new files.

**Step 1: Update `main` protection**

Require:
- `pytest`
- `scorecard`
- `codeql (python, actions)`
- `dependency-review`

**Step 2: Update `develop` protection**

Require the same checks.

**Step 3: Verify protections**

Run GitHub API reads for both branches and confirm the contexts list matches exactly.
