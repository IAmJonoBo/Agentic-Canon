#!/usr/bin/env python3
"""Validate MkDocs front matter against the frontiers schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import ValidationError, validate

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "frontiers" / "policy" / "frontiers.schema.json"
DOCS_DIR = REPO_ROOT / "docs"


def iter_markdown_files() -> list[Path]:
    return sorted(DOCS_DIR.rglob("*.md"))


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def parse_front_matter(markdown: Path) -> dict:
    text = markdown.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("unterminated YAML front matter")
    return yaml.safe_load(parts[1]) or {}


def main() -> int:
    schema = load_schema()
    errors: list[str] = []

    for md in iter_markdown_files():
        try:
            front_matter = parse_front_matter(md)
            validate(instance=front_matter, schema=schema)
        except (ValueError, ValidationError) as exc:
            errors.append(f"{md.relative_to(REPO_ROOT)}: {exc}")

    if errors:
        print("❌ Front matter validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("✅ Front matter validation passed for all docs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
