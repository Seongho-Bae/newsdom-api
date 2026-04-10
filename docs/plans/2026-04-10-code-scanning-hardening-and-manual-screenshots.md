# Code Scanning Hardening and Manual Screenshots Implementation Plan

> Execute this plan task-by-task and verify each step before moving on.

**Goal:** Close the highest-priority executable security and code-scanning
gaps by hardening repository review protections and CodeQL coverage, then
update the Korean manual with verified screenshots.

**Architecture:** Add repository-owned governance artifacts (`CODEOWNERS`)
and expand workflow coverage so GitHub code scanning evaluates both Python
and GitHub Actions. Keep verification split between local TDD for repo files
and live GitHub API checks for ruleset state, then regenerate manual
screenshots from localhost-served pages so docs reflect the current product
surface.

**Tech Stack:** Python, pytest, GitHub Actions, GitHub REST API (`gh api`),
MkDocs Material, FastAPI, Playwright

---

## Task 1: Add failing tests for security workflow and manual screenshot expectations

**Files:**

- Create: `tests/test_repository_governance.py`
- Keep: `tests/test_readme.py` unchanged

### Step 1: Write the failing test

Add tests that assert:

- `.github/CODEOWNERS` exists and references the maintainer path ownership.
- `.github/workflows/codeql.yml` includes `actions` in the configured
  languages.
- `manual/api-reference.md` references screenshot assets.
- `manual/development.md` documents enforced review gates.
- `.gitignore` excludes generated runtime artifacts.

### Step 2: Run test to verify it fails

Run: `uv run pytest tests/test_repository_governance.py -q`

Expected: FAIL because `CODEOWNERS` is missing, CodeQL scans only `python`,
screenshot references do not exist, review-gate docs are incomplete, and
generated runtime artifacts are not ignored.

### Step 3: Write minimal implementation

Create `CODEOWNERS`, update `codeql.yml`, and add screenshot references to
the manual with matching assets.

### Step 4: Run test to verify it passes

Run: `uv run pytest tests/test_repository_governance.py -q`

Expected: PASS

### Step 5: Commit

```bash
git add tests/test_repository_governance.py tests/test_readme.py \
  .github/CODEOWNERS .github/workflows/codeql.yml \
  manual/api-reference.md manual/assets/
git commit -m "security: harden code scanning and document UI evidence"
```

## Task 2: Generate verified manual screenshots from localhost services

**Files:**

- Create: `manual/assets/swagger-ui.png`
- Create: `manual/assets/redoc.png`
- Modify: `manual/api-reference.md`

### Task 2 Step 1: Write the failing test

Extend the governance and manual test to assert the screenshot files exist,
carry real PNG signatures, and are referenced from the API manual.

### Task 2 Step 2: Run test to verify it fails

Run:
`uv run pytest tests/test_repository_governance.py::`
`test_api_manual_references_screenshot_assets -q`

Expected: FAIL because the screenshot files do not exist yet.

### Task 2 Step 3: Write minimal implementation

Start the FastAPI app locally, open `/docs` and `/redoc` with Playwright, and
capture screenshots into `manual/assets/`, then add Markdown image embeds plus
explanatory captions in `manual/api-reference.md`.

### Task 2 Step 4: Run test to verify it passes

Run:
`uv run pytest tests/test_repository_governance.py::`
`test_api_manual_references_screenshot_assets -q`

Expected: PASS

### Task 2 Step 5: Commit

```bash
git add manual/api-reference.md manual/assets/swagger-ui.png \
  manual/assets/redoc.png tests/test_repository_governance.py
git commit -m "docs: add verified API console screenshots"
```

## Task 3: Verify live GitHub ruleset posture and align remediation evidence

**Files:**

- Modify: `.github/CODEOWNERS`
- Modify: `.github/workflows/codeql.yml`
- Modify: `manual/development.md`

### Task 3 Step 1: Write the failing verification target

Record the desired live conditions:

- active ruleset requires 2 approving reviews
- code owner review is required
- last-push approval remains required

### Task 3 Step 2: Run verification to show current gap

Run: `gh api repos/Seongho-Bae/newsdom-api/rulesets` and capture the `id` for
the `mirror-classic-protection-main-develop` ruleset, then query
`gh api repos/Seongho-Bae/newsdom-api/rulesets/<id>`.

Expected: JSON shows `required_approving_review_count` is `1` and
`require_code_owner_review` is `false`.

### Task 3 Step 3: Write minimal implementation

Patch the repository ruleset via `gh api --method PUT ...` so it requires 2
approvals and code owner review, then document the strengthened governance
path in `manual/development.md`.

### Task 3 Step 4: Run verification to prove it passes

Run: `gh api repos/Seongho-Bae/newsdom-api/rulesets/<id>` using the resolved
ruleset identifier from the previous step.

Expected: JSON shows `required_approving_review_count` is `2`,
`require_code_owner_review` is `true`, and `require_last_push_approval`
remains `true`.

### Task 3 Step 5: Commit

```bash
git add .github/CODEOWNERS .github/workflows/codeql.yml manual/development.md
git commit -m "security: strengthen review gates for protected branches"
```

## Task 4: Full verification and delivery evidence

**Files:**

- Modify: `README.md`
- Modify: `manual/index.md`

### Task 4 Step 1: Run repository verification

Run:

- `uv sync --extra dev`
- `uv run pytest -q`
- `python3 scripts/prompt_checks/validate_canonical_doc_refs.py --root .`
  (skip if the script is not present in this repository)

Expected: all repo checks required for this task pass.

### Task 4 Step 2: Run live and manual verification

Run:

- `gh api repos/Seongho-Bae/newsdom-api/code-scanning/alerts?state=open&per_page=100`
- review the latest Scorecard and CodeQL posture after the push-triggered
  workflow

Expected: branch protection alert evidence reflects the tightened ruleset, and
new workflow coverage is present for future scans.

### Task 4 Step 3: Update docs if verification reveals drift

Refresh manual and README wording so documentation matches the verified
workflow and review posture.

### Task 4 Step 4: Commit

```bash
git add README.md manual/index.md
git commit -m "docs: align manual with security verification evidence"
```
