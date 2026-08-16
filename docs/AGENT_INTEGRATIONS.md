# AI agent integrations

IsDomainOK is designed to be used as a factual domain-intelligence layer underneath an AI agent.

The agent should generate and rank names. IsDomainOK should verify domain facts.

## Architecture

```text
AI agent
  |
  | generates candidate names
  v
IsDomainOK MCP / CLI
  |
  +-- DNS
  +-- RDAP
  +-- GoDaddy Domains API (user's own GODADDY_PAT)
  |
  v
structured availability, confidence and price data
  |
  v
AI agent ranks the surviving names
```

There is no hosted IsDomainOK API requirement and no central IsDomainOK credential service.

## Install the MCP extra

The core CLI supports Python 3.9+. The official MCP Python SDK v2 requires Python 3.10+, so MCP support is an optional extra:

```bash
python -m pip install -e '.[mcp]'
```

When the package is published, the intended command is:

```bash
python -m pip install 'isdomainok[mcp]'
```

The MCP entry point is:

```bash
isdomainok-mcp
```

It runs locally over stdio and must not print application output to stdout because stdout belongs to the MCP protocol.

## MCP tools

### `about_isdomainok`

Returns server capabilities and whether GoDaddy credentials are configured. It never returns the token.

### `check_domain`

Checks one exact domain such as `example.com`.

Optional arguments:

- `include_market`: inspect a public landing page for sale signals;
- `locked_price`: request a read-only locked GoDaddy registration quote when applicable.

### `check_name`

Checks one base name across multiple TLDs.

Example intent:

```json
{
  "name": "framevo",
  "tlds": ["com", "ai", "io"]
}
```

### `screen_names`

Designed for naming agents. Pass a batch of generated names and optional TLD/budget constraints. It filters out registered, conflicting, unknown and over-budget candidates and sorts eligible results by confidence and known registration price.

Example intent:

```json
{
  "names": ["framevo", "cutory", "reelio"],
  "tlds": ["com", "ai"],
  "max_registration_price": 150,
  "currency": "USD"
}
```

If a maximum price is specified and the registration price is unknown, the candidate is excluded because the budget cannot be verified.

## GoDaddy credentials

Use the user's own GoDaddy Personal Access Token:

```bash
export GODADDY_PAT="..."
```

PowerShell:

```powershell
$env:GODADDY_PAT="..."
```

Do not place the token in a repository, MCP configuration file, prompt, Skill file, or issue.

Without a token, DNS and RDAP still work. GoDaddy availability and pricing are simply unavailable.

## Claude Code

A minimal stdio configuration is available at `examples/claude-code-mcp.json`.

After installing the MCP extra, Claude Code can launch `isdomainok-mcp` as a local process. The GoDaddy token can be inherited from the user's environment rather than embedded in the configuration file.

## Codex and other Agent Skills clients

The portable Agent Skill is located at:

```text
skills/isdomainok-domain-naming/SKILL.md
```

It follows the open Agent Skills format. The Skill contains the naming workflow while MCP provides the factual tools.

For a naming task, an agent should normally:

1. generate a diverse candidate pool;
2. call `screen_names` once with the batch;
3. inspect exact domains only for finalists;
4. rank the surviving names based on the user's creative criteria;
5. clearly show availability confidence and price when known.

## Security boundary

IsDomainOK is read-only with respect to registrars.

It does not expose a domain-purchase or registration tool. A locked quote is still read-only and cannot charge the user's account.

## Legal boundary

Domain availability is not trademark clearance, company-name clearance, or permission to use a brand. Important commercial naming decisions should be followed by a separate legal/trademark check.
