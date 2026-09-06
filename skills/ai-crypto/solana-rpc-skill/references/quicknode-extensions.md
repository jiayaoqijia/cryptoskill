# QuickNode Extensions (beyond standard RPC)

QuickNode offers standard Solana RPC plus optional **addons** enabled per-endpoint. Each addon adds specific methods to the same RPC URL.

## Setup

QuickNode gives you a custom URL per endpoint, e.g.:
```bash
export SOLANA_RPC_URL="https://YOUR-NAME.solana-mainnet.quiknode.pro/YOUR-TOKEN/"
```

No API key header — the URL itself is the credential. Scripts read from `SOLANA_RPC_URL`.

## Pricing model

QuickNode uses per-endpoint subscription (not credit-based). You pay for:
- RPS/burst allowance per endpoint
- Each addon separately

Free tier exists but limited. Production typically needs Build plan ($49/mo) or higher. Exact plan details vary — check user's dashboard.

## Priority Fee addon

### `qn_estimatePriorityFees(options)`
QuickNode's equivalent to Helius's `getPriorityFeeEstimate`.

Options:
- `last_n_blocks: 100` — how many recent blocks to sample (default varies)
- `account: "<address>"` — optional: focus on this writable account
- `api_version: 2`

Response:
```json
{
  "per_compute_unit": {
    "percentile_25": 1000,
    "percentile_50": 2500,
    "percentile_75": 10000,
    "percentile_95": 50000,
    "percentile_99": 100000
  },
  "per_transaction": {...}
}
```

**Rule of thumb:** use `percentile_75` for normal tx, `percentile_95` for urgent during congestion.

## Metaplex DAS API addon

Same DAS endpoints as Helius (`getAsset`, `getAssetsByOwner`, `getAssetsByGroup`, `searchAssets`, `getAssetProof`, `getSignaturesForAsset`). Must be enabled as addon on your QuickNode endpoint.

See `helius-extensions.md` — **DAS methods are identical** across providers.

## Lil JIT (Jito Bundles)

Submit transactions as Jito bundles — atomically bundled txs that land together, used for MEV and multi-tx strategies.

Methods added:
- `sendBundle(bundle, options)` — submit bundle of up to 5 signed txs
- `getBundleStatuses([bundle_id, ...])` — check status
- `getTipAccounts()` — Jito tip accounts (send tips to these for priority)

Use case: sandwich attacks, arbitrage, atomic multi-dex swaps.

## Metis (Trading API)

High-level DEX trading wrapper — quote & execute swaps across Jupiter aggregator.
- `qn_fetchQuote` — get swap route and amounts
- `qn_fetchSwapTransaction` — get signed-ready tx

Alternative to calling Jupiter v6 API directly. Simpler but less flexible.

## Yellowstone Geyser gRPC

Real-time streaming via Solana's Geyser plugin interface. Open-source equivalent of Helius LaserStream.
- gRPC transport, separate endpoint URL
- Available on Dedicated Nodes and Premium plans
- Use for: MEV bots, trading, real-time analytics

## Historical-aware RPC

QuickNode Solana endpoints include **full archive** by default on mainnet-beta (no pruning). Testnet/Devnet are pruned.

This means:
- `getBlock(old_slot)` works for any historical slot
- `getTransaction(old_sig)` works forever
- `getSignaturesForAddress` can paginate back to genesis

Helius also provides archive — most production providers do. Public RPC does NOT.

## Empirical performance (production)

- `getTransaction` on QuickNode: ~10k req/min sustainable, ~15 KB response per jsonParsed tx
- `getBlock` full: ~30s timeout needed, megabyte-size payload; use `transactionDetails: "signatures"` to shrink if you only need sig list
- 3× faster than Solscan for raw single-tx fetches
- No parsed swap/DeFi data — use Solscan or Helius Enhanced for that

## Picking between Helius and QuickNode

| Use case | Prefer |
|----------|--------|
| NFT-heavy (cNFTs, collections) | Helius (DAS + Webhooks polished) |
| Parsed tx history for analytics | Helius (Enhanced Tx > raw parsing) |
| Real-time at scale | Both work (LaserStream vs Yellowstone) |
| MEV / Jito bundles | QuickNode Lil JIT or direct Jito |
| Standard RPC at high throughput | Either — pricing/support decides |
| Simplest NFT queries | Helius DAS with showFungible |
| Archive history | Both OK (default on paid plans) |

## Addon selection checklist

Before enabling an addon, ask user:
- Do you actually need this data **realtime**? (else, use webhooks or polling from a cheaper tier)
- Are you submitting **many** txs? (Priority Fee + Jito worth it)
- Do you query **NFTs**? (DAS is mandatory — manual parsing is 10× slower)

Each addon costs extra — don't enable speculatively.
