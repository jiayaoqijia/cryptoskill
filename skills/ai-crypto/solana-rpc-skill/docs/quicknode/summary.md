# Solana RPC (QuickNode / Helius / Any Provider) — Summary

Собрано 2026-04-24 из helius.dev/llms.txt (сохранён в `helius-llms.txt`), Solana docs, QuickNode docs.

## Key insight

**Solana RPC is standardized** — all providers (QuickNode, Helius, Triton, Ankr, Chainstack, public endpoints) expose the same JSON-RPC methods. Only the URL and the extension endpoints differ.

**Provider endpoints:**
| Provider | Mainnet URL format |
|----------|-------------------|
| Public (Solana Foundation) | `https://api.mainnet-beta.solana.com` (rate-limited, not for production) |
| Helius | `https://mainnet.helius-rpc.com/?api-key=KEY` |
| QuickNode | Custom per-endpoint URL from dashboard |
| Triton | Custom per-endpoint URL |
| Ankr | `https://rpc.ankr.com/solana` + API key |
| Chainstack | Custom per-endpoint URL |

## Helius pricing (2026)

| Plan | Cost | Monthly credits | Rate limit |
|------|------|-----------------|------------|
| Free | $0 | 1,000,000 | 10 req/s |
| Developer | $49/mo | — | 50 req/s |
| Business | $499/mo | 100,000,000 | 200 req/s (50 sendTx/s) |
| Professional | $999/mo | 200,000,000 | 500 req/s (100 sendTx/s) |
| Enterprise | Custom | Custom | Custom |

Plus Dedicated Nodes at $2,300+/mo (no rate limits, no credits).

## QuickNode pricing

Different model — not credit-based. Subscribers get a fixed RPS/burst allowance per endpoint. Addons (Priority Fee, DAS, Lil JIT, Metis, Yellowstone Geyser) activated per-endpoint separately.

Public pricing not clearly documented — requires user's subscription details to quote exactly.

## Authentication

| Provider | How to authenticate |
|----------|---------------------|
| Helius | Query param: `?api-key=YOUR_KEY` |
| QuickNode | URL contains unique identifier (no header) |
| Ankr | Header or URL with key |
| Triton | URL with project ID |

Standardize via env var `SOLANA_RPC_URL` — scripts read this, don't hardcode.

## Helius extensions (over standard RPC)

| Extension | Method/Endpoint | Use case |
|-----------|-----------------|----------|
| **DAS API** | `getAsset`, `getAssetsByOwner`, `getAssetsByGroup`, `searchAssets`, `getSignaturesForAsset` | Unified NFT/token/cNFT queries |
| **Enhanced Transactions** | `getTransactionsForAddress`, POST `/v0/transactions` | Parsed, human-readable tx (NFT sales, swaps, transfers labeled) |
| **Priority Fee** | `getPriorityFeeEstimate` | Optimal fee for landing |
| **Webhooks** | Real-time HTTP POST | Event streaming without polling |
| **Enhanced WebSockets** | Filtered subscriptions | Real-time with advanced filters |
| **LaserStream gRPC** | gRPC streaming | Lowest latency, 24h replay |
| **Helius Sender** | Tx submission service | Higher landing rate via dual-route (validators + Jito) |
| **Wallet API** | REST endpoints | Simple wallet balances/history |
| **ZK Compression** | Compressed accounts | 98% cheaper on-chain storage |

## QuickNode extensions

| Addon | Method |
|-------|--------|
| Priority Fee API | `qn_estimatePriorityFees` |
| Metaplex DAS API | Same DAS methods as Helius (getAsset, etc) |
| Lil JIT | JITO bundle submission |
| Metis Trading API | DEX trading |
| Yellowstone Geyser gRPC | Real-time streaming |

## Critical "Don't Confuse" rules (Helius docs)

**Key anti-patterns that waste credits/time:**

