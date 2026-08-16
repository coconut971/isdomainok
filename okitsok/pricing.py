from __future__ import annotations

import json
import os
from typing import Dict, Optional
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


def godaddy_registration_quote(domain: str, timeout: float = 8.0, token: Optional[str] = None) -> Dict:
    """Return a one-year GoDaddy registration quote when credentials are available.

    No purchase is performed. The API call is read-only and the returned quote expires.
    """
    token = token or os.getenv("GODADDY_PAT")
    if not token:
        return {"status": "credentials_required", "env": "GODADDY_PAT"}

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    check_url = f"{API_BASE}/check-availability?{urlencode({'domain': domain})}"
    try:
        availability = _call_json(Request(check_url, headers=headers), timeout)
        if not availability.get("available"):
            return {"status": "not_available"}

        indicative = None
        for item in availability.get("prices") or []:
            if item.get("term") == "YEAR" and int(item.get("period", 0) or 0) == 1:
                indicative = _money(item.get("price") or {})
                if indicative:
                    break

        payload = json.dumps({"domain": domain, "period": 1}).encode("utf-8")
        quote_req = Request(
            f"{API_BASE}/registration-quotes",
            data=payload,
            headers={**headers, "Content-Type": "application/json"},
            method="POST",
        )
        quote = _call_json(quote_req, timeout)
    except HTTPError as exc:
        return {"status": "error", "error": f"http_{exc.code}"}
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return {"status": "error", "error": exc.__class__.__name__}

    exact = _money(quote.get("price") or {})
    chosen = exact or indicative
    if not chosen:
        return {"status": "error", "error": "missing_price"}

    return {
        "status": "ok",
        "value": chosen["value"],
        "currency": chosen["currency"],
        "source": "GoDaddy",
        "locked": exact is not None,
        "expires_at": quote.get("expiresAt"),
    }
