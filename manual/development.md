# 개발 및 기여 가이드

이 문서에서는 NewsDOM API의 로컬 개발 방법, 테스트, 그리고 **엄격한 픽스처(Fixture) 관리 규칙**을 설명합니다.

---

## 1. 테스트 실행하기

NewsDOM API는 Python의 `pytest` 프레임워크를 기반으로 테스트 코드가 작성되어 있습니다.
CI/CD 환경과 로컬에서 원활히 테스트할 수 있도록, 무거운 모델 실행 없이도 돌아가는 단위 테스트(Unit tests) 위주로 구성되어 있습니다.

```bash
# 기본 단위 테스트 실행
pytest

# 파이썬 경고(Warning)를 에러로 취급하여 꼼꼼하게 검사
PYTHONWARNINGS=error pytest

# 통합 테스트 포함 실행 (실제 MinerU CLI 및 다운로드된 모델 파일 필요)
pytest -m "integration"
```

---

## 2. 픽스처(Fixture) 정책 및 데이터 관리

뉴스 스캔본은 저작권 등 민감한 문제가 있을 수 있으므로, **저장소 내부의 파일 유지보수에 매우 엄격한 규칙**이 적용됩니다.

### 허용되는 항목 (저장소 커밋 가능)
- 합성된(Synthetic) 형태의 더미 PDF 파일
- 파싱 결과를 보여주기 위한 합성(Synthetic) 사이드카 JSON
- 텍스트 내용은 담지 않은, 구조적 메타데이터나 위치 좌표 등만 남은 파생된 구조 데이터 (Derived baseline)

### 엄격히 금지되는 항목 (절대 커밋 불가)
- 저작권이 있는 실제 원본 신문 PDF 파일
- 실제 참조 문서에서 추출되거나 복사된 원본 텍스트(OCR 결과물 전체)
- 원본에서 잘라낸 이미지 크롭 조각들

> **주의**: 위 사항들은 `.gitignore`에 정의되어 있더라도, 절대 실수로 `git add` 되지 않도록 주의해야 합니다. 픽스처 생성 이력 및 재생성에 관한 문서는 `tests/fixtures/README.md`를 참고하십시오.

---

## 3. 프라이빗 베이스라인 (Private Baseline) 갱신

로컬 컴퓨터에서 원본 참조 문서를 가지고 비공개로 모델 성능 개선 테스트를 진행할 경우, 파생된 구조적 베이스라인(JSON) 결과만 저장소로 가져와 갱신할 수 있습니다. 

로컬에서 베이스라인 갱신 시 제공되는 도구를 사용하십시오:

```bash
python tools/derive_private_baseline.py tests/fixtures/private_page_baseline.json
```

**반드시 원본 데이터가 아닌 파생된 JSON 파일만 저장소에 반영해야 합니다.**

---

## 4. 브랜치 워크플로우 (Branch Workflow)

이 프로젝트는 수동 **Git Flow 모델**을 사용합니다.
- 새로운 기능 개발, 버그 수정은 항상 `develop` 브랜치에서 파생(Branch)되어야 합니다.
- 작업 완료 후에는 `develop` 브랜치를 향해 Pull Request를 엽니다.
- `release/*` 및 `hotfix/*` 브랜치는 프로덕션 배포나 긴급 패치 용도로만 사용됩니다.

자세한 브랜치 전략은 `docs/workflow/git-flow.md` 문서를 확인하십시오.

---

## 5. 프로젝트 디렉토리 구조

프로젝트 주요 폴더는 다음과 같이 구성되어 있습니다:

- **`src/newsdom_api/`**: 
  - `main.py`: FastAPI 엔드포인트 및 앱 설정
  - `schemas.py`: Pydantic 기반 API 입출력 모델 (`PageNode`, `ArticleNode` 등)
  - `service.py`: PDF 파싱 비즈니스 로직 및 MinerU 래퍼 구현체
- **`tests/`**: 단위 테스트 코드와 커밋이 허용된 합성 픽스처 데이터 보관
- **`tools/`**: 로컬 유지보수 및 `derive_private_baseline.py` 등 관리용 스크립트 모음
- **`docs/plans/`**: 개발 디자인 및 구현 설계 기록들
