# Design: reviewer-capacity ruleset alignment

## Context

- The current canonical blocked delivery path is issue #36.
- PR #35 (`develop`) and PR #34 (`main`) are both green on code and required checks but blocked by the active repository ruleset.
- Live GitHub rules require 2 approving reviews, CODEOWNERS review, last-push approval, resolved review threads, and required checks on both `develop` and `main`.
- Live collaborator inventory currently exposes only the sole author/admin account.
- With one maintainer and `.github/CODEOWNERS` pointing only at `@Seongho-Bae`, any policy that still requires at least one non-author approval or required CODEOWNERS review remains operationally unsatisfiable.

## Constraints

- Preserve required CI checks, linear history, non-fast-forward prevention, and branch deletion protection.
- Avoid admin bypass merges as the normal path.
- Keep repository truth sources aligned with live GitHub settings.
- Keep the change MECE: solve the reviewer-capacity deadlock itself, not unrelated code paths already green in PR #34 and PR #35.
- Leave a durable trail for later re-tightening once reviewer capacity exists.

## Approaches considered

### 1. Keep the current 2-approval + CODEOWNERS + last-push policy

- Pros: strongest branch-protection posture and best future Scorecard branch-protection signal.
- Cons: not executable today because no non-author reviewer exists; leaves PR #34, PR #35, issue #32, issue #40, and issue #41 blocked.
- Verdict: reject for the current canonical task because it does not close the live blocker.

### 2. Merge through admin or other bypass mechanics without changing the ruleset

- Pros: would unblock the two PRs quickly.
- Cons: does not remove the root cause, weakens auditability, conflicts with the repository preference against protection bypass as a normal workflow, and leaves the next PR deadlocked again.
- Verdict: reject because it treats the symptom instead of the cause.

### 3. Phased single-maintainer ruleset alignment (recommended)

- Temporarily align the live ruleset with actual maintainer capacity by keeping PR-only flow and required checks/history protections, but removing the currently unsatisfiable mandatory approval/CODEOWNERS/last-push requirements.
- Update repository docs and governance tests to describe this as a single-maintainer exception rather than a permanent steady state.
- Record the restoration trigger: move back to at least 1 approval + CODEOWNERS + last-push approval once a non-author code owner exists, and only return to 2 approvals when two independent reviewers exist.
- Pros: closes the real blocker, preserves CI/security checks, restores merge/release flow, and documents the trade-off.
- Cons: weakens review-gate strength and may reduce Scorecard branch-protection posture until reviewer capacity grows.

## Recommended design

Implement approach 3 with an explicit rollback/re-tightening plan.

### Components

1. **Live GitHub ruleset**
   - Edit the `mirror-classic-protection-main-develop` ruleset for `main` and `develop`.
   - Keep:
     - pull-request-only merges
     - required status checks
     - required linear history
     - non-fast-forward prevention
     - branch deletion protection
   - Relax for the single-maintainer exception:
     - `required_approving_review_count = 0`
     - `require_code_owner_review = false`
     - `require_last_push_approval = false`

2. **Repository truth sources**
   - Update `manual/development.md` and `manual/index.md` so they match the live rules.
   - Update `docs/engineering/review-policy.md` to document the single-maintainer exception and the re-tightening trigger.
   - Add or update an ADR/governance note capturing why the exception exists and when it must be removed.

3. **Regression tests**
   - Add a failing test first for the new documented governance posture.
   - Update repository governance tests so they verify the manual and policy docs describe the temporary single-maintainer exception accurately.

4. **Delivery continuity**
   - Re-verify PR #35 and PR #34 mergeability after the ruleset change.
   - Merge them through the normal PR path if they become mergeable.
   - Re-check the downstream release path in issue #32 and the tracking issues #40 and #41.

## Data flow

1. Capture the current ruleset JSON for rollback evidence.
2. Add/update failing governance-doc tests.
3. Update docs/ADR/policy to the intended single-maintainer wording.
4. Run local verification until green.
5. Apply the live ruleset change through the GitHub API.
6. Re-query the ruleset and PR states to confirm the blocker moved.
7. Merge PR #35 and PR #34 if all required checks and mergeability conditions are satisfied.
8. Re-evaluate issue #32, issue #40, issue #41, and code-scanning state.

## Error handling and rollback

- Before editing the ruleset, persist the current live ruleset JSON in the design/plan evidence so the prior configuration can be restored.
- If the new policy causes unexpected workflow or merge behavior, restore the saved ruleset payload via the same GitHub API path.
- If post-change verification shows additional hidden blockers, document them in the linked issue/PR comments before moving downstream.

## Testing strategy

- **Red**: repository governance/manual test(s) fail because the docs still hard-code the unsatisfiable 2-approval + CODEOWNERS + last-push model.
- **Green**: update docs/tests/policy/ADR until local checks pass.
- **Live verification**:
  - `gh api repos/Seongho-Bae/newsdom-api/rulesets/14875805`
  - `gh api repos/Seongho-Bae/newsdom-api/rules/branches/develop`
  - `gh api repos/Seongho-Bae/newsdom-api/rules/branches/main`
  - PR #35 / PR #34 mergeability and check re-checks
- **Repository verification**:
  - targeted governance tests
  - `uv run pytest`
  - `uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100`
  - `uv run mkdocs build --strict`

## Decisions

- Treat issue #36 as the highest-priority executable canonical task.
- Prefer a documented temporary single-maintainer exception over permanent deadlock or admin bypass merging.
- Preserve non-review branch protections and CI gates while reviewer capacity is absent.
