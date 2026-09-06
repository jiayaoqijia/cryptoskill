#!/usr/bin/env python3
"""Plan database migrations and detect drift.

Author: Apple
Version: 1.0.0
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from migration_utils import (
    ensure_schema_table,
    get_applied_up_migrations,
    get_db_connection,
    list_migration_files,
    parse_migration_file,
)


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
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan migrations and detect drift")
    parser.add_argument("--migrations-dir", default="migrations", help="Path to migrations directory")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    payload = _read_json_stdin()
    params = _merge_params(args, payload)

    migrations_dir = Path(params["migrations_dir"]).resolve()

    try:
        conn = get_db_connection()
        ensure_schema_table(conn)
        applied = get_applied_up_migrations(conn)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1

    applied_map = {m["version"]: m for m in applied}

    files = list_migration_files(migrations_dir)
    parsed = [parse_migration_file(p) for p in files]

    pending = []
    drift = []
    for mig in parsed:
        if mig.version in applied_map:
            if applied_map[mig.version]["checksum"] != mig.checksum:
                drift.append(
                    {
                        "version": mig.version,
                        "expected": applied_map[mig.version]["checksum"],
                        "actual": mig.checksum,
                    }
                )
        else:
            pending.append(mig.version)

    output = {
        "ok": True,
        "migrations_dir": str(migrations_dir),
        "applied": [m["version"] for m in applied],
        "pending": pending,
        "drift": drift,
    }

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
