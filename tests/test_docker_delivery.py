from pathlib import Path

import yaml


def _load_container_image_workflow() -> dict:
    return yaml.safe_load(
        Path(".github/workflows/container-image.yml").read_text(encoding="utf-8")
    )


def _find_step_by_uses(steps: list[dict], uses: str) -> dict:
    return next(step for step in steps if step.get("uses") == uses)


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
    assert "python:3.12-slim@sha256:" in text
    assert "ghcr.io/astral-sh/uv@sha256:" in text


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
    assert "nvidia/cuda:12.6.3-cudnn-runtime-ubuntu22.04@sha256:" in text
    assert "ghcr.io/astral-sh/uv@sha256:" in text
    assert 'uv pip install --python .venv/bin/python "mineru[pipeline]==3.0.9"' in text
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


def test_container_image_workflow_sets_up_qemu_for_multi_arch_builds():
    data = _load_container_image_workflow()
    image_steps = data["jobs"]["image"]["steps"]
    assert any(
        step.get("uses")
        == "docker/setup-qemu-action@ce360397dd3f832beb865e1373c09c0e9f86d70a"
        for step in image_steps
    )


def test_container_image_workflow_exists_for_ghcr_release():
    data = _load_container_image_workflow()
    assert (
        data["jobs"]["image-nvidia"]["if"]
        == "github.event_name == 'workflow_dispatch' && github.event.inputs.publish_nvidia == 'true'"
    )
    image_steps = data["jobs"]["image"]["steps"]
    image_build_step = _find_step_by_uses(
        image_steps,
        "docker/build-push-action@10e90e3645eae34f1e60eeb005ba3a3d33f178e8",
    )
    nvidia_steps = data["jobs"]["image-nvidia"]["steps"]
    nvidia_build_step = _find_step_by_uses(
        nvidia_steps,
        "docker/build-push-action@10e90e3645eae34f1e60eeb005ba3a3d33f178e8",
    )

    assert data["jobs"]["image"]["env"]["REGISTRY"] == "ghcr.io"
    assert image_build_step["with"]["platforms"] == "linux/amd64,linux/arm64"
    assert nvidia_build_step["with"]["file"] == "./Dockerfile.nvidia"
