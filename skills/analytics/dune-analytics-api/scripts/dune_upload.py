#!/usr/bin/env python3
"""Dune Analytics data upload utility.

Usage:
    python dune_upload.py upload_csv --file data.csv --table-name my_table [--namespace my_user] [--private]
    python dune_upload.py create_table --table-name my_table --namespace my_user --schema '[{"name":"col1","type":"varchar"}]' [--private]
    python dune_upload.py insert --file data.csv --table-name my_table --namespace my_user

Requires: pip install dune-client
Environment: DUNE_API_KEY must be set.
"""

import argparse
import io
import json
import os
import sys

try:
    from dune_client.client import DuneClient
except ImportError:
    print("Error: dune-client not installed. Run: pip install dune-client", file=sys.stderr)
    sys.exit(1)


def get_client() -> DuneClient:
    api_key = os.environ.get("DUNE_API_KEY")
    if not api_key:
        print("Error: DUNE_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return DuneClient(api_key=api_key)


def read_file(path: str) -> str:
    """Read file contents, with size check."""
    if not os.path.exists(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(path) / (1024 * 1024)
    if size_mb > 200:
        print(f"Error: File is {size_mb:.1f}MB. Dune upload limit is 200MB.", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {path} ({size_mb:.2f}MB)...")
    with open(path, "r") as f:
        return f.read()


def detect_content_type(path: str) -> str:
    """Detect content type from file extension."""
    if path.endswith(".csv"):
        return "text/csv"
    elif path.endswith(".json") or path.endswith(".ndjson"):
        return "application/x-ndjson"
    else:
        print(f"Warning: Unknown file type for '{path}', assuming CSV.", file=sys.stderr)
        return "text/csv"


def cmd_upload_csv(args):
    """Quick CSV upload (overwrites existing table data)."""
    client = get_client()
    data = read_file(args.file)

    # Count rows for summary
    lines = data.strip().split("\n")
    row_count = len(lines) - 1  # minus header

    print(f"Uploading {row_count} rows to table '{args.table_name}'...")
    if args.private:
        print("  Mode: private")

    try:
        result = client.upload_csv(
            data=data,
            description=args.description or f"Uploaded from {os.path.basename(args.file)}",
            table_name=args.table_name,
            is_private=args.private,
        )
    except Exception as e:
        print(f"Error uploading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n✅ Upload successful!")
    print(f"   Table: {result if isinstance(result, str) else 'created/updated'}")
    print(f"   Rows: {row_count}")
    print(f"\n💡 Reference in SQL as: dune.{args.namespace or 'your_user'}.dataset_{args.table_name}")


def cmd_create_table(args):
    """Create a new table with explicit schema."""
    client = get_client()

    try:
        schema = json.loads(args.schema)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON for --schema: {e}", file=sys.stderr)
        print('Example: --schema \'[{"name":"address","type":"varchar"},{"name":"amount","type":"double"}]\'', file=sys.stderr)
        sys.exit(1)

    print(f"Creating table '{args.namespace}.{args.table_name}'...")
    print(f"  Columns: {len(schema)}")
    for col in schema:
        print(f"    - {col['name']}: {col['type']}")
    if args.private:
        print("  Mode: private")

    try:
        result = client.create_table(
            namespace=args.namespace,
            table_name=args.table_name,
            schema=schema,
            is_private=args.private,
            description=args.description or "",
        )
    except Exception as e:
        print(f"Error creating table: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n✅ Table created successfully!")
    print(f"   Full name: dune.{args.namespace}.{args.table_name}")
    print(f"\n💡 Now insert data with:")
    print(f"   python dune_upload.py insert --file data.csv --table-name {args.table_name} --namespace {args.namespace}")


def cmd_insert(args):
    """Insert/append data to an existing table."""
    client = get_client()
    content = read_file(args.file)
    content_type = detect_content_type(args.file)

    lines = content.strip().split("\n")
    row_count = len(lines) - 1 if content_type == "text/csv" else len(lines)

    print(f"Inserting {row_count} rows into '{args.namespace}.{args.table_name}'...")
    print(f"  Content type: {content_type}")

    try:
        result = client.insert_data(
            namespace=args.namespace,
            table_name=args.table_name,
            data=io.BytesIO(content.encode("utf-8")),
            content_type=content_type,
        )
    except Exception as e:
        print(f"Error inserting data: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n✅ Data inserted successfully!")
    print(f"   Rows appended: {row_count}")
    print(f"   Table: dune.{args.namespace}.{args.table_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Dune Analytics data upload utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # upload_csv
    p_upload = subparsers.add_parser("upload_csv", help="Quick CSV upload (overwrites)")
    p_upload.add_argument("--file", type=str, required=True, help="Path to CSV file")
    p_upload.add_argument("--table-name", type=str, required=True, help="Target table name")
    p_upload.add_argument("--namespace", type=str, default=None, help="Dune namespace/username")
    p_upload.add_argument("--description", type=str, default=None, help="Table description")
    p_upload.add_argument("--private", action="store_true", default=True, help="Make table private (default: True)")
    p_upload.add_argument("--public", action="store_true", help="Make table public")
    p_upload.set_defaults(func=cmd_upload_csv)

    # create_table
    p_create = subparsers.add_parser("create_table", help="Create table with explicit schema")
    p_create.add_argument("--table-name", type=str, required=True, help="Table name")
    p_create.add_argument("--namespace", type=str, required=True, help="Dune namespace/username")
    p_create.add_argument("--schema", type=str, required=True, help='Schema JSON: \'[{"name":"col","type":"varchar"}]\'')
    p_create.add_argument("--description", type=str, default=None, help="Table description")
    p_create.add_argument("--private", action="store_true", default=True, help="Make table private (default: True)")
    p_create.add_argument("--public", action="store_true", help="Make table public")
    p_create.set_defaults(func=cmd_create_table)

    # insert
    p_insert = subparsers.add_parser("insert", help="Insert/append data to existing table")
    p_insert.add_argument("--file", type=str, required=True, help="Path to CSV/NDJSON file")
    p_insert.add_argument("--table-name", type=str, required=True, help="Target table name")
    p_insert.add_argument("--namespace", type=str, required=True, help="Dune namespace/username")
    p_insert.set_defaults(func=cmd_insert)

    args = parser.parse_args()

    # Handle --public flag
    if hasattr(args, "public") and args.public:
        args.private = False

    args.func(args)


if __name__ == "__main__":
    main()
