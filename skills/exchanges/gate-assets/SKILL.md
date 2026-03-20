---
name: gate-exchange-assets
version: "2026.3.12-3"
updated: "2026-03-12"
description: "Gate Exchange asset and balance query skill. Use when user asks to check total assets, account balance, specific currency holdings, or sub-account assets (spot, futures, margin, options, finance, Alpha, TradFi). Trigger phrases: 'how much do I have', 'total assets', 'account balance', 'how many BTC', 'spot balance', 'futures account', 'margin account', 'options account', 'finance account', 'Alpha account', 'TradFi account'. Read-only, no trading."
---

# Gate Exchange Assets Assistant

Execute read-only asset and balance queries for Gate Exchange. Target users: external developers integrating Gate MCP, and end users (traders) who want quick asset overview, sub-account or currency-specific balance.

## Domain Knowledge

### MCP Tool Mapping (Gate gate-mcp)

| MCP Tool | Purpose | Key Fields |
|----------|---------|------------|
| `cex_wallet_get_total_balance` | Total balance (all sub-accounts, ~1min cache) | total.amount, details (spot/futures/delivery/finance/quant/meme_box/options/payment/margin/cross_margin) |
| `cex_spot_get_spot_accounts` | Spot balance (filter by currency) | currency, available, locked |
| `cex_unified_get_unified_accounts` | Unified account (single/cross/portfolio margin) | balances, unified_account_total, margin_mode |
| `cex_fx_get_fx_accounts` | Perpetual (settle=usdt or btc) | total, unrealised_pnl, available, point, bonus |
| `cex_delivery_list_delivery_accounts` | Delivery (settle=usdt) | total, unrealised_pnl, available |
| `cex_options_list_options_account` | Options | total_value, unrealised_pnl, available |
| `cex_margin_list_margin_accounts` | Isolated margin | currency_pair, mmr, base/quote (available/locked/borrowed/interest) |
| `cex_tradfi_query_user_assets` | TradFi assets | USDx balance, margin |
| `cex_earn_list_dual_balance`, `cex_earn_list_dual_orders`, `cex_earn_list_structured_orders` | Finance | Flexible savings / Dual currency / Structured |
| `cex_spot_list_spot_account_book` | Spot account book / ledger | ledger entries |

### Account Name Mapping (details key → Display)

| API key | Display |
|---------|---------|
| spot | Spot account / Trading account |
| futures | Futures account (USDT perpetual) |
| delivery | Delivery contract account |
| options | Options account |
| finance | Finance account |
| quant | Quant/bot account |
| meme_box | Alpha account |
| margin | Isolated margin account |
| cross_margin | Cross margin account |
| payment | Payment account (not in total) |

### Key Rules

- **Read-only**. No trading, transfer, or order placement.
- **TradFi / payment**: USDx and payment assets are NOT included in CEX total; display separately.
- **Unified account**: When margin_mode is classic/cross_margin/portfolio, spot may be merged into "trading account". Do NOT use internal terms like "advanced mode", "S1/S2".
- **Pair format**: Futures use no-slash (BTCUSDT); spot/margin use slash (BTC/USDT).
- **Precision**: Fiat valuation 2 decimals; dust (<$0.01) show as `<$0.01`; finance yesterday PnL up to 8 decimals.

## Case Routing Map

### I. Total & Overview (Case 1)

| Case | Trigger Phrases | MCP Tool | Output |
|------|-----------------|----------|--------|
| 1 | "How much do I have", "Show my CEX total assets", "Account asset distribution", "Account overview", "Check my balance" | `cex_wallet_get_total_balance` currency=USDT | Total amount, account distribution, coin distribution; TradFi/payment listed separately if any |

### II. Specific Currency (Case 2)

| Case | Trigger Phrases | MCP Tool | Output |
|------|-----------------|----------|--------|
| 2 | "How many BTC do I have", "How many USDT do I have" | Concurrent: `cex_spot_get_spot_accounts`, `cex_unified_get_unified_accounts`, `cex_fx_get_fx_accounts`, `cex_delivery_list_delivery_accounts`, `cex_margin_list_margin_accounts`, `cex_earn_list_dual_balance`, etc. | Total {COIN} held, distribution by account |

### III. Specific Account + Currency (Case 3)

| Case | Trigger Phrases | MCP Tool | Output |
|------|-----------------|----------|--------|
| 3 | "How much USDT in my spot account", "How much BTC in my spot account" | `cex_spot_get_spot_accounts` currency={COIN} or `cex_unified_get_unified_accounts` currency={COIN} | Account name, total, available, locked |

### IV. Sub-Account Queries (Case 4–15)

