from pathlib import Path


def test_dockerfile_exists():
    assert Path("Dockerfile").exists()


def test_nvidia_dockerfile_exists():
    assert Path("Dockerfile.nvidia").exists()


def test_dockerignore_exists():
    assert Path(".dockerignore").exists()


def test_dockerfile_uses_project_metadata_and_src_layout():
    text = Path("Dockerfile").read_text(encoding="utf-8")
    assert "pyproject.toml" in text
    assert "uv.lock" in text
    assert "src/" in text


def test_dockerfile_runs_uvicorn_with_healthcheck_and_external_mineru_path():
    text = Path("Dockerfile").read_text(encoding="utf-8")
    assert "uvicorn" in text
    assert "newsdom_api.main:app" in text
    assert "NEWSDOM_MINERU_BIN" in text
    assert "--host" in text
    assert "0.0.0.0" in text
    assert "8000" in text
    assert "HEALTHCHECK" in text
    assert "/health" in text


def test_nvidia_dockerfile_installs_mineru_pipeline_stack():
    text = Path("Dockerfile.nvidia").read_text(encoding="utf-8")
    assert "mineru[pipeline]==3.0.9" in text
    assert "NEWSDOM_MINERU_BIN" in text


def test_dockerignore_excludes_local_noise():
    text = Path(".dockerignore").read_text(encoding="utf-8")
    for entry in [".git", ".venv", "__pycache__", ".pytest_cache", ".coverage"]:
        assert entry in text


def test_readme_documents_docker_build_and_run():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docker build -t newsdom-api" in text
    assert "docker run -p 8000:8000 newsdom-api" in text
    assert "Dockerfile.nvidia" in text
    assert "Apple Silicon" in text
    assert "NVIDIA" in text


def test_container_image_workflow_exists_for_ghcr_release():
    text = Path(".github/workflows/container-image.yml").read_text(encoding="utf-8")
    assert "ghcr.io" in text
    assert "docker/build-push-action@" in text
    assert "linux/amd64,linux/arm64" in text
    assert "Dockerfile.nvidia" in text
