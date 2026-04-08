# 설치 가이드

이 문서에서는 NewsDOM API를 로컬 환경에 설치하는 방법을 안내합니다.

## 시스템 요구사항

- **Python**: `>=3.10`, `<3.14` 필수 (`python3.10` 권장)
- **운영체제**: Linux 또는 macOS 권장 (윈도우의 경우 WSL2 사용 권장)
- **메모리 / GPU**: `MinerU` 딥러닝 기반 파이프라인을 구동하기 위해서는 최소 **8GB 이상의 RAM**이 필요하며, 성능을 위해 **NVIDIA GPU(CUDA 호환)** 환경이 강력히 권장됩니다.

---

## 1. 기본 설치 (개발/테스트 모드)

가장 간단한 형태로 파이썬 가상환경(Virtual Environment)을 생성하고 패키지를 설치합니다. 이 모드에서는 실제 `MinerU` 모델이 로드되지 않으며, `pytest`나 합성 픽스처(Synthetic Fixtures) 기반 테스트 용도로 적합합니다.

```bash
# 가상 환경 생성
python3.10 -m venv .venv

# 가상 환경 활성화
# macOS / Linux
source .venv/bin/activate
# Windows (WSL 제외)
# .venv\Scripts\activate

# pip 업그레이드
python -m pip install --upgrade pip

# 의존성 패키지와 함께 개발 모드로 설치
pip install -e .[dev]
```

설치되는 기본 의존성은 다음과 같습니다:
- `fastapi>=0.115,<1.0`
- `uvicorn>=0.30,<1.0`
- `pydantic>=2.9,<3.0`
- `python-multipart>=0.0.9,<1.0`
- `reportlab>=4.2,<5.0`, `Pillow`, `pypdf` 등 PDF/이미지 처리 라이브러리
- 개발 환경용: `pytest`, `httpx`

---

## 2. MinerU 백엔드 포함 실제 파싱 모드 설치

`MinerU` 백엔드를 사용하여 실제 스캔된 일본어 신문 PDF 파싱 작업을 수행하려면 `[parser]` 선택 옵션을 추가로 설치해야 합니다.

```bash
# 파서 모듈까지 모두 설치
pip install -e .[parser]
```

이 옵션을 통해 **`mineru[pipeline]==3.0.9`** 버전이 설치되며 딥러닝 기반 모델이 함께 준비됩니다. 설치 후 처음 API 서버를 구동하고 PDF를 파싱할 때 모델(Weight) 파일을 백그라운드에서 다운로드할 수 있으므로, 첫 실행에는 다소 시간이 걸릴 수 있습니다.

---

## 확인하기

설치가 정상적으로 완료되었는지 확인하려면 기본 테스트를 구동해보세요.

```bash
# 단위 테스트 구동 (integration 테스트 제외)
pytest
```

모든 테스트가 통과했다면 서버를 실행할 준비가 된 것입니다.

👉 다음 단계: **[API 레퍼런스 및 사용 방법](api-reference.md)**