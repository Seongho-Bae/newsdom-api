import subprocess
import sys
from pathlib import Path


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
