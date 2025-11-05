#!/usr/bin/env python3
"""Scan frontiers/waivers for upcoming expirations."""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WAIVER_DIR = REPO_ROOT / "frontiers" / "waivers"
DEFAULT_WARNING_DAYS = 7

REQUIRED_FIELDS = {
    "id",
    "control",
    "category",
    "owner",
    "approver",
    "created",
    "expires",
    "description",
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--warning-days",
        type=int,
        default=DEFAULT_WARNING_DAYS,
        help="Number of days before expiry to raise warnings (default: 7).",
    )
    parser.add_argument(
        "--fail-expired",
        action="store_true",
        help="Exit with non-zero status when expired waivers are detected.",
    )
    return parser.parse_args()


def _load_waiver(path: Path) -> Dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data["__path"] = str(path.relative_to(REPO_ROOT))
    return data


def _to_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _evaluate_waivers(
    warning_days: int,
) -> Dict[str, List[Dict[str, Any]]]:
    today = date.today()
    upcoming: List[Dict[str, Any]] = []
    expired: List[Dict[str, Any]] = []
    invalid: List[Dict[str, Any]] = []

    if not WAIVER_DIR.exists():
        return {"upcoming": upcoming, "expired": expired, "invalid": invalid}

    for path in sorted(WAIVER_DIR.glob("*.yml")):
        record = _load_waiver(path)
        missing = REQUIRED_FIELDS - record.keys()
        if missing:
            record["missing_fields"] = sorted(missing)
            invalid.append(record)
            continue

        expiry = _to_date(str(record["expires"]))
        delta = (expiry - today).days
        record["days_until_expiry"] = delta

        if delta < 0:
            expired.append(record)
        elif delta <= warning_days:
            upcoming.append(record)

    return {"upcoming": upcoming, "expired": expired, "invalid": invalid}


def _write_github_output(results: Dict[str, List[Dict[str, Any]]]) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as handle:
        for key, value in results.items():
            handle.write(f"{key}={json.dumps(value)}\n")


def main() -> int:
    args = _parse_args()
    results = _evaluate_waivers(args.warning_days)
    _write_github_output(results)

    if not any(results.values()):
        print("✅ No waivers found.")
        return 0

    if results["invalid"]:
        print("⚠️ Invalid waiver files detected:")
        for waiver in results["invalid"]:
            print(f"  - {waiver['__path']} missing {', '.join(waiver['missing_fields'])}")

    if results["upcoming"]:
        print("⏰ Waivers expiring soon:")
        for waiver in results["upcoming"]:
            print(
                f"  - {waiver['id']} ({waiver['control']}) expires {waiver['expires']} "
                f"(in {waiver['days_until_expiry']} days) [{waiver['__path']}]"
            )

    if results["expired"]:
        print("❌ Expired waivers:")
        for waiver in results["expired"]:
            print(
                f"  - {waiver['id']} ({waiver['control']}) expired {waiver['expires']} "
                f"[{waiver['__path']}]"
            )

    if results["invalid"]:
        return 1
    if results["expired"] and args.fail_expired:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
