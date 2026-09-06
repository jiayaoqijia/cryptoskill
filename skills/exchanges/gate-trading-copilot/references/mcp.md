---
name: gate-exchange-trading-copilot-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP orchestration specification for composite trading copilot workflows across info, news, spot, and futures execution layers."
---

# Gate Trading Copilot MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Composite flow: analysis -> risk gate -> order draft -> explicit confirmation -> execution -> verification
- Spot and USDT perpetual futures workflows
- Order/position management after execution

Out of scope:
- Fully automatic execution without confirmation
- Unsupported products (options/alpha/defi/copy if not explicitly covered)

Misroute examples:
- Pure welfare/kyc/pay queries should route to dedicated skills.

## 2. MCP Detection and Fallback

Detection:
1. Verify availability of required tool groups for requested flow:
   - analysis (info/news/market data)
   - execution (spot/futures private endpoints)
2. Probe with minimal read endpoints before draft/execution.

Fallback:
- If execution endpoints unavailable, stay in analysis + draft-only mode.
- If analysis endpoints are partially unavailable, continue with available evidence and clearly label confidence.

## 3. Authentication

- Analysis may include public data, but execution/management requires authenticated API key permissions.
- If auth is invalid, block write operations and return draft-only guidance.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

Tool groups (representative, not exhaustive):
- Info/News: `info_*`, `news_feed_*`
- Spot market/execution: `cex_spot_*`
- Futures market/execution: `cex_fx_*`

Calling rules:
- Do not call undocumented tool families for this skill.
- For each scenario, use only minimum necessary modules.
- For writes, preserve exact draft parameters at execution time.

Common errors:
- symbol/contract mismatch
- insufficient balance/margin
- min-notional or precision violation
- missing order/position identifiers for management actions

## 6. Execution SOP (Non-Skippable)

1. Identify task mode: decision, draft+execute, or order/position management.
2. Narrow to one trade target and market (spot or futures) before execution.
3. Build Trading Brief with risk gates.
4. Produce Order Draft only when hard blocks are absent.
5. Require explicit immediate user confirmation.
6. Execute write action.
7. Verify with read-back endpoints and return post-state.

## 7. Output Templates

```markdown
## Trading Brief
- Target: {asset_and_market}
- Signals: {market_news_technical_liquidity}
- Risks: {hard_and_soft_flags}
- Decision: {GO_CAUTION_BLOCK}
```

```markdown
## Order Draft
- Action: {buy_sell_long_short_close}
- Symbol/Contract: {market_target}
- Price Type: {limit_or_market}
- Size: {amount_or_size}
- Risk Notes: {slippage_liquidation_funding}
Reply with explicit confirmation to execute.
```

```markdown
## Execution Result
- Status: {success_or_failed}
- Order/Position ID: {id_if_available}
- Post-State: {filled_open_partially_filled_closed}
```

## 8. Safety and Degradation Rules

1. Never skip confirmation for write operations.
2. Never bypass compliance/risk hard blocks.
3. Never fabricate market evidence, fills, or position states.
4. Keep analysis-only mode when execution tools/auth are unavailable.
5. Clearly separate probabilities from certainties in recommendations.
