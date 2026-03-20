# SQL Optimization Patterns for Dune

## Table of Contents
1. [CTE Optimization](#cte-optimization)
2. [JOIN Strategies](#join-strategies)
3. [Array Operations](#array-operations)
4. [Aggregation Patterns](#aggregation-patterns)
5. [Partition Pruning](#partition-pruning)

---

## CTE Optimization

### Merge CTEs to Reduce Nesting
```sql
-- ❌ Too many CTE layers
WITH step1 AS (...),
     step2 AS (SELECT * FROM step1 WHERE ...),
     step3 AS (SELECT * FROM step2 WHERE ...)
SELECT * FROM step3

-- ✅ Combine where possible
WITH combined AS (
  SELECT ... FROM base_table
  WHERE condition1 AND condition2
)
SELECT * FROM combined
```

### Materialize Heavy CTEs
For CTEs used multiple times, consider materializing:
```sql
WITH heavy_cte AS (
  SELECT /*+ MATERIALIZED */ ...
)
```

---

## JOIN Strategies

### Push Filters Before JOIN
```sql
-- ❌ Filter after JOIN (scans entire table)
SELECT * FROM big_table a
JOIN small_table b ON a.id = b.id
WHERE b.type = 'target'

-- ✅ Filter in subquery/CTE first
WITH filtered AS (
  SELECT * FROM small_table WHERE type = 'target'
)
SELECT * FROM big_table a
JOIN filtered b ON a.id = b.id
```

### Use Semi-JOIN for Existence Checks
```sql
-- ❌ Using IN with subquery
WHERE tx_id IN (SELECT tx_id FROM other_table)

-- ✅ Using EXISTS or JOIN
WHERE EXISTS (SELECT 1 FROM other_table o WHERE o.tx_id = t.tx_id)

-- Or INNER JOIN with DISTINCT
SELECT DISTINCT t.* FROM trades t
INNER JOIN other_table o ON t.tx_id = o.tx_id
```

### JOIN Order Matters
Place smaller/filtered tables first in JOIN chain.

---

## Array Operations

### Efficient Array Contains
```sql
-- For single value
CONTAINS(array_col, 'value')

-- For multiple values (check if ANY match)
cardinality(filter(array_col, x -> x IN ('v1','v2','v3'))) > 0

-- Using ANY_MATCH (cleaner)
ANY_MATCH(array_col, x -> x IN ('v1','v2','v3'))
```

### Avoid Double UNNEST
```sql
-- ❌ Creates cartesian product!
FROM table t, UNNEST(t.arr1) a1, UNNEST(t.arr2) a2

-- ✅ Process arrays separately or use FILTER
SELECT 
  FILTER(arr1, x -> condition) as filtered_arr1
FROM table
```

### Log Message Parsing
```sql
-- Extract order_id from "Program log: order_id: 12345"
REGEXP_EXTRACT(
  ARRAY_MIN(FILTER(log_messages, x -> x LIKE '%order_id:%')),
  'order_id: ([0-9]+)', 
  1
)

-- More efficient: check directly if order_id matches
ANY_MATCH(log_messages, x -> x LIKE '%order_id: 12345%')
```

---

## Aggregation Patterns

### Remove Constants from GROUP BY
```sql
-- ❌ Constants in GROUP BY (unnecessary)
SELECT 'solana' as chain, token, SUM(volume)
GROUP BY 1, 2

-- ✅ Only group by actual variables
SELECT 'solana' as chain, token, SUM(volume)
GROUP BY token  -- or GROUP BY 2
```

### Pre-aggregate Before JOIN
```sql
-- ❌ Aggregate after large JOIN
SELECT wallet, SUM(t.volume)
FROM huge_trades t
JOIN wallets w ON t.user = w.address
GROUP BY wallet

-- ✅ Aggregate first, then JOIN
WITH agg AS (
  SELECT user, SUM(volume) as total_volume
  FROM huge_trades
  GROUP BY user
)
SELECT w.wallet, a.total_volume
FROM agg a
JOIN wallets w ON a.user = w.address
```

### Use APPROX functions for large datasets
```sql
-- Exact (slow on large data)
COUNT(DISTINCT user)

-- Approximate (fast, ~2% error)
APPROX_DISTINCT(user)
```

---

## Partition Pruning

### Always Filter on Partition Columns
Most Dune tables are partitioned by date:
```sql
-- ✅ Uses partition pruning
WHERE block_date = DATE('2025-01-28')

-- ❌ No partition pruning (scans all)
WHERE DATE(block_time) = DATE('2025-01-28')

-- ✅ For ranges, be explicit
WHERE block_date >= DATE('2025-01-01') 
  AND block_date < DATE('2025-02-01')
```

### Common Partition Columns
- `block_date` - Most tables
- `block_month` - Some aggregated tables
- `evt_block_time` - Event tables

### Check Table Partitioning
```sql
SHOW CREATE TABLE dex_solana.trades
```
