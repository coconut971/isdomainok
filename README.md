<p align="center">
  <img src="docs/isdomainok.svg" alt="IsDomainOK banner" width="100%" />
</p>

<p align="center">
  <img alt="CI" src="https://github.com/coconut971/okitsok/actions/workflows/ci.yml/badge.svg" />
  <img alt="Python 3.9+" src="https://img.shields.io/badge/core-python%203.9%2B-3776AB" />
  <img alt="MCP Python 3.10+" src="https://img.shields.io/badge/MCP-python%203.10%2B-8A2BE2" />
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-2ea44f" />
  <img alt="Version 2.1" src="https://img.shields.io/badge/version-2.1-8be9fd" />
</p>

# IsDomainOK

**Local-first domain intelligence for humans, scripts and AI agents.**

IsDomainOK does not trust a single availability signal. It can combine DNS evidence, authoritative RDAP registration data and GoDaddy's Domains API, then expose a conservative consensus status, confidence level, registration/renewal pricing and optional public resale signals.

Version 2.1 also exposes the same engine as a **local MCP server** and ships a portable **Agent Skill** for project/product/company naming workflows.

> IsDomainOK never purchases or registers domains. Registrar integration is read-only.

## Why

AI assistants are good at inventing names but usually bad at knowing which suggestions are actually usable.

IsDomainOK separates the jobs:

