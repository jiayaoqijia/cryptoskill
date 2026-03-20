---
name: gate-exchange-staking
version: "2026.3.12-1"
updated: "2026-03-13"
description: "The on-chain staking query function of Gate Exchange. Use this skill to query staking positions, rewards, products, or order history. Trigger phrases include: staking, stake, earn, staking rewards, staking positions, earning records, staking history, available coins."
---

# Gate Staking Query Suite

## General Rules

Read and follow the shared runtime rules before proceeding:
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

---

This skill is the single entry for Gate Exchange staking (on-chain earn) **query-only** operations. It supports **four query modules**: positions, rewards, products, order history. User intent is routed to the matching reference and MCP tool.

## Module overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Positions** | Query staking positions, balances, available vs locked | `position`, `balance`, `staked`, `staking assets`, `holdings`, `redeemable` |
| **Rewards** | Query reward history, yesterday/monthly earnings | `reward`, `earning`, `profit`, `income`, `yesterday earnings`, `monthly earnings` |
| **Products** | Discover available staking products, APY, min amount | `products`, `available`, `APY`, `stakeable coins`, `high yield`, `flexible` |
| **Order history** | Query stake/redeem order list and pagination | `history`, `orders`, `transactions`, `staking records`, `redemption records` |

**Stake / Redeem (not supported)**: When the user intends to **perform** a stake or redeem operation, do not call any tool. Reply that the operation is temporarily not supported and offer query alternatives (e.g. show positions or products).

**Mint (not supported)**: When the user intends to **perform** a mint operation, do not call any tool. Reply that the operation is temporarily not supported and offer query alternatives.

## Domain Knowledge

### Product types

| productType | Label | Description |
|-------------|-------|-------------|
| 0 | Certificate | Flexible staking with instant redemption (redeemPeriod = 0) |
| 1 | Lock-up | Fixed-term staking with a defined lock period (redeemPeriod > 0) |
| 2 | US Treasury Bond | Products backed by US Treasury bonds (e.g. GUSD). Users stake crypto and receive yield derived from US Treasury interest rates. Typically has a fixed or semi-fixed APR with low risk. |

### Redeemable amount calculation

The redeemable amount for a position is **not** `mortgage_amount − freeze_amount`. The correct formula is:

```
redeemable = mortgage_amount × exchangeRate
```

Where `exchangeRate` comes from `cex_earn_find_coin` for the same `pid` and matching `currency`. Some products have exchangeRate = 1 (e.g. USDT flexible), while others vary (e.g. liquid staking tokens).

### Reward distribution

- `reward_delay_days = -1` means the reward is paid **on redeem**, not periodically.
- `interest_delay_days` indicates the delay after staking before rewards start accruing (typically 1 day / T+1).
- Multi-coin rewards: a single position can generate rewards in multiple coins (e.g. stake USDT in Compound V3, receive USDT + COMP).

### Number formatting

| Category | Precision | Trailing zeros | Examples |
|----------|-----------|----------------|----------|
| General amounts (mortgage_amount, freeze_amount, income_total, fee, etc.) | 8 decimals | Removed | `1.23` not `1.23000000`; `100` not `100.00000000` |
| Rate fields (estimateApr, APY, APR, exchangeRate) | 2 decimals | Retained | `5.20%` not `5.2%`; `8.00%` not `8%` |

## Routing rules

| Intent | Example phrases | Route to |
|--------|-----------------|----------|
| **Positions** | "Show my staking positions", "Check my staking assets", "What can I unstake?" | Read `references/staking-assets.md` |
| **Rewards** | "Staking rewards", "Yesterday's earnings", "Monthly earnings", "Earning records" | Read `references/staking-list.md` (Part 2: Reward List) |
| **Products** | "Available staking", "Stakeable coins", "Best APY", "Flexible only" | Read `references/staking-coins.md` |
| **Order history** | "Staking history", "Staking records", "Show redemptions", "Recent activity" | Read `references/staking-list.md` (Part 1: Order List) |
| **Stake / Redeem (not supported)** | "Stake 1 BTC", "Stake 100 USDT", "Redeem my ETH", "redeem", "I want to stake", "help me redeem" | **Do not call tools.** Reply in English: Staking and redemption are not supported here; please use the Gate website or app. I can help you query positions or products. |
| **Mint (not supported)** | "mint", "I want to mint", "Mint", "mint GT", "help me mint" | **Do not call tools.** Reply in English: Mint is not supported here; please use the Gate website or app. I can help you query positions or products. |
| **Unclear** | "Help with staking", "on-chain earn" | **Clarify**: positions / rewards / products / history, then route |

## Execution

### 1. Intent and parameters

