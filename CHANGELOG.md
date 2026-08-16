# Changelog

## [2.0.0] - 2026-08-16

### Identity

- User-facing project name changed from **okitsok** to **IsDomainOK**.
- New primary CLI command: `isdomainok`.
- Legacy `okitsok` command kept as a compatibility alias during the v2 transition.

### Domain intelligence

- Added RDAP lookups using the IANA RDAP bootstrap registry.
- DNS remains a fast signal, but DNS-only NXDOMAIN is no longer treated as definitive proof of registrability.
- Added conservative statuses: `registered`, `available`, `possibly_available`, and `unknown`.
- Added registrar, registration date, expiration date, and nameserver metadata when exposed by RDAP.
- Added multiple-name checks, custom TLD lists, and parallel execution.

### Pricing and resale signals

- Added optional inspection of public domain-for-sale landing pages.
- Added extraction of a public asking price only when the page clearly exposes one.
- Added marketplace detection for common sale landers.
- Added optional read-only GoDaddy v3 registration pricing through `GODADDY_PAT`.
- IsDomainOK deliberately does not invent resale valuations when no public price exists.

### Automation

- JSON output now returns structured domain reports suitable for scripts and AI agents.
- Added unit tests for core domain expansion, RDAP parsing, and public asking-price extraction.
- Added GitHub Actions CI across Python 3.9, 3.11, and 3.13.

### Documentation

- Rebuilt the README around the v2 behavior and limitations.
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

> This v1 availability model is retained here for historical reference. v2 uses RDAP to avoid treating DNS absence as definitive registration availability.
