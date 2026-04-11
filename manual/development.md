# 개발 및 기여 가이드

이 문서에서는 NewsDOM API의 로컬 개발 방법, 테스트 프레임워크(`pytest`), 그리고 매우 중요한 **엄격한 픽스처(Fixture) 관리 및 브랜치 규칙**을 설명합니다.

---

## 1. 픽스처(Fixture) 보안 및 데이터 정책

일본어 스캔본 신문 데이터는 저작권 등 법적 문제가 얽혀 있을 수 있으므로, **저장소 내부의 픽스처 유지보수에 매우 엄격한 규칙**이 적용됩니다.

### ✅ 허용되는 항목 (저장소 커밋 가능, `tests/fixtures/` 내)

- **합성된(Synthetic) 더미 PDF 파일** (`synthetic.py` 등 내부 생성기를 통해 만들어진 것만 허용)
- 파싱 로직 테스트를 위한 **합성(Synthetic) 사이드카 JSON** (`_content_list.json` 등)
- 텍스트 내용은 모두 제외하고 위치 좌표(BBox)나 구조적 메타데이터만 남은 파생 구조 데이터 (Derived baseline)

### ❌ 엄격히 금지되는 항목 (절대 커밋 불가)

- 저작권이 있는 실제 원본 신문 PDF 스캔본 파일
- 실제 참조 문서(Private Reference Page)에서 추출되거나 복사된 OCR 텍스트 전체
- 원본 스캔본에서 잘라낸 이미지 크롭(Crop) 조각 파일들

> **주의**: 위 사항들은 `.gitignore` 파일에 등재되어 있다 하더라도, 절대 `git add` 시 실수로 끼워 넣지 않도록 주의해야 합니다. 픽스처 생성 이력 및 재생성에 관한 문서는 `tests/fixtures/README.md`를 참고하십시오.

---

## 2. 프라이빗 베이스라인 (Private Baseline) 업데이트

로컬 컴퓨터에서 원본 참조 문서(Private Page)를 가지고 비공개로 파이프라인/모델 성능 개선 테스트를 진행할 경우, **원본 데이터를 저장소로 올리면 안 되며, 파생된 구조적 베이스라인(JSON)만 갱신해야 합니다.**

로컬 베이스라인 갱신 시 `tools/` 디렉토리에 제공된 전용 스크립트를 사용하십시오:

```bash
# 원본 문서는 로컬에 둔 채, 테스트를 위한 껍데기(baseline) JSON만 갱신합니다.
python tools/derive_private_baseline.py tests/fixtures/private_page_baseline.json
```

**반드시 원본 데이터가 아닌 이 스크립트를 통해 생성된 파생 JSON 파일만 저장소에 반영(Commit)해야 합니다.**

---

## 3. Git 워크플로우 (Branch Model)

이 프로젝트는 `git-flow init`과 같은 플러그인을 쓰지 않는 수동 **클래식 Git Flow 모델**(`docs/workflow/git-flow.md`)을 강제합니다.

### 🌿 브랜치 규칙

- **`main` 브랜치**: 안정적인 릴리즈(Stable Release) 전용. 직접 푸시 금지.
- **`develop` 브랜치**: 모든 새로운 작업의 시작점이자 통합 브랜치.
- **`feature/<topic>`, `fix/<topic>`, `chore/<topic>`**:
  - `develop`에서 파생(Branch)되어야 합니다.
  - 작업 완료 후 `develop` 브랜치를 향해 Pull Request를 엽니다.
- **`release/vX.Y.Z` 브랜치**:
  - 제품 릴리즈 준비 시 `develop`에서 파생합니다.
  - 릴리즈 및 안정화가 완료되면 `main`에 병합(Merge)한 후 버전을 태깅(Tag)하고, 변경 사항을 다시 `develop`으로 백머지(Back-merge)해야 합니다.
- **`hotfix/<topic>` 브랜치**:
  - 운영(Production) 장애 등 긴급 패치 시 `main`에서 파생합니다.
  - 수정 완료 후 `main`과 `develop` 모두에 병합해야 합니다.

모든 작업은 반드시 **Pull Request (PR)** 를 거쳐 병합되어야 하며, 로컬 저장소 컨벤션과 GitHub 설정(Default-branch protection)으로 강제됩니다.

---

## 4. 프로젝트 구조 안내

코드를 탐색하기 위한 핵심 프로젝트 폴더 아키텍처입니다:

- **`src/newsdom_api/`**:
  - `main.py`: FastAPI 서버 및 라우팅 (API 진입점)
  - `schemas.py`: Pydantic 기반 DOM 데이터 직렬화 모델 (`PageNode`, `ArticleNode` 등)
  - `service.py`: 비즈니스 로직. PDF 업로드를 받고 파서를 거쳐 DOM 빌더로 연결
  - `mineru_runner.py`: Python `subprocess`로 외부 `mineru` CLI 엔진 파이프라인 구동 및 JSON 로딩
  - `dom_builder.py`: MinerU의 선형 OCR 데이터를 트리 구조의 DOM으로 재구성
  - `synthetic.py`: 합성 더미 PDF 및 픽스처 생성 엔진
- **`tests/`**: 단위/통합 테스트 코드와 커밋이 허용된 합성 픽스처(`fixtures/`) 보관소
- **`tools/`**: `derive_private_baseline.py` 등 개발자용 로컬 스크립트 모음
- **`docs/plans/`**: 설계(Design) 문서 및 구현 일지, 백로그
- **`docs/workflow/`**: Git 브랜치 전략 및 운영 정책 규정
