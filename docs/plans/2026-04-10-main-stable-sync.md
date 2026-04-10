# Main Stable Sync Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Backport the release-hardening, Docker delivery, and fuzzing changes needed for the next stable `main` release without merging the whole `develop` branch.

**Architecture:** Start from `main`, add the missing regression tests first, then backport the corresponding workflow, metadata, release, Docker, and fuzzing files from `develop` until the same stable-facing behaviors are present on `main`. Keep manual-doc rewrite commits out of scope and finish with a clean PR into `main`.

**Tech Stack:** Python 3.10+, uv, pytest, GitHub Actions, Docker, ClusterFuzzLite.

---

## Task 1: Backport stable-release regression tests

### Files

- Modify: `tests/test_release_pipeline.py`
- Modify: `tests/test_security_policy.py`
- Modify: `tests/test_workflows.py`
- Modify: `tests/test_workflow_security.py`
- Modify: `tests/test_workflow_runtime_env.py`
- Modify: `tests/test_project_metadata.py`
- Create: `tests/test_docker_delivery.py`
- Create: `tests/test_fuzzing_integration.py`

### Step 1: Write the failing tests

Add the missing assertions from `develop` that prove `main` is missing:

- exported `*.intoto.jsonl` release assets
- optional `SCORECARD_TOKEN` wiring
- pinned `setup-uv` in `tests.yml`
- `gh-pages.yml` path coverage for `pyproject.toml`, `uv.lock`, and the local Pages action
- SPDX license string + fuzz extra metadata
- Docker delivery files and ClusterFuzzLite files

### Step 2: Run the failing tests

Run:

```bash
uv run pytest tests/test_release_pipeline.py tests/test_security_policy.py tests/test_workflows.py tests/test_workflow_security.py tests/test_workflow_runtime_env.py tests/test_project_metadata.py tests/test_docker_delivery.py tests/test_fuzzing_integration.py -v
```

Expected: FAIL on `main` before implementation files are backported.

### Step 3: Commit the red test baseline

```bash
git add tests/test_release_pipeline.py tests/test_security_policy.py tests/test_workflows.py tests/test_workflow_security.py tests/test_workflow_runtime_env.py tests/test_project_metadata.py tests/test_docker_delivery.py tests/test_fuzzing_integration.py
git commit -m "test: capture missing stable sync regressions"
```

## Task 2: Backport release and workflow hardening

### Files

- Modify: `.github/workflows/release.yml`
- Modify: `.github/workflows/scorecards.yml`
- Modify: `.github/workflows/tests.yml`
- Modify: `.github/workflows/gh-pages.yml`
- Modify: `CONTRIBUTING.md`
- Modify: `SECURITY.md`
- Modify: `README.md`
- Modify: `pyproject.toml`
- Create: `scripts/release/export_release_attestations.py`

### Step 1: Write the minimal implementation

Backport only the stable-facing changes from `develop`:

- export `*.intoto.jsonl` attestation bundles before artifact upload
- wire optional `SCORECARD_TOKEN`
- pin `setup-uv` in `tests.yml`
- expand `gh-pages.yml` push paths to cover lockfile and local action changes
- add explicit security-reporting links
- normalize `license = "MIT"`

### Step 2: Run the targeted tests

Run:

```bash
uv run pytest tests/test_release_pipeline.py tests/test_security_policy.py tests/test_workflows.py tests/test_workflow_security.py tests/test_workflow_runtime_env.py tests/test_project_metadata.py -v
```

Expected: PASS.

### Step 3: Commit

```bash
git add .github/workflows/release.yml .github/workflows/scorecards.yml .github/workflows/tests.yml .github/workflows/gh-pages.yml CONTRIBUTING.md SECURITY.md README.md pyproject.toml scripts/release/export_release_attestations.py tests/test_release_pipeline.py tests/test_security_policy.py tests/test_workflows.py tests/test_workflow_security.py tests/test_workflow_runtime_env.py tests/test_project_metadata.py
git commit -m "ci: backport stable release hardening to main"
```

## Task 3: Backport Docker delivery path

### Files

- Create: `.dockerignore`
- Create: `Dockerfile`
- Create: `Dockerfile.nvidia`
- Create: `.github/workflows/container-image.yml`
- Modify: `README.md`
- Create: `tests/test_docker_delivery.py`

### Step 1: Write the minimal implementation

Copy the lean multi-arch API image path and optional NVIDIA image path from `develop`, including the GHCR workflow and README usage notes.

### Step 2: Run the targeted tests

Run:

```bash
uv run pytest tests/test_docker_delivery.py tests/test_workflow_security.py tests/test_readme.py -v
```

Expected: PASS.

### Step 3: Commit

```bash
git add .dockerignore Dockerfile Dockerfile.nvidia .github/workflows/container-image.yml README.md tests/test_docker_delivery.py tests/test_workflow_security.py tests/test_readme.py
git commit -m "ci: backport container delivery workflow to main"
```

## Task 4: Backport fuzzing and digest pinning

### Files

- Create: `.clusterfuzzlite/Dockerfile`
- Create: `.clusterfuzzlite/build.sh`
- Create: `.clusterfuzzlite/project.yaml`
- Create: `.github/workflows/clusterfuzzlite.yml`
- Create: `fuzzers/dom_builder_fuzzer.py`
- Create: `fuzzers/corpus/dom_builder_fuzzer/mineru_sample.json`
- Modify: `Dockerfile`
- Modify: `Dockerfile.nvidia`
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Create: `tests/test_fuzzing_integration.py`
- Modify: `tests/test_project_metadata.py`

### Step 1: Write the minimal implementation

Backport the ClusterFuzzLite workflow, locked `fuzz` optional dependency group, corpus/fuzzer files, and digest-pinned Docker/fuzz base images.

### Step 2: Run the targeted tests

Run:

```bash
uv run pytest tests/test_fuzzing_integration.py tests/test_project_metadata.py tests/test_docker_delivery.py -v
```

Expected: PASS.

### Step 3: Commit

```bash
git add .clusterfuzzlite .github/workflows/clusterfuzzlite.yml fuzzers Dockerfile Dockerfile.nvidia pyproject.toml uv.lock tests/test_fuzzing_integration.py tests/test_project_metadata.py tests/test_docker_delivery.py
git commit -m "ci: backport fuzzing and pinned delivery assets to main"
```

## Task 5: Update changelog and verify the whole branch

### Files

- Modify: `CHANGELOG.md`

### Step 1: Update the unreleased changelog entry

Add concise Keep a Changelog entries describing the stable-sync backports.

### Step 2: Run the full verification suite

Run:

```bash
uv run pytest
```

Then run:

```bash
PYTHONWARNINGS=error uv run pytest
```

Then run filetype-aware checks:

```bash
python3 "$HOME/.config/opencode/scripts/lint_by_filetype.py" --json
```

Expected: all pass.

### Step 3: Commit

```bash
git add CHANGELOG.md
git commit -m "docs: record main stable sync backports"
```

## Task 6: Push and open the clean stable-sync PR

### Files

- No file changes.

### Step 1: Push the branch

```bash
git push -u origin chore/main-stable-sync
```

### Step 2: Check PR continuity

```bash
python3 "$HOME/.config/opencode/scripts/pr_continuity.py" --json --limit 50
```

### Step 3: Open the PR into `main`

Use a concise PR title such as:

```text
ci: backport stable release hardening from develop
```

Include a summary covering:

- release attestation export and Scorecard token wiring
- Docker and GHCR delivery backport
- ClusterFuzzLite + digest pinning backport
