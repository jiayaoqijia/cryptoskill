# Solscan Batch Patterns — MCP vs Script Decision

## Decision tree

```
How many API calls do I need?
│
├── 1–10 (single wallet, one token, etc.)
│    → use MCP directly
│
├── 10–30 (multiple wallets, batch of transactions)
│    → look for multi-endpoint (50× CU savings)
│    → if no multi-endpoint, write async script
│
└── > 30 or repeated structure
     → ALWAYS script
     → check export endpoints for bulk history
```

## Why scripts beat MCP for batches

| Aspect | MCP loop | Async script |
|--------|----------|--------------|
| Parallelism | Serial (one at a time) | `semaphore=25` → 25 in flight |
| Rate usage | Wastes Tier 2's 1000/min allowance | Uses full budget |
| Context tokens | Every response eats conversation context | Only aggregated summary returned |
| Resume | Manual replay of failed items | Checkpoint file, skip done |
| Output | Interleaved with chat | Clean CSV/JSON file |
| Multi-endpoints | Not exposed via MCP | Direct HTTP → use them |

## Multi-endpoints (50× CU savings)

Whenever you need the same data shape for many items:

| Instead of loop | Use multi |
|-----------------|-----------|
| N × `transaction/detail` | `transaction/detail/multi` up to 50 sigs |
| N × `token/meta` | `token/meta/multi` up to 50 mints |
| N × `token/price` | `token/price/multi` up to 50 mints |
| N × `account/metadata` | `account/metadata/multi` up to 50 addrs |
| N × `transaction/decoded` | `transaction/decoded/multi` up to 50 sigs |

**Invocation (GET with array param):**
```python
params = [("tx", sig) for sig in signatures[:50]]
r = await session.get(f"{BASE}/transaction/detail/multi", params=params)
```

## Export endpoints (for bulk history) — SYNCHRONOUS CSV

Export endpoints return **CSV directly** in the response body (confirmed by live testing 2026-04-24). No polling, no job IDs.

| Use case | Export endpoint | Max rows | CU cost |
|----------|-----------------|----------|---------|
| Full wallet transfer history | `account/transfer/export` | 5000 | ~200-400 |
| Full wallet DeFi history | `account/defi/activities/export` | 5000 | ~200-400 |
| Stake rewards (tax/accounting) | `account/stake-rewards/export` | 5000 | ~200-400 |
| Full token defi activity | `token/defi/activities/export` | 5000 | ~200-400 |

**Use export when:**
- Needed rows > 500 (paginating past 500 rows with 100 CU each beats the export cost)
- < 5000 rows fit in one export (~15× cheaper than paginating the same)

**Workflow:**
```bash
curl -H "token: $KEY" "https://pro-api.solscan.io/v2.0/account/transfer/export?address=<addr>&from_time=<unix>&to_time=<unix>" -o output.csv
```

Result is a CSV with columns like:
`Signature,Block Time,Human Time,Action,From,To,Amount,Flow,Value,Decimals,Token Address`

**For longer periods (> 5000 rows total):** chunk by time window (e.g. 30-day slices), export each, concatenate. See `examples/export_full_history.py` — it auto-shrinks window on 5000-row cap.

## Async script template

```python
import asyncio, aiohttp, os, json
from typing import List

BASE = "https://pro-api.solscan.io/v2.0"
KEY = os.environ["SOLSCAN_API_KEY"]
SEMAPHORE = asyncio.Semaphore(25)

async def call(session, path, params):
    async with SEMAPHORE:
        for attempt in range(5):
            async with session.get(f"{BASE}{path}", params=params) as r:
                if r.status == 429:
                    await asyncio.sleep(2 ** attempt)
                    continue
                r.raise_for_status()
                return await r.json()
        raise RuntimeError(f"429 retries exceeded for {path}")

async def fetch_wallet_defi(session, wallet: str):
    all_rows, page = [], 1
    while True:
        data = await call(session, "/account/defi/activities", {
            "address": wallet, "page_size": 100, "page": page,
            "sort_by": "block_time", "sort_order": "desc",
        })
        rows = data.get("data", [])
        if not rows:
            break
        all_rows.extend(rows)
        page += 1
        if len(rows) < 100:
            break
    return wallet, all_rows

async def main(wallets: List[str], out_path: str):
    done = set()
    if os.path.exists(out_path):
        with open(out_path) as f:
            done = {json.loads(l)["wallet"] for l in f}
    todo = [w for w in wallets if w not in done]

    async with aiohttp.ClientSession(headers={"token": KEY}) as session:
        tasks = [fetch_wallet_defi(session, w) for w in todo]
        with open(out_path, "a") as f:
            for coro in asyncio.as_completed(tasks):
                wallet, rows = await coro
                f.write(json.dumps({"wallet": wallet, "rows": rows}) + "\n")
                print(f"✓ {wallet}: {len(rows)} rows")

if __name__ == "__main__":
    wallets = open("wallets.txt").read().strip().split("\n")
    asyncio.run(main(wallets, "defi_activities.jsonl"))
```

## Resume pattern (critical for long jobs)

Any script fetching > 100 items should:

1. Write output incrementally (JSONL or append-CSV), one line per processed item
2. On startup, read the output file and skip already-processed IDs
3. Never keep everything in memory — flush after each item

```python
# At start:
done = set()
if os.path.exists(out_path):
    with open(out_path) as f:
        done = {json.loads(l)["id"] for l in f}
todo = [x for x in all_items if x not in done]

# In loop:
with open(out_path, "a") as f:
    f.write(json.dumps({"id": item_id, "data": result}) + "\n")
```

## When NOT to use a script

- User wants a quick lookup ("what's this wallet holding right now?")
- Exploring data shape before committing to a batch
- Single-transaction debugging
- Formatting a final summary from already-collected data

In these cases MCP is faster — no file I/O, no setup.
