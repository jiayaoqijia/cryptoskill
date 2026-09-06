---
name: solana-rpc
description: |
  Expert assistant for Solana JSON-RPC — works with any provider: QuickNode, Helius,
  Triton, Ankr, Chainstack, or public endpoints. Standard JSON-RPC methods are identical
  across providers; only the URL differs.

  Use whenever the user wants raw Solana data: fetch transactions by signature, read account
  state, get block data, check SPL token balances, query program accounts, submit transactions,
  estimate priority fees, or do anything requiring direct Solana node access.

  Also use when the user mentions Helius/QuickNode specifically, or wants Helius-specific
  features (DAS API, Enhanced Transactions, LaserStream, Webhooks) or QuickNode addons
  (qn_estimatePriorityFees, Metaplex DAS, Jito bundles).

  Enforces: batch JSON-RPC requests over loops, prefer DAS/Enhanced APIs over raw RPC
  when available, never use `getProgramAccounts` without tight filters.
compatibility:
  tools:
    - Bash
    - Write
    - Read
---

# Solana RPC Skill

Reference files:
- `references/core-methods.md` — standard Solana JSON-RPC methods, parameters, response shapes
- `references/helius-extensions.md` — DAS API, Enhanced Transactions, Priority Fee, Sender, LaserStream
- `references/quicknode-extensions.md` — `qn_estimatePriorityFees`, Metaplex DAS addon, Jito
- `references/patterns.md` — batching, rate limits, resume, cost optimization
- `references/examples/` — working Python scripts

---

## 🚨 Rule #1: use the provider's parsed/enhanced APIs when available

The biggest credit waste on Solana RPC is fetching raw data and parsing it yourself when the provider offers a parsed endpoint. Matrix:

