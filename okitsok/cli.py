from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable, List

from . import __version__
from .core import DEFAULT_EXTENSIONS, check_domains
from .models import DomainReport


def _money(value) -> str:
    if value is None:
        return "-"
    return f"{value.value:,.2f} {value.currency}"


def format_human_readable(results: Iterable[DomainReport]) -> str:
    rows = list(results)
    if not rows:
        return "No results"

    lines: List[str] = []
    for item in rows:
        parts = [
            f"{item.domain:<30}",
            f"{item.status:<18}",
            f"confidence={item.confidence}",
        ]
        if item.godaddy_status == "ok":
            parts.append(f"godaddy={'available' if item.godaddy_available else 'unavailable'}")
        if item.registrar:
            parts.append(f"registrar={item.registrar}")
        if item.for_sale is True:
            sale = f"for-sale={item.marketplace or 'yes'}"
            if item.asking_price:
                sale += f" asking={_money(item.asking_price)}"
            parts.append(sale)
        if item.registration_price:
            label = "register-locked" if item.registration_price_locked else "register"
            parts.append(f"{label}={_money(item.registration_price)}")
        if item.renewal_price:
            parts.append(f"renew={_money(item.renewal_price)}")
        lines.append("  ".join(parts))
        for note in item.notes:
            lines.append(f"  -> {note}")
    return "\n".join(lines)


def format_json(results: Iterable[DomainReport]) -> str:
    return json.dumps([item.to_dict() for item in results], indent=2, ensure_ascii=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="isdomainok",
        description="Domain intelligence CLI: DNS + RDAP + GoDaddy consensus, sale signals and pricing.",
    )
    parser.add_argument("names", nargs="+", help="Base names (example) or full domains (example.com).")
    parser.add_argument(
        "--tlds",
        nargs="+",
        default=DEFAULT_EXTENSIONS,
        metavar="TLD",
        help="TLDs to try for base names (default: com fr io ai app).",
    )
    parser.add_argument("--json", action="store_true", help="Emit stable machine-readable JSON.")
    parser.add_argument(
        "--dns-only",
        action="store_true",
        help="Use DNS evidence only; skip RDAP and GoDaddy.",
    )
    parser.add_argument(
        "--no-godaddy",
        action="store_true",
        help="Disable automatic GoDaddy availability/pricing checks even when GODADDY_PAT is configured.",
    )
    parser.add_argument(
        "--market",
        action="store_true",
        help="Inspect registered-domain landing pages for public sale signals and asking prices.",
    )
    parser.add_argument(
        "--price",
        action="store_true",
        help="Request a locked one-year GoDaddy quote. Indicative registration/renewal prices are automatic with GODADDY_PAT.",
    )
    parser.add_argument("--timeout", type=float, default=4.0, help="Network timeout in seconds (default: 4).")
    parser.add_argument("--workers", type=int, default=10, help="Parallel workers (default: 10, max: 32).")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        results = check_domains(
            names=args.names,
            extensions=args.tlds,
            timeout=args.timeout,
            max_workers=args.workers,
            use_rdap=not args.dns_only,
            use_godaddy=not args.dns_only and not args.no_godaddy,
            scan_market=args.market,
            fetch_price=args.price,
        )
        print(format_json(results) if args.json else format_human_readable(results))
        confirmed_available = any(item.status == "available" for item in results)
        sys.exit(0 if confirmed_available else 1)
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
