"""Build a release manifest for generated distribution artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def _sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(dist_dir: Path) -> dict[str, object]:
    """Build manifest metadata for all regular files in a dist directory."""

    artifacts = []
    for path in sorted(
        p
        for p in dist_dir.iterdir()
        if p.is_file() and p.name != "release-manifest.json"
    ):
        artifacts.append(
            {
                "name": path.name,
                "size": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )
    return {"dist_dir": str(dist_dir), "artifacts": artifacts}


def main() -> None:
    """Write the release manifest JSON for a distribution directory."""

    parser = argparse.ArgumentParser()
    parser.add_argument("dist_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    manifest = build_manifest(args.dist_dir)
    args.output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
