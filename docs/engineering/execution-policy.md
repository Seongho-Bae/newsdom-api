# Execution policy

## Default operating mode

- Pick the highest-impact executable task from the current repository
  state.
- Verify branch, PR, issue, workflow, and comment state before
  acting.
- Prefer repository-local docs over external conventions.
- Continue with adjacent executable work when a PR is blocked by
  external review or policy.

## Implementation rules

- Use TDD: write the failing test first, confirm the failure, then
  implement the minimal fix.
- Keep changes scoped to the current root cause plus required
  documentation and regression coverage.
- Re-check live GitHub state before claiming a blocker is external.
- Treat PR/issue comments as mandatory truth sources, not optional context.

## Delivery rules

- For normal work, branch from `develop` and target `develop`.
- For stable-release synchronization, operate on the `main` path
  deliberately and keep backports explicit.
- Prefer stacked PRs over mixing unrelated follow-up work into a
  blocked branch without documentation.
- If release work becomes unblocked, continue through changelog,
  artifact, and provenance verification instead of stopping at code
  completion.
