from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from . import __version__
from .core import DEFAULT_EXTENSIONS, check_domains, inspect_domain

try:
    from mcp.server import MCPServer
except ImportError as exc:  # pragma: no cover - exercised by the optional extra
    raise RuntimeError(
        "IsDomainOK MCP requires the optional MCP dependencies. "
        "Install with: python -m pip install 'isdomainok[mcp]'"
    ) from exc


mcp = MCPServer("IsDomainOK")


def _report_dict(report) -> Dict[str, Any]:
    return report.to_dict()


def _normalize_currency(value: Optional[str]) -> Optional[str]:
    return value.upper().strip() if value else None


@mcp.tool()
def about_isdomainok() -> Dict[str, Any]:
    """Describe this IsDomainOK server without exposing credentials."""
    return {
        "name": "IsDomainOK",
        "version": __version__,
        "local_first": True,
        "telemetry": False,
        "purchasing_supported": False,
        "godaddy_configured": bool(os.getenv("GODADDY_PAT")),
        "default_tlds": DEFAULT_EXTENSIONS,
        "signals": ["DNS", "RDAP", "GoDaddy (when GODADDY_PAT is configured)"],
    }


@mcp.tool()
def check_domain(
    domain: str,
    include_market: bool = False,
    locked_price: bool = False,
) -> Dict[str, Any]:
    """Check one exact domain using DNS, RDAP and optional GoDaddy consensus.

    include_market inspects a registered domain's public landing page for sale signals.
    locked_price asks GoDaddy for a read-only registration quote when the domain appears available.
    No purchase or registration action exists in this server.
    """
    value = domain.strip().lower().rstrip(".")
    if not value or "." not in value:
        return {
            "error": "exact_domain_required",
            "message": "Provide an exact domain such as example.com.",
        }

    return _report_dict(
        inspect_domain(
            value,
            scan_market=include_market,
            fetch_price=locked_price,
        )
    )


@mcp.tool()
def check_name(
    name: str,
    tlds: Optional[List[str]] = None,
    include_market: bool = False,
    locked_price: bool = False,
) -> List[Dict[str, Any]]:
    """Check a project or brand name across multiple TLDs.

    Example: name='acme', tlds=['com', 'ai', 'io'].
    The result keeps DNS, RDAP and GoDaddy signals separate and includes consensus confidence.
    """
    reports = check_domains(
        names=[name],
        extensions=tlds or DEFAULT_EXTENSIONS,
        scan_market=include_market,
        fetch_price=locked_price,
    )
    return [_report_dict(item) for item in reports]


@mcp.tool()
def screen_names(
    names: List[str],
    tlds: Optional[List[str]] = None,
    max_registration_price: Optional[float] = None,
    currency: Optional[str] = None,
    allow_possible: bool = False,
) -> Dict[str, Any]:
    """Screen candidate project/brand names and return domains worth considering.

    This is designed for naming agents: generate names first, then pass the candidates here.
    By default only confirmed `available` domains are eligible. Set allow_possible=true to
    include `possibly_available` results. If max_registration_price is supplied, candidates
    without a matching known registration price are excluded because the budget cannot be
    verified. Prices are registrar-specific and are normally available when GODADDY_PAT is set.
    """
    clean_names = [item.strip() for item in names if item and item.strip()]
    if not clean_names:
        return {"checked": 0, "eligible": [], "excluded": [], "error": "no_names"}

    reports = check_domains(
        names=clean_names,
        extensions=tlds or DEFAULT_EXTENSIONS,
        scan_market=False,
        fetch_price=False,
    )

    accepted_statuses = {"available"}
    if allow_possible:
        accepted_statuses.add("possibly_available")

    requested_currency = _normalize_currency(currency)
    eligible: List[Dict[str, Any]] = []
    excluded: List[Dict[str, Any]] = []

    for report in reports:
        data = _report_dict(report)
        reason: Optional[str] = None

        if report.status not in accepted_statuses:
            reason = f"status_{report.status}"
        elif report.status == "conflict":
            reason = "conflicting_sources"

        price = report.registration_price
        if reason is None and max_registration_price is not None:
            if price is None:
                reason = "registration_price_unknown"
            elif requested_currency and price.currency.upper() != requested_currency:
                reason = "registration_currency_mismatch"
            elif price.value > max_registration_price:
                reason = "registration_price_over_budget"

        if reason is None:
            eligible.append(data)
        else:
            excluded.append({"domain": report.domain, "reason": reason})

    confidence_order = {"high": 0, "medium": 1, "low": 2, "none": 3}
    eligible.sort(
        key=lambda item: (
            confidence_order.get(str(item.get("confidence", "none")), 4),
            (item.get("registration_price") or {}).get("value", float("inf")),
            item.get("domain", ""),
        )
    )

    return {
        "checked": len(reports),
        "eligible_count": len(eligible),
        "eligible": eligible,
        "excluded": excluded,
        "godaddy_configured": bool(os.getenv("GODADDY_PAT")),
        "note": "Domain availability is not trademark clearance.",
    }


def main() -> None:
    """Run the local MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
