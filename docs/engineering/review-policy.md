# Review policy

## Review expectations

- Human review is the merge authority when the ruleset requires it.
- CodeRabbit is advisory automation that can accelerate triage and
  small follow-up fixes.
- Required checks must be green before a PR is considered merge-ready.

## Thread handling

- Resolve review comments only after the underlying code, docs, or
  tests change.
- Keep unresolved external blockers visible in PR comments and linked issues.
- If the repository ruleset demands approvals that current reviewer
  capacity cannot satisfy, track that gap explicitly instead of
  pretending the PR is mergeable.

## Scope discipline

- Keep PRs MECE: one root cause family per PR, with stacked PRs for
  clearly separate follow-ups.
- Re-check review state after any push because last-push approval and
  stale-review dismissal are enabled.
