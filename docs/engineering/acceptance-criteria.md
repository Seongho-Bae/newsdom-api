# Acceptance criteria

Repository work is done only when the relevant code, documentation,
and delivery evidence all agree.

## Required verification

- `uv run pytest`
- `uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100`
- `uv run mkdocs build --strict` whenever user-facing manual content
  changes
- relevant targeted smoke tests for changed delivery paths
  (container, fuzz, release, or API)

## Additional gates

- New tests must fail first, then pass after the implementation.
- Documentation changes must match live workflow and repository settings.
- Required GitHub checks for the affected PR must be green before merge.
- If a task touches release or delivery code, the release path or
  blocker evidence must be updated.
- If a task touches API security posture,
  `docs/security/api-security-checklist.md` must still be satisfied.

## Non-acceptance conditions

- stale docs that contradict code or live GitHub settings
- green local tests with known broken workflow/release paths
- untracked external blockers without an issue or PR comment explaining them
