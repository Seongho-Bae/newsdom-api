"""Export GitHub attestation bundles as Scorecard-recognized release assets."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
from pathlib import Path


def _bundle_candidates(working_dir: Path, digest: str) -> tuple[Path, Path]:
    """Return possible attestation bundle filenames for a given digest."""

    return (
        working_dir / f"sha256:{digest}.jsonl",
        working_dir / f"sha256-{digest}.jsonl",
    )


def _resolve_gh_cli() -> str:
    """Resolve the GitHub CLI path required for attestation downloads."""

    gh_executable = shutil.which("gh")
    if gh_executable is None:
        raise FileNotFoundError("gh CLI is required to export release attestations")
    return gh_executable


def export_attestations(
    dist_dir: Path, repo: str, *, working_dir: Path | None = None
) -> list[Path]:
    """Download attestation bundles for release artifacts and rename them for Scorecard."""

    working_dir = (working_dir or Path.cwd()).resolve()
    gh_executable = _resolve_gh_cli()
    exported: list[Path] = []

    for artifact in sorted(dist_dir.iterdir()):
        if not artifact.is_file():
            continue
        if artifact.name in {"SHA256SUMS.txt", "release-manifest.json"}:
            continue
        if artifact.name.endswith(".intoto.jsonl"):
            continue

        artifact_path = artifact.resolve()
        subprocess.run(
            [gh_executable, "attestation", "download", str(artifact_path), "-R", repo],
            check=True,
            cwd=working_dir,
        )

        digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        bundle_path = next(
            (
                candidate
                for candidate in _bundle_candidates(working_dir, digest)
                if candidate.exists()
            ),
            None,
        )
        if bundle_path is None:
            raise FileNotFoundError(
                f"No attestation bundle downloaded for {artifact.name}"
            )

        output_path = dist_dir / f"{artifact.name}.intoto.jsonl"
        if output_path.exists():
            output_path.unlink()
        shutil.move(str(bundle_path), output_path)
        exported.append(output_path)

    return exported


def main() -> None:
    """Download and rename attestation bundles for the release dist directory."""

    parser = argparse.ArgumentParser(
        description="Export GitHub attestation bundles into dist/*.intoto.jsonl files"
    )
    parser.add_argument("dist_dir", type=Path)
    parser.add_argument("repo")
    args = parser.parse_args()

    export_attestations(args.dist_dir, args.repo)


if __name__ == "__main__":
    main()
