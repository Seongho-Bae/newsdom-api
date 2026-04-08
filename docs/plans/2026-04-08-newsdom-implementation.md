# NewsDOM API Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a private GitHub-hosted FastAPI service that parses scanned Japanese newspaper PDFs into DOM-like article trees and ships a copyright-safe synthetic newspaper fixture with equivalence validation.

**Architecture:** Wrap MinerU CLI in a subprocess-oriented Python service, normalize MinerU output into a canonical DOM schema, and generate a deterministic synthetic newspaper PDF whose structural metrics are matched against private-page-derived baselines. The copyrighted PDF stays local and is never committed.

**Tech Stack:** Python 3.10, FastAPI, Pydantic, pytest, MinerU 3.x CLI, reportlab, Pillow.

---

### Task 1: Scaffold package and API entrypoint

**Files:**
- Create: `pyproject.toml`
- Create: `src/newsdom_api/__init__.py`
- Create: `src/newsdom_api/main.py`
- Create: `tests/test_health.py`

**Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient
from newsdom_api.main import app


def test_healthcheck():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_health.py -v`
Expected: FAIL because `newsdom_api.main` does not exist.

**Step 3: Write minimal implementation**

Create a FastAPI app exposing `/health`.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_health.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add pyproject.toml src/newsdom_api/__init__.py src/newsdom_api/main.py tests/test_health.py
git commit -m "feat: scaffold NewsDOM API"
```

### Task 2: Add canonical schemas

**Files:**
- Create: `src/newsdom_api/schemas.py`
- Create: `tests/test_schemas.py`

**Step 1: Write the failing test**

```python
from newsdom_api.schemas import ArticleNode, ParseResponse


def test_parse_response_schema_round_trip():
    article = ArticleNode(article_id="a1", headline="headline", body_blocks=[])
    response = ParseResponse(document_id="doc1", pages=[])
    assert article.article_id == "a1"
    assert response.document_id == "doc1"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_schemas.py -v`
Expected: FAIL because schema models are missing.

**Step 3: Write minimal implementation**

Define Pydantic models for document/page/article/image/caption/quality output.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_schemas.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add src/newsdom_api/schemas.py tests/test_schemas.py
git commit -m "feat: add canonical DOM schemas"
```

### Task 3: Wrap MinerU CLI

**Files:**
- Create: `src/newsdom_api/mineru_runner.py`
- Create: `tests/test_mineru_runner.py`

**Step 1: Write the failing test**

```python
from pathlib import Path
from newsdom_api.mineru_runner import build_mineru_command


def test_build_mineru_command_uses_pipeline_backend(tmp_path: Path):
    cmd = build_mineru_command(Path("input.pdf"), tmp_path)
    assert "pipeline" in cmd
    assert "ocr" in cmd
    assert "japan" in cmd
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_mineru_runner.py -v`
Expected: FAIL because runner module is missing.

**Step 3: Write minimal implementation**

Implement command construction and subprocess execution helpers.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_mineru_runner.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add src/newsdom_api/mineru_runner.py tests/test_mineru_runner.py
git commit -m "feat: add MinerU CLI runner"
```

### Task 4: Normalize MinerU output into DOM

**Files:**
- Create: `src/newsdom_api/dom_builder.py`
- Create: `tests/fixtures/mineru_sample.json`
- Create: `tests/test_dom_builder.py`

**Step 1: Write the failing test**

```python
import json
from pathlib import Path
from newsdom_api.dom_builder import build_dom


def test_build_dom_extracts_articles_from_mineru_sample():
    sample = json.loads(Path("tests/fixtures/mineru_sample.json").read_text())
    dom = build_dom(sample, document_id="doc1")
    assert len(dom.pages) == 1
    assert len(dom.pages[0].articles) >= 1
```
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_dom_builder.py -v`
Expected: FAIL because DOM builder is missing.

**Step 3: Write minimal implementation**

Map MinerU block labels to canonical article/headline/body/image nodes.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_dom_builder.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add src/newsdom_api/dom_builder.py tests/fixtures/mineru_sample.json tests/test_dom_builder.py
git commit -m "feat: normalize MinerU output into article DOM"
```

### Task 5: Add parse endpoint

**Files:**
- Modify: `src/newsdom_api/main.py`
- Create: `src/newsdom_api/service.py`
- Create: `tests/test_parse_endpoint.py`

**Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient
from newsdom_api.main import app


def test_parse_endpoint_requires_pdf_file():
    client = TestClient(app)
    response = client.post("/parse")
    assert response.status_code == 422
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_parse_endpoint.py -v`
Expected: FAIL because endpoint is missing.

**Step 3: Write minimal implementation**

Add `POST /parse` to run MinerU and return normalized DOM JSON.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_parse_endpoint.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add src/newsdom_api/main.py src/newsdom_api/service.py tests/test_parse_endpoint.py
git commit -m "feat: expose PDF parse endpoint"
```

### Task 6: Build synthetic newspaper fixture generator

**Files:**
- Create: `src/newsdom_api/synthetic.py`
- Create: `tests/test_synthetic_fixture.py`

**Step 1: Write the failing test**

```python
from pathlib import Path
from newsdom_api.synthetic import generate_fixture


def test_generate_fixture_writes_pdf_and_truth(tmp_path: Path):
    pdf_path, truth_path = generate_fixture(tmp_path, seed=7)
    assert pdf_path.exists()
    assert truth_path.exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_synthetic_fixture.py -v`
Expected: FAIL because generator is missing.

**Step 3: Write minimal implementation**

Generate a seeded, scanned-style Japanese newspaper page PDF and a ground-truth JSON sidecar.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_synthetic_fixture.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add src/newsdom_api/synthetic.py tests/test_synthetic_fixture.py
git commit -m "feat: add synthetic newspaper fixture generator"
```

### Task 7: Add equivalence metrics and baseline test

**Files:**
- Create: `src/newsdom_api/equivalence.py`
- Create: `tests/fixtures/private_page_baseline.json`
- Create: `tests/test_fixture_equivalence.py`
- Create: `tools/derive_private_baseline.py`

**Step 1: Write the failing test**

```python
import json
from pathlib import Path
from newsdom_api.equivalence import compare_fixture_to_baseline
from newsdom_api.synthetic import generate_fixture


def test_synthetic_fixture_matches_private_baseline(tmp_path: Path):
    pdf_path, truth_path = generate_fixture(tmp_path, seed=7)
    baseline = json.loads(Path("tests/fixtures/private_page_baseline.json").read_text())
    result = compare_fixture_to_baseline(truth_path, baseline)
    assert result["equivalent"] is True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_fixture_equivalence.py -v`
Expected: FAIL because equivalence module and baseline are missing.

**Step 3: Write minimal implementation**

Implement metric comparison using committed non-expressive private-page-derived structural stats.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_fixture_equivalence.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add src/newsdom_api/equivalence.py tests/fixtures/private_page_baseline.json tests/test_fixture_equivalence.py tools/derive_private_baseline.py
git commit -m "feat: add synthetic fixture equivalence checks"
```

### Task 8: Add packaging, docs, and ignore rules

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Create: `LICENSE`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_readme_mentions_copyright_safe_fixture():
    text = Path("README.md").read_text()
    assert "synthetic" in text.lower()
    assert "copyright" in text.lower()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_readme.py -v`
Expected: FAIL because documentation files are missing.

**Step 3: Write minimal implementation**

Add docs, ignore the private source PDF and temp outputs, and document local-only baseline derivation.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_readme.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add .gitignore README.md LICENSE tests/test_readme.py
git commit -m "docs: document safe fixture workflow and repository usage"
```
