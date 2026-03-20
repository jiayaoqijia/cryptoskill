# Table Discovery

Find and inspect Dune tables programmatically before writing SQL.

## Table of Contents
1. [Get Table Schema](#get-table-schema)
2. [Search Tables by Name](#search-tables-by-name)
3. [Search Tables by Contract Address](#search-tables-by-contract-address)
4. [Search Dune Documentation](#search-dune-documentation)
5. [List Schemas](#list-schemas)
6. [List User Uploads](#list-user-uploads)
7. [Common Discovery Patterns](#common-discovery-patterns)

---

## Get Table Schema

Inspect columns, types, and nullability of any table using its slug (e.g., `dex.trades`, `ethereum.transactions`).

```python
from dune_client.client import DuneClient
import os

client = DuneClient(api_key=os.environ['DUNE_API_KEY'])

# Get schema for a curated table
result = client.get_dataset("dex.trades")
print(f"Table: {result.full_name}")
print(f"Type: {result.type}")
for col in result.columns:
    print(f"  {col.name}: {col.type} (nullable={col.nullable})")
```

**Supported slugs:** Use `schema.table` format:
- Curated: `dex.trades`, `dex_aggregator.trades`, `dex_solana.trades`, `nft.trades`, `tokens.erc20`, `prices.usd`
- Raw: `ethereum.transactions`, `solana.transactions`, `polygon.logs`
- User uploads: `dune.<namespace>.dataset_<table_name>`

## Search Tables by Name

Use `information_schema.tables` via SQL to search for tables by keyword:

```python
# Search for tables containing a keyword
result = client.run_sql(
    query_sql="""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE CAST(table_schema AS VARCHAR) LIKE '%keyword%'
       OR CAST(table_name AS VARCHAR) LIKE '%keyword%'
    LIMIT 20
    """,
    performance='medium',
    ping_frequency=5
)
for row in result.result.rows:
    print(f"{row['table_schema']}.{row['table_name']}")
```

**⚠️ Notes:**
- `information_schema` queries consume credits (uses `run_sql`, Plus plan required)
- Cast columns to VARCHAR for LIKE comparisons
- Use specific filters to avoid scanning millions of decoded tables

### Targeted Search Examples

```python
# Find all event tables for a protocol on a specific chain
result = client.run_sql(
    query_sql="""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE CAST(table_schema AS VARCHAR) = 'uniswap_v3_ethereum'
      AND CAST(table_name AS VARCHAR) LIKE 'evt_%'
    LIMIT 50
    """,
    performance='medium',
    ping_frequency=5
)

# Find all tables related to a token/project
result = client.run_sql(
    query_sql="""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE CAST(table_name AS VARCHAR) LIKE '%swap%'
      AND CAST(table_schema AS VARCHAR) LIKE '%ethereum%'
    LIMIT 20
    """,
    performance='medium',
    ping_frequency=5
)
```

## Search Tables by Contract Address

Given a contract address, find all decoded event and call tables on Dune. Uses the `<chain>.contracts` table which stores decoded contract metadata (namespace, name, ABI).

**Supported chains:** ethereum, polygon, arbitrum, optimism, base, bnb, avalanche_c, gnosis, fantom, celo, zksync, scroll, linea, zora, blast, mantle, etc.

### Step 1: Check if contract is decoded

```python
# Check if a contract address has been decoded on a specific chain
result = client.run_sql(
    query_sql="""
    SELECT
        namespace,
        name,
        address,
        dynamic,
        factory,
        detection_source,
        created_at
    FROM ethereum.contracts
    WHERE address = 0xYOUR_CONTRACT_ADDRESS
    """,
    performance='medium',
    ping_frequency=5
)
for row in result.result.rows:
    print(f"Namespace: {row['namespace']}, Name: {row['name']}")
    print(f"Dynamic: {row['dynamic']}, Factory: {row['factory']}")
```

### Step 2: Find all decoded tables for that contract

Once you have the `namespace` from Step 1 (e.g., `uniswap_v3`), list all event/call tables:

```python
# Find all decoded tables for a namespace on a chain
namespace = "uniswap_v3"  # from Step 1
chain = "ethereum"

result = client.run_sql(
    query_sql=f"""
    SELECT table_name
    FROM information_schema.tables
    WHERE CAST(table_schema AS VARCHAR) = '{namespace}_{chain}'
    ORDER BY table_name
    LIMIT 100
    """,
    performance='medium',
    ping_frequency=5
)
for row in result.result.rows:
    table_name = row['table_name']
    table_type = "event" if table_name.startswith("evt_") else "call" if table_name.startswith("call_") else "other"
    print(f"  {namespace}_{chain}.{table_name} [{table_type}]")
```

### Auto-detect chain (search across all chains)

If you don't know which chain the contract is on:

```python
# Search across multiple chains for a contract address
chains = ['ethereum', 'polygon', 'arbitrum', 'optimism', 'base', 'bnb', 'avalanche_c', 'gnosis']
chain_list = ", ".join(f"'{c}'" for c in chains)

result = client.run_sql(
    query_sql=f"""
    SELECT * FROM (
        {'UNION ALL'.join(f"""
        SELECT '{chain}' as blockchain, namespace, name, address
        FROM {chain}.contracts
        WHERE address = 0xYOUR_CONTRACT_ADDRESS
        """ for chain in chains)}
    )
    """,
    performance='medium',
    ping_frequency=5
)
```

### One-shot: Contract address → all decoded tables

Complete pattern combining both steps:

```python
def find_tables_by_contract(client, contract_address, chain='ethereum'):
    """Find all decoded event/call tables for a contract address."""

    # Step 1: Get namespace from contracts table
    result = client.run_sql(
        query_sql=f"""
        SELECT DISTINCT namespace, name
        FROM {chain}.contracts
        WHERE address = {contract_address}
        """,
        performance='medium',
        ping_frequency=5
    )
    if not result.result.rows:
        print(f"Contract {contract_address} not decoded on {chain}")
        return []

    tables = []
    for row in result.result.rows:
        ns = row['namespace']
        contract_name = row['name']
        schema_name = f"{ns}_{chain}"

        # Step 2: List all tables in that schema
        tables_result = client.run_sql(
            query_sql=f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE CAST(table_schema AS VARCHAR) = '{schema_name}'
              AND (CAST(table_name AS VARCHAR) LIKE '%{contract_name}%'
                   OR CAST(table_name AS VARCHAR) LIKE 'evt_%'
                   OR CAST(table_name AS VARCHAR) LIKE 'call_%')
            ORDER BY table_name
            LIMIT 100
            """,
            performance='medium',
            ping_frequency=5
        )
        for t in tables_result.result.rows:
            tables.append(f"{schema_name}.{t['table_name']}")

    return tables

# Usage
tables = find_tables_by_contract(client, "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", "ethereum")
for t in tables:
    print(t)
```

**⚠️ Notes:**
- `<chain>.contracts` is a free-tier queryable table (no special permissions needed for `run_sql`)
- Contract addresses must be in `0x...` hex format (Dune auto-casts to `varbinary`)
- A single contract can appear in multiple namespaces (e.g., if the same bytecode is used by different protocols)
- `dynamic=true` means the contract was auto-detected via factory patterns, not manually submitted

---

## Search Dune Documentation

Search the Dune docs for guides, examples, SQL patterns, and API references. Useful when you need to understand a concept, find example queries, or look up API details.

### Method 1: Fetch the docs index

```python
import requests

# Get the complete documentation index
response = requests.get("https://docs.dune.com/llms.txt")
docs_index = response.text

# Search for relevant pages by keyword
keyword = "decoded"  # or "stablecoin", "dex", "nft", etc.
for line in docs_index.split('\n'):
    if keyword.lower() in line.lower():
        print(line)
```

### Method 2: Fetch a specific docs page

```python
# Once you find a relevant URL from the index, fetch its content
response = requests.get("https://docs.dune.com/data-catalog/evm/ethereum/decoded/overview")
# Parse the content for the information you need
```

### Common doc pages for quick reference

| Topic | URL |
|-------|-----|
| DuneSQL reference | `https://docs.dune.com/query-engine/DuneSQL-reference` |
| EVM decoded tables | `https://docs.dune.com/data-catalog/evm/ethereum/decoded/overview` |
| Curated DEX tables | `https://docs.dune.com/data-catalog/curated/trading/dex-trades` |
| Prices tables | `https://docs.dune.com/data-catalog/curated/prices/overview` |
| API authentication | `https://docs.dune.com/api-reference/overview/authentication` |
| API rate limits | `https://docs.dune.com/api-reference/overview/rate-limits` |
| API billing | `https://docs.dune.com/api-reference/overview/billing` |
| Materialized views | `https://docs.dune.com/api-reference/materialized-views/overview` |
| Query pipelines | `https://docs.dune.com/api-reference/pipelines/overview` |
| Data upload | `https://docs.dune.com/api-reference/upload/endpoint/upload-csv` |

### When to search docs

- **Before writing complex SQL** — check DuneSQL syntax (e.g., array functions, varbinary casting)
- **When encountering errors** — look up troubleshooting guides
- **For new features** — Dune frequently adds new tables, chains, and API endpoints
- **For billing questions** — understand credit costs before running expensive queries

**💡 Tip:** The full docs index at `https://docs.dune.com/llms.txt` is designed for LLM consumption and is the best starting point for any docs search.

---

## List Schemas

Find available schemas (protocol + chain namespaces):

```python
# List all schemas matching a keyword
result = client.run_sql(
    query_sql="SHOW SCHEMAS LIKE '%uniswap%'",
    performance='medium',
    ping_frequency=5
)
for row in result.result.rows:
    print(row['Schema'])
```

**Schema naming conventions:**
- Decoded tables: `<protocol>_<chain>` (e.g., `uniswap_v3_ethereum`, `aave_v3_polygon`)
- Raw tables: `<chain>` (e.g., `ethereum`, `solana`, `polygon`)
- Curated: `dex`, `dex_solana`, `nft`, `tokens`, `prices`, `labels`
- User uploads: `dune.<namespace>`

## List User Uploads

List tables uploaded via CSV or create_table API:

```python
result = client.list_uploads(limit=50)
for table in result.tables:
    print(f"{table.full_name} ({table.table_size_bytes} bytes)")
    for col in table.columns:
        print(f"  - {col.name}: {col.type}")
```

## Common Discovery Patterns

### 1. "What tables exist for protocol X on chain Y?"

```python
# Step 1: Find the schema
result = client.run_sql(
    query_sql="SHOW SCHEMAS LIKE '%aave%ethereum%'",
    performance='medium', ping_frequency=5
)
# → aave_v3_ethereum, aave_v2_ethereum, ...

# Step 2: List tables in that schema
result = client.run_sql(
    query_sql="""
    SELECT table_name FROM information_schema.tables
    WHERE CAST(table_schema AS VARCHAR) = 'aave_v3_ethereum'
    LIMIT 50
    """,
    performance='medium', ping_frequency=5
)

# Step 3: Inspect a specific table
schema = client.get_dataset("aave_v3_ethereum.evt_Supply")
```

### 2. "What columns does this table have?"

```python
result = client.get_dataset("dex_aggregator.trades")
for col in result.columns:
    print(f"{col.name}: {col.type}")
```

### 3. "What curated/spell tables are available?"

```python
result = client.list_datasets(type="spell", limit=250)
for ds in result.datasets:
    print(f"{ds.full_name}")
```

Available types: `spell`, `decoded_table`, `uploaded_table`, `transformation_view`, `transformation_table`, `dune_table`
