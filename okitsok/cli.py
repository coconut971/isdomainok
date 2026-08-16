from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable, List

from . import __version__
from .core import DEFAULT_EXTENSIONS, check_domains
from .models import DomainReport


def format_human_readable(results: Iterable[DomainReport]) -> str:
    rows = list(results)
    if not rows:
        return "No results"

    lines: List[str] = []
    for item in rows:
        parts = [f"{item.domain:<30}", f"{item.status:<18}"]
        if item.registrar:
            parts.append(f"registrar={item.registrar}")
        lines.append("  ".join(parts))
        for note in item.notes:
            lines.append(f"  -> {note}")
    return "\n".join(lines)


def format_json(results: Iterable[DomainReport]) -> str:
    return json.dumps([item.to_dict() for item in results], indent=2, ensure_ascii=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="isdomainok",
        description="Domain intelligence CLI: availability and registration data through DNS + RDAP.",
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
    parser.add_argument("--dns-only", action="store_true", help="Skip RDAP and use DNS evidence only.")
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
        )
        print(format_json(results) if args.json else format_human_readable(results))
        confirmed_available = any(item.status == "available" for item in results)
        sys.exit(0 if confirmed_available else 1)
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
