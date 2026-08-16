from __future__ import annotations

import json
import threading
from typing import Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"
_BOOTSTRAP_CACHE: Optional[Dict[str, str]] = None
_BOOTSTRAP_LOCK = threading.Lock()


def _request_json(url: str, timeout: float) -> Dict:
    req = Request(url, headers={"Accept": "application/rdap+json, application/json", "User-Agent": "IsDomainOK/2"})
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _load_bootstrap(timeout: float = 5.0) -> Dict[str, str]:
    global _BOOTSTRAP_CACHE
    if _BOOTSTRAP_CACHE is not None:
        return _BOOTSTRAP_CACHE
    with _BOOTSTRAP_LOCK:
        if _BOOTSTRAP_CACHE is not None:
            return _BOOTSTRAP_CACHE
        data = _request_json(BOOTSTRAP_URL, timeout)
        mapping: Dict[str, str] = {}
        for tlds, services in data.get("services", []):
            if not services:
                continue
            base = services[0].rstrip("/")
            for tld in tlds:
                mapping[tld.lower()] = base
        _BOOTSTRAP_CACHE = mapping
        return mapping


def _event_value(data: Dict, action: str) -> Optional[str]:
    for event in data.get("events", []):
        if event.get("eventAction") == action:
            return event.get("eventDate")
    return None


def _registrar_name(data: Dict) -> Optional[str]:
    for entity in data.get("entities", []):
        if "registrar" not in entity.get("roles", []):
            continue
        vcard = entity.get("vcardArray")
        if not isinstance(vcard, list) or len(vcard) < 2:
            continue
        for row in vcard[1]:
            if row and row[0] == "fn" and len(row) >= 4:
                return row[3]
    return None


def lookup_domain(domain: str, timeout: float = 5.0) -> Dict:
    tld = domain.rsplit(".", 1)[-1].lower()
    try:
        base = _load_bootstrap(timeout).get(tld)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        base = None

    if not base:
        return {"status": "unsupported"}

    url = f"{base}/domain/{quote(domain)}"
    try:
        data = _request_json(url, timeout)
    except HTTPError as exc:
        if exc.code == 404:
            return {"status": "available", "source": url}
        return {"status": "unknown", "source": url, "error": f"rdap_http_{exc.code}"}
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return {"status": "unknown", "source": url, "error": exc.__class__.__name__}

    nameservers = [item.get("ldhName", "").lower() for item in data.get("nameservers", []) if item.get("ldhName")]
    return {
        "status": "registered",
        "source": url,
        "registrar": _registrar_name(data),
        "registered_at": _event_value(data, "registration"),
        "expires_at": _event_value(data, "expiration") or _event_value(data, "registrar expiration"),
        "nameservers": nameservers,
    }
