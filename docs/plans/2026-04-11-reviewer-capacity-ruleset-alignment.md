# Reviewer-capacity ruleset alignment Implementation Plan

> **Execution note:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove the unsatisfiable reviewer-capacity deadlock on `main` and `develop`, keep non-review branch protections intact, and align repository docs/tests with the live single-maintainer exception.

**Architecture:** Update repository governance truth sources and regression tests first, then apply the live GitHub ruleset change with a durable rollback payload, re-verify mergeability for PR #35 and PR #34, and close the now-stale blocker tracking issues. Preserve required CI checks, linear history, non-fast-forward protection, and deletion protection throughout.

**Tech Stack:** Python/pytest, MkDocs, GitHub rulesets via `gh api`, GitHub PR/issue state via `gh`.

---

### Task 1: Add the failing governance-doc regression tests

**Files:**
- Modify: `tests/test_repository_governance.py`
- Modify: `tests/test_engineering_canonical_docs.py`

**Step 1: Write the failing tests**

Add a new manual-governance expectation and a new review-policy expectation.

```python
def test_development_manual_documents_single_maintainer_exception() -> None:
    manual_text = Path("manual/development.md").read_text(encoding="utf-8")
    for phrase in (
        "단일 유지보수자 예외",
        "필수 상태 체크",
        "리뷰어 용량이 확보되면",
        "CODEOWNERS",
    ):
        assert phrase in manual_text


def test_review_policy_documents_single_maintainer_exception() -> None:
    text = Path("docs/engineering/review-policy.md").read_text(encoding="utf-8").lower()
    for expected in (
        "single-maintainer",
        "reviewer capacity",
        "required checks",
        "re-tighten",
    ):
        assert expected in text
```

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_repository_governance.py tests/test_engineering_canonical_docs.py -q`

Expected: FAIL because the current docs still describe the unsatisfiable 2-approval + CODEOWNERS + last-push model and do not mention a single-maintainer exception.

**Step 3: Commit the red test changes only after you have seen the failure**

```bash
git add tests/test_repository_governance.py tests/test_engineering_canonical_docs.py
git commit -m "test: add failing reviewer-capacity governance expectations"
```

### Task 2: Update durable governance truth sources

**Files:**
- Modify: `manual/development.md`
- Modify: `manual/index.md`
- Modify: `docs/engineering/review-policy.md`
- Add: `docs/adr/0002-single-maintainer-review-exception.md`

**Step 1: Write the minimal documentation changes**

Update the manual and review-policy docs so they all say the same thing:

- `main` and `develop` still require PR-based flow, required checks, linear history, non-fast-forward prevention, and thread resolution.
- While the repository has only one maintainer, review requirements are running under a documented **single-maintainer exception**.
- The stronger steady-state target is restored only after non-author reviewer capacity exists.

Use wording equivalent to the following in `manual/development.md`:

```md
### ✅ GitHub 보호 규칙과 단일 유지보수자 예외

`main` 및 `develop` 브랜치에는 GitHub ruleset이 적용되어 있으며, 현재는
단일 유지보수자 저장소 예외로 운영됩니다.

- Pull Request를 거쳐서만 병합할 수 있습니다.
- `pytest`, `scorecard`, `codeql (python, actions)`, `dependency-review`,
  `quality-gate` 필수 체크는 계속 강제됩니다.
- 선형 히스토리, force-push 금지, 브랜치 삭제 금지는 계속 유지됩니다.
- 리뷰어 용량이 확보되면 `1명 이상의 비작성자 승인 + CODEOWNERS + 마지막 푸시 승인`
  정책으로 다시 강화하고, 두 명의 독립 리뷰어가 확보되면 그때 2명 승인으로 올립니다.
```

Use wording equivalent to the following in the new ADR:

```md
# ADR-0002: Single-maintainer protected-branch review exception

## Status

Accepted

## Decision

Temporarily relax mandatory approval/CODEOWNERS/last-push review gates while the
repository has only one maintainer, but keep PR-only flow, required checks, and
history protections in place.

## Revisit trigger

Restore at least 1 non-author approval + CODEOWNERS + last-push approval as soon
as one non-author code owner exists, and restore 2 approvals only when two
independent reviewers exist.
```

**Step 2: Run the targeted tests to verify they now pass**

Run: `uv run pytest tests/test_repository_governance.py tests/test_engineering_canonical_docs.py -q`

Expected: PASS.

**Step 3: Commit the docs + test green state**

```bash
git add tests/test_repository_governance.py tests/test_engineering_canonical_docs.py \
  manual/development.md manual/index.md docs/engineering/review-policy.md \
  docs/adr/0002-single-maintainer-review-exception.md
