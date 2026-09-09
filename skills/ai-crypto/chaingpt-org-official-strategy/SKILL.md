---
name: strategy
description: "Build trading strategy plans via the ChainGPT plugin: DCA (dollar-cost-averaging), grid trading, Hyperliquid funding-rate arbitrage, copy-trading from a target wallet, and DCA backtesting against historical price data. The strategy tools COMPUTE THE PLAN; Claude executes the steps one by one via Tier 1-3 tools (research, risk, dex, defi, hl, pm) — every action still gated by the mainnet acknowledgement refusal. Triggers: DCA, dollar cost average, grid trade, funding arb, copy trade, copy trading, strategy, backtest, replay strategy, recurring buy, periodic buy, ladder."
---

# ChainGPT Strategy Skill

You build trading strategy *plans* — not execute them autonomously. Every plan output by these tools lists the exact Tier 1-3 tools Claude should call to execute the steps, in order. Each executing step still goes through the existing mainnet-ack gates. This keeps the agent layer reviewable and refusal-safe.

## Tools

| Tool | What | Output |
|---|---|---|
| `chaingpt_strategy_dca_plan` | DCA schedule for one token | List of buys (timestamp + USD size) + the exact MCP calls to execute each |
| `chaingpt_strategy_grid_plan` | Grid-trading ladder | Buy + sell limit levels with sizes; HL / PM / DEX-flavored execution |
| `chaingpt_strategy_funding_arb_plan` | HL funding-rate carry suggester | Side / leverage / hourly+daily carry estimate + execution sequence |
| `chaingpt_strategy_copy_plan` | Mirror a target wallet's swaps | Step-by-step: fetch txs → decode → risk-check each outToken → scale + mirror |
| `chaingpt_backtest_dca` | Replay DCA against CoinGecko history | DCA P&L vs buy-and-hold baseline |

## Execution discipline

When the user asks "build me a DCA into ETH for $1000 over a week":

1. Call `chaingpt_strategy_dca_plan outToken=<weth-on-base> network=base totalUsd=1000 intervals=7 cadenceHours=24`
2. **Show the plan to the user.** Surface the per-buy size, cadence, and pre-flight tools. Get confirmation.
3. For each step in the plan, execute via `chaingpt_dex_build_swap_tx network=base ... acknowledgeMainnet=true`. The user signs each one externally.
4. After execution, optionally call `chaingpt_onchain_tx hash=…` to confirm fill.

Never auto-loop without the user's express turn-by-turn confirmation. If you need true automation, use a cron / scheduler tool — the strategy tools themselves don't fire orders.

## Refusal protocol

These planner tools are read-only, so they don't refuse — but the executing tools they recommend (chaingpt_dex_build_swap_tx, chaingpt_hl_place_order_payload, chaingpt_pm_place_order_payload) all require `acknowledgeMainnet: true`. Surface that to the user before any execution.

## What this skill does NOT do

- **Custody.** Plans are returned; user signs every step externally.
- **Truly autonomous execution.** No daemon, no cron loop, no auto-rebalancing. Each step is a separate user-signed transaction.
- **ERC-4337 session keys** with bounded auto-execution — deferred to a follow-up that needs its own security review.
- **Strategy persistence.** Plans aren't stored; each call recomputes. For long-running strategies, save the plan output to your own data layer.
- **Live order-management.** Cancellation + replacement is the user's responsibility; planner doesn't track open orders.

## Backtesting caveats

`chaingpt_backtest_dca` uses CoinGecko's free `/market_chart` endpoint. Caveats:
- Max 90 days of daily candles on the free tier (some coins).
- Past performance doesn't predict future performance — DCA tends to win in choppy / down-then-up markets, B&H wins in steady uptrends.
- Backtest ignores gas costs, slippage, and the bid-ask spread — real-world DCA returns will be lower.

## Credit accounting

Strategy planners + backtester cost 0 ChainGPT credits — the data comes from public APIs (Hyperliquid, CoinGecko). Credit funnel comes from the executed steps (each DEX swap triggers a `chaingpt_risk_token` pre-flight; each Aave borrow triggers a `chaingpt_defi_aave_health` read; each new-token research triggers `chaingpt_intel_token` which burns the news-fetch credit).
