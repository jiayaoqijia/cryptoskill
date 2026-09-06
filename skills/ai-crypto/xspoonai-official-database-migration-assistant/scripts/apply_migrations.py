#!/usr/bin/env python3
"""Apply pending migrations.

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
    record_migration,
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
        "dry_run": payload.get("dry_run", args.dry_run),
        "to_version": payload.get("to_version", args.to_version),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply pending migrations")
    parser.add_argument("--migrations-dir", default="migrations", help="Path to migrations directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview SQL without executing")
    parser.add_argument("--to-version", help="Apply up to a target version (inclusive)")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    payload = _read_json_stdin()
    params = _merge_params(args, payload)

    migrations_dir = Path(params["migrations_dir"]).resolve()
    dry_run = bool(params["dry_run"])
    to_version = params.get("to_version")

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
    pending = [m for m in parsed if m.version not in applied_map]

    if to_version:
        pending = [m for m in pending if m.version <= to_version]

    if not pending:
        print(json.dumps({"ok": True, "message": "No pending migrations", "applied": []}, indent=2))
        return 0

    planned = []
    applied_versions = []

    for mig in pending:
        if not mig.up_sql:
            print(json.dumps({"ok": False, "error": f"Missing up SQL for {mig.version}"}))
            return 1

        if dry_run:
            planned.append({"version": mig.version, "name": mig.name, "sql": mig.up_sql})
            continue

        try:
            with conn.cursor() as cur:
                cur.execute(mig.up_sql)
            conn.commit()
            record_migration(
                conn,
                version=mig.version,
                name=mig.name,
                checksum=mig.checksum,
                direction="up",
                status="success",
            )
            applied_versions.append(mig.version)
        except Exception as exc:
            conn.rollback()
            record_migration(
                conn,
                version=mig.version,
                name=mig.name,
                checksum=mig.checksum,
                direction="up",
                status="failed",
                error_message=str(exc)[:500],
            )
            print(json.dumps({"ok": False, "error": str(exc), "failed": mig.version}))
            return 1

    output = {
        "ok": True,
        "dry_run": dry_run,
        "planned": planned,
        "applied": applied_versions,
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
