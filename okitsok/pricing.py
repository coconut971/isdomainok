from __future__ import annotations

import json
import os
from typing import Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://api.godaddy.com/v3/domains"


def _call_json(req: Request, timeout: float) -> Dict:
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _money(price: Dict) -> Optional[Dict]:
    value = price.get("value")
    currency = price.get("currencyCode")
    if value is None or not currency:
        return None
    return {"value": float(value) / 100, "currency": str(currency)}


def _one_year_prices(prices) -> Tuple[Optional[Dict], Optional[Dict]]:
    for item in prices or []:
        if item.get("term") == "YEAR" and int(item.get("period", 0) or 0) == 1:
            return _money(item.get("price") or {}), _money(item.get("renewalPrice") or {})
    return None, None


def godaddy_availability(
    domain: str,
    timeout: float = 8.0,
    token: Optional[str] = None,
    optimize_for: str = "ACCURACY",
) -> Dict:
    """Check GoDaddy v3 availability and indicative registration pricing.

    The endpoint is read-only. With ``optimize_for='ACCURACY'`` GoDaddy is asked
    to favour availability accuracy over speed. No quote or registration is
    created by this function.
    """
    token = token or os.getenv("GODADDY_PAT")
    if not token:
        return {"status": "credentials_required", "env": "GODADDY_PAT"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    query = urlencode({"domain": domain, "optimizeFor": optimize_for})
    url = f"{API_BASE}/check-availability?{query}"

    try:
        data = _call_json(Request(url, headers=headers), timeout)
    except HTTPError as exc:
        return {"status": "error", "error": f"http_{exc.code}"}
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return {"status": "error", "error": exc.__class__.__name__}

    registration, renewal = _one_year_prices(data.get("prices"))
    return {
        "status": "ok",
        "available": bool(data.get("available")),
        "registration_price": registration,
        "renewal_price": renewal,
        "source": "GoDaddy",
        "optimize_for": optimize_for,
    }


def godaddy_registration_quote(
    domain: str,
    timeout: float = 8.0,
    token: Optional[str] = None,
    availability: Optional[Dict] = None,
) -> Dict:
    """Return a locked one-year GoDaddy registration quote.

    A registration quote is free/read-only and does not purchase the domain.
    The returned ``quoteToken`` is intentionally not exposed by the CLI because
    IsDomainOK does not implement domain purchase operations.
    """
    token = token or os.getenv("GODADDY_PAT")
    if not token:
        return {"status": "credentials_required", "env": "GODADDY_PAT"}

    availability = availability or godaddy_availability(domain, timeout=timeout, token=token)
    if availability.get("status") != "ok":
        return availability
    if not availability.get("available"):
        return {"status": "not_available"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = json.dumps({"domain": domain, "period": 1}).encode("utf-8")
    quote_req = Request(
        f"{API_BASE}/registration-quotes",
        data=payload,
        headers=headers,
        method="POST",
    )

    try:
        quote = _call_json(quote_req, timeout)
    except HTTPError as exc:
        return {"status": "error", "error": f"http_{exc.code}"}
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return {"status": "error", "error": exc.__class__.__name__}

    exact = _money(quote.get("price") or {})
    if not exact:
        return {"status": "error", "error": "missing_price"}

    return {
        "status": "ok",
        "available": bool(quote.get("available", True)),
        "value": exact["value"],
        "currency": exact["currency"],
        "source": "GoDaddy",
        "locked": True,
        "expires_at": quote.get("expiresAt"),
        "renewal_price": availability.get("renewal_price"),
    }
