# 시스템 환경 및 설치 가이드

이 문서에서는 NewsDOM API를 로컬 환경에 설치하는 방법을 안내합니다.

## 🛠️ 시스템 요구사항

- **Python**: Required: `>=3.10, <3.14` / Recommended: `python3.10`
- **운영체제**: Linux 또는 macOS 권장 (윈도우의 경우 WSL2 사용 권장)
- **하드웨어 (GPU)**: `MinerU` 딥러닝 기반 파이프라인을 구동하기 위해서는 최소 **8GB 이상의 RAM**이 필요하며, 실시간 처리를 위해 **NVIDIA GPU(CUDA 11.x/12.x 호환)** 및 `PyTorch` 환경이 권장됩니다.
- **의존성 (Python)**:
  - `fastapi>=0.115,<1.0`, `uvicorn>=0.30,<1.0`, `pydantic>=2.9,<3.0`
  - `python-multipart`, `reportlab`, `Pillow`, `pypdf` 등

---

## 1. 기본 테스트 및 개발 모드 설치

가장 간단한 형태로 파이썬 가상환경(Virtual Environment)을 생성하고 패키지를 설치합니다. 이 모드에서는 실제 `MinerU` 모델이 로드되지 않으며, `pytest`나 합성 픽스처(Synthetic Fixtures) 기반 테스트 용도로 적합합니다.

```bash
# 가상 환경 생성 (권장 예시: python3.10)
python3 -m venv .venv

# 가상 환경 활성화
# macOS / Linux
source .venv/bin/activate
# Windows (WSL 환경 제외)
# .venv\Scripts\activate

# pip 업그레이드
python -m pip install --upgrade pip

# 의존성 패키지와 함께 개발 모드로 설치
pip install -e ".[dev]"
```

---

## 2. MinerU 백엔드 포함 실제 파싱 모드 설치

`MinerU` 백엔드를 사용하여 실제 스캔된 일본어 신문 PDF 파싱 작업을 수행하려면 MinerU CLI를 별도로 설치해야 합니다.

```bash
# MinerU 파이프라인 CLI 설치
pip install "mineru[pipeline]==3.0.9"
```

이 명령어를 통해 **`mineru[pipeline]==3.0.9`** 버전이 설치되며 딥러닝 기반 모델을 위한 준비가 완료됩니다. 설치 후 처음 API 서버를 구동하고 PDF를 파싱할 때 모델(Weight) 파일을 백그라운드에서 다운로드할 수 있으므로, 첫 실행에는 다운로드 대기 시간이 발생할 수 있습니다.

### 커스텀 MinerU 실행 경로 (고급)
만약 `mineru` CLI 바이너리가 시스템 PATH에 잡혀있지 않거나, 특정 가상환경의 실행 파일을 수동으로 지정하고 싶다면 환경변수를 설정하세요:

```bash
# newsdom_api/mineru_runner.py 에서 이 환경변수를 우선 탐색합니다.
export NEWSDOM_MINERU_BIN="/path/to/custom/mineru"
```

---

## 3. 설치 확인 및 상태 점검

설치가 정상적으로 완료되었는지 확인하려면 기본 테스트를 구동해보세요.

```bash
# 파이썬 경고(Warning)를 에러로 취급하여 꼼꼼하게 검사
PYTHONWARNINGS=error pytest

# 통합 테스트 포함 실행 (실제 MinerU CLI 및 다운로드된 모델 파일 필요)
pytest -m "integration"
```

모든 단위 테스트(`tests/`)가 성공적으로 통과했다면 API 서버를 실행할 준비가 된 것입니다.

👉 다음 단계: **[API 레퍼런스 및 사용 방법](api-reference.md)**
