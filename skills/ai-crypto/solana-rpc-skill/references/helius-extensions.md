# Helius Extensions (beyond standard RPC)

Helius adds proprietary APIs on top of standard Solana RPC. If the user has a Helius endpoint, prefer these over raw RPC + manual parsing.

## Setup

```bash
export SOLANA_RPC_URL="https://mainnet.helius-rpc.com/?api-key=YOUR_KEY"
```

All Helius APIs use the same URL (RPC methods + DAS + Enhanced are multiplexed on the same endpoint). Auth via `?api-key=...` query param.

## Pricing tiers (2026)

| Plan | Cost | Monthly credits | RPS | Notable |
|------|------|-----------------|-----|---------|
| Free | $0 | 1M | 10 | Good for dev |
| Developer | $49/mo | — | 50 | Enhanced WebSockets |
| Business | $499/mo | 100M | 200 (50 sendTx) | LaserStream gRPC |
| Professional | $999/mo | 200M | 500 (100 sendTx) | |
| Dedicated Nodes | $2,300+/mo | — | unlimited | No credits/limits |

Per-request credit cost varies by method — DAS calls and Enhanced Tx are heavier than standard RPC. Check `X-Credits-Used` response header.

## DAS API (Digital Asset Standard)

**Single API for all Solana digital assets: NFTs, compressed NFTs (cNFTs), fungible tokens, Token 2022, MPL Core.**

All DAS methods are JSON-RPC calls on the same RPC URL.

### `getAsset(id)`
Metadata for a single asset (NFT, token, cNFT). Response includes content, compression status, ownership, royalties, grouping (collection).

### `getAssetsByOwner({ownerAddress, page, limit, displayOptions})`
All assets owned by a wallet.
- `displayOptions.showFungible: true` — **include SPL tokens too** (with metadata)
- `displayOptions.showNativeBalance: true` — include SOL balance
- `displayOptions.showCollectionMetadata: true` — include parent collection info
- `page`, `limit` (max 1000) — pagination
**Use this instead of `getTokenAccountsByOwner`** for wallet-holdings queries.

### `getAssetsByGroup({groupKey, groupValue, page, limit})`
All assets in a collection. Typical: `groupKey="collection"`, `groupValue=<collection_mint>`.
**Use this instead of `getProgramAccounts`** for "all NFTs in collection X".

### `searchAssets({conditions, page, limit})`
Advanced NFT search — filter by compressed, frozen, burnt, owner, creator, authority, royaltyTargetType, grouping, etc.

### `getAssetProof(id)`
Merkle proof for a compressed NFT — required for cNFT transfers.

### `getSignaturesForAsset(id)`
Full tx history for a compressed NFT (where raw `getSignaturesForAddress` doesn't work).

## Enhanced Transactions API

**Human-readable parsed transaction data** — Helius auto-labels swaps, NFT sales, transfers, DeFi ops.

### `getTransactionsForAddress(address, options)`
Complete wallet tx history with decoded instructions and **includes token-account history** (unlike raw `getSignaturesForAddress` which misses SPL activity on associated token accounts).

Options: `limit` (up to 100 per call), `before`, `until`, `type` (filter: NFT_SALE, SWAP, TRANSFER, etc), `source` (program filter).

Response: array of enhanced tx objects with `type`, `description` (string like "A transferred X USDC to B"), `events.nft`, `events.swap`, `tokenTransfers`, `nativeTransfers`.

### POST `/v0/transactions`
Parse a list of raw signatures in one request. Body: `{"transactions": ["sig1", "sig2", ...]}`. Max ~100 per batch.

### Enhanced Tx types (filter values)
`ANY`, `UNKNOWN`, `NFT_SALE`, `NFT_LISTING`, `NFT_BID`, `NFT_CANCEL_LISTING`, `NFT_MINT`, `TOKEN_MINT`, `EXECUTE_TRANSACTION`, `SWAP`, `TRANSFER`, `STAKE`, `BURN`, `...` (many more — check docs).

## Priority Fee API

### `getPriorityFeeEstimate(options)`
Optimal priority fee for landing. Much better than raw `getRecentPrioritizationFees`.

Options:
- `accountKeys`: array of writable accounts your tx will touch
- `transaction`: base58-encoded tx (alternative to accountKeys)
- `options.priorityLevel`: `"Min"` | `"Low"` | `"Medium"` | `"High"` | `"VeryHigh"` | `"UnsafeMax"` | `"Default"` (Medium)
- `options.includeAllPriorityFeeLevels: true` — return all levels
- `options.recommended: true` — single recommended value

Response: `{priorityFeeEstimate: <microlamports>}` or `{priorityFeeLevels: {...}}`.

## Helius Sender

Faster, more reliable tx submission than standard `sendTransaction`.
- Dual-routes through staked validator connections AND Jito bundles simultaneously
- Higher landing rate, especially during congestion
- Same sign + submit flow, different RPC endpoint
Docs: https://www.helius.dev/docs/api-reference/sender

## Webhooks

Real-time HTTP POST when events occur on-chain.
- Configure at dashboard: target URL + account addresses / tx types to watch
- Event types: same as Enhanced Tx types (NFT_SALE, SWAP, etc)
- **Avoid polling** — webhooks save massive credits

## LaserStream (gRPC streaming)

Lowest latency real-time streaming, 24h historical replay, auto-reconnect.
- gRPC transport
- Filter by accounts, programs, tx types
- Business plan+ only
- Enhanced WebSockets (Developer plan+) as simpler alternative

## Wallet API (REST)

Simple REST endpoints on `api.helius.xyz` for wallet-specific queries. Each is one HTTP call:
- `GET /v0/addresses/<addr>/balances` — SOL + all tokens with metadata
- `GET /v0/addresses/<addr>/transactions` — enhanced tx history
- `GET /v0/addresses/<addr>/nft-events` — NFT activity

Good for quick integrations without setting up JSON-RPC plumbing.

## ZK Compression API

Work with compressed accounts (98% cheaper on-chain storage via zero-knowledge proofs). Only needed if user is specifically building with ZK compression.

## Deprecated — don't use

| Deprecated | Use |
|------------|-----|
| `mintCompressedNft` | Metaplex Bubblegum SDK directly |
| `queryMetadataV1` | DAS `getAsset` or `searchAssets` |

## Credit optimization tips

1. **Use DAS instead of raw RPC loops** — one `getAssetsByOwner` beats N × `getTokenAccountBalance`
2. **Use Enhanced Tx `getTransactionsForAddress`** instead of getSignaturesForAddress + N × getTransaction — single method vs N+1 pattern
3. **Webhooks over polling** — real-time notifications use 1 credit per event vs constant polling
4. **Priority Fee API once per tx**, not every block poll
5. **Check `X-Credits-Used` / `X-Credits-Remaining`** in response headers