| Case | Account | Trigger Phrases | MCP Tool |
|------|---------|-----------------|----------|
| 4 | Spot | "What's in my spot account", "Show my spot account assets" | `cex_spot_get_spot_accounts` or `cex_unified_get_unified_accounts` |
| 5 | Futures | "How much in futures account", "USDT perpetual", "BTC perpetual", "Delivery" | `cex_fx_get_fx_accounts` settle=usdt/btc, `cex_delivery_list_delivery_accounts` |
| 6 | Trading (Unified) | "How much in trading account", "How much in unified account" | `cex_unified_get_unified_accounts` |
| 7 | Options | "How much in options account", "Show my options assets" | `cex_options_list_options_account` or `cex_unified_get_unified_accounts` |
| 8 | Finance | "How much in finance account", "Show my finance account assets" | `cex_earn_list_dual_balance`, `cex_earn_list_dual_orders`, `cex_earn_list_structured_orders` |
| 9 | Alpha | "How much in Alpha account", "Show my Alpha assets" | `cex_wallet_get_total_balance` details.meme_box |
| 12 | Isolated Margin | "How much in isolated margin account", "Show my isolated margin assets" | `cex_margin_list_margin_accounts` |
| 15 | TradFi | "How much in TradFi account", "Show my TradFi assets" | `cex_tradfi_query_user_assets` |

### V. Account Book (Legacy 5–7)

| Case | Intent | MCP Tool |
|------|--------|----------|
| 5 | Account book for coin | `cex_spot_list_spot_account_book` |
| 6 | Ledger + current balance | `cex_spot_list_spot_account_book` → `cex_spot_get_spot_accounts` |
| 7 | Recent activity | `cex_spot_list_spot_account_book` |

## Special Scenario Handling

| Scenario | Handling |
|----------|----------|
| Total < 10 USDT | Show small-asset tip; recommend [Deposit] or [Dust conversion] |
| Unified account migration | "Your account is upgrading to unified account, asset data may be incomplete, please retry in ~5 minutes" |
| Dust (>10 dust coins) | "~${total_val} dust across {N} currencies" → [Dust conversion] |
| API timeout/error | "Data fetch error, please retry later" → [Refresh] |
| Account/coin balance = 0 | Do NOT show "your xx account is 0"; skip that item |
| USDT + TradFi | Show TradFi (USDx) separately; "TradFi in USDx, 1:1 with USDT, not in CEX total" |
| GTETH / voucher tokens | Explain: On-chain earn voucher, cannot withdraw to chain |
| ST token | Risk warning, suggest checking official announcements |
| Delisted token | Explain delisting, suggest withdrawal |
| Unified account, user asks "spot" | Inform spot merged into trading account; show trading account balance |

## Output Templates

**Case 1 – Total Balance:**
```
Your total CEX asset valuation ≈ ${total.amount} USDT
🕒 Updated: {time} (UTC+8)
💰 Account distribution: details keys (spot/futures/delivery etc.) amount, show only amount > 0
```

**Case 2 – Specific Currency:**
```
You hold {total_qty} {COIN} (≈ ${total_val} USDT)
🕒 Updated: {time} (UTC+8)
💰 Asset distribution: {account}: {qty} {COIN}, ≈ ${val} ({pct}%)
```

**Case 15 – TradFi:**
```
Your TradFi account details:
Net value: {net_value} USDx | Balance: {balance} USDx | Unrealised PnL: {unrealised_pnl} USDx
Margin: {margin} USDx | Available margin: {available_margin} USDx | Margin ratio: {ratio}% (max 999+%)
⚠ TradFi account in USDx, 1:1 with USDT, not in CEX total valuation.
```

## Acceptance Test Queries (Validation)

| Scenario | Query |
|----------|-------|
| Total balance – normal | How much do I have? |
| Total balance – overview | Show my CEX total assets |
| Total balance – small (<10U) | My account asset distribution |
| Specific currency – normal | How many BTC do I have? |
| Specific currency – zero | How much DOGE do I have? |
| Specific account+currency | How much USDT in my spot account? |
| Spot account | What's in my spot account? |
| Futures – with assets | How much in futures account |
| Futures – USDT+BTC perpetual | Show my perpetual contract assets |
| Futures – no assets | Show my USDT perpetual assets |
| Trading account | How much in trading account |
| Options | Show my options assets |
| Alpha | How much in Alpha account |
| Isolated margin | Show my isolated margin assets |
| TradFi | How much in TradFi account |

## Cross-Skill Workflows

- **Before trading**: User asks "Can I buy 100U BTC?" → This skill: `cex_spot_get_spot_accounts` currency=USDT → Route to `gate-exchange-spot` if sufficient.
- **After transfer**: Route to this skill for updated balance when user asks.
- **Transfer card**: When futures/options = 0, recommend [Transfer] and trigger transfer skill.

## Safety Rules

- **Read-only only**. Never call create_order, cancel_order, create_transfer, or any write operation.
- If user intent includes trading, transfer, or order placement → route to appropriate skill.
- Always clarify currency and scope (spot vs all wallets) when ambiguous.

For detailed scenario templates and edge cases, see [references/scenarios.md](references/scenarios.md).
