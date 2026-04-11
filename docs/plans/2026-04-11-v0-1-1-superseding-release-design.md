# Design: v0.1.1 superseding signed release

## Context

- Issue #32 tracks the immutable `v0.1.0` release history problem: the existing release is immutable and does not contain `*.intoto.jsonl` provenance bundles, so the live signed-release posture cannot be repaired in place.
- PR #34 has now merged into `main`, so the stable branch carries the release workflow hardening needed to export attestation bundles.
- PR #35 has merged into `develop`, so the integration branch is unblocked and can be used to cut a proper `release/v0.1.1` branch per `docs/workflow/git-flow.md`.
- The current release workflow builds artifacts from `pyproject.toml` version metadata and uploads release assets only when a tag is pushed.
- `pyproject.toml` and `CHANGELOG.md` still describe `0.1.0`, so the next stable cut requires explicit version/changelog work before tagging.

## Constraints

- Follow the repository Git Flow release path: cut `release/v0.1.1` from `develop`, merge it into `main`, back-merge into `develop`, then tag from `main`.
- Preserve the current release workflow structure; the task is to use the hardened path, not redesign it.
- Produce a real GitHub release/tag with release assets and `*.intoto.jsonl` bundles as live evidence.
- Keep `CHANGELOG.md` in Keep a Changelog format and align `pyproject.toml` version metadata with the new tag.
- Leave `v0.1.0` untouched because the existing release is immutable and the issue comment already selected the superseding-release path.
- Re-check post-tag workflow runs and release assets before considering the task complete.

## Approaches considered

### 1. Delete and recreate `v0.1.0`

- Pros: would repair the historical release directly.
- Cons: conflicts with the immutability blocker already observed in issue #32, rewrites release history, and adds avoidable operational risk.
- Verdict: reject.

### 2. Tag `main` directly as `v0.1.1` without a release branch

- Pros: shortest path to a new release.
- Cons: bypasses the repository's documented Git Flow release branch model and skips a durable place for version/changelog stabilization.
- Verdict: reject unless the documented release path becomes impossible.

### 3. Cut `release/v0.1.1` from `develop`, stabilize version/changelog/tests there, merge to `main`, back-merge to `develop`, then tag `main` (recommended)

- Pros: matches repository workflow, keeps stabilization MECE, produces a clean release handoff, and generates the superseding release issue #32 expects.
- Cons: more steps than direct tagging and requires explicit post-merge verification on both protected branches plus the tag-triggered workflow.
- Verdict: recommend.

## Recommended design

Use approach 3.

### Components

1. **Release metadata**
   - Update `pyproject.toml` from `0.1.0` to `0.1.1`.
   - Promote `CHANGELOG.md` from `[Unreleased]` to a dated `0.1.1` entry with the notable post-`0.1.0` delivery/security/release changes.
   - Update changelog tests so they fail first for the missing `0.1.1` entry and then pass after the metadata change.

2. **Release branch delivery path**
   - Work on `release/v0.1.1` cut from `develop`.
   - Verify locally with the full regression/coverage/docs suite before merging.
   - Open a PR from `release/v0.1.1` to `main`, merge it through the normal PR path, then back-merge the same release branch into `develop`.

3. **Live release execution**
   - Tag `main` as `v0.1.1` only after the release branch lands on `main` and post-merge checks are green.
   - Push the tag and watch `.github/workflows/release.yml` complete.
   - Verify the resulting GitHub release contains at least:
     - distribution artifacts
     - `SHA256SUMS.txt`
     - `release-manifest.json`
     - one or more `*.intoto.jsonl` provenance bundles

4. **Backlog cleanup**
   - Update issue #32 with release evidence and close it when the new release exists.
   - Re-check open code-scanning / Scorecard items after the release to see which remain external/time-based.

## Data flow

1. Add failing release-metadata tests.
2. Update version/changelog.
3. Run local verification.
4. Push `release/v0.1.1` and merge it into `main`.
5. Back-merge `release/v0.1.1` into `develop`.
6. Tag `main` as `v0.1.1`.
7. Watch release workflow and collect release asset evidence.
8. Close issue #32 and re-evaluate remaining open issues.

## Error handling and rollback

- If local verification fails, fix the release metadata/tests before opening the PR.
- If the release PR or back-merge PR uncovers merge conflicts, resolve them on the release branch and re-run the full verification suite.
- If the tag-triggered release workflow fails, inspect the full workflow logs, fix the root cause on a follow-up branch, and re-run with a new tag only after the path is green again.
- If release assets are incomplete, do not close issue #32; upload or regenerate the missing assets only after verifying the workflow failure mode.

## Testing strategy

- **Red**: changelog/version tests fail because `0.1.1` metadata is absent.
- **Green**: update version + changelog + tests until they pass.
- **Repository verification**:
  - `uv run pytest`
  - `uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100`
  - `uv run mkdocs build --strict`
- **Live release verification**:
  - PR checks on `release/v0.1.1`
  - post-merge checks on `main` and `develop`
  - tag-triggered `release` workflow
  - GitHub release asset inventory for `v0.1.1`

## Decisions

- Treat issue #32 as the next highest-priority executable canonical task.
- Use the superseding release path rather than mutating `v0.1.0`.
- Keep the release flow anchored to the documented Git Flow release branch model.