git commit -m "docs: record single-maintainer review exception"
```

### Task 3: Re-run full repository verification before touching live GitHub rules

**Files:**
- Modify: none

**Step 1: Run the test suite**

Run: `uv run pytest`

Expected: PASS.

**Step 2: Run the coverage gate**

Run: `uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100`

Expected: PASS with 100% coverage.

**Step 3: Run the manual/docs build**

Run: `uv run mkdocs build --strict`

Expected: PASS.

**Step 4: Commit only if any verification-driven file change was necessary**

```bash
git add <only-the-files-you-had-to-fix>
git commit -m "fix: align governance docs with verification feedback"
```

### Task 4: Capture the current ruleset and apply the live single-maintainer exception

**Files:**
- Add: `docs/plans/2026-04-11-reviewer-capacity-ruleset-before.json`

**Step 1: Capture the rollback payload**

Run:

```bash
gh api repos/Seongho-Bae/newsdom-api/rulesets/14875805 > docs/plans/2026-04-11-reviewer-capacity-ruleset-before.json
```

Expected: the file contains the current 2-approval + CODEOWNERS + last-push payload for rollback.

**Step 2: Verify the current live state one more time**

Run:

```bash
gh api repos/Seongho-Bae/newsdom-api/rules/branches/develop && gh api repos/Seongho-Bae/newsdom-api/rules/branches/main
```

Expected: both branches still show `required_approving_review_count: 2`, `require_code_owner_review: true`, and `require_last_push_approval: true`.

**Step 3: Apply the minimal ruleset change**

Run:

```bash
gh api --method PUT repos/Seongho-Bae/newsdom-api/rulesets/14875805 \
  --input - <<'EOF'
{
  "name": "mirror-classic-protection-main-develop",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "exclude": [],
      "include": ["refs/heads/main", "refs/heads/develop"]
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "required_reviewers": [],
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true,
        "allowed_merge_methods": ["merge", "squash", "rebase"]
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "do_not_enforce_on_create": true,
        "required_status_checks": [
          {"context": "pytest", "integration_id": 15368},
          {"context": "scorecard", "integration_id": 15368},
          {"context": "codeql (python, actions)", "integration_id": 15368},
          {"context": "dependency-review"},
          {"context": "quality-gate"}
        ]
      }
    },
    {"type": "required_linear_history"},
    {"type": "non_fast_forward"},
    {"type": "deletion"}
  ],
  "bypass_actors": []
}
EOF
```

Expected: GitHub returns the updated ruleset JSON.

**Step 4: Re-query the ruleset to verify the live change**

Run:

```bash
gh api repos/Seongho-Bae/newsdom-api/rulesets/14875805
```

Expected: `required_approving_review_count` is `0`, `require_code_owner_review` is `false`, `require_last_push_approval` is `false`, and the required status checks/history protections are unchanged.

**Step 5: Commit the durable rollback payload**

```bash
git add docs/plans/2026-04-11-reviewer-capacity-ruleset-before.json
git commit -m "docs: capture pre-exception ruleset payload"
```

### Task 5: Verify PR continuity, mergeability, and close the blocker chain

**Files:**
- Modify: none

**Step 1: Re-check PR #35 and PR #34 state**

Run:

```bash
gh pr view 35 --json reviewDecision,mergeStateStatus,statusCheckRollup,url && \
gh pr view 34 --json reviewDecision,mergeStateStatus,statusCheckRollup,url
```

Expected: checks remain green and the merge blocker is no longer `REVIEW_REQUIRED`.

**Step 2: Merge PR #35 first**

Run: `gh pr merge 35 --merge --delete-branch=false`

Expected: PR #35 merges into `develop` without bypass.

**Step 3: Merge PR #34 second**

Run: `gh pr merge 34 --merge --delete-branch=false`

Expected: PR #34 merges into `main` without bypass.

**Step 4: Close/update the tracking issues**

Run equivalent GitHub updates:

- add a closing comment to issue #36 explaining the ruleset alignment and merged PRs
- close issue #36 as completed
- close issue #40 and issue #41 because their blocked changes have now landed on `develop`

**Step 5: Re-check downstream release readiness**

Run:

```bash
gh issue view 32 --comments && gh pr list --state open
```

Expected: issue #32 is now the next executable canonical task and open PR inventory no longer includes #34 or #35.
