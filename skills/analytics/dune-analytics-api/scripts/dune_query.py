#!/usr/bin/env python3
"""Dune Analytics query execution and management.

Usage:
    python dune_query.py execute --query-id 123456 [--params '{"key":"value"}'] [--performance medium] [--format table]
    python dune_query.py get_latest --query-id 123456 [--format json]
    python dune_query.py get_sql --query-id 123456
    python dune_query.py update_sql --query-id 123456 --sql "SELECT ..."

Requires: pip install dune-client
Environment: DUNE_API_KEY must be set.
"""

import argparse
import json
import os
import sys
import csv
import io
from datetime import datetime

try:
    from dune_client.client import DuneClient
    from dune_client.query import QueryBase
    from dune_client.types import QueryParameter
except ImportError:
    print("Error: dune-client not installed. Run: pip install dune-client", file=sys.stderr)
    sys.exit(1)


def get_client() -> DuneClient:
    api_key = os.environ.get("DUNE_API_KEY")
    if not api_key:
        print("Error: DUNE_API_KEY environment variable not set.", file=sys.stderr)
        print("Set it with: export DUNE_API_KEY=your_key_here", file=sys.stderr)
        sys.exit(1)
    return DuneClient(api_key=api_key)


def format_rows(rows: list, fmt: str) -> str:
    """Format result rows as json, csv, or table."""
    if not rows:
        return "(no rows returned)"

    if fmt == "json":
        return json.dumps(rows, indent=2, default=str)

    if fmt == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        return output.getvalue()

    # table format
    if not rows:
        return "(empty)"
    headers = list(rows[0].keys())
    col_widths = {h: len(str(h)) for h in headers}
    for row in rows[:100]:  # limit display rows for table
        for h in headers:
            col_widths[h] = max(col_widths[h], len(str(row.get(h, ""))))

    # cap column width
    for h in headers:
        col_widths[h] = min(col_widths[h], 40)

    header_line = " | ".join(str(h).ljust(col_widths[h]) for h in headers)
    sep_line = "-+-".join("-" * col_widths[h] for h in headers)
    lines = [header_line, sep_line]
    for row in rows[:100]:
        line = " | ".join(str(row.get(h, "")).ljust(col_widths[h])[:col_widths[h]] for h in headers)
        lines.append(line)
    if len(rows) > 100:
        lines.append(f"... ({len(rows)} total rows, showing first 100)")
    return "\n".join(lines)


def parse_params(params_json: str) -> list:
    """Parse JSON params string into QueryParameter list."""
    if not params_json:
        return []
    try:
        params = json.loads(params_json)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON for --params: {e}", file=sys.stderr)
        sys.exit(1)

    query_params = []
    for key, value in params.items():
        query_params.append(QueryParameter.text_type(name=key, value=str(value)))
    return query_params


def cmd_execute(args):
    client = get_client()
    params = parse_params(args.params)
    query = QueryBase(query_id=args.query_id, params=params) if params else QueryBase(query_id=args.query_id)

    print(f"Executing query {args.query_id} (performance: {args.performance})...")
    start = datetime.now()

    try:
        result = client.run_query(
            query=query,
            performance=args.performance,
            ping_frequency=5,
        )
    except Exception as e:
        print(f"Error executing query: {e}", file=sys.stderr)
        sys.exit(1)

    elapsed = (datetime.now() - start).total_seconds()
    rows = result.result.rows if result.result else []

    print(f"\n{'='*60}")
    print(f"Query {args.query_id} completed in {elapsed:.1f}s")
    print(f"Rows returned: {len(rows)}")

    # Credits info from metadata if available
    if hasattr(result, "execution_id"):
        print(f"Execution ID: {result.execution_id}")
    if result.result and hasattr(result.result, "metadata"):
        meta = result.result.metadata
        if hasattr(meta, "total_row_count"):
            print(f"Total row count: {meta.total_row_count}")
        if hasattr(meta, "datapoint_count"):
            print(f"Datapoints: {meta.datapoint_count}")
    print(f"{'='*60}\n")

    print(format_rows(rows, args.format))


def cmd_get_latest(args):
    client = get_client()
    print(f"Fetching latest cached result for query {args.query_id}...")

    try:
        result = client.get_latest_result(query_id=args.query_id)
    except Exception as e:
        print(f"Error fetching results: {e}", file=sys.stderr)
        sys.exit(1)

    rows = result.result.rows if result.result else []
    print(f"Rows: {len(rows)}")
    if result.result and hasattr(result.result, "metadata"):
        meta = result.result.metadata
        if hasattr(meta, "execution_ended_at") and meta.execution_ended_at:
            print(f"Last executed: {meta.execution_ended_at}")
    print()
    print(format_rows(rows, args.format))


def cmd_get_sql(args):
    client = get_client()
    try:
        query_info = client.get_query(args.query_id)
    except Exception as e:
        print(f"Error fetching query: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"-- Query {args.query_id}: {getattr(query_info, 'name', 'N/A')}")
    print(f"-- Owner: {getattr(query_info, 'owner', 'N/A')}")
    print()
    print(query_info.sql)


def cmd_update_sql(args):
    client = get_client()
    if not args.sql:
        print("Error: --sql is required for update_sql", file=sys.stderr)
        sys.exit(1)

    try:
        client.update_query(query_id=args.query_id, query_sql=args.sql)
    except Exception as e:
        print(f"Error updating query: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Query {args.query_id} SQL updated successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Dune Analytics query execution and management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # execute
    p_exec = subparsers.add_parser("execute", help="Execute a saved query")
    p_exec.add_argument("--query-id", type=int, required=True, help="Dune query ID")
    p_exec.add_argument("--params", type=str, default=None, help='Query parameters as JSON: \'{"key":"value"}\'')
    p_exec.add_argument("--performance", type=str, default="medium", choices=["medium", "large"], help="Performance tier")
    p_exec.add_argument("--format", type=str, default="table", choices=["json", "csv", "table"], help="Output format")
    p_exec.set_defaults(func=cmd_execute)

    # get_latest
    p_latest = subparsers.add_parser("get_latest", help="Get cached result (no re-execution)")
    p_latest.add_argument("--query-id", type=int, required=True, help="Dune query ID")
    p_latest.add_argument("--format", type=str, default="table", choices=["json", "csv", "table"], help="Output format")
    p_latest.set_defaults(func=cmd_get_latest)

    # get_sql
    p_sql = subparsers.add_parser("get_sql", help="Get query SQL text")
    p_sql.add_argument("--query-id", type=int, required=True, help="Dune query ID")
    p_sql.set_defaults(func=cmd_get_sql)

    # update_sql
    p_update = subparsers.add_parser("update_sql", help="Update query SQL")
    p_update.add_argument("--query-id", type=int, required=True, help="Dune query ID")
    p_update.add_argument("--sql", type=str, required=True, help="New SQL text")
    p_update.set_defaults(func=cmd_update_sql)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