- Determine module (Positions / Rewards / Products / Order history) **or** whether the user intends to **perform stake/redeem** **or** **mint**.
- **Stake / Redeem intent**: If the user clearly wants to **execute** a stake or redeem—e.g. "stake 1 BTC", "stake 100 USDT", "redeem", "I want to stake", "help me redeem"—**do not** call any MCP tool. Reply with the **not supported** message (see Safety rules) and offer to query positions or products instead. Then stop.
- **Mint intent**: If the user clearly wants to **execute** a mint—e.g. "mint", "I want to mint", "mint GT", "help me mint"—**do not** call any MCP tool. Reply with the **not supported** message (see Safety rules) and offer to query positions or products instead. Then stop.
- Extract: `coin`, `pid`, `page`; for order list also `type` (0=stake, 1=redeem).
- **Missing**: if user says "my staking" without specifying positions/rewards/products/history, ask which one or show positions by default.

### 2. Tool selection

| Module | MCP tool | Optional params |
|--------|----------|-----------------|
| Positions | `cex_earn_asset_list` | `coin`, `pid` |
| Rewards | `cex_earn_award_list` | `coin`, `pid`, `page` |
| Products | `cex_earn_find_coin` | `cointype` |
| Order history | `cex_earn_order_list` | `coin`, `pid`, `type`, `page` |

- **Positions**: When showing redeemable amount, call **`cex_earn_find_coin`** (optionally with `cointype`), find the product with same **pid** and matching **currency** as each position; use that item’s **exchangeRate** (or **exchangeRateReserve** per API). Redeemable = mortgage_amount × that rate. Do not use mortgage_amount − freeze_amount.
- Response structures: **Positions** → array of items (pid, mortgage_coin, mortgage_amount, freeze_amount, income_total, yesterday_income / yesterday_income_multi, etc.). **Redeemable** is **not** mortgage_amount − freeze_amount; redeemable = mortgage_amount × exchange rate, where exchange rate comes from **`cex_earn_find_coin`** for the same **pid** and matching **currency** (coin). **Order list** → object with page, pageSize, pageCount, totalCount, list[]. **Reward list** → object with page, pageSize, pageCount, totalCount, list[] (pid, mortgage_coin, reward_coin, interest, bonus_date, etc.). **Products** → array (pid, currency, estimateApr, minStakeAmount, protocolName, redeemPeriod, productType, isDefi, currencyRewards, **exchangeRate**, etc.).

### 3. Format response

- Use the **Response Template** and field names from the reference file for the chosen module.
- Positions: show mortgage_amount, freeze_amount, **redeemable** (mortgage_amount × exchange rate; get exchange rate from **`cex_earn_find_coin`** for the same **pid** and matching **currency**), income_total, yesterday_income; group by coin or show per pid. Do not use mortgage_amount − freeze_amount for redeemable.
- Rewards: show list entries with reward_coin, interest, bonus_date, pid, mortgage_coin; sum by reward_coin; use totalCount/page/pageCount when relevant.
- Products: show protocolName, currency, estimateApr, minStakeAmount, maxStakeAmount, redeemPeriod, productType, isDefi; sort by estimateApr or filter by cointype.
- Order history: show list with coin, amount, type (0=Stake, 1=Redeem), createStamp, status, pid, fee; use totalCount, page, pageCount for pagination.

## Report template

After each query, output a short standardized result consistent with the reference (e.g. positions summary, reward summary, product table, or order list). Use the exact response fields from the API (see references) so the user sees correct field names and values.

## Safety rules

### Read-only

- This skill **does not** perform stake, redeem, or mint. Only query tools are used.
- **Stake / Redeem intent**: When the user asks to **perform** a stake or redeem, reply **in English**: "Staking and redemption are not supported here; please use the Gate website or app. I can help you query positions or products." Do **not** call any tool. Optionally offer to show current positions (`cex_earn_asset_list`) or available products (`cex_earn_find_coin`).
- **Mint intent**: When the user asks to **perform** a mint, reply **in English**: "Mint is not supported here; please use the Gate website or app. I can help you query positions or products." Do **not** call any tool. Optionally offer to show positions or products.

### Errors

| Scenario | Action |
|----------|--------|
| Empty positions (`list` empty or totalCount 0) | "You don't have any staking positions. Browse available products to start earning." Suggest `references/staking-coins.md`. |
| No rewards yet | "No rewards found. Rewards typically start accruing 24 hours after staking." Optionally show positions from `cex_earn_asset_list`. |
| Product not found / no capacity | Suggest alternatives from `cex_earn_find_coin()` (e.g. by estimateApr). |
| API error / 401 | "Unable to fetch staking data. Please try again later." or "Please log in to view staking data." |
