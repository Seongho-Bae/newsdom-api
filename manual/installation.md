# 설치 가이드

이 문서에서는 NewsDOM API를 로컬 환경에 설치하는 방법을 안내합니다.

## 시스템 요구사항

- **Python**: 3.10 이상 3.14 미만
- **운영체제**: Linux 또는 macOS 권장 (윈도우의 경우 WSL2 사용 권장)

---

## 1. 기본 설치 (개발/테스트 모드)

가장 간단한 형태로 파이썬 가상환경(Virtual Environment)을 생성하고 패키지를 설치합니다.

```bash
# 가상 환경 생성
python3.10 -m venv .venv

# 가상 환경 활성화
source .venv/bin/activate

# 의존성 패키지와 함께 개발 모드로 설치
pip install -e .[dev]
```

## 2. MinerU 백엔드 포함 실제 파싱 모드 설치

`MinerU` 백엔드를 사용하여 실제 PDF 파싱 작업을 수행하려면 `parser` 옵션을 추가로 설치해야 합니다.

```bash
pip install -e .[parser]
```

이 옵션을 통해 `MinerU` 파이프라인(3.0.9 버전)이 설치되며 딥러닝 기반 모델이 준비됩니다.

---

> **참고**: GitHub 저장소에서는 테스트를 위한 합성(Synthetic) 픽스처 데이터만 포함하여 제공하고 있습니다. 실제 파싱은 로컬 컴퓨터의 GPU 환경 등에 따라 성능이 달라질 수 있습니다.

설치가 완료되었으면 서버를 실행해보세요!
👉 [사용 방법 알아보기](usage.md)