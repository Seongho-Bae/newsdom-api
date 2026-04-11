# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Lean multi-arch container delivery workflow with an optional NVIDIA image publishing path
- ClusterFuzzLite DOM-normalization fuzzing harness with a locked fuzz toolchain

### Changed

- Release automation now exports `*.intoto.jsonl` provenance bundles alongside build artifacts
- Tests now pin `uv` setup more tightly, and Pages rebuilds docs when lockfile or local Pages action inputs change

## [0.1.0] - 2026-04-09

### Added

- MinerU-backed DOM parsing API for scanned Japanese newspaper PDFs
- Synthetic newspaper fixture generation and structural equivalence checks
- Protected-branch CI, security gates, release provenance workflow, and Git Flow documentation

[Unreleased]: https://github.com/Seongho-Bae/newsdom-api/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Seongho-Bae/newsdom-api/releases/tag/v0.1.0
