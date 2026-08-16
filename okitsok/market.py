from __future__ import annotations

import re
import ssl
from html import unescape
from typing import Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MARKETPLACES = {
    "afternic": "Afternic",
    "sedo": "Sedo",
    "hugedomains": "HugeDomains",
    "atom.com": "Atom",
    "squadhelp": "Atom",
    "dan.com": "GoDaddy/Dan",
    "godaddy": "GoDaddy",
}

SALE_PHRASES = (
    "domain is for sale",
    "this domain is for sale",
    "buy this domain",
    "domain for sale",
    "make an offer",
    "buy now",
)

_PRICE_PATTERNS = [
    re.compile(r"(?:buy now|price|asking price)[^$€£]{0,80}([$€£])\s*([0-9][0-9,.\s]{1,14})", re.I),
    re.compile(r"([$€£])\s*([0-9][0-9,.\s]{1,14})[^\n<]{0,80}(?:buy now|purchase|domain)", re.I),
]


def _currency(symbol: str) -> str:
    return {"$": "USD", "€": "EUR", "£": "GBP"}.get(symbol, symbol)


def _parse_amount(raw: str) -> Optional[float]:
    cleaned = raw.replace(" ", "").strip(".,")
    if not cleaned:
        return None
    if "," in cleaned and "." not in cleaned:
        chunks = cleaned.split(",")
        if len(chunks[-1]) == 3:
            cleaned = "".join(chunks)
        else:
            cleaned = cleaned.replace(",", ".")
    else:
        cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def extract_asking_price(text: str) -> Optional[Tuple[float, str]]:
    for pattern in _PRICE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        amount = _parse_amount(match.group(2))
        if amount is not None and 1 <= amount <= 100_000_000:
            return amount, _currency(match.group(1))
    return None


def inspect_sale_page(domain: str, timeout: float = 5.0) -> Dict:
    context = ssl.create_default_context()
    last_error = None
    for scheme in ("https", "http"):
        url = f"{scheme}://{domain}/"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; IsDomainOK/2; +https://github.com/coconut971/okitsok)"})
        try:
            with urlopen(req, timeout=timeout, context=context if scheme == "https" else None) as response:
                final_url = response.geturl()
                body = response.read(512_000).decode("utf-8", errors="ignore")
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc.__class__.__name__
            continue

        text = unescape(re.sub(r"<[^>]+>", " ", body)).lower()
        haystack = f"{final_url.lower()} {body.lower()} {text}"
        marketplace = next((label for needle, label in MARKETPLACES.items() if needle in haystack), None)
        sale_signal = any(phrase in text for phrase in SALE_PHRASES) or marketplace is not None
        if not sale_signal:
            return {"for_sale": False, "url": final_url}

        price = extract_asking_price(text)
        result = {"for_sale": True, "url": final_url, "marketplace": marketplace}
        if price:
            result["asking_price"] = {"value": price[0], "currency": price[1]}
        return result

    return {"for_sale": None, "error": last_error or "unreachable"}
