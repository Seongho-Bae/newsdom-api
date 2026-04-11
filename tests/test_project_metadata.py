from pathlib import Path
import re


def _locked_package_version(name: str) -> tuple[int, ...]:
    text = Path("uv.lock").read_text(encoding="utf-8")
    match = re.search(
        rf'\[\[package\]\]\nname = "{re.escape(name)}"\nversion = "([^"]+)"',
        text,
    )
    assert match is not None, f"package {name!r} missing from uv.lock"
    return tuple(int(part) for part in match.group(1).split("."))


def test_project_metadata_does_not_bundle_mineru_extra():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    dependencies_section = text.split("dependencies = [", 1)[1].split("]", 1)[0]
    assert "mineru[pipeline]" not in dependencies_section


def test_project_version_is_prepared_for_v0_1_1_release():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "0.1.1"' in text


def test_uv_lock_tracks_project_version() -> None:
    pyproject_text = Path("pyproject.toml").read_text(encoding="utf-8")
    pyproject_version = re.search(r'^version = "([^"]+)"', pyproject_text, re.MULTILINE)
    assert pyproject_version is not None

    uv_lock_text = Path("uv.lock").read_text(encoding="utf-8")
    lock_version = re.search(
        r'\[\[package\]\]\nname = "newsdom-api"\nversion = "([^"]+)"',
        uv_lock_text,
    )
    assert lock_version is not None
    assert lock_version.group(1) == pyproject_version.group(1)


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


def test_uv_lock_pins_pypdf_at_patched_release():
    assert _locked_package_version("pypdf") >= (6, 10, 0)
