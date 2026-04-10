# 시스템 환경 및 설치 가이드

이 문서에서는 NewsDOM API를 로컬 환경에 설치하는 방법을 안내합니다.

## 🛠️ 시스템 요구사항

- **Python**: Required: `>=3.10, <3.14`
- **운영체제**: Linux 또는 macOS 권장
  (윈도우의 경우 WSL2 사용 권장)
- **하드웨어 (GPU)**: `MinerU` 딥러닝 기반 파이프라인을 구동하려면
  최소 **8GB 이상의 RAM**이 필요합니다. 실시간 처리를 위해
  **NVIDIA GPU(CUDA 11.x/12.x 호환)** 및 `PyTorch` 환경을 권장합니다.
- **의존성 (Python)**:
  - `fastapi>=0.115,<1.0`, `uvicorn>=0.30,<1.0`,
    `pydantic>=2.9,<3.0`
  - `python-multipart`, `reportlab`, `Pillow`, `pypdf` 등

---

## 1. 기본 테스트 및 개발 모드 설치

가장 간단한 형태로 저장소가 관리하는 가상환경을 `uv`로 동기화합니다.
이 모드에서는 실제 `MinerU` 모델이 로드되지 않으며, `pytest`나 합성
픽스처(Synthetic Fixtures) 기반 테스트 용도로 적합합니다. `uv sync`는
저장소 루트의 `.venv`를 자동으로 생성/갱신하므로 별도 `venv` 생성이나
활성화가 필수는 아닙니다.

```bash
# 저장소 루트에서 개발/테스트/문서 extras까지 모두 동기화
uv sync --frozen --all-extras
```

---

## 2. MinerU 백엔드 포함 실제 파싱 모드 설치

`MinerU` 백엔드를 사용하여 실제 스캔된 일본어 신문 PDF 파싱 작업을
수행하려면 MinerU CLI를 별도로 설치해야 합니다.

```bash
# MinerU 파이프라인 CLI 설치
uv pip install --python .venv/bin/python "mineru[pipeline]==3.0.9"
```

Windows에서는 `.venv/bin/python` 대신 `.venv\Scripts\python.exe` 경로를 사용하세요.

이 명령어를 통해 **`mineru[pipeline]==3.0.9`** 버전이 설치되며
딥러닝 기반 모델을 위한 준비가 완료됩니다. 설치 후 처음 API 서버를
구동하고 PDF를 파싱할 때 모델(Weight) 파일을 백그라운드에서 다운로드할
수 있으므로, 첫 실행에는 다운로드 대기 시간이 발생할 수 있습니다.

### 커스텀 MinerU 실행 경로 (고급)

만약 `mineru` CLI 바이너리가 시스템 PATH에 잡혀 있지 않거나,
특정 가상환경의 실행 파일을 수동으로 지정하고 싶다면 환경변수를
설정하세요.

```bash
# newsdom_api/mineru_runner.py 에서 이 환경변수를 우선 탐색합니다.
export NEWSDOM_MINERU_BIN="/path/to/custom/mineru"
```

---

## 3. 설치 확인 및 상태 점검

설치가 정상적으로 완료되었는지 확인하려면 기본 테스트를 구동해보세요.

```bash
# 파이썬 경고(Warning)를 에러로 취급하여 꼼꼼하게 검사
PYTHONWARNINGS=error uv run pytest
```

현재 저장소에는 별도의 `integration` 마커 테스트 묶음이 없으므로,
설치 확인의 기준은 기본 `pytest` 스위트 통과입니다. 추가로 MinerU
경로와 API 동작까지 확인하려면 서버를 직접 띄운 뒤 수동 API 점검
단계를 수행하세요.

```bash
# 별도 터미널에서 API 서버 기동
uv run uvicorn --app-dir src newsdom_api.main:app --host 0.0.0.0 --port 8000 --reload

# 다른 터미널에서 상태 확인
curl -sS http://127.0.0.1:8000/health
```

정상 응답 예시는 `{"status": "ok"}`이며 HTTP 200 상태 코드를 반환해야 합니다.

모든 테스트(`tests/`)가 성공적으로 통과했다면 API 서버를 실행할
준비가 된 것입니다.

👉 다음 단계: **[API 레퍼런스 및 사용 방법](api-reference.md)**
