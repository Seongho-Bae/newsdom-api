# ADR-0002: Single-maintainer protected-branch review exception

## Status

Accepted

## Context

The repository currently has one maintainer/admin account and no
non-author code owners or reviewers. The live protected-branch ruleset
for `main` and `develop` had been strengthened to require 2 approvals,
required `CODEOWNERS` review, and last-push approval.

That posture is desirable once reviewer capacity exists, but it is not
operationally satisfiable while the repository still has only the sole
author/admin account. As a result, merge-ready PRs and downstream stable
release work become permanently blocked even when required checks are
green.

## Decision

Temporarily relax the mandatory approval, required `CODEOWNERS` review,
and last-push approval gates while the repository remains a
single-maintainer project.

Keep the following protections active:

- pull-request-only merge flow
- required CI/status checks
- required review-thread resolution
- linear history
- no force pushes
- no protected-branch deletion

## Consequences

### Positive

- Removes an unsatisfiable governance deadlock.
- Preserves the stronger non-review protections and CI evidence path.
- Restores a normal merge and release path without relying on admin
  bypass merges as the standard workflow.

### Negative

- Weakens the live review gate until reviewer capacity exists.
- May reduce branch-protection scoring compared with the ideal
  multi-reviewer posture.

## Revisit trigger

- When the repository gains one non-author code owner/reviewer, restore
  at least `1` non-author approval + `CODEOWNERS` review + last-push
  approval.
- Only restore the two-approval requirement when two independent human
  reviewers are available in practice.
