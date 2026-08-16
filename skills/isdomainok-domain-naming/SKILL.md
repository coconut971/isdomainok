---
name: isdomainok-domain-naming
description: Generate, screen, and rank project, product, company, app, and brand names by checking real domain availability with IsDomainOK. Use when a user asks for naming ideas, available domains, brandable names, TLD comparisons, or wants to avoid suggestions whose domains are already registered or over budget.
license: MIT
compatibility: Requires IsDomainOK locally. Prefer its MCP tools when available; otherwise use the isdomainok CLI. GoDaddy pricing requires the user's own GODADDY_PAT. Network access is required for RDAP and registrar checks.
metadata:
  author: coconut971
  version: "1.0"
---

# IsDomainOK Domain Naming

Use this skill to turn naming work from brainstorming into a verified shortlist.

## Core rule

Do not recommend a name as a strong final candidate until its relevant domains have been checked.

The language model should do the creative work. IsDomainOK should do the factual domain work. Do not add a separate LLM API call inside the workflow.

## Preferred workflow

1. Understand the naming brief:
   - what is being named;
   - desired language and tone;
   - length constraints;
   - important keywords or concepts;
   - forbidden words or styles;
   - preferred TLDs;
   - registration budget if any.
2. Generate a broad candidate pool, normally 20 to 50 distinct names.
3. Remove obvious duplicates, spelling traps, confusing pronunciations, and names that violate the brief.
4. Send the remaining names to IsDomainOK in one batch.
5. Prefer `screen_names` when the MCP server is available.
6. Keep the raw availability sources separate. Do not hide a `conflict` result.
7. Rank the surviving names using both creative quality and domain evidence.
8. Present a compact shortlist with factual domain status and price information.

## MCP tools

When IsDomainOK MCP is connected, prefer these tools:

- `about_isdomainok` — confirm capabilities and whether GoDaddy credentials are configured without exposing the token.
- `check_domain` — inspect one exact domain.
- `check_name` — inspect one base name across several TLDs.
- `screen_names` — batch-filter generated names and return the best domain candidates.

For naming tasks, `screen_names` is usually the best first tool after brainstorming.

Example intent:

- names: 30 generated brand names
- tlds: `com`, `ai`, `io`
- max_registration_price: user budget when supplied
- currency: currency requested by the user
- allow_possible: `false` by default

## CLI fallback

If MCP is unavailable, use the CLI:

```bash
isdomainok nameone nametwo namethree --tlds com ai io --json
```

If a GoDaddy token is configured, normal checks can include registrar availability and indicative registration/renewal prices automatically.

For a locked read-only registration quote on a specific promising domain:

```bash
isdomainok example.com --price --json
```

Never attempt to register or purchase a domain. IsDomainOK intentionally has no purchase capability.

## Availability rules

Interpret results conservatively:

- `available` + high confidence: strong candidate.
- `available` + medium confidence: usable candidate, but mention the confidence level.
- `possibly_available`: do not present as confirmed unless the user explicitly wants speculative candidates.
- `registered`: exclude from a normal available-domain shortlist.
- `conflict`: exclude from the final shortlist until manually confirmed.
- `unknown`: exclude unless the user asks to investigate further.

A DNS NXDOMAIN result alone is not proof that a domain can be registered.

## Pricing rules

There are two different price concepts:

1. Registration price for a currently unregistered domain.
2. Asking/resale price for a domain already owned by someone else.

Do not confuse them.

When the user gives a registration budget:

- pass the budget to `screen_names`;
- do not claim a candidate is under budget when its price is unknown;
- state the registrar and currency when known;
- remember that registrar prices can change.

Do not invent resale valuations. Only report a resale price when a public sale page actually exposes one.

## Ranking guidance

After factual filtering, rank names using criteria relevant to the brief, such as:

- memorability;
- pronunciation;
- spelling clarity;
- brevity;
- distinctiveness;
- fit with the product or company;
- international usability;
- domain quality (`.com` may outrank alternatives when the user values it);
- availability confidence;
- registration price.

Do not let a cheap domain rescue a weak name. Domain availability is a constraint, not the only naming criterion.

## Recommended final output

Return a small shortlist, normally 3 to 10 candidates. For each candidate include:

- name;
- best available domain;
- availability status;
- confidence;
- registration price and renewal price when known;
- one short reason the name fits the brief.

Also mention notable rejected candidates only when that information helps the user understand the tradeoff.

## Safety and legal boundary

Domain availability is not trademark clearance, company-name clearance, or legal permission to use a brand. Never imply otherwise.

If the naming decision is commercially important, recommend a separate trademark/company-name check before launch.

Never expose, print, copy, or commit `GODADDY_PAT` or any other credential.
