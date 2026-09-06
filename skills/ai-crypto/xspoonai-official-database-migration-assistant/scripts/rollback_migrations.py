#!/usr/bin/env python3
"""Rollback applied migrations.

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
    get_applied_up_migrations_desc,
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
        "to_version": payload.get("to_version", args.to_version),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rollback migrations")
    parser.add_argument("--migrations-dir", default="migrations", help="Path to migrations directory")
    parser.add_argument("--to-version", help="Rollback migrations newer than this version")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    payload = _read_json_stdin()
    params = _merge_params(args, payload)

    migrations_dir = Path(params["migrations_dir"]).resolve()
    to_version = params.get("to_version")

    try:
        conn = get_db_connection()
        ensure_schema_table(conn)
        applied_desc = get_applied_up_migrations_desc(conn)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1

    if not applied_desc:
        print(json.dumps({"ok": True, "message": "No applied migrations to rollback", "rolled_back": []}, indent=2))
        return 0

    files = list_migration_files(migrations_dir)
    parsed = [parse_migration_file(p) for p in files]
    migrations_by_version = {m.version: m for m in parsed}

    if to_version:
        targets = [m for m in applied_desc if m["version"] > to_version]
    else:
        targets = applied_desc[:1]

    if not targets:
        print(json.dumps({"ok": True, "message": "No migrations to rollback for target", "rolled_back": []}, indent=2))
        return 0

    rolled_back = []

    for mig in targets:
        version = mig["version"]
        migration = migrations_by_version.get(version)
        if not migration:
            print(json.dumps({"ok": False, "error": f"Missing migration file for {version}"}))
            return 1
        if not migration.down_sql:
            print(json.dumps({"ok": False, "error": f"Missing down SQL for {version}"}))
            return 1

        try:
            with conn.cursor() as cur:
                cur.execute(migration.down_sql)
            conn.commit()
            record_migration(
                conn,
                version=version,
                name=migration.name,
                checksum=migration.checksum,
                direction="down",
                status="success",
            )
            rolled_back.append(version)
        except Exception as exc:
            conn.rollback()
            record_migration(
                conn,
                version=version,
                name=migration.name,
                checksum=migration.checksum,
                direction="down",
                status="failed",
                error_message=str(exc)[:500],
            )
            print(json.dumps({"ok": False, "error": str(exc), "failed": version}))
            return 1

    print(json.dumps({"ok": True, "rolled_back": rolled_back}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
