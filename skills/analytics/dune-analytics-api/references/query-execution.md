# Query Execution Patterns

## Setup

```bash
pip install dune-client
```

```python
from dune_client.client import DuneClient
import os

client = DuneClient(api_key=os.environ['DUNE_API_KEY'])
```

## Execute a Query

```python
from dune_client.query import QueryBase
from dune_client.types import QueryParameter

query = QueryBase(query_id=123456)

# With parameters
params = [QueryParameter.text_type(name='dt', value='2025-01-28')]

# Run and wait for result
result = client.run_query(query=query, performance='medium', ping_frequency=5)
print(f"Rows: {len(result.result.rows)}")
```

## Get Latest Cached Result (No Re-execution)

```python
result = client.get_latest_result(query_id=123456)
```

## Get Query SQL

```python
query = client.get_query(123456)
print(query.sql)
```

## Update Query SQL

```python
client.update_query(query_id=123456, query_sql="SELECT ...")
```

## Create a Query

```python
# ✅ Prefer private, fall back to public
try:
    query = client.create_query(
        name="My Query",
        query_sql=sql,
        params=params,
        is_private=True
    )
except Exception as e:
    # Private queries require a paid plan, fall back to public
    query = client.create_query(
        name="My Query",
        query_sql=sql,
        params=params,
        is_private=False
    )
    print("⚠️ Private query not available on your plan, created as public instead.")
```

## Run SQL Directly (Plus Plan Only)

Execute SQL without creating/saving a query.

```python
result = client.run_sql(
    query_sql="SELECT * FROM ethereum.transactions LIMIT 10",
    performance='medium',
    ping_frequency=5
)
print(f"Rows: {len(result.result.rows)}")
```

**⚠️ Notes:**
- `{{param}}` not supported — values must be hardcoded in SQL
- Best for ad-hoc testing and one-off queries

| Method | Requires Saved Query | Supports Parameters | Plan Required |
|--------|---------------------|-------------------|---------------|
| `run_query` | ✅ needs query_id | ✅ `{{param}}` | Free |
| `run_sql` | ❌ direct execution | ❌ not supported | Plus |

## Subqueries (Calling Other Queries)

**Wrap parameterized subquery calls in double quotes:**

```sql
-- ✅ Correct
SELECT * FROM "query_123456(dt='{{dt}}')"

-- ❌ Wrong: will error
SELECT * FROM query_123456(dt='{{dt}}')

-- ✅ No-param subqueries don't need quotes
SELECT * FROM query_123456
```

Union multiple subqueries:
```sql
SELECT * FROM "query_111111(dt='{{dt}}')"
UNION ALL
SELECT * FROM "query_222222(dt='{{dt}}')"
```

## Fetching Multi-Day Data

Many Dune queries use a `{{dt}}` parameter for single-day data. Loop through dates:

```python
from datetime import datetime, timedelta
import time

query_id = 123456
days = 3

today = datetime.now()
dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]

all_results = []
for date in dates:
    query = QueryBase(
        query_id=query_id,
        params=[QueryParameter.text_type(name='dt', value=date)]
    )
    result = client.run_query(query=query, performance='medium', ping_frequency=5)

    if result and result.result and result.result.rows:
        all_results.extend(result.result.rows)

    time.sleep(1)  # Rate limiting
```

**Key Points:**
- Check query SQL first with `client.get_query(query_id).sql` to identify parameters
- Each `run_query` takes 30-90 seconds depending on complexity
- Use `time.sleep(1)` between requests to avoid rate limiting
- Today's data may be empty if query depends on end-of-day aggregation
- For historical data, prefer previous days (data more complete after UTC 12:00)

## Credits Tracking

```python
def get_credits_used(client):
    """Get credits used in current billing period"""
    try:
        usage = client.get_usage()
        if usage and usage.billing_periods:
            return usage.billing_periods[0].credits_used
        return None
    except Exception as e:
        print(f"⚠️ Failed to get usage: {e}")
        return None

# Before execution
credits_before = get_credits_used(client)

# ... execute query ...

# After execution
credits_after = get_credits_used(client)
credits_consumed = credits_after - credits_before
print(f"💰 Credits consumed: {credits_consumed}")
```

**Reporting format:**
```
📊 Dune Credits consumed: X credits
   Before: YYYY | After: ZZZZ
```
