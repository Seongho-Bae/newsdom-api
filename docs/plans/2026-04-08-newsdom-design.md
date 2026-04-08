# NewsDOM API Design

**Date:** 2026-04-08

## Goal

Create a GitHub-hosted API service that parses scanned Japanese newspaper PDFs into a DOM-like article tree using MinerU as the primary parser, while shipping only fully synthetic newspaper fixtures that are layout-equivalent to a private copyrighted sample.

## Constraints

- The original newspaper PDF is copyrighted and cannot be committed or uploaded.
- The service must work without human-in-the-loop review.
- We need a redistributable test file that is structurally equivalent to the real page.
- The implementation must be deterministic enough for API use and tests.
- The runtime should avoid deprecated APIs and treat warnings as defects in the code we control.
- GitHub owner target is the authenticated account whose display name is **Seongho Bae** and login is **seonghobae**.

## Evidence

- `gh api user` confirms the target owner login is `seonghobae` and display name is `Seongho Bae`.
- MinerU `3.0.9` with `pipeline` backend successfully parsed the first page of a private reference sample under Python 3.10 with `mineru[pipeline]` installed.
- MinerU output contained the structural signals needed for DOM reconstruction:
  - `doc_title`
  - `vertical_text`
  - `image`
  - `header`
- Multiple headline candidates and article blocks were extracted from the private page during validation, confirming that the layout primitives were sufficient for DOM building.
- YomiToku also parsed the page, but the OSS package license is `CC BY-NC-SA 4.0` and it emitted Hugging Face unauthenticated-request warnings at runtime, which weakens it for the intended API service.
- PaddleOCR-VL documentation is strong, but CPU/Apple Silicon validation showed heavy startup and runtime warnings before we could establish a clean, fast local production path.

## Approaches Considered

### Approach A — Build directly around MinerU and ship no fixture

**Pros**
- Fastest path to service code
- Uses the best validated parser

**Cons**
- No redistributable regression corpus
- Cannot prove fixture equivalence in CI

**Decision**
- Rejected.

### Approach B — MinerU API wrapper + synthetic layout-clone fixture + equivalence metrics

**Pros**
- Uses validated primary parser
- Keeps private sample out of repo
- Ships a deterministic, redistributable test corpus
- Supports CI through derived layout metrics only

**Cons**
- Requires generator and equivalence tooling

**Decision**
- Accepted.

### Approach C — Japan-origin parser as primary

**Pros**
- Strong Japanese specialization story

**Cons**
- YomiToku license is not a clean default for a general API repo
- YomiToku runtime emitted warnings during validation
- MinerU is better validated on the target sample and provides stronger generic deployment options

**Decision**
- Rejected as primary. Keep only as future comparison candidate.

## Recommended Architecture

### Repository contents

- `src/newsdom_api/`
  - FastAPI service
  - MinerU subprocess wrapper
  - DOM normalization
  - synthetic fixture generation
  - equivalence metrics
- `tests/`
  - unit tests
  - synthetic fixture tests
  - DOM normalization tests
  - equivalence tests against committed derived metrics
- `tools/`
  - local-only script to derive metrics from the private page

### Runtime flow

1. API receives a PDF.
2. Service stores it temporarily and invokes MinerU CLI in a subprocess.
3. Service reads MinerU JSON output.
4. Service converts MinerU blocks into canonical DOM:
   - `document`
   - `page`
   - `article`
   - `headline`
   - `body_blocks`
   - `images`
   - `captions`
   - `ads`
5. API returns JSON.

### Fixture strategy

Use a **layout-clone, content-replace** generator:

- Keep only structural statistics from the private page.
- Generate synthetic Japanese newspaper-like content from hand-authored seed text and deterministic templates.
- Render a vertical multi-column newspaper page with synthetic headlines, body blocks, images, captions, and ad blocks.
- Export the fixture as PDF plus sidecar ground-truth JSON.

### Equivalence strategy

The repository will contain only **derived, non-expressive metrics** from the private page, for example:

- page size ratio
- column count
- normalized article bounding boxes
- block type counts
- image/caption/ad counts
- article title count
- reading-order edge count

The equivalence test will verify that the synthetic fixture remains within tolerances of these structural metrics.

## Testing Strategy

- Unit tests for DOM normalization using small synthetic MinerU-like samples.
- Unit tests for synthetic fixture generator determinism.
- Equivalence test comparing generated fixture metrics to committed baseline metrics.
- Optional integration test for live MinerU execution, skipped unless enabled.

## Key Decisions

- **Primary parser:** MinerU `pipeline` backend.
- **Language runtime:** Python `3.10` because MinerU pipeline validation succeeded there.
- **Service style:** subprocess-based wrapper instead of in-process MinerU imports, to isolate parser side effects.
- **Fixture format:** generated scanned-style PDF plus ground-truth JSON.
- **Remote repo owner:** `seonghobae`.
- **Repo visibility:** public is acceptable because the repository contains only synthetic fixtures and non-expressive private-page-derived metrics.

## Risks and Mitigations

- **MinerU cold start is slow** → document startup expectations, keep integration tests optional.
- **MinerU model downloads are network-dependent on first run** → add local model cache instructions and avoid test dependence on online fetches.
- **Synthetic fixture may drift from target complexity** → enforce equivalence tests with committed structural baselines.
- **Accidental copyright leakage** → keep derivation script local-only and commit only numeric baselines.
