# Solscan Pro API v2 — Documentation Summary

Собрано 2026-04-23 из официальной документации и эмпирического API-тестирования.

## Basics

- **Base URL:** `https://pro-api.solscan.io/v2.0`
- **Auth:** header `token: <api-key>`
- **Method:** GET for most endpoints
- **All endpoints cost 100 CU per request** (after Nov 2025 unification)

## Rate limits

**Not explicitly documented officially.** Empirical values from bounded API testing:
- **~950 req/min** — safe baseline
- **~3000 req/min** — burst, may hit 429

Best throughput achieved: async aiohttp with semaphore=25 → **~170 wallets/min** for defi/activities with page_size=100.

## Data history depth

| Endpoint | How far back |
|----------|--------------|
| Transfers | 3 years (since July 2021) |
| Balance Change | 6 months |
| DeFi Activities | 6 months |
| Token price | 3-minute delay |
| Token list | Top 2000 by market cap |

## page_size — DISCRETE VALUES ONLY

**Critical gotcha:** `page_size` is not continuous. Allowed values:
`10, 20, 30, 40, 60, 100`

- `page_size=50` → **FAILS** (not in list)
- `page_size=100` → works, maximum
- `page_size=200+` → **FAILS**

Always use `100` for batch work.

## Endpoint list (50 endpoints)

### Account (15)
- `account/detail` — balance, owner, type
- `account/data-decoded` — decoded account data
- `account/transfer` — transfer history with filters
- `account/defi/activities` — swaps, liquidity, staking
- `account/balance_change/activities` — balance changes
- `account/transactions` — raw tx list (max limit 50)
- `account/portfolio` — full portfolio
- `account/token-accounts` — SPL token accounts
- `account/stake` — stake accounts
- `account/stake-rewards/export` — rewards export
- `account/transfer/export` — transfer bulk export
- `account/defi/activities/export` — defi bulk export
- `account/metadata` — single address metadata
- `account/metadata/multi` — batch metadata lookup
- `account/leaderboard` — ranked accounts

### Token (14)
- `token/transfer` — token transfers across wallets
- `token/defi/activities` — defi per token
- `token/markets` — DEX pools, liquidity
- `token/meta` — single token metadata
- `token/meta/multi` — batch metadata
- `token/price` — price history (daily)
- `token/price/multi` — batch prices
- `token/holders` — top holders
- `token/list` — top 2000 tokens by mcap
- `token/top` — ranked by volume/activity
- `token/trending` — trending tokens
- `token/latest` — newest tokens
- `token/defi/activities/export` — bulk export
- `token/historical-data` — historical aggregates

### NFT (4)
- `nft/new` — newly minted
- `nft/activities` — trades/transfers for collection or item
- `nft/collection/lists` — collection directory
- `nft/collection/items` — items in collection

### Transaction (6)
- `transaction/last` — latest tx on chain
- `transaction/detail` — single tx full details
- `transaction/detail/multi` — **up to 50 signatures per call** — MAJOR CU saver (100 CU vs 50×100)
- `transaction/decoded` — parsed instructions
- `transaction/decoded/multi` — batch decoded
- `transaction/fees` — fee statistics

### Block (3)
- `block/last`, `block/transactions`, `block/detail`

### Market (3)
- `market/listing-pool` — all pools
- `market/info` — pool details
- `market/historical-data` — time series

### Program (2)
- `program/list` — active programs
- `program/popular-platforms`

### Data Export (2) — for bulk downloads
- `datafile/list` — list of downloadable files
- `datafile/download` — download prepared file

### Monitoring (1)
- `monitor/usage` — **current CU consumption for current plan**

## Multi-endpoints (batch CU savers)

When you need the same data for many items, use these instead of N separate calls:

| Multi endpoint | Single item cost | Multi cost | Savings |
|----------------|------------------|------------|---------|
| `transaction/detail/multi` (up to 50 tx) | 50 × 100 = 5000 CU | 100 CU | **50×** |
| `token/meta/multi` (up to 50 tokens) | 50 × 100 = 5000 CU | 100 CU | **50×** |
| `account/metadata/multi` | same | 100 CU | **50×** |

