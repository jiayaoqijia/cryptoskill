#!/usr/bin/env python3
"""Migration utilities for database-migration-assistant.

Author: Apple
Version: 1.0.0
"""
from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

try:
    import psycopg2
    from psycopg2.extensions import connection as PGConnection
except Exception:
    psycopg2 = None
    PGConnection = object  # type: ignore

DIRECTION_RE = re.compile(r"^\s*--\s*DIRECTION:\s*(up|down)\s*$", re.IGNORECASE)
MIGRATION_RE = re.compile(r"^\s*--\s*MIGRATION:\s*(.+?)\s*$", re.IGNORECASE)


@dataclass
class MigrationFile:
    version: str
    name: str
    up_sql: str
    down_sql: Optional[str]
    checksum: str
    path: Path


def compute_checksum(sql_text: str) -> str:
    return hashlib.sha256(sql_text.encode("utf-8")).hexdigest()


def list_migration_files(migrations_dir: Path) -> List[Path]:
    if not migrations_dir.exists():
        return []
    files = [p for p in migrations_dir.iterdir() if p.is_file() and p.suffix.lower() == ".sql"]
    return sorted(files)


def parse_migration_file(path: Path) -> MigrationFile:
    text = path.read_text(encoding="utf-8")
    name = path.stem
    migration_name = None
    up_lines: List[str] = []
    down_lines: List[str] = []
    current = None

    for line in text.splitlines():
        m = MIGRATION_RE.match(line)
        if m:
            migration_name = m.group(1).strip()
            continue
        d = DIRECTION_RE.match(line)
        if d:
            current = d.group(1).lower()
            continue
        if current == "up":
            up_lines.append(line)
        elif current == "down":
            down_lines.append(line)

    up_sql = "\n".join(up_lines).strip()
    down_sql_text = "\n".join(down_lines).strip()
    down_sql = down_sql_text if down_sql_text else None

    return MigrationFile(
        version=name,
        name=migration_name or name,
        up_sql=up_sql,
        down_sql=down_sql,
        checksum=compute_checksum(text),
        path=path,
    )


def get_db_url() -> str:
    url = os.getenv("DB_URL")
    if not url:
        raise RuntimeError("DB_URL is required but not set.")
    return url


def get_db_connection() -> PGConnection:
    if psycopg2 is None:
        raise RuntimeError("psycopg2 is not installed. Install psycopg2-binary.")
    return psycopg2.connect(get_db_url())


def ensure_schema_table(conn: PGConnection) -> None:
    sql = """
    CREATE TABLE IF NOT EXISTS schema_migrations (
        id SERIAL PRIMARY KEY,
        version VARCHAR(64) NOT NULL,
        name TEXT NOT NULL,
        checksum TEXT NOT NULL,
        applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        direction VARCHAR(8) NOT NULL,
        status VARCHAR(16) NOT NULL,
        error_message TEXT
    );
    CREATE UNIQUE INDEX IF NOT EXISTS idx_schema_migrations_version_dir
        ON schema_migrations(version, direction)
        WHERE status = 'success';
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def get_applied_up_migrations(conn: PGConnection) -> List[dict]:
    sql = """
    SELECT version, name, checksum, applied_at
    FROM schema_migrations
    WHERE direction = 'up' AND status = 'success'
    ORDER BY applied_at ASC;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return [
        {"version": r[0], "name": r[1], "checksum": r[2], "applied_at": r[3]}
        for r in rows
    ]


def get_applied_up_migrations_desc(conn: PGConnection) -> List[dict]:
    sql = """
    SELECT version, name, checksum, applied_at
    FROM schema_migrations
    WHERE direction = 'up' AND status = 'success'
    ORDER BY applied_at DESC;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return [
        {"version": r[0], "name": r[1], "checksum": r[2], "applied_at": r[3]}
        for r in rows
    ]


def record_migration(
    conn: PGConnection,
    *,
    version: str,
    name: str,
    checksum: str,
    direction: str,
    status: str,
    error_message: Optional[str] = None,
) -> None:
    sql = """
    INSERT INTO schema_migrations (version, name, checksum, direction, status, error_message)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.execute(sql, (version, name, checksum, direction, status, error_message))
    conn.commit()
