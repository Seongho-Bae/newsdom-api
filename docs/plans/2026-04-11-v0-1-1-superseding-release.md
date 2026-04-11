# v0.1.1 Superseding Release Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ship a real `v0.1.1` stable release from `main` so the active release window contains provenance-backed `*.intoto.jsonl` assets and issue #32 can close without mutating immutable `v0.1.0`.

**Architecture:** Work on `release/v0.1.1` from `develop`, add failing metadata/changelog tests first, update `pyproject.toml` and `CHANGELOG.md`, then merge the release branch into `main` and back into `develop`. Tag `main` as `v0.1.1`, watch the release workflow, and verify the GitHub release asset inventory before closing the tracking issue.

**Tech Stack:** Python/pytest, Keep a Changelog, GitHub PR/tag/release workflow, `gh` CLI, `uv`.

---

### Task 1: Add the failing `0.1.1` release metadata tests

**Files:**
- Modify: `tests/test_changelog.py`
- Modify: `tests/test_project_metadata.py`

**Step 1: Write the failing tests**

Add tests shaped like this:

```python
def test_changelog_prepares_the_0_1_1_release_entry() -> None:
    text = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [0.1.1] - 2026-04-11" in text
    assert "[Unreleased]: https://github.com/Seongho-Bae/newsdom-api/compare/v0.1.1...HEAD" in text
    assert "[0.1.1]: https://github.com/Seongho-Bae/newsdom-api/compare/v0.1.0...v0.1.1" in text


def test_project_version_is_prepared_for_v0_1_1_release() -> None:
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "0.1.1"' in text
```

**Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_changelog.py tests/test_project_metadata.py -q`

Expected: FAIL because `CHANGELOG.md` and `pyproject.toml` still refer to `0.1.0`.

**Step 3: Commit the red tests**

```bash
git add tests/test_changelog.py tests/test_project_metadata.py
git commit -m "test: add failing v0.1.1 release metadata checks"
```

### Task 2: Update version and changelog for the superseding release

**Files:**
- Modify: `pyproject.toml`
- Modify: `CHANGELOG.md`
- Modify: `tests/test_changelog.py`
- Modify: `tests/test_project_metadata.py`

**Step 1: Write the minimal implementation**

Update `pyproject.toml`:

```toml
[project]
version = "0.1.1"
```

Update `CHANGELOG.md` so it contains:

```markdown
## [Unreleased]

## [0.1.1] - 2026-04-11

### Added

- GHCR-ready multi-arch API image delivery, ClusterFuzzLite coverage, and exported `*.intoto.jsonl` release provenance bundles for stable releases

### Changed

- Protected-branch governance docs, CodeQL coverage, and manual screenshots now reflect the current repository delivery path
- Public setup guidance, Markdown lint scope, and docs toolchain policy are aligned with the merged `develop` / `main` workflow state

### Fixed

- Patched `pypdf` lockfile to `6.10.0` for GHSA-3crg-w4f6-42mx / CVE-2026-40260 coverage

[Unreleased]: https://github.com/Seongho-Bae/newsdom-api/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/Seongho-Bae/newsdom-api/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Seongho-Bae/newsdom-api/releases/tag/v0.1.0
```

Adjust the new tests if the exact category wording differs, but keep them focused on `0.1.1` metadata and release links.

**Step 2: Run the targeted tests to verify they pass**

Run: `uv run pytest tests/test_changelog.py tests/test_project_metadata.py -q`

Expected: PASS.

**Step 3: Commit the metadata update**

```bash
git add pyproject.toml CHANGELOG.md tests/test_changelog.py tests/test_project_metadata.py
git commit -m "chore(release): prepare v0.1.1 metadata"
```

### Task 3: Re-run repository verification on the release branch

**Files:**
- Modify: none unless verification exposes drift

**Step 1: Run the full test suite**

Run: `uv run pytest`

Expected: PASS.

**Step 2: Run the coverage gate**

Run: `uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100`

Expected: PASS with 100% coverage.

**Step 3: Run the docs build**

Run: `uv run mkdocs build --strict`

Expected: PASS.

**Step 4: Commit only if verification requires fixes**

```bash
git add <only-files-fixed-during-verification>
git commit -m "fix: keep v0.1.1 release branch green"
```

### Task 4: Push `release/v0.1.1` and merge it into `main`

**Files:**
- Modify: none locally unless PR feedback requires it

**Step 1: Push the release branch**

Run: `git push -u origin release/v0.1.1`

Expected: remote branch created.

**Step 2: Open the release PR to `main`**

Run:

```bash
gh pr create --base main --head release/v0.1.1 --title "release: cut v0.1.1" --body "$(cat <<'EOF'
## Summary
- prepare the superseding `v0.1.1` release metadata from `develop`
- use the hardened stable release path on `main` so the next tag ships `*.intoto.jsonl` provenance bundles
- unblock issue #32 without mutating immutable `v0.1.0`

