---
name: cdcx-autonomy-levels
description: Progressive agent autonomy — from read-only to fully autonomous. Pick the lowest level that gets the job done.
---

# Autonomy Levels

## Philosophy

Agents should operate at the lowest autonomy level that accomplishes their task. Each level upward trades human oversight for agent independence.

## Safety Tiers (the underlying mechanism)

Every cdcx MCP tool is classified into one of four tiers:

| Tier             | Agent Behaviour                                      | Example                            |
|------------------|------------------------------------------------------|------------------------------------|
| `read`           | Runs freely, no acknowledgement                      | `cdcx_market_ticker`               |
| `sensitive_read` | Runs freely, no acknowledgement                      | `cdcx_account_summary`             |
| `mutate`         | Requires `acknowledged: true` in tool arguments      | `cdcx_trade_order`                 |
| `dangerous`      | Refused unless server was started `--allow-dangerous`| `cdcx_trade_cancel_all`, `cdcx_funding_withdraw` |

## Level 0 — Read-only

Agent can observe the market but cannot touch the account.

```bash
cdcx mcp config --reset   # ensures only market is enabled
```

Use for: market research agents, price alerts, chart commentary.

## Level 1 — Paper

Agent can read live market data plus read authenticated account info; any actual trading is paper-only and handled CLI-side (not via MCP).

```bash
cdcx mcp config --enable account
```

Pair the MCP server with shell access to `cdcx paper` for simulated execution. Paper has no MCP tools; execution stays outside the agent's tool surface.

Use for: strategy research with real account context, backtest harnesses.

## Level 2 — Supervised Live

Agent can place and cancel real orders, but every mutation requires explicit acknowledgement from the host application (human-in-the-loop).

```bash
cdcx mcp config --enable account,trade,advanced
```

The agent calls `cdcx_trade_order`; the host MUST echo the intent to the human and only pass `acknowledged: true` once approved. Dangerous tools (`cancel-all`, `withdraw`) are refused at the server since `allow_dangerous` is not set.

Use for: semi-automated trading with human oversight, production with guardrails.

## Level 3 — Autonomous

Agent executes anything without per-call confirmation. Dangerous tier is available.

```bash
cdcx mcp config --enable account,trade,advanced,funding
cdcx mcp config --allow-dangerous
```

Even at level 3, `mutate` tools still require `acknowledged: true` in the tool arguments — but an autonomous agent will pass it automatically without a human prompt. `--allow-dangerous` additionally unlocks cancel-all and withdrawals.

Use for: fully automated strategies with external risk controls (position limits, drawdown circuit breakers, monitoring alerts). Rare in production.

## Promotion Criteria

| From → To | Requirement |
|-----------|-------------|
| 0 → 1 | Agent correctly interprets market data, no hallucinated instruments |
| 1 → 2 | Strategy is profitable or sound on paper; agent handles API errors gracefully |
| 2 → 3 | Agent has operated supervised without unexpected actions for a meaningful period |

## Service Group Reference

Valid MCP service groups: `market`, `account`, `trade`, `advanced`, `margin`, `staking`, `funding`, `fiat`, `otc`, `stream`.

- `account` also exposes `history` (orders/trades/transactions)
- `funding` maps to the `wallet` CLI group (deposit/withdraw/networks)
- `paper` is **not** an MCP group — paper trading is CLI-only
- `cdcx mcp config --enable all` is a shortcut to enable everything

## Notes

- Withdrawals (`funding withdraw`) should only be unlocked at Level 3 and only with `--allow-dangerous`; they are the highest-risk action available
- You can run multiple cdcx MCP servers side by side with different autonomy levels (one agent at level 1, another at level 2)
- `allow_dangerous` only affects the dangerous tier. Mutate tools always need `acknowledged: true` regardless
