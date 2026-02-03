# okitsok - Project Structure

## Core Files

### Source Code
- `okitsok/__init__.py` - Package metadata and version
- `okitsok/__main__.py` - Entry point for binary distribution
- `okitsok/cli.py` - Command-line interface
- `okitsok/core.py` - Domain checking orchestration
- `okitsok/dns.py` - DNS verification logic (NS/SOA/A/AAAA)

### Configuration
- `pyproject.toml` - Python package configuration
- `okitsok.spec` - PyInstaller binary build configuration
- `.gitignore` - Git exclusions

## Documentation

### User Documentation
- `README.md` - Main documentation (human + AI)
- `EXAMPLES.md` - Integration examples (Python, Node.js, Shell, Go, Rust)
- `BUILD.md` - Binary build instructions
- `RELEASE.md` - Version 1.0.0 release notes
- `CHANGELOG.md` - Version history and philosophy

### Tool Declaration (for AI agents)
- `ai-tool.yaml` - Primary descriptor for AI agents and frameworks
- `okitsok.tool.json` - JSON version for automated loaders
- `TOOLS.md` - Integration documentation for agents and curators

### Project Documentation
- `FINALIZATION.md` - Finalization summary and next steps
- `PROJECT.md` - This file (project structure overview)
- `LICENSE` - MIT License

## Distribution

### Binary (built with PyInstaller)
- `dist/okitsok.exe` - Windows standalone binary (~9 MB)
- `dist/okitsok` - macOS/Linux standalone binary (to be built)

### Python Package
- Available via `pip install okitsok`
- Available via `pipx install okitsok`

## File Purpose Summary

### For End Users
- `README.md` - Start here
- `dist/okitsok.exe` - Download and run

### For Developers
- `BUILD.md` - How to build binaries
- `EXAMPLES.md` - How to integrate in code
- `pyproject.toml` - Package dependencies

### For AI Agents
- `ai-tool.yaml` - Primary descriptor (install + usage)
- `okitsok.tool.json` - JSON descriptor (automated parsing)
- `TOOLS.md` - Integration guide

### For Maintainers
- `FINALIZATION.md` - Project status and roadmap
- `CHANGELOG.md` - History and decisions
- `PROJECT.md` - Structure overview

## Build Artifacts (not in git)

- `build/` - PyInstaller build cache
- `dist/` - Generated binaries
- `__pycache__/` - Python bytecode cache
- `*.egg-info/` - Package metadata cache

## Philosophy

okitsok is:
- Local-first (no external services)
- DNS-based (technical indicator only)
- Simple (one clear purpose)
- Declarable (machine-readable descriptors)
- Durable (stable, long-term tool)

okitsok is not:
- A registrar
- A certification service
- A web service
- An API

## Key Design Decisions

1. **Standalone binaries** - No Python installation required
2. **JSON output** - Machine-readable, no text pollution
3. **Exit codes** - Script integration friendly
4. **Tool descriptors** - AI agent discoverable
5. **Honest limitations** - Clear about what it does and doesn't do

## Next Steps After 1.0.0

1. Generate macOS and Linux binaries
2. Create GitHub Release with all three binaries
3. Optional: Publish to PyPI
4. Replace OWNER in descriptor files with actual GitHub username
5. Consider creating a minimal tool registry

## Maintenance Guidelines

### Can be improved
- Performance optimizations
- Better error handling
- Support for more TLDs
- Bug fixes
- Documentation improvements

### Should not be changed
- Core philosophy (local, DNS-only)
- Output format (breaking changes)
- Complexity creep (keep it simple)
- External dependencies (stay self-contained)
