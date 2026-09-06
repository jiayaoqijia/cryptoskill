# Solscan Pro API v2 — Endpoint Reference

Base: `https://pro-api.solscan.io/v2.0`
Auth: header `token: <SOLSCAN_API_KEY>`
All endpoints: **GET**, **100 CU each**.

Common pagination params: `page`, `page_size` (10/20/30/40/60/100), `sort_by=block_time`, `sort_order=asc|desc`.
Common time params: `from_time`, `to_time` (unix seconds).

## Account endpoints (15)

### `account/detail`
- `address` (required) — wallet
- Returns: SOL balance, type, owner, executable, rent_epoch

### `account/transfer`
Transfer history (SPL + SOL, based on activity_type).
- `address` (required)
- `activity_type[]` — ACTIVITY_SPL_TRANSFER, ACTIVITY_SPL_BURN, ACTIVITY_SPL_MINT, ACTIVITY_SPL_CREATE_ACCOUNT, ACTIVITY_SPL_CLOSE_ACCOUNT, ACTIVITY_SPL_TOKEN_WITHDRAW_STAKE, ACTIVITY_SPL_TOKEN_SPLIT_STAKE, ACTIVITY_SPL_TOKEN_MERGE_STAKE, ACTIVITY_SPL_VOTE_WITHDRAW, ACTIVITY_SPL_SET_OWNER_AUTHORITY
- `token_account`, `token` (up to 5), `from`/`to`/`exclude_from`/`exclude_to` (up to 5 each)
- `amount[]=min&amount[]=max`, `value[]=min&value[]=max` (USD)
- `flow` = "in"|"out", `exclude_amount_zero`
- `from_time`, `to_time`

### `account/defi/activities`
Swaps, liquidity, staking, borrowing, bridging.
- `address` (required)
- `activity_type[]` — ACTIVITY_TOKEN_SWAP, ACTIVITY_AGG_TOKEN_SWAP, ACTIVITY_TOKEN_ADD_LIQ, ACTIVITY_TOKEN_REMOVE_LIQ, ACTIVITY_POOL_CREATE, ACTIVITY_SPL_TOKEN_STAKE, ACTIVITY_LST_STAKE, ACTIVITY_SPL_TOKEN_UNSTAKE, ACTIVITY_LST_UNSTAKE, ACTIVITY_TOKEN_DEPOSIT_VAULT, ACTIVITY_TOKEN_WITHDRAW_VAULT, ACTIVITY_SPL_INIT_MINT, ACTIVITY_ORDERBOOK_ORDER_PLACE, ACTIVITY_BORROWING, ACTIVITY_REPAY_BORROWING, ACTIVITY_LIQUIDATE_BORROWING, ACTIVITY_BRIDGE_ORDER_IN, ACTIVITY_BRIDGE_ORDER_OUT
- `platform[]` (up to 5 program IDs), `source[]` (up to 5)
- `from`, `token`, `from_time`, `to_time`

### `account/balance_change/activities`
Balance deltas regardless of reason. 6-month depth.

### `account/transactions`
Raw tx list.
- `address` (required)
- `before` (tx signature — paginate by cursor)
- `limit` — **max 50** (different from other endpoints, uses cursor not page)

### `account/portfolio`
Full portfolio snapshot: SOL + SPL + staking + USD values.

### `account/token-accounts`
All SPL token accounts for a wallet.
- `type` = "token"|"nft"
- `hide_zero` — exclude zero balances

### `account/stake`
Stake accounts for a wallet.

### `account/stake-rewards/export`
Export endpoint — returns CSV job.

### `account/metadata` / `account/metadata/multi`
Label, name_tag, categories. Multi: up to 50 addresses per call.

### `account/leaderboard`
Top accounts by balance/activity.

### `account/transfer/export` / `account/defi/activities/export`
**Returns CSV directly** (not async). Max 5000 rows, ~200-400 CU. Same filter params as non-export version. For > 5000 rows: chunk by time window. See `batch-patterns.md` and `examples/export_full_history.py`.

### `account/data-decoded`
Decoded account data (for program accounts).

## Token endpoints (14)

### `token/meta` / `token/meta/multi`
Name, symbol, decimals, supply, holders count, price. Multi: up to 50 mints.

### `token/price` / `token/price/multi`
Historical daily prices.
- `address` — mint
- `from_time`, `to_time` (unix seconds, must align to day boundaries)
- Multi: up to 50 mints, returns latest only

### `token/transfer`
Transfer history for a specific token (across all wallets).
- `address` (token mint, required)
- Same pagination/time/filter params as account/transfer

### `token/defi/activities`
DeFi activity filtered by token.

### `token/markets`
DEX pools trading this token. Columns: pool_id, program_id, token0/1, liquidity.

### `token/holders`
Top holders paginated.
- `address` (mint, required)
- `page`
- `page_size` — **only 10, 20, 30, 40** (not 60/100!)
- `from_amount`, `to_amount` — raw amount range
- `from_value`, `to_value` — USD value range filter
Response per item: `address` (token account), `amount`, `decimals`, `owner`, `rank`, `value` (USD), `percentage`. Top-level: `total` (total holders).

### `token/list`
Top 2000 tokens by market cap.
- `sort_by` = "market_cap" | "volume" | "holder" | "created_time"
- `sort_order`

### `token/top`, `token/trending`, `token/latest`
Various ranked lists.

### `token/defi/activities/export`
Bulk CSV export.

### `token/historical-data`
Aggregates (holders count, price, volume) over time.

## NFT endpoints (4)

### `nft/new`
Newly minted NFTs.

### `nft/activities`
Sales/transfers for a collection or individual NFT.

### `nft/collection/lists` / `nft/collection/items`
Directory + items within a collection.

## Transaction endpoints (6)

### `transaction/detail`
- `tx` (signature) — required
- Returns: fee, priority_fee, compute_units_consumed, sol_bal_change, token_bal_change, status, programs_involved, parsed_instructions, log_message

### `transaction/detail/multi` — **50 sigs per call, 100 CU**
- `tx[]` array of signatures (up to 50)
- Same response shape per item

### `transaction/decoded` / `transaction/decoded/multi`
Decoded instruction view. Multi: up to 50.

### `transaction/last`
Most recent tx on chain.

### `transaction/fees`
Network fee statistics.

## Block endpoints (3)

### `block/last`
Latest block.

### `block/transactions`
All txs in a block (paginated).

### `block/detail`
Block metadata.

## Market endpoints (3)

### `market/listing-pool`
All DEX pools across platforms.

### `market/info`
Single pool details.

### `market/historical-data`
OHLCV time series for a pool.

## Program endpoints (2)

### `program/list`
Active Solana programs indexed.

### `program/popular-platforms`
DeFi/DEX platform rankings.

## Data Export

`*/export` endpoints return CSV synchronously — no separate list/download step needed for Tier 2. `datafile/*` endpoints exist but are not used by the synchronous export flow we confirmed.

## Monitoring (1)

### `monitor/usage`
**Critical for budget awareness.** Returns:
- `used` — CU consumed this billing period
- `quota` — total CU allowed
- `reset_time` — unix timestamp of next reset
- `tier` — plan tier

Call at the start of a big batch to estimate how much budget is available.