| Want to... | Use | Not | Why |
|-----------|-----|-----|-----|
| Get wallet NFTs/tokens | `getAssetsByOwner` (DAS) | `getTokenAccountsByOwner` | Raw accounts w/o metadata, need extra lookups |
| Complete tx history | `getTransactionsForAddress` (Helius Enhanced) | `getSignaturesForAddress` | Latter misses token account history |
| cNFT tx history | `getSignaturesForAsset` (DAS) | `getSignaturesForAddress` | Doesn't work for compressed NFTs |
| Priority fee estimate | `getPriorityFeeEstimate` (Helius) | `getRecentPrioritizationFees` | Requires manual calculation |
| Search NFTs by collection | `getAssetsByGroup` / `searchAssets` (DAS) | `getProgramAccounts` | Expensive, slow, not indexed |
| Stream real-time | LaserStream gRPC / Enhanced WS | Polling | Higher latency, wastes credits |
| Reliable tx submission | Helius Sender | `sendTransaction` | Lower landing rate on plain RPC |

## Commitment levels

| Level | Meaning | Use for |
|-------|---------|---------|
| `processed` | Block processed, may revert | Fastest, not safe for finality |
| `confirmed` | 2/3 stake voted | Basically final, OK for reads |
| `finalized` | Guaranteed (32+ confirmations) | Financial transactions, audit |

Default for reads: `confirmed`. For money: `finalized`. Never `processed` for production.

## Standard Solana RPC methods (most common)

### Accounts
- `getAccountInfo(address)` — account state and data
- `getBalance(address)` — SOL balance in lamports
- `getMultipleAccounts([addresses])` — batch up to 100
- `getProgramAccounts(program_id, filters)` — **expensive**, prefer DAS where possible
- `getTokenAccountBalance(token_account)`
- `getTokenAccountsByOwner(owner, mint_or_program)`

### Blocks
- `getSlot()` — current slot
- `getBlockHeight()`
- `getLatestBlockhash()`
- `getBlock(slot, config)` — full block; **~30s response time, large payload**
- `getBlockTime(slot)` — unix seconds precision only (not sub-second)
- `getBlocks(start, end)` — list of confirmed slots in range

### Transactions
- `getTransaction(sig, config)` — full tx; config `encoding: "jsonParsed"` for readable
- `getSignaturesForAddress(address, {limit, before, until})` — signatures list; **limit max 1000**
- `getSignatureStatuses([sigs])` — batch status check, up to 256
- `simulateTransaction(tx)` — dry-run without sending
- `sendTransaction(tx, config)` — submit signed tx

### Fees
- `getFeeForMessage(message)` — estimate cost
- `getRecentPrioritizationFees([addresses])` — historical priority fees

### Cluster
- `getHealth()`, `getEpochInfo()`, `getClusterNodes()`, `getVersion()`

## JSON-RPC batch requests (biggest credit saver)

Standard JSON-RPC supports arrays — send multiple method calls in ONE HTTP request:

```json
[
  {"jsonrpc": "2.0", "id": 1, "method": "getTransaction", "params": ["sig1"]},
  {"jsonrpc": "2.0", "id": 2, "method": "getTransaction", "params": ["sig2"]},
  {"jsonrpc": "2.0", "id": 3, "method": "getTransaction", "params": ["sig3"]}
]
```

Returns array of responses. Typical max 100 per batch. **Always use batching for multi-item fetches** — same credit count (provider-dependent), vastly less HTTP overhead.

## Historical empirical notes

- `getTransaction` on QuickNode: ~10k req/min, ~15KB response per tx, jsonParsed works well
- `getBlock` on QuickNode: requires ~30s timeout due to full payload
- `getBlockTime` precision: seconds only (useless for sub-second analysis)
- QuickNode ~3× faster than Solscan for raw single-tx fetches but doesn't parse DeFi/swaps — use Solscan or Helius Enhanced Tx for parsed data

## Sources

- https://solana.com/docs/rpc (standard JSON-RPC reference)
- https://www.helius.dev/llms.txt (Helius index, saved)
- https://www.helius.dev/docs/api-reference (Helius API reference)
- https://www.quicknode.com/docs/solana (QuickNode Solana docs)
- https://www.helius.dev/pricing (plan tiers)
