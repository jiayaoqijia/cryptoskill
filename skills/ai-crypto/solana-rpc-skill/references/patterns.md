# Solana RPC — Patterns & Optimization

## 1. JSON-RPC batching (THE #1 credit saver)

Standard JSON-RPC supports array requests: send multiple methods in **one HTTP request**, get array of responses back.

```python
import httpx

def batch_get_tx(signatures: list[str], rpc_url: str) -> list:
    body = [
        {
            "jsonrpc": "2.0",
            "id": i,
            "method": "getTransaction",
            "params": [sig, {
                "encoding": "jsonParsed",
                "maxSupportedTransactionVersion": 0,
                "commitment": "confirmed",
            }],
        }
        for i, sig in enumerate(signatures)
    ]
    r = httpx.post(rpc_url, json=body, timeout=60)
    r.raise_for_status()
    return [item["result"] for item in r.json()]
```

Typical max batch size: **100 items** (provider-dependent, some allow 250). Break larger jobs into chunks.

Benefit: 100 txs in 1 HTTP round-trip instead of 100. Same credit count, drastically less latency.

## 2. Async batching with semaphore

For many batches in parallel:

```python
import asyncio, aiohttp

SEMAPHORE = asyncio.Semaphore(20)  # tune per provider

async def post_batch(session, rpc_url, body):
    async with SEMAPHORE:
        async with session.post(rpc_url, json=body) as r:
            r.raise_for_status()
            return await r.json()
```

Tuning:
- **Helius Business**: `semaphore=15-20` (200 rps / 10 per batch = 20 concurrent safe)
- **Helius Professional**: `semaphore=30-50`
- **QuickNode Build**: `semaphore=10`
- **Helius Free / public RPC**: `semaphore=2-3`

If 429: drop semaphore by 50%, respect `Retry-After` header if present.

## 3. Prefer batch endpoints over looped individual

| Looping (DON'T) | Batch (DO) |
|-----------------|------------|
| N × `getAccountInfo` | 1 × `getMultipleAccounts` (up to 100) |
| N × `getTransaction` | 1 JSON-RPC batch with N items |
| N × `getSignatureStatuses(sig)` | 1 × `getSignatureStatuses([sig,...])` (up to 256) |
| N × `getTokenAccountBalance` | 1 × `getMultipleAccounts` with filter + parse |
| N × `getTokenAccountsByOwner(owner)` | 1 × DAS `getAssetsByOwner` (all owners in one call via pagination) |

## 4. When to use raw RPC vs enhanced/parsed

| Task | Pick |
|------|------|
| Need exact lamports / raw instructions | Raw RPC |
| Need "what happened" human-readable | **Helius Enhanced Tx** or Solscan |
| Wallet holdings with metadata | **Helius/QN DAS `getAssetsByOwner`** |
| NFT collection listing | **DAS `getAssetsByGroup`** |
| Historical single tx | Raw `getTransaction` (3× faster than Solscan for raw data) |
| DeFi swap details parsed | **Helius Enhanced Tx** — raw RPC doesn't know protocols |
| Priority fee for submission | `getPriorityFeeEstimate` (Helius) or `qn_estimatePriorityFees` (QN) |

## 5. Resume / checkpoint pattern

Long jobs (> 1000 calls) MUST have resume support. Pattern:

```python
import json, os

def load_done(path):
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                try: done.add(json.loads(line)["id"])
                except: pass
    return done

def save_result(path, id, data):
    with open(path, "a") as f:
        f.write(json.dumps({"id": id, "data": data}) + "\n")
        f.flush()
```

On startup: `todo = [x for x in all_items if x not in load_done(out_path)]`.

## 6. Handling common edge cases

### "Slot skipped" (error -32009 on `getBlock`)
```python
try:
    block = rpc.getBlock(slot, ...)
except RpcError as e:
    if e.code == -32009:
        return None   # silently skip, move on
    raise
```
Solana has gaps where slots weren't produced. Always handle.

### Transaction version errors (`-32602` "not supported")
Always include `maxSupportedTransactionVersion: 0` in config. Most modern txs are v0.

### Large `getBlock` responses
```python
block = rpc.getBlock(slot, {
    "encoding": "jsonParsed",
    "maxSupportedTransactionVersion": 0,
    "transactionDetails": "signatures",  # tiny payload
    "rewards": False,
})
```
Then fetch specific txs with `getTransaction` individually (batched).

### Cursor pagination on `getSignaturesForAddress`
Empty response = end. Don't stop on less-than-1000 — continue until empty:
```python
while True:
    sigs = rpc.getSignaturesForAddress(addr, {"limit": 1000, "before": before})
    if not sigs: break
    all_sigs.extend(sigs)
    before = sigs[-1]["signature"]
```

## 7. Rate limits & backoff

Most providers return `429` with `Retry-After` header. Respect it:

```python
async def call_with_retry(session, url, body, max_retries=5):
    for attempt in range(max_retries):
        async with session.post(url, json=body) as r:
            if r.status == 429:
                retry = int(r.headers.get("Retry-After", 2 ** attempt))
                await asyncio.sleep(retry)
                continue
            r.raise_for_status()
            return await r.json()
    raise RuntimeError("Max retries")
```

For Helius: `X-Credits-Used` and `X-Credits-Remaining` headers. Stop batches if remaining drops below threshold.

## 8. Multi-provider fallback

If user has multiple endpoints configured:

```python
PRIMARY = os.environ.get("SOLANA_RPC_URL_PRIMARY") or os.environ["SOLANA_RPC_URL"]
FALLBACK = os.environ.get("SOLANA_RPC_URL_FALLBACK")

async def call_with_fallback(session, body):
    try:
        return await call_with_retry(session, PRIMARY, body)
    except (HTTPError, TimeoutError):
        if FALLBACK:
            return await call_with_retry(session, FALLBACK, body)
        raise
```

Useful patterns:
- PRIMARY = Helius, FALLBACK = QuickNode (or public RPC as last resort)
- Split by workload: DAS calls → Helius, standard RPC → QuickNode

## 9. Cost estimation heuristics

Roughly (varies by provider):
- `getAccountInfo`, `getBalance`, small read: 1 credit
- `getTransaction`, `getBlock` (signatures only): 1-3 credits
- `getBlock` full: 5-10 credits
- `getProgramAccounts` without filter: **ENORMOUS** (often timeouts) — avoid
- DAS `getAsset` / `getAssetsByOwner`: 5-10 credits
- Enhanced Tx (parsed): 5 credits
- `getPriorityFeeEstimate`: 1-2 credits
- WebSocket subscriptions: 0.1-1 credit per message (or flat)

Helius credit monitoring: `X-Credits-Remaining` header after every call.
QuickNode: RPS limit, not credit — watch for 429.

## 10. When to write a script vs. direct call

Same rule as other skills:
- 1-10 individual calls → inline `curl` / `httpx`
- 10-100 → Python script with JSON-RPC batching
- 100+ → async script with semaphore, resume, checkpoint file

Never `for x in items: rpc.getTransaction(x)` — always batch.
