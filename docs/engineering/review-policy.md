# Review policy

## Review expectations

- Human review is the merge authority when the ruleset requires it.
- CodeRabbit is advisory automation that can accelerate triage and
  small follow-up fixes.
- Required checks must be green before a PR is considered merge-ready.

## Single-maintainer exception

- If reviewer capacity is limited to the sole author/admin account,
  do not pretend that non-author approvals or required CODEOWNERS
  review are satisfiable.
- In that state, prefer a documented temporary single-maintainer
  exception that keeps PR flow, required checks, thread resolution,
  and history protections intact.
- Re-tighten the ruleset to require at least one non-author approval,
  CODEOWNERS review, and last-push approval as soon as reviewer
  capacity exists beyond the sole maintainer.
- Restore the stronger two-approval policy only when two independent
  human reviewers are actually available.

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
