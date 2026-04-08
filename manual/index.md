# NewsDOM API 개요

[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/Seongho-Bae/newsdom-api/badge)](https://securityscorecards.dev/viewer/?uri=github.com/Seongho-Bae/newsdom-api)

**NewsDOM API**는 스캔된 일본어 신문 PDF 문서를 분석하여, DOM 형태의 문서 트리 구조로 파싱해주는 API 서비스입니다.

과거의 신문 이미지는 단순 텍스트 추출(OCR)만으로는 다단 레이아웃이나 이미지/캡션, 기사별 흐름을 파악하기 매우 어렵습니다. 이 프로젝트는 **MinerU 모델 파이프라인**을 활용해 지면을 단일 기사(Article) 단위로 쪼개고, 마치 웹 브라우저의 DOM(Document Object Model)과 같이 트리 구조의 JSON 데이터로 변환해 줍니다.

---

## 핵심 구조 및 기능

- **백엔드 엔진**: `MinerU` 파이프라인 (v3.0.9)
- **API 프레임워크**: `FastAPI` 기반 비동기 API 서버
- **DOM 변환기**: 
  - 신문 지면 1장(Page) 단위를 분석하여, 그 안의 기사(Articles), 광고(Ads), 헤더(Headers) 영역을 구분합니다.
  - 각 기사는 헤드라인(Headline), 본문 블록(Body blocks), 연관된 이미지(Images) 및 이미지 캡션(Captions)으로 다시 세분화됩니다.
  - 모든 구성 요소는 원본 문서 내 위치 좌표(`BoundingBox`)를 포함할 수 있습니다.

## 아키텍처 개요

1. **사용자 요청**: 사용자가 API(`/parse`)로 신문 스캔본 PDF 파일을 업로드합니다.
2. **FastAPI 처리**: 비동기 서버가 파일을 메모리로 읽어들여 파싱 모듈로 넘깁니다.
3. **MinerU 파이프라인**: 딥러닝 기반 레이아웃 분석 및 OCR을 수행합니다.
4. **DOM 빌더**: 인식된 영역들을 기사 논리에 맞게 트리 구조(Canonical JSON)로 병합하고 반환합니다.

---

👉 다음 단계로 **[설치 가이드](installation.md)**를 읽고 직접 환경을 구성해 보세요.