## Verification
- uv run pytest
- uv run pytest --cov=src/newsdom_api --cov-branch --cov-report=term-missing --cov-fail-under=100
- uv run mkdocs build --strict
EOF
)"
```

Expected: PR URL returned.

**Step 3: Watch the PR checks**

Run: `gh pr checks --watch`

Expected: required checks complete successfully.

**Step 4: Merge the release PR into `main`**

Run: `gh pr merge <release-pr-number> --squash --delete-branch=false`

Expected: PR merges into `main`.

### Task 5: Back-merge the same release branch into `develop`

**Files:**
- Modify: none locally unless back-merge feedback requires it

**Step 1: Open the back-merge PR**

Run:

```bash
gh pr create --base develop --head release/v0.1.1 --title "release: back-merge v0.1.1 metadata" --body "$(cat <<'EOF'
## Summary
- back-merge the `v0.1.1` release metadata from the release branch into `develop`
- keep `develop` aligned with the stable release line after the `main` merge

## Verification
- inherited from release/v0.1.1 branch verification
EOF
)"
```

Expected: PR URL returned.

**Step 2: Watch the back-merge PR checks**

Run: `gh pr checks --watch`

Expected: required checks complete successfully.

**Step 3: Merge the back-merge PR into `develop`**

Run: `gh pr merge <backmerge-pr-number> --squash --delete-branch=false`

Expected: PR merges into `develop`.

### Task 6: Create and push the `v0.1.1` tag from `main`

**Files:**
- Modify: none

**Step 1: Update the local `main` ref**

Run:

```bash
git fetch origin --tags
git checkout main
git merge --ff-only origin/main
```

Expected: local `main` matches the merged release PR.

**Step 2: Create the tag**

Run: `git tag -a v0.1.1 -m "v0.1.1"`

Expected: local annotated tag created.

**Step 3: Push the tag**

Run: `git push origin v0.1.1`

Expected: remote tag created and the `release` workflow starts.

### Task 7: Verify the live GitHub release and close issue #32

**Files:**
- Modify: none

**Step 1: Watch the release workflow**

Run: `gh run watch --exit-status $(gh run list --workflow release --limit 1 --json databaseId --jq '.[0].databaseId')`

Expected: the workflow completes successfully.

**Step 2: Verify release asset inventory**

Run:

```bash
gh release view v0.1.1 --json assets,body,name,tagName,url
```

Expected: assets include at least one wheel or sdist, `SHA256SUMS.txt`, `release-manifest.json`, and one or more `*.intoto.jsonl` files.

**Step 3: Close issue #32 with release evidence**

Add a comment summarizing:

- the merged release and back-merge PRs
- the `v0.1.1` release URL
- the presence of `*.intoto.jsonl` assets

Then close issue #32 as completed.

### Task 8: Re-evaluate the remaining repository backlog

**Files:**
- Modify: none unless new blockers surface

**Step 1: Check remaining open issues and code-scanning alerts**

Run:

```bash
gh issue list --state open
gh api repos/Seongho-Bae/newsdom-api/code-scanning/alerts?state=open\&per_page=100
```

Expected: only genuinely remaining tasks stay open.

**Step 2: Record the next canonical task**

If issue #31 or a fresh release/code-scanning regression remains executable, capture it in a new design/plan doc before implementation.
