from __future__ import annotations

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


def _dependencies_section(text: str) -> str:
    marker = "dependencies = ["
    if marker not in text:
        raise AssertionError("pyproject.toml is missing a project dependencies section")

    start = text.index(marker) + len(marker)
    bracket_depth = 1
    in_string = False
    escape = False

    for index in range(start, len(text)):
        char = text[index]

        if in_string:
            if escape:
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue
        if char == "[":
            bracket_depth += 1
            continue
        if char == "]":
            bracket_depth -= 1
            if bracket_depth == 0:
                return text[start:index]

    raise AssertionError("pyproject.toml dependencies array is not properly closed")


def test_dependencies_section_reports_missing_marker_clearly():
    try:
        _dependencies_section("[project]\nname = 'newsdom-api'\n")
    except AssertionError as exc:
        assert str(exc) == "pyproject.toml is missing a project dependencies section"
    else:
        raise AssertionError("expected missing dependencies marker assertion")


def test_dependencies_section_handles_dependency_extras_safely():
    text = '[project]\ndependencies = [\n  "example[docs]>=1.0",\n  "plain>=2.0",\n]\n'

    section = _dependencies_section(text)

    assert '"example[docs]>=1.0"' in section
    assert '"plain>=2.0"' in section


def test_project_metadata_does_not_bundle_mineru_extra():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    dependencies_section = _dependencies_section(text)
    assert "mineru[pipeline]" not in dependencies_section


def test_docs_theme_range_stays_below_warning_release():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert '"mkdocs-material>=9.6,<9.7"' in text


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
