from pathlib import Path


def test_project_metadata_does_not_bundle_mineru_extra():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    dependencies_section = text.split("dependencies = [", 1)[1].split("]", 1)[0]
    assert "mineru[pipeline]" not in dependencies_section


def test_docs_theme_range_stays_below_warning_release():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert '"mkdocs-material>=9.6,<9.7"' in text


def test_docs_core_range_stays_below_mkdocs_two():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert '"mkdocs>=1.6,<2.0"' in text


def test_contributing_documents_docs_toolchain_hold():
    text = Path("CONTRIBUTING.md").read_text(encoding="utf-8")
    expected_phrases = [
        "MkDocs 1.x",
        "mkdocs<2.0",
        "mkdocs-material<9.7",
        "uv.lock",
        "migration path",
    ]
    for phrase in expected_phrases:
        assert phrase in text


def test_project_uses_spdx_license_string_not_deprecated_table():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert 'license = "MIT"' in text
    assert 'license = {text = "MIT"}' not in text


def test_project_declares_locked_fuzz_extra_without_bundling_nvidia_stack():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert "fuzz = [" in text
    assert '"atheris==3.0.0 ;' in text
    assert '"pyinstaller==6.16.0"' in text
    assert "nvidia = [" not in text
