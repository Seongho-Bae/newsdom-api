# NewsDOM API 시작하기

[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/Seongho-Bae/newsdom-api/badge)](https://securityscorecards.dev/viewer/?uri=github.com/Seongho-Bae/newsdom-api)

**NewsDOM API**는 스캔된 일본어 신문 PDF 문서를 분석하여, DOM 형태의 문서 트리 구조로 파싱해주는 강력한 API 서비스입니다.

---

## 주요 기능

- **핵심 엔진**: `MinerU` 파이프라인 백엔드를 통해 정확한 텍스트 및 레이아웃 인식
- **서비스 래퍼**: `FastAPI` 기반의 고성능 비동기 API 서버
- **출력 결과물**: 
  - 페이지, 기사, 헤드라인, 본문 블록, 이미지, 캡션 및 품질 메타데이터가 모두 포함된 **정규화된 JSON(Canonical JSON)**

## 왜 NewsDOM인가요?

과거의 스캔된 신문 이미지는 단순한 텍스트 추출(OCR)만으로는 기사의 흐름을 파악하기 어렵습니다. 
NewsDOM API는 복잡한 다단 레이아웃과 이미지, 제목 구조를 파악하여 웹 브라우저의 DOM(Document Object Model)과 유사한 형태로 구조화해 줍니다. 

따라서 프론트엔드나 앱에서 쉽게 렌더링하고, 데이터 분석 작업에 즉시 활용할 수 있습니다.

---

다음 단계로 넘어가 직접 설치해 보세요!
👉 [설치 가이드 확인하기](installation.md)
