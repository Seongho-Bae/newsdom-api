# Security Gates Design

**Date:** 2026-04-08

## Goal

Add GitHub-native security gates centered on OpenSSF Scorecard and make them required for protected branches.

## Constraints

- The repository already uses GitHub Actions for tests.
- `main` and `develop` are branch-protected and should treat security workflows as required gates.
- Changes should remain lightweight for a small Python FastAPI repository.
- Security workflows should be least-privilege and avoid unnecessary secrets.

## Approaches considered

### Approach A — Scorecard only
- Add OpenSSF Scorecard workflow and badge.
- Low effort, but misses code and dependency risk coverage.

### Approach B — Scorecard + CodeQL + Dependency Review (recommended)
- Scorecard for repository posture.
- CodeQL for Python SAST.
- Dependency Review for pull-request dependency deltas.

### Approach C — Broad security suite (Semgrep, Trivy, etc.)
- Stronger coverage but too heavy for the current repository size and request scope.

## Decision

Choose **Approach B**.

## Required checks

- `pytest`
- `scorecard`
- `codeql (python, actions)`
- `dependency-review`

## Operational notes

- Add minimal README signal via a Scorecard badge.
- Keep workflow permissions explicit.
- Trigger CodeQL and Scorecard on both `develop` and `main` so both protected branches can require them.
