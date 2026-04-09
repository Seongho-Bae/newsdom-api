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


def _gh_executable() -> str:
    """Return the gh executable path used to download attestations."""

    gh = shutil.which("gh")
    if gh is None:
        raise FileNotFoundError("gh executable not found in PATH")
    return gh


def export_attestations(
    dist_dir: Path, repo: str, *, working_dir: Path | None = None
) -> list[Path]:
    """Download attestation bundles for release artifacts and rename them for Scorecard."""

    working_dir = (working_dir or Path.cwd()).resolve()
    exported: list[Path] = []
    gh = _gh_executable()

    for artifact in sorted(dist_dir.iterdir()):
        if not artifact.is_file():
            continue
        if artifact.name in {"SHA256SUMS.txt", "release-manifest.json"}:
            continue
        if artifact.name.endswith(".intoto.jsonl"):
            continue

        subprocess.run(
            [gh, "attestation", "download", str(artifact), "-R", repo],
            check=True,
            cwd=working_dir,
        )

        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
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
