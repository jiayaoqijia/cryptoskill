# Custom SQL (Allium Explorer)

**Base URL:** `https://api.allium.so` · **Auth:** `X-API-KEY: $API_KEY` · **Rate limit:** 1 req/s

Use SQL when the typed endpoints don't cover what you need. Allium's data warehouse is the closest thing to "Dune-style queryable on-chain data" — useful for DeFi protocol analytics, NFT marketplace data, bridge flows, MEV, entity resolution, labeled wallets, and **Solana staking analytics**.

---

## Workflow

SQL queries are **async**: create → run → poll → fetch.

```
POST /explorer/queries                      ← one-time setup, returns query_id
POST /explorer/queries/{query_id}/run-async ← starts a run, returns run_id
GET  /explorer/query-runs/{run_id}/status   ← poll until status = success
GET  /explorer/query-runs/{run_id}/results  ← fetch rows
```

The `query_id` is created once and reused for many runs (with different `sql_query` parameters). Keep it in `~/.allium/credentials` as `QUERY_ID=...`.

---

## 1. Create a parametrized query (one-time)

If your `~/.allium/credentials` doesn't already have a `QUERY_ID`, create one:

```bash
curl -X POST "https://api.allium.so/api/v1/explorer/queries" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{
    "title": "Custom SQL Query",
    "config": {
      "sql": "{{ sql_query }}",
      "limit": 10000
    }
  }'
# Returns: {"query_id": "..."}
```

`{{ sql_query }}` is the placeholder substituted at runtime via `parameters.sql_query`. Append the returned id to `~/.allium/credentials`:

```bash
echo "QUERY_ID=<returned-id>" >> ~/.allium/credentials
```

---

## 2. Start a run

```bash
curl -X POST "https://api.allium.so/api/v1/explorer/queries/${QUERY_ID}/run-async" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"parameters": {"sql_query": "SELECT * FROM ethereum.raw.blocks ORDER BY block_number DESC LIMIT 10"}}'
# Returns: {"run_id": "..."}
```

---

## 3. Poll status

```bash
curl "https://api.allium.so/api/v1/explorer/query-runs/${RUN_ID}/status" \
  -H "X-API-KEY: $API_KEY"
```

Status progression: `created` → `queued` → `running` → `success` | `failed`

Poll with backoff (start at 1s, capped — respect the global 1 req/s rate limit).

---

## 4. Fetch results

Once status is `success`:

```bash
curl "https://api.allium.so/api/v1/explorer/query-runs/${RUN_ID}/results?f=json" \
  -H "X-API-KEY: $API_KEY"
```

`f=json` returns JSON; other formats may also be available — see Allium docs.

---

## Schema discovery

Before writing SQL against unfamiliar tables, discover what's available:

```bash
# Search schemas by keyword (e.g. "stake", "uniswap", "bridge")
curl "https://api.allium.so/api/v1/docs/schemas/search?q=stake" \
  -H "X-API-KEY: $API_KEY"

# Browse a schema's tables and columns
curl "https://api.allium.so/api/v1/docs/schemas/browse?schema=solana.dim" \
  -H "X-API-KEY: $API_KEY"

# Browse human-written docs
curl "https://api.allium.so/api/v1/docs/docs/browse?path=schemas/overview.md" \
  -H "X-API-KEY: $API_KEY"
```

---

## Example use cases

### Solana staking yield (per-epoch)

```sql
SELECT epoch, SUM(rewards) AS total_rewards
FROM solana.dim.stake_account_rewards
WHERE delegator = '<delegator-address>'
GROUP BY epoch
ORDER BY epoch DESC
LIMIT 30
```

### Uniswap v3 pool TVL over time

```sql
SELECT date, SUM(tvl_usd) AS total_tvl
FROM ethereum.dex.uniswap_v3_pool_stats_daily
WHERE pool = LOWER('<pool-address>')
GROUP BY date
ORDER BY date DESC
```

### Cross-chain bridge volume

```sql
SELECT bridge_name, source_chain, dest_chain, SUM(amount_usd) AS volume
FROM crosschain.bridge.transfers
WHERE block_time >= '2026-04-01'
GROUP BY bridge_name, source_chain, dest_chain
ORDER BY volume DESC
LIMIT 20
```

### Wallet entity resolution / labels

```sql
SELECT address, label, label_type, source
FROM crosschain.dim.address_labels
WHERE address = LOWER('<address>')
```

(Schema names are illustrative — use schema discovery above to find the exact tables for your use case.)

---

## Errors

| Status | Meaning | Fix |
| --- | --- | --- |
| 400 | Bad request | Check JSON syntax |
| 401 | Unauthorized | Check API key |
| 422 | Validation failed | Check request shape (common with `parameters` field) |
| 429 | Rate limited | Wait 1 second; no batching workaround |
| 500 | Server error | Retry with backoff |
