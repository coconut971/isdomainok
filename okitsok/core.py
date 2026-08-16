from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List

from .dns import check_domain_detailed
from .market import inspect_sale_page
from .models import DomainReport, Money
from .pricing import godaddy_registration_quote
from .rdap import lookup_domain

DEFAULT_EXTENSIONS = [".com", ".fr", ".io", ".ai", ".app"]


def normalize_tlds(tlds: Iterable[str] | None) -> List[str]:
    values = list(tlds or DEFAULT_EXTENSIONS)
    result: List[str] = []
    for value in values:
        value = value.strip().lower()
        if not value:
            continue
        result.append(value if value.startswith(".") else f".{value}")
    return list(dict.fromkeys(result))


def expand_domains(names: Iterable[str], tlds: Iterable[str] | None = None) -> List[str]:
    extensions = normalize_tlds(tlds)
    domains: List[str] = []
    for raw in names:
        value = raw.strip().lower().rstrip(".")
        if not value:
            continue
        if "." in value:
            domains.append(value)
        else:
            domains.extend(f"{value}{ext}" for ext in extensions)
    return list(dict.fromkeys(domains))


def inspect_domain(
    domain: str,
    timeout: float = 4.0,
    use_rdap: bool = True,
    scan_market: bool = False,
    fetch_price: bool = False,
) -> DomainReport:
    report = DomainReport(domain=domain)
    report.dns_status = check_domain_detailed(domain, timeout)

    rdap = lookup_domain(domain, timeout) if use_rdap else {"status": "not_checked"}
    report.rdap_status = rdap.get("status", "unknown")
    report.registrar = rdap.get("registrar")
    report.registered_at = rdap.get("registered_at")
    report.expires_at = rdap.get("expires_at")
    report.nameservers = rdap.get("nameservers") or []

    if report.rdap_status == "registered":
        report.status = "registered"
    elif report.rdap_status == "available":
        report.status = "available"
    elif report.dns_status == "taken":
        report.status = "registered"
        report.notes.append("RDAP was unavailable; registration inferred from DNS.")
    elif report.dns_status == "available":
        report.status = "possibly_available"
        report.notes.append("DNS returned NXDOMAIN but RDAP could not confirm availability.")
    else:
        report.status = "unknown"

    if scan_market and report.status == "registered":
        market = inspect_sale_page(domain, timeout)
        report.for_sale = market.get("for_sale")
        report.marketplace = market.get("marketplace")
        report.sale_url = market.get("url")
        if market.get("asking_price"):
            price = market["asking_price"]
            report.asking_price = Money(
                value=price["value"],
                currency=price["currency"],
                source=report.marketplace or "public sale page",
                kind="asking",
                url=report.sale_url,
            )
        elif report.for_sale:
            report.notes.append("The domain appears to be for sale, but no public asking price was detected. Consider contacting the marketplace, registrar or a domain broker.")

    if fetch_price and report.status in ("available", "possibly_available"):
        quote = godaddy_registration_quote(domain, timeout=max(timeout, 8.0))
        if quote.get("status") == "ok":
            report.registration_price = Money(
                value=quote["value"],
                currency=quote["currency"],
                source=quote["source"],
                kind="registration",
            )
        elif quote.get("status") == "credentials_required":
            report.notes.append("Live registration pricing requires GODADDY_PAT.")
        elif quote.get("status") == "not_available":
            report.notes.append("Registrar pricing API reports the domain as unavailable.")
        else:
            report.notes.append(f"Registration price unavailable ({quote.get('error', 'unknown error')}).")

    return report


def check_domains(
    names: Iterable[str],
    extensions: Iterable[str] | None = None,
    timeout: float = 4.0,
    max_workers: int = 10,
    use_rdap: bool = True,
    scan_market: bool = False,
    fetch_price: bool = False,
) -> List[DomainReport]:
    domains = expand_domains(names, extensions)
    results = {}
    with ThreadPoolExecutor(max_workers=max(1, min(max_workers, 32))) as executor:
        futures = {
            executor.submit(inspect_domain, domain, timeout, use_rdap, scan_market, fetch_price): domain
            for domain in domains
        }
        for future in as_completed(futures):
            domain = futures[future]
            try:
                results[domain] = future.result()
            except Exception as exc:
                results[domain] = DomainReport(domain=domain, notes=[f"Unhandled check error: {exc.__class__.__name__}"])
    return [results[d] for d in domains]
