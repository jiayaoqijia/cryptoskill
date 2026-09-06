---
name: gate-exchange-staking-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for staking/earn staking flows: staking assets, rewards, orders, and stake/redeem actions."
---

# Gate Staking MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Staking asset/reward/order queries
- Staking coin discovery
- Stake/redeem execution

Out of scope:
- Non-staking trading actions

## 2. MCP Detection and Fallback

Detection:
1. Verify staking-related `cex_earn_*` tools.
2. Probe with `cex_earn_asset_list`.

Fallback:
- If write endpoint unavailable, provide read-only staking status.

## 3. Authentication

- API key required.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

- `cex_earn_asset_list`
- `cex_earn_award_list`
- `cex_earn_find_coin`
- `cex_earn_order_list`
- `cex_earn_swap_staking_coin`

## 6. Execution SOP (Non-Skippable)

1. Resolve user intent: query vs stake/redeem.
2. For stake/redeem, pre-check coin and amount validity.
3. Show stake/redeem draft with operation side and amount.
4. Require explicit confirmation.
5. Execute and verify through order/asset query.

## 7. Output Templates

```markdown
## Staking Action Draft
- Action: {stake_or_redeem}
- Coin: {coin}
- Amount: {amount}
- Notes: {protocol_or_limit}
Reply "Confirm action" to proceed.
```

```markdown
## Staking Result
- Status: {success_or_failed}
- Coin/Amount: {coin} {amount}
- Updated Position: {position_summary}
```

## 8. Safety and Degradation Rules

1. Never execute stake/redeem without explicit immediate confirmation.
2. Preserve operation side (`stake` vs `redeem`) exactly.
3. If amount/coin invalid, block and explain constraints.
4. Keep read-only fallback when write path is unavailable.
5. Do not fabricate reward projections.
