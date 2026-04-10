import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType


def test_clusterfuzzlite_integration_files_exist():
    assert Path(".clusterfuzzlite/project.yaml").exists()
    assert Path(".clusterfuzzlite/Dockerfile").exists()
    assert Path(".clusterfuzzlite/build.sh").exists()
    assert Path(".github/workflows/clusterfuzzlite.yml").exists()
    assert Path("fuzzers/dom_builder_fuzzer.py").exists()
    assert Path("fuzzers/corpus/dom_builder_fuzzer/mineru_sample.json").exists()


def test_clusterfuzzlite_workflow_runs_pinned_python_code_change_fuzzing():
    text = Path(".github/workflows/clusterfuzzlite.yml").read_text(encoding="utf-8")
    assert (
        "google/clusterfuzzlite/actions/build_fuzzers@52ecc61cb587ee99c26825a112a21abf19c7448c"
        in text
    )
    assert (
        "google/clusterfuzzlite/actions/run_fuzzers@52ecc61cb587ee99c26825a112a21abf19c7448c"
        in text
    )
    assert "language: python" in text
    assert "mode: code-change" in text
    assert "fuzz-seconds: 300" in text
    assert "github-token: ${{ github.token }}" in text
    assert "bad-build-check: false" in text


def test_clusterfuzzlite_dockerfile_places_build_script_at_src_root():
    text = Path(".clusterfuzzlite/Dockerfile").read_text(encoding="utf-8")
    assert "gcr.io/oss-fuzz-base/base-builder-python@sha256:" in text
    assert "ghcr.io/astral-sh/uv@sha256:" in text
    assert "COPY .clusterfuzzlite/build.sh /src/build.sh" in text


def test_clusterfuzzlite_build_script_uses_locked_uv_fuzz_extra():
    text = Path(".clusterfuzzlite/build.sh").read_text(encoding="utf-8")
    assert "uv sync --frozen --extra fuzz" in text
    assert "pip3 install . pyinstaller atheris" not in text


def test_dom_builder_fuzzer_smoke_mode_runs_without_cluster():
    completed = subprocess.run(
        [
            sys.executable,
            "fuzzers/dom_builder_fuzzer.py",
            "--smoke",
            "tests/fixtures/mineru_sample.json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "Traceback" not in completed.stderr


def test_dom_builder_fuzzer_forwards_libfuzzer_flags_to_atheris(monkeypatch):
    module_path = Path("fuzzers/dom_builder_fuzzer.py")
    spec = importlib.util.spec_from_file_location("dom_builder_fuzzer", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    fake_atheris = ModuleType("atheris")
    captured: dict[str, object] = {}

    def fake_setup(argv, callback):
        captured["argv"] = argv
        captured["callback"] = callback

    def fake_fuzz():
        captured["fuzz_called"] = True

    fake_atheris.Setup = fake_setup
    fake_atheris.Fuzz = fake_fuzz
    monkeypatch.setitem(sys.modules, "atheris", fake_atheris)

    result = module.main(["-timeout=1", "-runs=0"])

    assert result == 0
    assert captured["argv"] == [module_path.name, "-timeout=1", "-runs=0"]
    assert captured["fuzz_called"] is True
