# Data Upload (CSV/NDJSON)

Upload custom data to Dune as user-owned tables. Two approaches:

| Approach | Use Case | Append Support | Schema Control |
|----------|----------|----------------|----------------|
| `upload_csv` | Quick one-shot upload, auto schema inference | ❌ Overwrites | Auto-inferred |
| `create_table` + `insert_data` | Production pipelines, incremental loads | ✅ Append | Explicit schema |

## Setup

```python
from dune_client.client import DuneClient
import os

client = DuneClient(api_key=os.environ['DUNE_API_KEY'])
```

## Approach 1: Quick CSV Upload (upload_csv)

Simplest method. Uploads CSV string, auto-infers schema. **Overwrites** existing table data.

```python
# From CSV string
result = client.upload_csv(
    data="date,price\n2025-01-01,42000.5\n2025-01-02,43000.0",
    description="BTC daily prices",
    table_name="btc_prices",
    is_private=True
)
print(result.table_name)  # "dataset_btc_prices" (auto-prefixed with "dataset_")

# From CSV file
with open("data.csv") as f:
    result = client.upload_csv(
        data=f.read(),
        description="My dataset",
        table_name="my_data",
        is_private=True
    )
```

**⚠️ Notes:**
- Table name gets `dataset_` prefix automatically → query as `dune.<namespace>.dataset_<table_name>`
- Re-uploading to same name **overwrites** all existing data
- Schema is auto-inferred from CSV headers and values
- Max file size: 500MB per upload

## Approach 2: Create + Insert (Recommended for Production)

More control: define schema explicitly, supports **appending** data.

### Step 1: Create Table (once)

```python
result = client.create_table(
    namespace="my_namespace",       # Your Dune username or team name
    table_name="btc_prices",
    description="BTC daily prices",
    schema=[
        {"name": "date", "type": "timestamp"},
        {"name": "price", "type": "double", "nullable": True},
        {"name": "symbol", "type": "varchar", "nullable": False}
    ],
    is_private=True
)
print(result.full_name)       # "dune.my_namespace.btc_prices"
print(result.example_query)   # "select * from dune.my_namespace.btc_prices limit 10"
```

**Supported column types:** `varchar`, `integer`, `bigint`, `double`, `boolean`, `timestamp`, `varbinary`

### Step 2: Insert Data (repeatable, appends)

```python
import io

# From CSV bytes
csv_data = io.BytesIO(b"date,price,symbol\n2025-01-01T00:00:00Z,42000.5,BTC\n2025-01-02T00:00:00Z,43000.0,BTC")
result = client.insert_data(
    namespace="my_namespace",
    table_name="btc_prices",
    data=csv_data,
    content_type="text/csv"
)
print(f"Rows: {result.rows_written}, Bytes: {result.bytes_written}")

# From CSV file
with open("prices.csv", "rb") as f:
    result = client.insert_data(
        namespace="my_namespace",
        table_name="btc_prices",
        data=f,
        content_type="text/csv"
    )

# From NDJSON bytes
import json
rows = [
    {"date": "2025-01-01T00:00:00Z", "price": 42000.5, "symbol": "BTC"},
    {"date": "2025-01-02T00:00:00Z", "price": 43000.0, "symbol": "BTC"}
]
ndjson = "\n".join(json.dumps(r) for r in rows).encode()
result = client.insert_data(
    namespace="my_namespace",
    table_name="btc_prices",
    data=io.BytesIO(ndjson),
    content_type="application/x-ndjson"
)
```

**⚠️ Notes:**
- Data must conform to the table schema (same column names)
- Each insert **appends** to existing data
- Timestamps must be ISO 8601 format
- Varbinary: use hex (`0x...`) or base64 encoding
- Max request size: 1.2GB
- Concurrent inserts supported (keep under 5-10 for best performance)
- All-or-nothing: either all rows inserted, or none (safe to retry on error)

## Manage Tables

### List Uploaded Tables

```python
result = client.list_uploads(limit=10)
for table in result.tables:
    print(f"{table.full_name} ({table.table_size_bytes} bytes, private={table.is_private})")
    for col in table.columns:
        print(f"  - {col.name}: {col.type} (nullable={col.nullable})")
```

### Clear Table Data (keep schema)

```python
result = client.clear_table(
    namespace="my_namespace",
    table_name="btc_prices"
)
print(result.message)
```

### Delete Table (permanent)

```python
result = client.delete_table(
    namespace="my_namespace",
    table_name="btc_prices"
)
print(result.message)
```

## Complete Example: Upload DataFrame to Dune

```python
import pandas as pd
import io
from dune_client.client import DuneClient
import os

client = DuneClient(api_key=os.environ['DUNE_API_KEY'])

NAMESPACE = "my_namespace"
TABLE_NAME = "my_analysis"

# Prepare DataFrame
df = pd.DataFrame({
    "date": ["2025-01-01", "2025-01-02"],
    "wallet": ["0xabc...", "0xdef..."],
    "volume_usd": [1000.5, 2500.0]
})

# Method A: Quick upload (overwrites)
csv_str = df.to_csv(index=False)
client.upload_csv(
    data=csv_str,
    description="Wallet analysis results",
    table_name=TABLE_NAME,
    is_private=True
)
# Query as: SELECT * FROM dune.<namespace>.dataset_<table_name>

# Method B: Create + Insert (append-friendly)
client.create_table(
    namespace=NAMESPACE,
    table_name=TABLE_NAME,
    description="Wallet analysis results",
    schema=[
        {"name": "date", "type": "varchar"},
        {"name": "wallet", "type": "varchar"},
        {"name": "volume_usd", "type": "double"}
    ],
    is_private=True
)

csv_bytes = df.to_csv(index=False).encode()
client.insert_data(
    namespace=NAMESPACE,
    table_name=TABLE_NAME,
    data=io.BytesIO(csv_bytes),
    content_type="text/csv"
)
# Query as: SELECT * FROM dune.<namespace>.<table_name>
```

## Credits & Limits

| Action | Credits | Limits |
|--------|---------|--------|
| Create table | 10 credits | — |
| Upload CSV / Insert data | 3 credits per GB written (min 1) | 500MB per upload, 1.2GB per insert |
| List uploads | Free | — |
| Clear table | Free | — |
| Delete table | Free | — |
| **Storage** | — | Free: 100MB, Plus: 15GB, Enterprise: 200GB+ |

## Querying Uploaded Data

```sql
-- Tables created via create_table:
SELECT * FROM dune.<namespace>.<table_name>

-- Tables created via upload_csv (auto-prefixed):
SELECT * FROM dune.<namespace>.dataset_<table_name>

-- Join with on-chain data:
SELECT t.wallet, t.volume_usd, b.eth_balance
FROM dune.my_namespace.my_analysis t
LEFT JOIN ethereum.balances b ON t.wallet = b.address
```