| Task | Cheap option | Expensive / broken option |
|------|--------------|---------------------------|
| Wallet NFTs + tokens | **Helius DAS `getAssetsByOwner`** | `getTokenAccountsByOwner` + metadata lookups |
| Complete tx history | **Helius `getTransactionsForAddress`** | `getSignaturesForAddress` + N × `getTransaction` |
| Parsed DEX swap details | **Helius Enhanced Tx** or Solscan | `getTransaction` + manual program parsing |
| NFTs by collection | **DAS `getAssetsByGroup` / `searchAssets`** | `getProgramAccounts` (expensive + slow) |
| Priority fee estimate | **`getPriorityFeeEstimate` (Helius)** or `qn_estimatePriorityFees` (QuickNode) | `getRecentPrioritizationFees` (raw, needs math) |
| Compressed NFT history | **DAS `getSignaturesForAsset`** | `getSignaturesForAddress` (doesn't work for cNFTs) |

When in doubt: check `references/helius-extensions.md` first — if Helius has a purpose-built endpoint, use it.

## 🚨 Rule #2: batch JSON-RPC requests

**Single HTTP request can carry an array of JSON-RPC calls:**

```json
[
  {"jsonrpc":"2.0","id":1,"method":"getTransaction","params":["sig1",{"encoding":"jsonParsed","maxSupportedTransactionVersion":0}]},
  {"jsonrpc":"2.0","id":2,"method":"getTransaction","params":["sig2",{"encoding":"jsonParsed","maxSupportedTransactionVersion":0}]},
  ...up to ~100 items
]
```

Response is an array. Most providers count each call individually but save massive HTTP overhead. **Always batch when fetching N items of same shape.**

See `references/patterns.md` for semaphore tuning and provider-specific batch limits.

## 🚨 Rule #3: never `getProgramAccounts` without tight filters

`getProgramAccounts` scans ALL accounts under a program. On popular programs (SPL Token, Token 2022, NFT programs) it's catastrophically slow and expensive, often times out.

**Always apply:**
- `dataSize` filter (exact byte length)
- `memcmp` filter (matches at specific offset) — typically for mint address, owner, or discriminator

If you're querying NFTs or tokens by collection/owner: **use DAS instead** (`getAssetsByGroup`, `getAssetsByOwner`).

---

## Setup: provider URL

All Solana RPC calls need a URL. Configure via env var:

```bash
# Helius
export SOLANA_RPC_URL="https://mainnet.helius-rpc.com/?api-key=YOUR_KEY"

# QuickNode
export SOLANA_RPC_URL="https://YOUR-ENDPOINT.solana-mainnet.quiknode.pro/YOUR-TOKEN/"

# Ankr
export SOLANA_RPC_URL="https://rpc.ankr.com/solana/YOUR_KEY"

# Public (DON'T use for production)
export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"
```

Scripts read from `SOLANA_RPC_URL`. Never hardcode. If user has separate endpoints for archive vs. frontend (common on QuickNode), support `SOLANA_RPC_URL_ARCHIVE` additionally.

## Multi-provider fallback (optional)

If user has both Helius and QuickNode, you can configure fallback:
- `SOLANA_RPC_URL_PRIMARY` — first choice
- `SOLANA_RPC_URL_FALLBACK` — used when PRIMARY hits 429 or errors 5×× persistently

Script pattern in `references/examples/`.

## Step-by-step workflow

**1. Classify the task**
- Read account data → `getAccountInfo`, `getMultipleAccounts`
- Read tx → `getTransaction` (raw) or Helius Enhanced (parsed)
- Read history → `getSignaturesForAddress` + batch `getTransaction`, OR Helius `getTransactionsForAddress`
- Read token balances/NFTs → **DAS `getAssetsByOwner`** (preferred) or `getTokenAccountsByOwner`
- Submit tx → `sendTransaction` or **Helius Sender** (better landing rate)
- Estimate fee → `getPriorityFeeEstimate` (Helius) or `qn_estimatePriorityFees` (QuickNode)
- Stream real-time → WebSocket / LaserStream (not polling)

**2. Check for batch opportunities**
If > 3 items of same method → batch them in one HTTP request. Don't loop.

**3. Pick commitment level**
- Default `confirmed` for reads
- `finalized` for financial audit / history
- Never `processed` for production (may revert)

**4. Execute (MCP or script)**
- Single call: curl or httpx inline
- Batch: Python script with aiohttp + JSON-RPC array, output JSONL

**5. Present results**
- Lamports → divide by 1e9 for SOL
- Token amounts → divide by 10^decimals
- Timestamps: `block_time` is unix seconds (no sub-second precision on `getBlockTime`)

---

## Common mistakes & error codes

| Error | Cause | Fix |
|-------|-------|-----|
| `-32009` "Slot ... skipped" | Asked for a slot that wasn't produced | Use `getBlock` with `commitment: "confirmed"` and skip error silently |
| `-32602` Invalid params | Wrong encoding / missing `maxSupportedTransactionVersion: 0` | Add `"maxSupportedTransactionVersion": 0` to all tx reads |
| 429 Too Many Requests | Rate limit | Respect provider's `Retry-After`, lower semaphore |
| Response timeout on `getBlock` | Large response (~MBs) | Set HTTP timeout ≥ 30s; consider `transactionDetails: "signatures"` or `accounts` if full tx not needed |
| Empty result on `getSignaturesForAddress` | No sigs in the range OR wrong `before`/`until` cursors | Verify cursor with `getSignatureStatuses` |
| DAS methods missing | Not Helius/QuickNode with DAS addon | Fall back to raw RPC or enable addon |

## Memory updates

Old memory says:
- "QuickNode `getTransaction`: ~10k/min, ~15KB response, 3x faster than Solscan for single-tx" — ✅ still valid
- "`getBlock`: ~30s timeout needed, large response" — ✅ still valid
- "`getBlockTime`: seconds precision only" — ✅ still valid

Add:
- `maxSupportedTransactionVersion: 0` is **required** for modern tx reads — otherwise you get "Transaction version (0) is not supported" errors on v0 tx
- Helius DAS now supports fungible tokens too (`showFungible: true` on `getAssetsByOwner`)
- Priority fee: prefer `getPriorityFeeEstimate` (Helius) over raw `getRecentPrioritizationFees`

## Reference files

- `references/core-methods.md` — standard Solana JSON-RPC: accounts, blocks, transactions, fees
- `references/helius-extensions.md` — DAS, Enhanced Tx, Priority Fee, Sender, Webhooks, LaserStream
- `references/quicknode-extensions.md` — qn_estimatePriorityFees, DAS addon, Jito
- `references/patterns.md` — batching details, rate limits, fallback, cost
- `references/examples/fetch_tx_batch.py` — batched `getTransaction` for N signatures
- `references/examples/wallet_full_history.py` — Helius `getTransactionsForAddress` with pagination
- `references/examples/wallet_holdings_das.py` — DAS `getAssetsByOwner` with full token metadata
