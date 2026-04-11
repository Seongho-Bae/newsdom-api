# PR continuity

## Canonical PR selection

- One branch should map to one canonical PR.
- Prefer the already-open PR for the branch before creating a new
  one.
- Use stacked PRs only when the follow-up task is distinct and the
  parent branch is not mergeable yet.

## Repository branch targets

- `feature/*`, `fix/*`, `chore/*` normally target `develop`.
- `release/*` targets `main` and is then back-merged into `develop`.
- `hotfix/*` targets `main` and is then back-merged into `develop`.

## Blocker handling

- If a PR is code/CI green but blocked by reviewer capacity or branch
  policy, keep the PR open and link the blocker issue.
- Do not open duplicate PRs for the same head branch.
- Re-check merge state, review decision, and required checks before
  every merge-path action.
