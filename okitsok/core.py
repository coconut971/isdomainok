from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Optional, Tuple

from .dns import check_domain_detailed
from .market import inspect_sale_page
from .models import DomainReport, Money
from .pricing import godaddy_availability, godaddy_registration_quote
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


def resolve_consensus(
    dns_status: str,
    rdap_status: str,
    godaddy_available: Optional[bool],
) -> Tuple[str, str, List[str]]:
    """Resolve a conservative status from independent availability signals."""
    notes: List[str] = []

    # Strong contradictions must be surfaced instead of silently picking a source.
    if rdap_status == "registered" and godaddy_available is True:
        return "conflict", "none", ["RDAP reports registered while GoDaddy reports available."]
    if rdap_status == "available" and godaddy_available is False:
        return "conflict", "none", ["RDAP reports available while GoDaddy reports unavailable."]
    if dns_status == "taken" and (rdap_status == "available" or godaddy_available is True):
        return "conflict", "none", ["DNS has positive records while an availability source reports the domain available."]

    if rdap_status == "registered" or godaddy_available is False:
        supporting = int(rdap_status == "registered") + int(godaddy_available is False) + int(dns_status == "taken")
        confidence = "high" if supporting >= 2 else "medium"
        if rdap_status != "registered" and godaddy_available is False:
            notes.append("GoDaddy reports the domain unavailable for registration.")
        return "registered", confidence, notes

    if rdap_status == "available" or godaddy_available is True:
        supporting = int(rdap_status == "available") + int(godaddy_available is True) + int(dns_status == "available")
        confidence = "high" if supporting >= 2 else "medium"
        return "available", confidence, notes

    if dns_status == "taken":
        return "registered", "low", ["Registration inferred from DNS because registrar/RDAP confirmation was unavailable."]
    if dns_status == "available":
        return "possibly_available", "low", ["DNS returned NXDOMAIN but no registrar/RDAP source confirmed availability."]
    return "unknown", "low", notes


def _money_from_provider(value, source: str, kind: str) -> Optional[Money]:
    if not value:
        return None
    return Money(
        value=value["value"],
        currency=value["currency"],
        source=source,
        kind=kind,
    )


def inspect_domain(
    domain: str,
    timeout: float = 4.0,
    use_rdap: bool = True,
    use_godaddy: bool = True,
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

    godaddy = godaddy_availability(domain, timeout=max(timeout, 8.0)) if use_godaddy else {"status": "skipped"}
    report.godaddy_status = godaddy.get("status", "unknown")
    if report.godaddy_status == "ok":
        report.godaddy_available = bool(godaddy.get("available"))
        report.registration_price = _money_from_provider(
            godaddy.get("registration_price"), "GoDaddy", "registration_indicative"
        )
        report.renewal_price = _money_from_provider(
            godaddy.get("renewal_price"), "GoDaddy", "renewal_indicative"
        )

    report.status, report.confidence, consensus_notes = resolve_consensus(
        report.dns_status,
        report.rdap_status,
        report.godaddy_available,
    )
    report.notes.extend(consensus_notes)

    if fetch_price:
        quote = godaddy_registration_quote(
            domain,
            timeout=max(timeout, 8.0),
            availability=godaddy if report.godaddy_status == "ok" else None,
        )
        if quote.get("status") == "ok":
            report.godaddy_status = "ok"
            report.godaddy_available = bool(quote.get("available", True))
            report.registration_price = Money(
                value=quote["value"],
                currency=quote["currency"],
                source="GoDaddy",
                kind="registration_locked_quote",
            )
            report.registration_price_locked = True
            if quote.get("renewal_price"):
                report.renewal_price = _money_from_provider(
                    quote.get("renewal_price"), "GoDaddy", "renewal_indicative"
                )
            report.status, report.confidence, consensus_notes = resolve_consensus(
                report.dns_status,
                report.rdap_status,
                report.godaddy_available,
            )
            report.notes.extend(note for note in consensus_notes if note not in report.notes)
        elif quote.get("status") == "credentials_required":
            report.notes.append("A locked GoDaddy quote requires GODADDY_PAT.")
        elif quote.get("status") == "not_available":
            report.godaddy_status = "ok"
            report.godaddy_available = False
            report.status, report.confidence, consensus_notes = resolve_consensus(
                report.dns_status,
                report.rdap_status,
                report.godaddy_available,
            )
            report.notes.extend(note for note in consensus_notes if note not in report.notes)
        else:
            report.notes.append(f"Locked registration quote unavailable ({quote.get('error', 'unknown error')}).")

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
            report.notes.append(
                "The domain appears to be for sale, but no public asking price was detected. "
                "Consider contacting the marketplace, registrar or a domain broker."
            )

    return report


def check_domains(
    names: Iterable[str],
    extensions: Iterable[str] | None = None,
    timeout: float = 4.0,
    max_workers: int = 10,
    use_rdap: bool = True,
    use_godaddy: bool = True,
    scan_market: bool = False,
    fetch_price: bool = False,
) -> List[DomainReport]:
    domains = expand_domains(names, extensions)
    results = {}
    with ThreadPoolExecutor(max_workers=max(1, min(max_workers, 32))) as executor:
        futures = {
            executor.submit(
                inspect_domain,
                domain,
                timeout,
                use_rdap,
                use_godaddy,
                scan_market,
                fetch_price,
            ): domain
            for domain in domains
        }
        for future in as_completed(futures):
            domain = futures[future]
            try:
                results[domain] = future.result()
            except Exception as exc:
                results[domain] = DomainReport(
                    domain=domain,
                    notes=[f"Unhandled check error: {exc.__class__.__name__}"],
                )
    return [results[d] for d in domains]