```text
AI agent
  |
  | invents names
  v
IsDomainOK
  |-- DNS
  |-- RDAP
  `-- GoDaddy (user's own token)
  |
  v
availability + confidence + real registrar pricing
  |
  v
AI agent ranks the surviving names
```

There is no hosted IsDomainOK API requirement, no shared registrar account and no central secret store.

## The three-signal model

When `GODADDY_PAT` is configured, a normal check uses:

1. **DNS** — fast evidence from NS, SOA, A and AAAA records.
2. **RDAP** — public registration data discovered through the IANA bootstrap registry.
3. **GoDaddy Domains v3** — registrar availability with `optimizeFor=ACCURACY`, plus indicative registration and renewal prices.

The sources remain separate in JSON. IsDomainOK never silently turns disagreement into certainty.

Typical outcomes:

- `available` + `confidence=high` — independent availability signals agree.
- `registered` + `confidence=high` — independent registration/unavailability signals agree.
- `possibly_available` — DNS says NXDOMAIN but no stronger source confirmed it.
- `conflict` — strong sources disagree; manual confirmation is recommended.
- `unknown` — insufficient evidence.

## Features

- DNS checks: NS, SOA, A and AAAA
- RDAP lookup using the IANA bootstrap registry
- automatic GoDaddy availability checks when `GODADDY_PAT` exists
- GoDaddy `ACCURACY` optimization
- indicative registration and renewal prices
- optional locked read-only registration quote with `--price`
- registrar, registration date, expiration date and nameservers when public
- multiple names and custom TLDs in one call
- parallel checks
- public domain-for-sale signal and asking-price detection
- stable JSON output
- local MCP server for AI hosts
- portable Agent Skill for naming workflows
- no database, account, telemetry or hosted backend required

## Install the CLI

The package is not claimed as published on PyPI yet. For now install from a clone:

```bash
git clone https://github.com/coconut971/okitsok.git
cd okitsok
python -m pip install -e .
```

Core CLI support remains Python 3.9+.

Once published, the intended install command will be:

```bash
pipx install isdomainok
```

## Install MCP support

The official MCP Python SDK v2 requires Python 3.10+. MCP is therefore an optional extra rather than a dependency of the core CLI:

```bash
python -m pip install -e '.[mcp]'
```

This installs the local stdio entry point:

```bash
isdomainok-mcp
```

## Configure GoDaddy

Create a GoDaddy Personal Access Token with the required Domains permissions and keep it outside the repository:

```bash
export GODADDY_PAT="your-token"
```

PowerShell:

```powershell
$env:GODADDY_PAT="your-token"
```

Do **not** commit the token to Git or place it in prompts/config examples. With the environment variable configured, GoDaddy checks become automatic.

Skip GoDaddy for one call:

```bash
isdomainok lightsraw --no-godaddy
```

Use DNS only:

```bash
isdomainok lightsraw --dns-only
```

## CLI quick start

```bash
isdomainok lightsraw
```

Default TLDs are `.com`, `.fr`, `.io`, `.ai` and `.app`.

With `GODADDY_PAT`, output can include:

```text
lightsraw.com                  registered          confidence=high  godaddy=unavailable
lightsraw.ai                   available           confidence=high  godaddy=available  register=74.99 USD  renew=74.99 USD
```

Prices above are only an illustration; IsDomainOK prints values returned at request time.

Check exact domains:

```bash
isdomainok example.com example.net
```

Choose TLDs:

```bash
isdomainok lightsraw --tlds com fr ai dev tech
```

Machine-readable output:

```bash
isdomainok lightsraw --json
```

## MCP tools

The MCP server exposes four read-only tools.

### `about_isdomainok`

Returns capabilities, version, default TLDs and whether GoDaddy is configured. It never exposes the token.

### `check_domain`

Checks one exact domain with the same consensus engine as the CLI.

### `check_name`

Checks one base name across multiple TLDs.

### `screen_names`

Built specifically for naming agents. Pass generated project/product/company names in one batch and optionally provide TLD and registration-budget constraints.

Conceptual request:

```json
{
  "names": ["framevo", "cutory", "reelio"],
  "tlds": ["com", "ai"],
  "max_registration_price": 150,
  "currency": "USD"
}
```

By default it only keeps confirmed `available` results, excludes `conflict`/`unknown`/registered domains, and sorts survivors by confidence and known registration price.

If a price ceiling is supplied, a domain whose price is unknown is excluded because the budget cannot be verified.

## Agent Skill

The portable naming Skill lives at:

```text
skills/isdomainok-domain-naming/SKILL.md
```

It follows the open Agent Skills format and is intended for Codex, Claude Code and other compatible agent clients.

The Skill tells the agent to:

1. understand the naming brief;
2. generate a broad pool of names itself;
3. batch-screen them through IsDomainOK;
4. reject registered/conflicting/unknown candidates;
5. respect a registration budget when supplied;
6. rank the remaining names on creative quality plus domain evidence;
7. clearly distinguish domain availability from trademark clearance.

The AI model remains responsible for creativity. IsDomainOK does **not** call another model API.

## Claude Code

A minimal stdio example is included at:

```text
examples/claude-code-mcp.json
```

After installing `.[mcp]`, configure Claude Code to launch `isdomainok-mcp`. Let the process inherit `GODADDY_PAT` from the user's environment rather than embedding the token in JSON.

See [`docs/AGENT_INTEGRATIONS.md`](docs/AGENT_INTEGRATIONS.md) for the complete integration model.

## Locked registration price

A normal GoDaddy availability request can return indicative registration/renewal prices. For stronger pre-purchase verification:

```bash
isdomainok mynewname.com --price
```

`--price` requests a one-year registration quote. The quote re-checks availability and can lock the registration price for its validity window.

**There is still no purchase endpoint in IsDomainOK.**

## Public resale prices

Inspect a registered domain's public landing page with:

```bash
isdomainok example.com --market
```

If a recognizable marketplace or explicit asking price is present, IsDomainOK reports it. No resale valuation is invented when the owner has not published one.

## Accuracy rules

IsDomainOK intentionally stays conservative:

- GoDaddy available + RDAP available -> `available`, high confidence.
- GoDaddy unavailable + RDAP registered -> `registered`, high confidence.
- GoDaddy available while RDAP registered -> `conflict`.
- DNS contains positive records while RDAP/GoDaddy says available -> `conflict`.
- DNS NXDOMAIN alone -> `possibly_available`, not a guaranteed purchase opportunity.

The registrar still performs the final authoritative verification at quote/registration time.

## Price limitations

There are two very different prices:

1. **Registration price** for an unregistered domain — registrar-specific and obtainable through GoDaddy when credentials are configured.
2. **Resale/asking price** for a registered domain — knowable only when the owner/marketplace publishes it or a broker supplies it.

IsDomainOK returns price unavailable rather than fabricating a resale valuation.

## Privacy and security

Depending on configuration and flags, IsDomainOK may contact:

- DNS resolvers configured on the machine
- IANA's RDAP bootstrap registry and authoritative RDAP services
- GoDaddy's Domains API when `GODADDY_PAT` is configured
- the target domain when `--market` is enabled

No telemetry is sent by IsDomainOK itself. The GoDaddy token is read from the environment and never included in tool/CLI output.

The MCP server is read-only with respect to registrars and exposes no registration or purchase tool.

## Legal boundary

Domain availability is not trademark clearance, company-name clearance or legal permission to use a brand. Commercial naming decisions should be followed by an appropriate trademark/company-name check.

## Compatibility

The Python package internals remain under `okitsok` during the v2 transition. Both CLI commands work:

```bash
isdomainok example
okitsok example
```

## Development

Core tests:

```bash
python -m unittest discover -s tests -v
```

MCP test (Python 3.10+):

```bash
python -m pip install -e '.[mcp]'
python -m unittest tests.test_mcp -v
```

CI tests the core on Python 3.9, 3.11 and 3.13, plus a dedicated MCP v2 job on Python 3.13.

## License

MIT
