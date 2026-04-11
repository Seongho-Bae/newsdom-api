# Truth Source Alignment Design

**Date:** 2026-04-10

## Goal

Restore repository truth-source integrity for documentation and workflow
contracts that drifted after the governance hardening work.

## Constraints

- PR #34 and PR #35 are currently code/CI green but blocked on external
  reviewer capacity.
- The next executable task should avoid destabilizing the already-green
  security and release work.
- The repository currently has no `integration`-marked tests, no `master`
  branch, and the active CodeQL contract is `codeql (python, actions)`.
- This task is documentation/workflow contract alignment only; no API,
  release, or LLM live path changes are required.

## Approaches Considered

### Approach A — Leave drift in place until blocked PRs merge

- Lowest immediate effort.
- Rejected because manuals, ADRs, and workflow plans would continue to
  advertise inaccurate verification and branch-policy facts.

### Approach B — Targeted contract alignment with regression tests (recommended)

- Add focused tests for doc/workflow truth.
- Update only the files that are currently stale: installation manual, GitHub
  Pages trigger, ADR follow-up text, and security-gates planning docs.
- Keeps scope narrow while preventing the same drift from recurring.

### Approach C — Broader documentation sweep

- Could normalize many docs at once.
- Rejected for now because it would expand scope beyond the current verified
  mismatches and risk delaying more urgent blocked-path work.

## Decision

Choose **Approach B**.

## Planned Changes

- Add a regression test module that verifies:
  - the installation manual does not advertise an empty `integration` marker
    run,
  - the GitHub Pages workflow does not trigger on the nonexistent `master`
    branch,
  - security-gates planning docs match the current
    `codeql (python, actions)` required check name,
  - ADR-0001 no longer points to stale resolved issue numbers.
- Update the affected docs/workflow to satisfy those tests.

## Verification Strategy

- Red/green the new regression tests first.
- Run the new focused test file.
- Run the full pytest suite.
- Run lint on changed files.

## Live Test Assessment

Live test is **not required** for this task. The affected surface is
documentation and GitHub Actions trigger metadata, and the acceptance criteria
are fully verifiable through local file parsing, YAML validation, and
repository tests.
