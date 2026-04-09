# Quality Gate Design

**Date:** 2026-04-08

## Goal

Establish an enforced repository quality baseline for source documentation and line coverage, then bring the current codebase up to that baseline.

## Evidence

- The repository has no coverage tooling or thresholds in `pyproject.toml`.
- The test workflow runs plain `pytest` only.
- Source docstrings are effectively absent outside `__init__.py`.
- Current source footprint is small enough to raise standards immediately.

## Decision

Introduce a single `quality-gate` workflow and local test command that enforce:

- 100% line coverage for `src/newsdom_api`
- 100% docstring coverage for source modules, classes, and functions

## Scope

- Add coverage dependencies and config.
- Add a docstring audit test.
- Backfill docstrings for all source modules, classes, and functions.
- Add focused tests for uncovered modules and branches.
- Add a required `quality-gate` workflow on `main` and `develop`.

## Rationale

Security and branch workflows are already in place, but they do not stop shallow or undocumented code from merging. A strict quality gate closes the highest remaining merge-risk gap with a small-codebase-friendly change.
