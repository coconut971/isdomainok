# Changelog

## [1.0.0] - 2026-02-03

### Vision

okitsok is finalized as a **universal building block** usable by humans AND AI:
- Local, non-interactive, deterministic tool
- Strictly machine-readable JSON output
- Standalone binary distribution (no Python installation required)
- Complete documentation for multi-language integrations

### Finalized Features

- **Robust DNS logic**: Hierarchical checking (NS → SOA → A → AAAA)
- **Stable CLI**: Non-interactive, standardized output
- **Pure JSON output**: No text pollution, guaranteed format
- **Documented exit codes**: Easy script integration
- **Standalone distribution**: Windows/macOS/Linux binaries with PyInstaller

### Documentation

- **Restructured README**: Human + AI sections
- **BUILD.md**: Binary generation instructions
- **EXAMPLES.md**: Integration examples (Python, Node.js, Shell, Go, Rust)
- Exit codes and deterministic behavior documented

### Technical

- Dependency: `dnspython>=2.0.0` (included in binaries)
- Parallel DNS checks (concurrent.futures)
- Socket fallback if dnspython absent
- PyInstaller spec for multi-platform builds

### Philosophy (unchanged)

- **Technical indicator**: Not certification, not guarantee
- **Responsibility**: Limitations clearly documented
- **Simplicity**: Fundamental, durable, universal tool
- **Transparency**: What okitsok does AND doesn't do

### Status (standardized)

- `available`: No DNS records (NXDOMAIN)
- `taken`: At least one DNS record exists
- `unknown`: Cannot determine (timeout, error)

### Exit codes

- `0`: At least one domain available
- `1`: No domains available
- `130`: User interrupted
