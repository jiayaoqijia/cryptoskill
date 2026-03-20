---
name: dune-analytics-api
version: 2.0.0
description: "Dune Analytics API skill for querying, analyzing, and uploading blockchain data. Use this skill whenever the user mentions Dune, on-chain data, blockchain analytics, token trading volume, DEX activity, wallet tracking, Solana/EVM transaction analysis, or wants to explore crypto data — even if they don't explicitly say 'Dune'. Also use for: running or creating Dune queries, finding blockchain tables and schemas, uploading CSV/NDJSON data to Dune, optimizing SQL for DuneSQL (Trino), checking token prices or trading pairs, analyzing wallet behavior, or any task involving dex.trades, decoded event logs, or raw blockchain transactions. Triggers on: Dune, blockchain data, on-chain, DEX trades, token volume, Solana transactions, wallet analysis, query optimization, data upload, table discovery, contract address lookup, crypto analytics, DuneSQL."
homepage: https://github.com/LZ-Web3/dune-analytics-api-skills
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins:
        - python3
      env:
        - DUNE_API_KEY
    primaryEnv: DUNE_API_KEY
    files:
      - "references/*"
      - "scripts/*"
---

# Dune Analytics API

A skill for querying and analyzing blockchain data via the [Dune Analytics](https://dune.com) API.

## Setup

```bash
pip install dune-client
```

Set `DUNE_API_KEY` via environment variable, `.env` file, or agent config.

## Best Practices

1. **Read references first** — The reference files contain critical table names, anti-patterns, and chain-specific gotchas that aren't obvious from table names alone. Reading the right reference before writing SQL prevents common mistakes like using `dex.trades` for wallet analysis (which inflates volume ~30%) or missing Solana's dedup requirement.

2. **Prefer private queries** — Creating queries with `is_private=True` keeps the user's workspace clean and avoids polluting the public Dune namespace. Fall back to public if it fails (free plan limitation), and let the user know.

3. **Reuse before creating** — Dune charges credits per execution. Reusing or updating an existing query avoids unnecessary duplicates and makes credit tracking easier. Only create new queries when the user explicitly asks.

4. **Confirm before updating** — Modifying an existing query's SQL is destructive (previous version isn't saved by default). A quick confirmation avoids overwriting work the user might want to keep.

