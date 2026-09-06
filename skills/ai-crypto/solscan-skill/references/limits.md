# Solscan Pro API — Limits, Quotas, Gotchas

## Tier 2 (user's plan) — exact numbers

Confirmed from live `monitor/usage` response and Solscan pricing screenshot (2026-04-24):

| Metric | Value |
|--------|-------|
| Price | $129.35/mo (discounted from $199) or $1,552.20/yr |
| Monthly CU quota | **150,000,000** |
| Rate limit | **1,000 requests per 60 seconds** |
| Reset cycle | Monthly (see `renew_date` in `monitor/usage`) |

## CU (Compute Unit) model

Most endpoints cost **100 CU per request** — flat rate after Nov 2025 unification.

**Exceptions observed in live testing:**
- `*/export` endpoints: **~200–400 CU** per request (depends on result size). Still vastly cheaper than paginating.
- Multi-endpoints: still 100 CU flat, returns up to 50 items — the 50× savings headline.

## Live rate limit monitoring — HTTP response headers

Every Solscan response includes these headers (use them in scripts to self-throttle):

```
ratelimit-limit: 1000            — per-minute max
ratelimit-remaining: 997         — remaining in current window
ratelimit-reset: 31              — seconds until window resets
cu-ratelimit-limit: 150000000    — monthly CU quota
cu-ratelimit-remaining: 148536190
cu-ratelimit-reset: 2080624      — seconds until monthly reset
```

**Best practice:** every script should read `ratelimit-remaining` and `cu-ratelimit-remaining`, log them, and back off when remaining drops below a safety threshold (e.g. 10% of limit).

## Monitor usage endpoint

`GET /v2.0/monitor/usage` (100 CU) returns:

```json
{
  "success": true,
  "data": {
    "renew_date": "2026-04-18T00:00:00.000Z",
    "end_date": "2026-05-18T00:00:00.000Z",
    "last_cu_reset_date": "2026-04-18T00:00:00.000Z",
    "remaining_cus": 148536490,
    "usage_cus": 1463510,
    "total_requests_24h": 650,
    "success_rate_24h": 99.69,
    "total_cu_24h": 64800
  }
}
```

Call at the start of any batch to check budget.

## Handling 429

```python
async def call_with_retry(session, url, params, max_retries=5):
    for attempt in range(max_retries):
        async with session.get(url, params=params) as r:
            if r.status == 429:
                reset = int(r.headers.get("ratelimit-reset", "30"))
                await asyncio.sleep(reset + 1)
                continue
            return await r.json()
    raise RuntimeError("Max retries exceeded")
```

Prefer reading `ratelimit-reset` from headers to the naive `2 ** attempt` — it's the exact seconds to wait.

## Recommended concurrency

- **semaphore=25** for regular endpoints — proven ~170 wallets/min throughput in production
- **semaphore=50** for multi-endpoints (less data per call)
- **semaphore=5-10** for exports (each is heavier)
- Drop semaphore if `ratelimit-remaining < 100`

At 1000/min and 25 concurrent → you use ~2.5s per request cycle, never spiking above limit.

## page_size — DISCRETE VALUES (differs by endpoint!)

Most endpoints: `10, 20, 30, 40, 60, 100`. **Always use 100 for batch.**

| Endpoint | Allowed page_size |
|----------|-------------------|
| `account/transfer` | 10, 20, 30, 40, 60, 100 |
| `account/defi/activities` | 10, 20, 30, 40, 60, 100 |
| `account/balance_change/activities` | 10, 20, 30, 40, 60, 100 |
| `account/transactions` | max **50** (not 100) |
| `token/transfer` | 10, 20, 30, 40, 60, 100 |
| `token/defi/activities` | 10, 20, 30, 40, 60, 100 |
| **`token/holders`** | **10, 20, 30, 40 only** — no 60/100 |
| `token/price` | 10, 20, 30, 40, 60, 100 |
| `nft/activities` | 10, 20, 30, 40, 60, 100 |

Using a disallowed value silently fails or errors 400. Hardcode to max allowed per endpoint.

## Export endpoint specifics

Export endpoints return **CSV directly** in the response body (not async jobs). Content-type may show `text/html` but body is CSV.

| Constraint | Value |
|------------|-------|
| Max items per export | **5,000 rows** |
| Documented limit "Max 1 req/min" | Not observed in Tier 2 practice — back-to-back requests succeed |
| CU cost per export | ~200–400 (size-dependent) |
| Output columns example (`transfer/export`) | `Signature,Block Time,Human Time,Action,From,To,Amount,Flow,Value,Decimals,Token Address` |

**When to use export vs pagination:**

| Scenario | Approach |
|----------|----------|
| < 500 rows needed | Paginate (1 call, 100 CU) |
| 500–5000 rows | Export (1 call, ~300 CU) — cheaper than 5 paginated calls (500 CU) |
| > 5000 rows | Split by time window, export each slice |

For wallets with years of history: chunk by month, export each slice, concatenate CSVs.

## Time range

All time params use **unix seconds** (`from_time`, `to_time`). Examples:
```python
now = int(time.time())
last_24h = now - 86400
last_7d  = now - 7 * 86400
last_30d = now - 30 * 86400
```

## Historical data depth

| Data type | How far back |
|-----------|--------------|
| Transfers (SPL & SOL) | 3 years (since July 2021) |
| Balance Change activities | 6 months |
| DeFi Activities | 6 months |
| Token price | From token's first trade (3-min delay on latest) |
| Token list | Top 2000 by market cap only |

Queries outside window return empty `data` silently — check `response.data` length, not just status.

## Address input limits

Many filter params accept **up to 5 comma-separated addresses**:
- `from`, `exclude_from`, `to`, `exclude_to` — max 5 each
- `token` — max 5 mints
- `platform`, `source` — max 5 program IDs

For > 5 addresses: split into separate calls.

## Batch endpoint limits

| Endpoint | Max items per call |
|----------|--------------------|
| `transaction/detail/multi` | 50 signatures |
| `transaction/decoded/multi` | 50 signatures |
| `token/meta/multi` | 50 mints |
| `token/price/multi` | 50 mints |
| `account/metadata/multi` | 50 addresses |

200 items → 4 multi calls (400 CU) vs 200 single calls (20,000 CU) = **50× cheaper**.

## Error codes quick reference

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad request (wrong param value, e.g. page_size=50) | Check params against endpoint spec |
| 401 | Bad/expired key | Check `SOLSCAN_API_KEY` |
| 403 | Endpoint not in your plan | Upgrade tier |
| 404 | Address/tx not found | Verify with `/search` |
| 429 | Rate limit hit | Sleep `ratelimit-reset` seconds |
| 500 | Server error | Retry once, then report to user |

Empty `data` array is not an error — no records in filter window.

## Sources

- https://docs.solscan.io/api-access/pro-api-endpoints
- https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-monitor-usage
- Live testing with user's Tier 2 key (2026-04-24)
- Solscan pricing page screenshot (Tier 2 = 150M CU, 1000 req/min, $129.35/mo)
