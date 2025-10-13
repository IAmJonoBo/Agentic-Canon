#!/usr/bin/env python3
"""Synchronise templates/manifest.json from templates/manifest.yaml."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import]
except ImportError as exc:  # pragma: no cover - tooling ensures PyYAML is present
    raise SystemExit("PyYAML is required to sync the manifest") from exc


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_DIR = REPO_ROOT / "templates"
YAML_PATH = MANIFEST_DIR / "manifest.yaml"
JSON_PATH = MANIFEST_DIR / "manifest.json"


def load_yaml() -> dict:
    if not YAML_PATH.exists():
        raise FileNotFoundError(f"YAML manifest missing at {YAML_PATH}")
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Manifest root must be a mapping")
    return data


def load_json() -> dict | None:
    if not JSON_PATH.exists():
        return None
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def dump_json(data: dict) -> None:
    JSON_PATH.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _normalise_key(key: object) -> str:
    if isinstance(key, bool):
        return str(key).lower()
    return str(key)


def normalise(data: object) -> object:
    if isinstance(data, dict):
        return {
            _normalise_key(key): normalise(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [normalise(item) for item in data]
    return data


def manifests_match(source: dict, target: dict | None) -> bool:
    return target is not None and normalise(source) == normalise(target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Verify that JSON is up-to-date and exit"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    desired = load_yaml()
    current = load_json()

    if args.check:
        if manifests_match(desired, current):
            return 0
        print("manifest.json is out of date", file=sys.stderr)
        return 1

    dump_json(desired)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())