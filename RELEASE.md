# okitsok 1.0.0 - Release Notes

## Overview

okitsok 1.0.0 is the first stable version of this DNS-based domain name availability checker.

## What is okitsok?

okitsok is a **technical indicator** that queries DNS servers to determine if a domain name has active DNS records. It is a:

- **Local** tool: No web service, no external API
- **Simple** tool: Single command, clear output
- **Universal** tool: Usable by humans, scripts, and AI
- **Reliable** tool: No third-party service dependencies

## What's new in version 1.0.0

### Standalone distribution

- **Standalone binaries** for Windows, macOS, and Linux
- No Python installation required
- Size: ~9-10 MB (including Python and dependencies)
- Ready to use, zero-configuration

### Standardized CLI

- Simple command: `okitsok example`
- Pure JSON output for scripts: `okitsok example --json`
- Documented exit codes for workflow integration
- Non-interactive, deterministic

### Robust DNS logic

- Hierarchical checking: NS → SOA → A → AAAA
- Parallel checks for speed
- Configurable timeout
- Complete error handling

### Complete documentation

- **README**: Complete guide for humans and AI
- **EXAMPLES.md**: Integrations for Python, Node.js, Shell, Go, Rust
- **BUILD.md**: Binary build instructions
- **CHANGELOG.md**: Version history

## Download

### Binaries (recommended)

- **Windows**: `okitsok.exe` (~9 MB)
- **macOS**: `okitsok` (~9 MB)
- **Linux**: `okitsok` (~9 MB)

### pip installation

```bash
pip install okitsok
```

### pipx installation (isolation)

```bash
pipx install okitsok
```

## Quick usage

```bash
# Basic check
okitsok example

# JSON output
okitsok example --json

# With timeout
okitsok example --timeout 5
```

## Returned statuses

- **`available`**: No DNS records (NXDOMAIN)
- **`taken`**: DNS records detected
- **`unknown`**: Cannot determine (timeout, error)

## Exit codes

- **`0`**: At least one domain available
- **`1`**: No domains available
- **`130`**: User interrupted

## AI usage

okitsok is designed to be called by conversational agents, scripts, or other tools:

```python
import subprocess
import json

result = subprocess.run(
    ["okitsok", "example", "--json"],
    capture_output=True,
    text=True
)
domains = json.loads(result.stdout)
print(domains["example.com"])  # "taken" | "available" | "unknown"
```

See **EXAMPLES.md** for more integrations.

## Important limitations

okitsok provides a **technical indicator**, not a **certification**:

- Does NOT guarantee a domain is registrable
- Does NOT check prices or restrictions
- Does NOT contact registrars
- ONLY checks public DNS records

**Recommendation**: Use okitsok as initial filter, always verify with official registrar for final confirmation.

## Philosophy

okitsok is built to last:

- **Simple**: One feature, done well
- **Honest**: No marketing, limitations clearly documented
- **Universal**: For humans and machines
- **Local**: No external service dependencies
- **Responsible**: No false promises

## Support

- **Issues**: Report bugs or suggestions on the repository
- **Documentation**: README.md, EXAMPLES.md, BUILD.md
- **License**: MIT (free to use)

## Contributors

Thanks to everyone who contributed to making okitsok a simple and reliable tool.

---

**okitsok 1.0.0** - February 2026
