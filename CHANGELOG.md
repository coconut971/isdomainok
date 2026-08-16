# Changelog

## [2.1.0] - 2026-08-16

### AI agent integration

- Added an optional local MCP server using the official MCP Python SDK v2.
- Added the `isdomainok-mcp` stdio entry point.
- Added MCP tools for server capabilities, exact-domain checks, base-name checks across TLDs, and batch screening of generated names.
- Added budget-aware candidate filtering for naming workflows.
- MCP remains optional so the core CLI can keep Python 3.9+ support while MCP uses Python 3.10+.

### Agent Skill

- Added `skills/isdomainok-domain-naming/SKILL.md` following the open Agent Skills format.
- The Skill keeps creative name generation in the host AI and uses IsDomainOK only for factual domain verification.
- Added conservative rules for conflicts, unknown results, unverified prices and trademark/legal boundaries.

### Integrations and testing

- Added a Claude Code stdio MCP configuration example.
- Added `docs/AGENT_INTEGRATIONS.md` with the local-first/BYOK architecture.
- Added a dedicated CI job that installs the MCP extra and calls the MCP server through the SDK client.
- Version bumped to 2.1.0.

## [2.0.0] - 2026-08-16

### Identity

- User-facing project name changed from **okitsok** to **IsDomainOK**.
- New primary CLI command: `isdomainok`.
- Legacy `okitsok` command kept as a compatibility alias during the v2 transition.

### Domain intelligence

- Added RDAP lookups using the IANA RDAP bootstrap registry.
- DNS remains a fast signal, but DNS-only NXDOMAIN is no longer treated as definitive proof of registrability.
- Added conservative statuses: `registered`, `available`, `possibly_available`, `conflict`, and `unknown`.
- Added registrar, registration date, expiration date, and nameserver metadata when exposed by RDAP.
- Added multiple-name checks, custom TLD lists, and parallel execution.
- Added GoDaddy as an independent availability source when `GODADDY_PAT` is configured.
- Added confidence levels derived from DNS, RDAP and GoDaddy consensus.

### Pricing and resale signals

- Added optional inspection of public domain-for-sale landing pages.
- Added extraction of a public asking price only when the page clearly exposes one.
- Added marketplace detection for common sale landers.
- Added read-only GoDaddy v3 indicative registration and renewal pricing through `GODADDY_PAT`.
- Added optional read-only locked registration quotes.
- IsDomainOK deliberately does not invent resale valuations when no public price exists.

### Automation

- JSON output returns structured domain reports suitable for scripts and AI agents.
- Added unit tests for core domain expansion, RDAP parsing, public asking-price extraction, GoDaddy parsing and consensus rules.
- Added GitHub Actions CI across Python 3.9, 3.11, and 3.13.

### Documentation

- Rebuilt the README around v2 behavior and limitations.
- Added a lightweight SVG project banner and truthful CI/Python/license/version badges.
- Added explicit network/privacy documentation and pricing limitations.

## [1.0.0] - 2026-02-03

### Vision

okitsok was finalized as a small DNS-based building block usable by humans and automation:
- Local, non-interactive tool
- Machine-readable JSON output
- Standalone binary distribution plan
- Multi-language integration documentation

### Features

- DNS checking in the order NS → SOA → A → AAAA
- Standardized CLI output
- JSON output
- Documented exit codes
- Parallel DNS checks
- Socket fallback if `dnspython` is unavailable

### Historical status model

- `available`: DNS returned NXDOMAIN
- `taken`: At least one DNS record existed
- `unknown`: Timeout or resolver error

> This v1 availability model is retained here for historical reference. v2 uses RDAP and registrar consensus to avoid treating DNS absence as definitive registration availability.
