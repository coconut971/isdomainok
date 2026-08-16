<p align="center">
  <img src="docs/isdomainok.svg" alt="IsDomainOK banner" width="100%" />
</p>

<p align="center">
  <img alt="CI" src="https://github.com/coconut971/okitsok/actions/workflows/ci.yml/badge.svg" />
  <img alt="Python 3.9+" src="https://img.shields.io/badge/python-3.9%2B-3776AB" />
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-2ea44f" />
  <img alt="Version 2.0" src="https://img.shields.io/badge/version-2.0-8be9fd" />
</p>

# IsDomainOK

**A small domain-intelligence CLI for humans, scripts and AI agents.**

IsDomainOK does not trust a single signal. It can combine local DNS evidence, authoritative RDAP registration data and GoDaddy's current Domains API availability result, then expose a conservative consensus status and confidence level.

> Version 2 is the successor to `okitsok`. The old `okitsok` command remains available as a compatibility alias.

## The three-signal model

When `GODADDY_PAT` is configured, a normal check uses:

1. **DNS** — fast evidence from NS, SOA, A and AAAA records.
2. **RDAP** — public registration data discovered through the IANA bootstrap registry.
3. **GoDaddy Domains v3** — registrar availability with `optimizeFor=ACCURACY`, plus indicative registration and renewal prices.

The sources are deliberately kept separate in JSON. IsDomainOK never silently converts disagreement into certainty.

Typical outcomes:

- `available` + `confidence=high` — at least two independent availability signals agree.
- `registered` + `confidence=high` — at least two registration/unavailability signals agree.
- `possibly_available` — DNS says NXDOMAIN but no registrar/RDAP source confirmed it.
- `conflict` — strong sources disagree; manual confirmation is recommended.
- `unknown` — insufficient evidence.

## Features

- DNS checks: NS, SOA, A and AAAA
- RDAP lookup using the IANA bootstrap registry
- automatic GoDaddy availability checks when `GODADDY_PAT` exists
- GoDaddy `ACCURACY` optimization for availability checks
- indicative one-year registration and renewal prices from GoDaddy
- optional locked GoDaddy registration quote with `--price`
- registration metadata: registrar, registration date, expiration date and nameservers when public
- multiple names and custom TLDs in one call
- parallel checks
- conservative sale-page detection for registered domains
- public asking-price extraction when a sale page clearly exposes a price
- stable JSON output for automation and agents
- no database, account or hosted backend required

## Install

The v2 package is not claimed as published on PyPI yet. For now install it from a clone:

```bash
git clone https://github.com/coconut971/okitsok.git
cd okitsok
python -m pip install -e .
```

Once the package is published, the intended install command will be:

```bash
pipx install isdomainok
```

## Configure GoDaddy

Create a GoDaddy Personal Access Token with the required Domains read permissions, then keep it outside the repository:

```bash
export GODADDY_PAT="your-token"
```

On Windows PowerShell:

```powershell
$env:GODADDY_PAT="your-token"
```

Do **not** commit the token to Git. With the variable configured, GoDaddy checks become automatic; no extra CLI flag is required.

To deliberately skip GoDaddy for one call:

```bash
isdomainok lightsraw --no-godaddy
```

For an entirely local DNS-only check:

```bash
isdomainok lightsraw --dns-only
```

## Quick start

```bash
isdomainok lightsraw
```

Default TLDs are `.com`, `.fr`, `.io`, `.ai` and `.app`.

With `GODADDY_PAT`, output can include:

```text
lightsraw.com                  registered          confidence=high  godaddy=unavailable
lightsraw.ai                   available           confidence=high  godaddy=available  register=74.99 USD  renew=74.99 USD
```

Prices above are only an illustration; IsDomainOK prints the values returned at request time.

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

## Locked registration price

A normal GoDaddy availability request can return indicative registration/renewal prices. For a stronger pre-purchase verification, use:

```bash
isdomainok mynewname.com --price
```

`--price` asks GoDaddy for a one-year registration quote. The quote re-checks availability and locks the registration price for its validity window. IsDomainOK **does not implement the purchase endpoint**, so this action cannot register or charge for a domain.

## Public resale prices

Inspect a registered domain's public landing page with:

```bash
isdomainok example.com --market
```

If a recognizable marketplace or public asking price is present, IsDomainOK reports it. No resale valuation is invented when the owner has not published a price.

## JSON model

Example shape:

```json
[
  {
    "domain": "example.com",
    "status": "registered",
    "confidence": "high",
    "dns_status": "taken",
    "rdap_status": "registered",
    "godaddy_status": "ok",
    "godaddy_available": false,
    "registrar": "Example Registrar",
    "registered_at": "1995-08-14T04:00:00Z",
    "expires_at": "2027-08-13T04:00:00Z",
    "nameservers": ["a.iana-servers.net", "b.iana-servers.net"],
    "for_sale": false,
    "marketplace": null,
    "asking_price": null,
    "registration_price": null,
    "renewal_price": null,
    "registration_price_locked": false,
    "sale_url": null,
    "notes": []
  }
]
```

## Accuracy rules

IsDomainOK intentionally stays conservative:

- GoDaddy says available + RDAP says available → `available`, high confidence.
- GoDaddy says unavailable + RDAP says registered → `registered`, high confidence.
- GoDaddy says available while RDAP says registered → `conflict`.
- DNS contains positive records while RDAP/GoDaddy says available → `conflict`.
- DNS NXDOMAIN alone → `possibly_available`, not a guaranteed purchase opportunity.

The registrar itself still performs the final authoritative verification at quote/registration time.

## Price limitations

There are two very different prices:

1. **Registration price** for an unregistered domain — registrar-specific and available through GoDaddy when credentials are configured.
2. **Resale/asking price** for a registered domain — only knowable when the owner/marketplace publishes it or a broker provides it.

IsDomainOK intentionally returns “price unavailable” rather than fabricating a resale valuation.

## Privacy and network requests

Depending on configuration and flags, IsDomainOK may contact:

- DNS resolvers configured on the machine
- IANA's RDAP bootstrap registry and authoritative RDAP services
- GoDaddy's Domains API when `GODADDY_PAT` is configured
- the target domain itself when `--market` is enabled

No telemetry is sent by IsDomainOK itself. The GoDaddy token is read from the environment and is never included in output.

## Compatibility

The Python package internals remain under `okitsok` for the 2.0 transition. Both commands work:

```bash
isdomainok example
okitsok example
```

## Development

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

CI runs on Python 3.9, 3.11 and 3.13.

## License

MIT
