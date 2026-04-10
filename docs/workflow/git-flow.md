# Git Flow

This repository uses a manual classic Git Flow model implemented with
GitHub branches and pull requests.

## Branch roles

- `main`: stable release branch
- `develop`: integration branch and default branch for normal work
- `feature/<topic>`: new work cut from `develop`, merged back into `develop`
- `fix/<topic>`: non-release fixes cut from `develop`, merged back into `develop`
- `chore/<topic>`: maintenance work cut from `develop`, merged back into `develop`
- `release/vX.Y.Z`: release hardening branch cut from `develop`,
  merged into `main` and back into `develop`
- `hotfix/<topic>`: urgent production fix cut from `main`,
  merged into `main` and back into `develop`

## Daily workflow

### Feature, fix, and chore work

1. Branch from `develop`
2. Open a pull request back to `develop`
3. Merge after checks pass

### Release flow

1. Cut `release/vX.Y.Z` from `develop`
2. Stabilize and version the release there
3. Merge `release/vX.Y.Z` into `main`
4. Back-merge the same release branch into `develop`
5. Tag from `main`

### Hotfix flow

1. Cut `hotfix/<topic>` from `main`
2. Merge into `main`
3. Back-merge into `develop`

## Pull request targets

- `feature/*`, `fix/*`, `chore/*` → `develop`
- `release/*` → `main`, then back to `develop`
- `hotfix/*` → `main`, then back to `develop`

## Notes

- This rollout intentionally avoids `git flow init` and any git
  config mutation.
- The branch model is enforced by repository convention, GitHub
  default-branch settings, and pull request guidance.
- `main` and `develop` are intended to be protected branches with
  pull-request-based updates and CI checks.
