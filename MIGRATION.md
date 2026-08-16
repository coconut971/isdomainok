# Migrating from okitsok 1.x to IsDomainOK 2.x

IsDomainOK 2.x keeps the old `okitsok` command as a compatibility alias, but the behavior and JSON model are intentionally richer.

## Command name

Preferred:

```bash
isdomainok example
```

Compatibility alias:

```bash
okitsok example
```

## Availability semantics

Version 1 treated DNS NXDOMAIN as `available`. Version 2 is more conservative:

- `available`: RDAP confirms the domain is not registered.
- `possibly_available`: DNS says NXDOMAIN, but RDAP could not confirm it.
- `registered`: RDAP or positive DNS evidence indicates registration/use.
- `unknown`: no reliable conclusion could be reached.

If your automation previously assumed that every DNS NXDOMAIN result was registrable, update it to require `status == "available"` for a confirmed result.

## JSON output

Version 2 emits a list of structured domain reports instead of a simple domain-to-status mapping. Each report can include DNS/RDAP evidence, registrar metadata, sale signals, public asking price, live registration price, and notes.

## New optional network checks

- `--market` visits the target domain landing page to look for explicit sale signals and public asking prices.
- `--price` calls GoDaddy's Domains API when `GODADDY_PAT` is set. It requests availability and pricing only; it never purchases a domain.

Both features are opt-in.

## Custom TLDs and multiple names

```bash
isdomainok brand-one brand-two --tlds com fr ai dev
```

Exact domains can be mixed with base names:

```bash
isdomainok brand example.net --tlds com fr
```
