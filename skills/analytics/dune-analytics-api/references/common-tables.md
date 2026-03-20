# Dune Common Tables Reference

Quick reference for frequently used tables. This is **not** an exhaustive list — if the table you need isn't listed here, use the [Table Discovery](table-discovery.md) methods to search by keyword, inspect schemas, and find decoded tables for specific protocols.

## 1. Raw Tables

Table naming: `<chain>.<table>`, e.g. `ethereum.transactions`

| Table | Description | Delay |
|-------|-------------|-------|
| `<chain>.blocks` | Block info (number, timestamp, base_fee, miner) | < 1 min |
| `<chain>.transactions` | All transactions (from/to/value/gas/hash) | < 1 min |
| `<chain>.traces` | Internal call traces (call/create/delegatecall) | < 1 min |
| `<chain>.logs` | Event logs (topics[], data) | < 1 min |
| `<chain>.creation_traces` | Contract creation records | < 1 min |

**Supported EVM chains:** ethereum, polygon, arbitrum, base, optimism, bnb, fantom, zksync, blast, linea, avalanche, gnosis, celo, scroll, etc. (40+)

**Solana raw:**

| Table | Description |
|-------|-------------|
| `solana.transactions` | Raw transactions (account_keys, log_messages, signatures) |
| `solana.blocks` | Block data |
| `solana.rewards` | Staking/voting rewards |
| `solana.account_activity` | Account-level activity |

## 2. Decoded Tables

Table naming: `<project>_<chain>.evt_<EventName>` / `<project>_<chain>.call_<FuncName>`

Examples:
- `uniswap_v3_ethereum.evt_PoolCreated` — Uniswap V3 pool creation events
- `uniswap_v3_ethereum.call_swap` — Uniswap V3 swap function calls
- `erc20_ethereum.evt_Transfer` — ERC20 Transfer events

## 3. Curated / Spellbook Tables

### DEX Trading

| Table | Description | Notes |
|-------|-------------|-------|
| `dex.trades` | All EVM DEX trades (cross-chain) | ⚠️ Multi-hop counted multiple times, volume inflated ~30% |
| `dex_aggregator.trades` | Aggregator-level trades | Accurate volume, no multi-hop duplication |
| `dex_solana.trades` | Solana DEX trades | No aggregator table; dedupe by tx_id |

### NFT

| Table | Description |
|-------|-------------|
| `nft.trades` | NFT trades across marketplaces |
| `nft.mints` | NFT minting events |
| `nft.transfers` | NFT transfer records |
| `tokens.nft` | NFT metadata (name, collection, etc.) |

### Token / Asset Tracking

| Table | Description |
|-------|-------------|
| `tokens.erc20` | ERC20 token metadata (symbol, name, decimals, contract_address) |
| `tokens_<chain>.transfers` | Token transfer events (ERC20 + native) |
| `tokens_<chain>.balances` | Address balances (daily snapshot) |

### Prices

| Table | Description |
|-------|-------------|
| `prices.usd` | Historical token USD prices (JOIN by contract_address + minute) |
| `prices.usd_latest` | Latest token prices |

### Labels

| Table | Description |
|-------|-------------|
| `labels.all` | Address labels (exchanges, projects, whales, contracts, etc.) |

### Solana Curated

| Table | Description |
|-------|-------------|
| `dex_solana.trades` | Solana DEX trades with token info |
| `tokens_solana.transfers` | SPL token + SOL transfers |

## 4. Community / Off-Chain Data

| Table | Description |
|-------|-------------|
| `farcaster.*` | Farcaster social data |
| `hyperliquid.*` | Hyperliquid perps/spot data |
| `snapshot.*` | Governance voting data |
| `reservoir.*` | NFT marketplace data |

## 5. Data Freshness

| Data Layer | Delay | Tables |
|------------|-------|--------|
| Raw | < 1 min | `solana.transactions`, `ethereum.transactions` |
| Decoded | 15-60 sec | Program-specific |
| Curated | ~1 hour+ | `dex.trades`, `dex_solana.trades` |

**Recommendation:** Query previous day's data after **UTC 12:00** for completeness.

## 6. Common Query Patterns

```sql
-- Get token price at trade time
SELECT t.*, p.price
FROM dex.trades t
LEFT JOIN prices.usd p
  ON p.contract_address = t.token_bought_address
  AND p.blockchain = t.blockchain
  AND p.minute = date_trunc('minute', t.block_time)

-- Get address label
SELECT a.address, l.name, l.category
FROM my_addresses a
LEFT JOIN labels.all l ON l.address = a.address

-- Token balance with metadata
SELECT b.*, t.symbol, t.decimals
FROM tokens_ethereum.balances b
LEFT JOIN tokens.erc20 t
  ON t.contract_address = b.token_address
  AND t.blockchain = 'ethereum'
WHERE b.address = 0x...
```
