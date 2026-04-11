# Agent docs

This directory anchors repository-local instructions for autonomous
maintenance.

## Read order

1. `../../AGENTS.md`
2. `../engineering/canonical-docs.md`
3. `../engineering/execution-policy.md`
4. `../engineering/acceptance-criteria.md`
5. `../../ARCHITECTURE.md`

## Intent

- Keep agent behavior tied to repository truth instead of external defaults.
- Preserve a single durable map for testing, review, release, and
  security expectations.
- Make stacked PR work, live verification, and blocker handling
  reproducible across sessions.
