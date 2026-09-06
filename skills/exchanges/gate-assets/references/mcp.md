---
name: gate-exchange-assets-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for cross-account asset query: spot, margin, futures, options, unified, earn, tradfi and total balance aggregation."
---

# Gate Assets MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Read-only asset overview across account systems
- Account-book and holdings query
- Total balance valuation

Out of scope:
- Any trade/transfer/mutation operations

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate MCP read tools are available (`cex_wallet_get_total_balance` + account-specific reads).
2. Probe with total balance endpoint.

Fallback:
- If one account module fails, return partial asset report with degraded marker.

## 3. Authentication

- API key required for account-level read data.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

- `cex_wallet_get_total_balance`
- `cex_spot_get_spot_accounts`
- `cex_spot_list_spot_account_book`
- `cex_margin_list_margin_accounts`
- `cex_fx_get_fx_accounts`
- `cex_dc_list_dc_accounts`
- `cex_options_list_options_account`
- `cex_unified_get_unified_accounts`
- `cex_earn_list_dual_balance`
- `cex_earn_list_dual_orders`
- `cex_earn_list_structured_orders`
- `cex_tradfi_query_user_assets`

## 6. Execution SOP (Non-Skippable)

1. Identify requested account scope (all vs specific module).
2. Fetch requested modules in parallel where independent.
3. Normalize balances and valuation units.
4. Return layered summary + per-module details.

## 7. Output Templates

```markdown
## Assets Overview
- Total Balance: {total_balance}
- Spot: {spot_summary}
- Margin: {margin_summary}
- Futures/Delivery/Options: {derivatives_summary}
- Unified: {unified_summary}
- Earn/TradFi: {earn_tradfi_summary}
- Notes: {degraded_modules_or_time_window}
```

## 8. Safety and Degradation Rules

1. Keep responses strictly read-only.
2. Preserve API precision and raw valuation values.
3. Mark missing account modules explicitly.
4. Do not infer hidden balances for unavailable modules.
5. Distinguish snapshot values vs account-book historical changes.
