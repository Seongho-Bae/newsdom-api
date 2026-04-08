# Git Flow Rollout Design

**Date:** 2026-04-08

## Goal

Adopt a modern classic Git Flow structure for `newsdom-api` using GitHub-native branches and documentation, without relying on `git flow init` or any Git config changes.

## Constraints

- Do not update global or local git config.
- Existing repository already uses `main` and is published at `Seongho-Bae/newsdom-api`.
- README must remain user-facing.
- Maintainer workflow detail should live outside README.
- The change should be operational on GitHub, not merely described.

## Approaches considered

### Approach A — Lightweight GitHub flow
- Keep `main` as default.
- Use `feature/*`, `fix/*`, `hotfix/*`.
- Optional release branches.

**Pros:** lowest overhead.  
**Cons:** not what the user asked for; lacks a dedicated integration branch.

### Approach B — Manual classic Git Flow (recommended)
- `main` = stable/release branch.
- `develop` = default integration branch.
- `feature/*` from `develop`.
- `release/*` from `develop`, merged to `main` and back to `develop`.
- `hotfix/*` from `main`, merged to both `main` and `develop`.

**Pros:** matches the user request; no git config required; works with GitHub settings and branch conventions.  
**Cons:** slightly more operational complexity.

### Approach C — Environment branches
- `develop`, `staging`, `main`.

**Pros:** useful for staged deployment.  
**Cons:** unnecessary for this small repo; adds overhead beyond the request.

## Decision

Choose **Approach B**.

## Rollout plan

1. Create and push `develop` from the current `main` HEAD.
2. Set GitHub default branch to `develop`.
3. Add maintainer-facing workflow documentation in `docs/workflow/git-flow.md`.
4. Add a brief pointer from `CONTRIBUTING.md` and a one-line reference from `README.md`.
5. Add a PR template reminding contributors which base branch to use.

## Branch model

- `main`: stable branch, production-ready history only.
- `develop`: integration branch, default base for day-to-day work.
- `feature/<topic>`: created from `develop`, merged back to `develop`.
- `release/vX.Y.Z`: cut from `develop`, used for stabilization, merged to `main` and back to `develop`.
- `hotfix/<topic>`: created from `main`, merged to both `main` and `develop`.

## Documentation split

- `README.md`: user-facing, with only a brief workflow pointer.
- `CONTRIBUTING.md`: contributor entry point and link to workflow doc.
- `docs/workflow/git-flow.md`: canonical maintainer workflow.
- `docs/plans/*`: implementation notes only.

## Verification

Verification evidence must include:

- `develop` exists locally and on GitHub.
- GitHub default branch is `develop`.
- Working tree is clean.
- Tests still pass after documentation/template changes.