5. **Track credits** — Each execution costs credits depending on the performance tier and data scanned. Reporting credits consumed helps the user manage their budget. See [query-execution.md](references/query-execution.md#credits-tracking).

## Scripts — Common Operations

For common operations, use the scripts in `scripts/` to avoid writing boilerplate code every time. All scripts read `DUNE_API_KEY` from the environment automatically.

| Script | Command | What it does |
|--------|---------|-------------|
| `dune_query.py` | `execute --query-id ID` | Execute a saved query (supports `--params`, `--performance`, `--format`) |
| `dune_query.py` | `get_latest --query-id ID` | Get cached result without re-execution |
| `dune_query.py` | `get_sql --query-id ID` | Print query SQL |
| `dune_query.py` | `update_sql --query-id ID --sql "..."` | Update query SQL |
| `dune_discover.py` | `search --keyword "uniswap"` | Search tables by keyword |
| `dune_discover.py` | `schema --table "dex.trades"` | Show table columns and types |
| `dune_discover.py` | `list_schemas --namespace "uniswap_v3"` | List tables in a namespace |
| `dune_discover.py` | `contract --address "0x..."` | Find decoded tables by contract address |
| `dune_discover.py` | `docs --keyword "dex"` | Search Dune documentation |
| `dune_upload.py` | `upload_csv --file data.csv --table-name tbl` | Quick CSV upload (overwrites) |
| `dune_upload.py` | `create_table --table-name tbl --namespace ns --schema '[...]'` | Create table with explicit schema |
| `dune_upload.py` | `insert --file data.csv --table-name tbl --namespace ns` | Append data to existing table |

**Example:**
```bash
# Execute query with parameters
python scripts/dune_query.py execute --query-id 123456 --params '{"token":"ETH"}' --format table

# Upload a CSV privately
python scripts/dune_upload.py upload_csv --file wallets.csv --table-name my_wallets --private
```

## Reference Selection

**Before writing any SQL, route to the correct reference file(s) based on your task:**

| Task involves... | Read this reference |
|-----------------|-------------------|
| Finding tables / inspecting schema / discovering protocols | [table-discovery.md](references/table-discovery.md) |
| Finding decoded tables by contract address | [table-discovery.md](references/table-discovery.md#search-tables-by-contract-address) |
| Searching Dune documentation / guides / examples | [table-discovery.md](references/table-discovery.md#search-dune-documentation) |
| Wallet / address tracking / router identification | [wallet-analysis.md](references/wallet-analysis.md) |
| Table selection / common table names | [common-tables.md](references/common-tables.md) |
| SQL performance / complex joins / array ops | [sql-optimization.md](references/sql-optimization.md) |
| API calls / execution / caching / parameters | [query-execution.md](references/query-execution.md) |
| Uploading CSV/NDJSON data to Dune | [data-upload.md](references/data-upload.md) |

If your task spans multiple categories, read **all** relevant files. The references contain critical details (e.g., specialized tables, anti-patterns) that aren't covered in this overview — guessing table names or query patterns leads to subtle bugs.

## Quick Start

```python
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import os

client = DuneClient(api_key=os.environ['DUNE_API_KEY'])

# Execute a query
result = client.run_query(query=QueryBase(query_id=123456), performance='medium', ping_frequency=5)
print(f"Rows: {len(result.result.rows)}")

# Get cached result (no re-execution)
result = client.get_latest_result(query_id=123456)

# Get/update SQL
sql = client.get_query(123456).sql
client.update_query(query_id=123456, query_sql="SELECT ...")

# Upload CSV data (quick, overwrites existing)
client.upload_csv(
    data="col1,col2\nval1,val2",
    description="My data",
    table_name="my_table",
    is_private=True
)

# Create table + insert (supports append)
client.create_table(
    namespace="my_user",
    table_name="my_table",
    schema=[{"name": "col1", "type": "varchar"}, {"name": "col2", "type": "double"}],
    is_private=True
)
import io
client.insert_data(
    namespace="my_user",
    table_name="my_table",
    data=io.BytesIO(b"col1,col2\nabc,1.5"),
    content_type="text/csv"
)
```

## Subscription Tiers

| Method | Description | Plan |
|--------|-------------|------|
| `run_query` | Execute saved query (supports `{{param}}`) | Free |
| `run_sql` | Execute SQL directly (no params) | Plus |

## Key Concepts

### dex.trades vs dex_aggregator.trades

| Table | Use Case | Volume |
|-------|----------|--------|
| `dex.trades` | Per-pool analysis | ⚠️ Inflated ~30% (multi-hop counted multiple times) |
| `dex_aggregator.trades` | User/wallet analysis | Accurate |

> **Why this matters:** If you're analyzing a specific wallet's trading activity and use `dex.trades`, you'll see inflated volume because a single swap through an aggregator gets split into multiple pool-level trades. `dex_aggregator.trades` captures the user-level intent — one row per user swap. See [wallet-analysis.md](references/wallet-analysis.md) for full patterns.

Solana has no `dex_aggregator_solana.trades`. Dedupe by `tx_id`:
```sql
SELECT tx_id, MAX(amount_usd) as amount_usd
FROM dex_solana.trades
GROUP BY tx_id
```

### Data Freshness

| Layer | Delay | Example |
|-------|-------|---------|
| Raw | < 1 min | `ethereum.transactions`, `solana.transactions` |
| Decoded | 15-60 sec | `uniswap_v3_ethereum.evt_Swap` |
| Curated | ~1 hour+ | `dex.trades`, `dex_solana.trades` |

Query previous day's data after **UTC 12:00** for completeness.

## References

Detailed documentation is organized in the `references/` directory:

| File | Description |
|------|-------------|
| [table-discovery.md](references/table-discovery.md) | Table discovery: search tables by name, inspect schema/columns, list schemas and uploads |
| [query-execution.md](references/query-execution.md) | API patterns: execute, update, cache, multi-day fetch, credits tracking, subqueries |
| [common-tables.md](references/common-tables.md) | Quick reference of commonly used tables: raw, decoded, curated, community data |
| [sql-optimization.md](references/sql-optimization.md) | SQL optimization: CTE, JOIN strategies, array ops, partition pruning |
| [wallet-analysis.md](references/wallet-analysis.md) | Wallet tracking: Solana/EVM queries, multi-chain aggregation, fee analysis |
| [data-upload.md](references/data-upload.md) | Data upload: CSV/NDJSON upload, create table, insert data, manage tables, credits |
