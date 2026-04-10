# ADR-0001: OpenSSF Best Practices Badge Enrollment

## Status

Accepted

## Context

The repository already has branch protection, CI checks, CodeQL, OpenSSF
Scorecard, Dependabot, a security policy, locked workflow dependencies, and a
planned release pipeline. Scorecard still reports a best-practices gap because
the OpenSSF Best Practices badge program has not been started.

The current repository also has only one organization member and one repository
collaborator, so external reviewer capacity is not yet in place. The first
tagged release is not available yet because the current PR stack still needs
external review before it can merge into protected branches.

## Decision

We will **defer** OpenSSF Best Practices badge enrollment until after:

1. the current protected-branch PR stack is merged,
2. the first tagged release has been produced with release provenance, and
3. at least one external reviewer is available for normal protected-branch
   review flow.

## Consequences

### Positive

- Keeps focus on finishing concrete repository hardening already underway.
- Avoids starting a badge questionnaire before the release and review processes
  are stable.
- Preserves a clear, auditable decision in the repository.

### Negative

- Scorecard will continue to report the best-practices gap until enrollment is
  revisited.

## Follow-up

- Revisit enrollment after the blocked protected-branch PR stack has merged,
  the first provenance-backed stable release has shipped, and reviewer
  capacity exists beyond the sole author/admin account.
- If the repository still intends to pursue the badge at that time, assign an
  owner, link the active release and reviewer-capacity issues, and complete
  the OpenSSF questionnaire.
