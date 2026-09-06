#!/usr/bin/env python3
"""Generate a new migration template.

Author: Apple
Version: 1.0.0
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def _read_json_stdin() -> dict:
    if sys.stdin.isatty():
        return {}
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def _merge_params(args: argparse.Namespace, payload: dict) -> dict:
    return {
        "migrations_dir": payload.get("migrations_dir", args.migrations_dir),
        "name": payload.get("name", args.name),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a migration template")
    parser.add_argument("--migrations-dir", default="migrations", help="Path to migrations directory")
    parser.add_argument("--name", required=True, help="Migration name, e.g. add_user_status")
    return parser.parse_args()


def _sanitize_name(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]+", "_", name.strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        raise ValueError("Invalid migration name")
    return cleaned


def main() -> int:
    args = _parse_args()
    payload = _read_json_stdin()
    params = _merge_params(args, payload)

    migrations_dir = Path(params["migrations_dir"]).resolve()
    migrations_dir.mkdir(parents=True, exist_ok=True)

    try:
        migration_name = _sanitize_name(params["name"])
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{migration_name}.sql"
    path = migrations_dir / filename

    if path.exists():
        print(json.dumps({"ok": False, "error": f"File already exists: {path}"}))
        return 1

    content = (
        f"-- MIGRATION: {migration_name}\n"
        "-- DIRECTION: up\n"
        "-- TODO: Add your schema changes here.\n\n"
        "-- DIRECTION: down\n"
        "-- TODO: Add rollback SQL here.\n"
    )

    path.write_text(content, encoding="utf-8")

    print(json.dumps({"ok": True, "created": str(path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
