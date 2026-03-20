#!/usr/bin/env python3
"""Dune Analytics table discovery and schema inspection.

Usage:
    python dune_discover.py search --keyword "uniswap"
    python dune_discover.py schema --table "dex.trades"
    python dune_discover.py list_schemas --namespace "uniswap_v3"
    python dune_discover.py contract --address "0x1234..." [--chain ethereum]
    python dune_discover.py docs --keyword "dex trades"

Requires: pip install dune-client
Environment: DUNE_API_KEY must be set.
"""

import argparse
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


def cmd_search(args):
    """Search tables by keyword."""
    client = get_client()
    keyword = args.keyword

    print(f"Searching tables for '{keyword}'...")
    try:
        results = client.search_tables(keyword)
    except Exception as e:
        print(f"Error searching tables: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print(f"No tables found for '{keyword}'.")
        return

    print(f"\nFound {len(results)} table(s):\n")
    for t in results:
        schema = getattr(t, "schema_name", getattr(t, "namespace", "?"))
        name = getattr(t, "table_name", getattr(t, "name", "?"))
        full_name = getattr(t, "full_name", f"{schema}.{name}")
        desc = getattr(t, "description", "") or ""
        print(f"  📊 {full_name}")
        if desc:
            print(f"     {desc[:120]}")
        print()


def cmd_schema(args):
    """Get table schema (columns and types)."""
    client = get_client()
    table = args.table

    # Split table into namespace.table_name
    if "." in table:
        namespace, table_name = table.split(".", 1)
    else:
        print("Error: Table must be in format 'namespace.table_name' (e.g., 'dex.trades')", file=sys.stderr)
        sys.exit(1)

    print(f"Schema for {namespace}.{table_name}:\n")
    try:
        schema = client.get_table_schema(namespace=namespace, table_name=table_name)
    except Exception as e:
        print(f"Error fetching schema: {e}", file=sys.stderr)
        sys.exit(1)

    if not schema:
        print("No schema info returned.")
        return

    # Handle different response formats
    columns = schema if isinstance(schema, list) else getattr(schema, "columns", [])
    if not columns:
        print(f"Raw response: {schema}")
        return

    max_name_len = max(len(getattr(c, "name", str(c))) for c in columns) if columns else 10
    max_name_len = min(max_name_len, 40)

    print(f"  {'Column'.ljust(max_name_len)}  Type")
    print(f"  {'-'*max_name_len}  {'-'*20}")
    for col in columns:
        name = getattr(col, "name", str(col))
        col_type = getattr(col, "type", "?")
        nullable = getattr(col, "nullable", None)
        suffix = " (nullable)" if nullable else ""
        print(f"  {name.ljust(max_name_len)}  {col_type}{suffix}")

    print(f"\n  Total columns: {len(columns)}")


def cmd_list_schemas(args):
    """List all schemas/tables under a namespace."""
    client = get_client()
    namespace = args.namespace

    print(f"Listing schemas matching '{namespace}'...")
    try:
        results = client.search_tables(namespace)
    except Exception as e:
        print(f"Error listing schemas: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print(f"No schemas found for '{namespace}'.")
        return

    # Group by schema
    schemas = {}
    for t in results:
        schema = getattr(t, "schema_name", getattr(t, "namespace", "?"))
        name = getattr(t, "table_name", getattr(t, "name", "?"))
        schemas.setdefault(schema, []).append(name)

    for schema, tables in sorted(schemas.items()):
        print(f"\n📁 {schema} ({len(tables)} tables)")
        for tbl in sorted(tables):
            print(f"   └─ {tbl}")


def cmd_contract(args):
    """Find decoded tables by contract address."""
    client = get_client()
    address = args.address.lower()
    chain = args.chain

    print(f"Searching decoded tables for contract {address}...")
    if chain:
        print(f"Chain filter: {chain}")

    # Use the search endpoint to find contract-related tables
    # Try searching with the address (Dune may index by contract)
    try:
        # First try direct table search
        results = client.search_tables(address)
    except Exception as e:
        print(f"Error searching: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        # Suggest alternative approach
        print(f"\nNo tables directly indexed for {address}.")
        print("\nTry this SQL approach to find decoded tables:")
        print(f"""
  SELECT
    namespace,
    name,
    schema_name
  FROM information_schema.tables
  WHERE namespace LIKE '%{address[:10]}%'
  LIMIT 20;
""")
        print("Or check if the contract is decoded on Dune's website:")
        print(f"  https://dune.com/contracts/{chain or 'ethereum'}/{address}")
        return

    print(f"\nFound {len(results)} table(s):\n")
    for t in results:
        schema = getattr(t, "schema_name", getattr(t, "namespace", "?"))
        name = getattr(t, "table_name", getattr(t, "name", "?"))
        full_name = getattr(t, "full_name", f"{schema}.{name}")
        print(f"  📊 {full_name}")


def cmd_docs(args):
    """Search Dune documentation."""
    client = get_client()
    keyword = args.keyword

    print(f"Searching Dune docs for '{keyword}'...\n")

    # Common doc URLs for quick reference
    doc_map = {
        "dex": "https://docs.dune.com/data-catalog/curated/trading/dex-trades",
        "trades": "https://docs.dune.com/data-catalog/curated/trading/dex-trades",
        "erc20": "https://docs.dune.com/data-catalog/curated/balances/erc20-balances",
        "nft": "https://docs.dune.com/data-catalog/curated/nft/nft-trades",
        "prices": "https://docs.dune.com/data-catalog/curated/financial/prices",
        "solana": "https://docs.dune.com/data-catalog/chains/solana",
        "ethereum": "https://docs.dune.com/data-catalog/chains/ethereum",
        "upload": "https://docs.dune.com/api-reference/upload",
        "api": "https://docs.dune.com/api-reference/overview",
        "sql": "https://docs.dune.com/query-engine/Functions-and-operators",
        "trino": "https://docs.dune.com/query-engine/overview",
        "dunesql": "https://docs.dune.com/query-engine/overview",
    }

    # Find matching docs
    kw_lower = keyword.lower()
    matches = []
    for key, url in doc_map.items():
        if key in kw_lower or kw_lower in key:
            matches.append((key, url))

    if matches:
        print("📖 Relevant documentation pages:")
        for key, url in matches:
            print(f"  • {key}: {url}")
    else:
        print("No exact match in quick reference. Try these starting points:")
        print(f"  • Docs home: https://docs.dune.com")
        print(f"  • Data catalog: https://docs.dune.com/data-catalog")
        print(f"  • API reference: https://docs.dune.com/api-reference")

    # Also try the API's doc search if available
    print(f"\n💡 For comprehensive search, try fetching:")
    print(f"   https://docs.dune.com/api/search?query={keyword.replace(' ', '+')}")


def main():
    parser = argparse.ArgumentParser(
        description="Dune Analytics table discovery and schema inspection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = subparsers.add_parser("search", help="Search tables by keyword")
    p_search.add_argument("--keyword", type=str, required=True, help="Search keyword")
    p_search.set_defaults(func=cmd_search)

    # schema
    p_schema = subparsers.add_parser("schema", help="Get table schema (columns and types)")
    p_schema.add_argument("--table", type=str, required=True, help="Table name (e.g., dex.trades)")
    p_schema.set_defaults(func=cmd_schema)

    # list_schemas
    p_list = subparsers.add_parser("list_schemas", help="List tables in a namespace")
    p_list.add_argument("--namespace", type=str, required=True, help="Namespace to search (e.g., uniswap_v3)")
    p_list.set_defaults(func=cmd_list_schemas)

    # contract
    p_contract = subparsers.add_parser("contract", help="Find decoded tables by contract address")
    p_contract.add_argument("--address", type=str, required=True, help="Contract address")
    p_contract.add_argument("--chain", type=str, default=None, help="Chain name (e.g., ethereum, base, solana)")
    p_contract.set_defaults(func=cmd_contract)

    # docs
    p_docs = subparsers.add_parser("docs", help="Search Dune documentation")
    p_docs.add_argument("--keyword", type=str, required=True, help="Search keyword")
    p_docs.set_defaults(func=cmd_docs)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
