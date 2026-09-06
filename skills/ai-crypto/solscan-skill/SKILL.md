---
name: solscan
description: |
  Expert assistant for analyzing Solana blockchain data using the Solscan Pro API v2.
  Use this skill whenever the user wants to: look up a Solana wallet, check SOL or SPL
  token balances, view token transfer history, analyze a Solana transaction, find top
  token holders, check token price or market data, explore NFT activity, research DeFi
  activity on Solana, or investigate any Solana address or signature. Trigger even if
  the user doesn't say "Solscan" — any Solana on-chain data request should use this
  skill. Also trigger when the user pastes a Solana address (base58, 32–44 chars) or
  a transaction signature (~88 chars).

  Enforces "script-for-batch" rule: direct MCP calls only for exploration, write async
  scripts for any collection > 10 items.
compatibility:
  tools:
    - solscan_account_info
    - solscan_account_transfers
    - solscan_account_tokens
    - solscan_account_transactions
    - solscan_account_defi_activities
    - solscan_transaction
    - solscan_token_info
    - solscan_token_holders
    - solscan_token_price
    - solscan_token_markets
    - solscan_token_transfers
    - solscan_nft_info
    - solscan_nft_activities
    - solscan_search
---

# Solscan Pro API Skill

You have access to the Solscan Pro API v2 for Solana data.

Read reference files when you need depth:
- `references/endpoints.md` — full endpoint catalog with all parameters
- `references/limits.md` — CU model, rate limits, page_size gotchas
- `references/batch-patterns.md` — MCP vs script decision, multi-endpoints, export endpoints
- `references/examples/` — ready-to-run Python scripts for common batch tasks

---

## 🚨 Rule #1: scripts for batch, MCP for exploration

The #1 way this API gets wasted is calling MCP tools in a loop. Each call consumes API credits AND burns tokens in the conversation context, and serial MCP calls don't parallelize.

| Task size | Tool |
|-----------|------|
| 1–10 API calls, exploratory | MCP tools directly |
| 10–30 calls | Script preferred, especially if same shape of request repeats |
| > 30 calls | **Always** write a script |
| Any batch where responses are parsed, aggregated, or filtered | **Always** a script |

When writing a script: `async aiohttp + asyncio.Semaphore(25)`, output to CSV/JSON, resume pattern (skip already-processed IDs). See `references/examples/` for working templates.

## 🚨 Rule #2: use multi-endpoints and exports

Solscan charges 100 CU per request flatly, so **batch endpoints are 50× cheaper** than per-item loops:

| Instead of | Use |
|------------|-----|
| 50 × `transaction/detail` (5000 CU) | 1 × `transaction/detail/multi` (100 CU) |
| 50 × `token/meta` | 1 × `token/meta/multi` |
| 50 × `account/metadata` | 1 × `account/metadata/multi` |
| Paginating `account/defi/activities` past 10k rows | `account/defi/activities/export` |
| Paginating `account/transfer` for full history | `account/transfer/export` |

**Before writing a loop, check if a multi-endpoint exists** (see `references/endpoints.md`).

## 🚨 Rule #3: page_size is DISCRETE

Allowed values: `10, 20, 30, 40, 60, 100`.

- `page_size=50` → **fails** silently or returns error
- `page_size=100` → works, use this for batch
- `page_size=200+` → fails

Default is often `20` — always set `100` for batch work.

---

## Tool reference (MCP)

| MCP tool | Endpoint | When to use |
|----------|----------|-------------|
| `solscan_account_info` | `account/detail` | SOL balance, account type, owner |
| `solscan_account_tokens` | `account/token-accounts` | SPL balances |
| `solscan_account_transfers` | `account/transfer` | Transfer history (single wallet exploration) |
| `solscan_account_transactions` | `account/transactions` | Raw tx list |
| `solscan_account_defi_activities` | `account/defi/activities` | Swaps/liquidity/staking |
| `solscan_transaction` | `transaction/detail` | One tx |
| `solscan_token_info` | `token/meta` | Token metadata |
| `solscan_token_holders` | `token/holders` | Top holders (paginated) |
| `solscan_token_price` | `token/price` | Price history |
| `solscan_token_markets` | `token/markets` | DEX pools |
| `solscan_token_transfers` | `token/transfer` | Recent transfers across wallets |
| `solscan_nft_info` | `nft/info` | NFT metadata |
| `solscan_nft_activities` | `nft/activities` | Sales/transfers |
| `solscan_search` | `search` | Find by name/partial addr |

For batch work not covered by MCP (multi-endpoints, exports): use direct HTTP with the same key. See `references/examples/`.

---

## Step-by-step workflow

**Step 1 — Identify input type**
- Wallet address (base58, 32–44 chars) → start with `solscan_account_info` → `solscan_account_tokens`
- Token mint → `solscan_token_info`
- Tx signature (~88 chars base58) → `solscan_transaction`
- Token name/symbol → `solscan_search` first to get mint
- NFT mint → `solscan_nft_info`

**Step 2 — Assess size**
If the request involves > 10 items (N wallets, N tokens, N signatures) → go to `references/batch-patterns.md` and write a script. Don't loop MCP calls.

**Step 3 — Apply Rules 1–3 above**
- Exploration: MCP directly
- Batch: script with `page_size=100`, async semaphore=25, multi-endpoints where possible
- Bulk history: export endpoints + `datafile/download`

**Step 4 — Present results**
- SOL: divide lamports by 1e9
- Tokens: divide raw amount by 10^decimals
- Address shortening: `So11...1112` (first 4 + last 4)
- Link format: `https://solscan.io/account/<addr>` or `https://solscan.io/tx/<sig>`

---

## Address formats

- Base58 strings, 32–44 chars for addresses, ~88 chars for tx signatures
- No `0x` prefix
- Well-known:
  - SOL (wrapped): `So11111111111111111111111111111111111111112`
  - USDC: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
  - USDT: `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`
  - BONK: `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263`
  - WIF: `EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm`
  - JUP: `JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN`
  - RAY: `4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R`

---

## Time parameters

All Solscan endpoints use **unix timestamps in seconds**.

- Last 24h: `from_time = now - 86400`
- Last 7d: `from_time = now - 604800`
- Last 30d: `from_time = now - 2592000`

Historical depth (see `references/limits.md`):
- Transfers: 3 years
- Balance Change: 6 months
- DeFi Activities: 6 months

---

## Error handling

- **401** → key wrong/expired. Check `SOLSCAN_API_KEY` env var
- **429** → rate limit. Back off (see `references/limits.md` — Tier 2 is 1000/min, above that you need exponential backoff or lower concurrency)
- **404 / empty `data`** → address may not exist or no activity in filter range. Widen time window, verify via `solscan_search`
- **Invalid `page_size`** → must be 10, 20, 30, 40, 60, or 100

Check consumption with `monitor/usage` endpoint if the user suspects CU drain.

---

## Reference files

- **`references/endpoints.md`** — all 50 endpoints grouped, parameters, enum values
- **`references/limits.md`** — CU model, rate limits, monthly quotas, page_size trap, history depth
- **`references/batch-patterns.md`** — when to script vs MCP, async template, multi endpoints, export workflow
- **`references/examples/fetch_defi_activities.py`** — fetch defi for N wallets (async)
- **`references/examples/batch_tx_details.py`** — 50x CU savings via `transaction/detail/multi`
- **`references/examples/export_full_history.py`** — export + poll + download for bulk