**Rule:** whenever you're about to loop `for x in items: call_single(x)`, check if `multi` endpoint exists for that data.

## Export endpoints (for heavy data)

When you need full wallet history (more than a few pages worth), use dedicated export endpoints:
- `account/transfer/export`
- `account/defi/activities/export`
- `account/stake-rewards/export`
- `token/defi/activities/export`

These return preformatted CSV files — cheaper than iterating pages.

**Workflow:**
1. POST to the export endpoint with params → returns file job
2. Poll `datafile/list` until file ready
3. `datafile/download` to fetch

Exact CU cost for exports not documented — assume 100 CU per request + whatever size-based charge.

## Account Transfer params (reference example)

`GET /v2.0/account/transfer?address=<addr>&page_size=100&page=1`

All parameters:
- `address` (required) — wallet
- `activity_type[]` — ACTIVITY_SPL_TRANSFER, ACTIVITY_SPL_BURN, ACTIVITY_SPL_MINT, ACTIVITY_SPL_CREATE_ACCOUNT, ACTIVITY_SPL_CLOSE_ACCOUNT, ACTIVITY_SPL_TOKEN_WITHDRAW_STAKE, ACTIVITY_SPL_TOKEN_SPLIT_STAKE, ACTIVITY_SPL_TOKEN_MERGE_STAKE, ACTIVITY_SPL_VOTE_WITHDRAW, ACTIVITY_SPL_SET_OWNER_AUTHORITY
- `token_account` — filter specific SPL account
- `from`, `exclude_from`, `to`, `exclude_to` — up to 5 comma-separated addresses each
- `token` — up to 5 token mints comma-separated
- `amount[]=min&amount[]=max` — range filter
- `value[]=1&value[]=10` — USD range filter
- `from_time`, `to_time` — unix seconds
- `exclude_amount_zero` — bool
- `flow` — "in" | "out"
- `page`, `page_size` (10/20/30/40/60/100), `sort_by=block_time`, `sort_order=asc|desc`

## DeFi Activities activity_type values

ACTIVITY_TOKEN_SWAP, ACTIVITY_AGG_TOKEN_SWAP, ACTIVITY_TOKEN_ADD_LIQ, ACTIVITY_TOKEN_REMOVE_LIQ, ACTIVITY_POOL_CREATE, ACTIVITY_SPL_TOKEN_STAKE, ACTIVITY_LST_STAKE, ACTIVITY_SPL_TOKEN_UNSTAKE, ACTIVITY_LST_UNSTAKE, ACTIVITY_TOKEN_DEPOSIT_VAULT, ACTIVITY_TOKEN_WITHDRAW_VAULT, ACTIVITY_SPL_INIT_MINT, ACTIVITY_ORDERBOOK_ORDER_PLACE, ACTIVITY_BORROWING, ACTIVITY_REPAY_BORROWING, ACTIVITY_LIQUIDATE_BORROWING, ACTIVITY_BRIDGE_ORDER_IN, ACTIVITY_BRIDGE_ORDER_OUT

## Transaction detail response fields

Useful fields from `transaction/detail`:
- `tx_hash`, `block_id`, `block_time`
- `fee`, `priority_fee` — lamports
- `compute_units_consumed` — Solana CU (not Solscan CU)
- `sol_bal_change` — per-account SOL delta
- `token_bal_change` — per-account token deltas
- `status` — 1 success, 0 error
- `programs_involved`, `parsed_instructions`, `log_message`

## MCP vs direct API

MCP server at `/path/to/solscan-mcp/index.js` (stdio, local Node).
- Good for interactive single queries
- **For batch work (100+ wallets), use direct HTTP with async aiohttp + semaphore**
- MCP serializes requests — loses parallelism benefit

## Sources

- https://docs.solscan.io/api-access/pro-api-endpoints
- https://docs.solscan.io/api-access/solscan-pro-api-faq
- https://pro-api.solscan.io/pro-api-docs/v2.0
- https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer
- https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities
- https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-detail
- https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-detail-multi
