# Main Stable Sync Design

**Date:** 2026-04-10

## Goal

Prepare `main` for the next stable release by backporting the release-hardening and delivery changes that currently exist only on `develop`, without repeating the previously closed dirty `develop -> main` sync attempt.

## Evidence

- `main` and `develop` are currently diverged.
- `main` already contains equivalent backports for some earlier docs/release-history commits under different SHAs, so a direct merge would reintroduce noisy overlap.
- The latest stable release is `v0.1.0`, and issue `#32` tracks that future stable releases must ship `*.intoto.jsonl` provenance bundles.
- `main` still lacks the `export_release_attestations.py` release step, the optional `SCORECARD_TOKEN` wiring, the Docker delivery files, the ClusterFuzzLite integration, and the digest-pinned follow-up changes now present on `develop`.
- The open repository issues are governance/release follow-ups (`#31`, `#32`), so the next in-repo canonical task is to make `main` capable of producing a better next stable release.

## Constraints

- Keep `main` stable-focused; do not pull in unrelated manual-doc churn just to reduce branch divergence.
- Prefer a clean PR from a new branch off `main` over a direct `develop -> main` merge.
- Follow TDD: add failing regression tests on `main` before backporting implementation files.
- Preserve existing ruleset/required-check expectations.
- Keep release and workflow changes pinned, least-privilege, and compatible with the existing `uv`-locked project setup.

## Approaches considered

### Approach A — Directly merge `develop` into `main`

- **Pros:** fastest branch convergence.
- **Cons:** repeats the dirty-sync problem, mixes already-backported history with new changes, and widens stable-release scope with unrelated docs churn.

### Approach B — Cherry-pick every unique `develop` commit

- **Pros:** preserves original commit boundaries.
- **Cons:** still drags along coupled docs/runtime changes that are not required for the next stable release, and some commits overlap existing `main` state only partially.

### Approach C — Test-first selective stable-sync backport (recommended)

- Add the missing regression tests from `develop` onto a branch from `main`.
- Backport only the files needed for stable release hardening and supported delivery:
  - release attestation export + Scorecard token wiring
  - workflow hardening follow-ups (`tests.yml`, `gh-pages.yml`)
  - Docker delivery files and README coverage
  - ClusterFuzzLite, fuzz metadata, and digest pinning
- Leave manual-doc rewrite commits out of this sync.

## Decision

Choose **Approach C**.

## Scope

### In scope

- `.github/workflows/release.yml`
- `.github/workflows/scorecards.yml`
- `.github/workflows/tests.yml`
- `.github/workflows/gh-pages.yml`
- `scripts/release/export_release_attestations.py`
- `SECURITY.md`, `CONTRIBUTING.md`, `README.md`, `CHANGELOG.md`
- `Dockerfile`, `Dockerfile.nvidia`, `.dockerignore`, `.github/workflows/container-image.yml`
- `.clusterfuzzlite/*`, `fuzzers/*`
- `pyproject.toml`, `uv.lock`
- the matching regression tests under `tests/`

### Out of scope

- The larger manual-doc rewrite commits (`cd441ea`, `c24751c`)
- Any GitHub ruleset change that would require stronger human-review capacity than the repo currently has
- Rewriting or deleting the immutable `v0.1.0` release

## Verification

- Targeted RED runs for the newly backported tests on `main`
- GREEN runs for targeted test modules after each backport slice
- Fresh full-suite verification with `uv run pytest`
- Fresh lint/type evidence via filetype-aware checks if changes touch supported filetypes
- GitHub branch/PR continuity check before reporting completion

## Expected outcome

`main` will be able to produce the next stable release with release-attestation assets, stable Docker delivery files, fuzzing/pinned-dependency coverage, and the workflow regressions already fixed on `develop`, while avoiding another noisy whole-branch sync.
