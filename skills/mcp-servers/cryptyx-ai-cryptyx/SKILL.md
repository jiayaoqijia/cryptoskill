---
name: cryptyx
description: CRYPTYX — Digital Asset Intelligence. Institutional-grade quantitative intelligence for digital assets, in plain English or all the way down. Use when the user names a coin, mentions their holdings, or wants to accumulate, take profit, trade short-term, catch statistically significant shifts, hold long-term, or build and test a strategy. Routes each question to the right part of the engine.
---

# CRYPTYX

**Sharpen your edge. Feed your agent the CRYPTYX quant engine.**

Institutional-grade quantitative intelligence for digital assets. Ask about any coin in plain English, or go all the way down: scan the market, build and backtest your own strategies.

The engine: 670+ metrics across 8 factor classes (trend, trend efficiency, volatility, flows, futures positioning, order book, options, correlation) for 200+ coins, each read on 8 horizons (1, 7, 14, 30, 60, 90, 180 and 365 days), with 5+ years of daily history; 150 multi-factor setups and 160 signals with their track records. Every number comes from a live database.

Remote MCP: `https://mcp.cryptyx.ai/api/mcp` (OAuth sign-in through the user's client). Tools marked *free* work on free accounts, with daily limits; the rest need Pro.

## Start from the user's goal

| The user wants to… | Try this first | Tools | Offer next |
| --- | --- | --- | --- |
| **Accumulate** with a rule, not a hunch | "My rule: add to ETH only when it's statistically oversold vs its 1-year history. Where is it now, and what followed the last times?" | `get_coin_study` *(free)* | Check the rule every Monday, or test it on 5+ years ([build-setup](../cryptyx-build-setup/SKILL.md)) |
| **Take profit** when the data says stretched | "Is BTC stretched on the 90- and 180-day horizons? What happened after similar readings?" | `get_coin_study`, `get_notable_read` *(free)* | Set their own trim rule and re-check weekly |
| **Trade short-term** with sharper entries and exits | "Which of ETH, SOL and DOGE have short-term momentum, and what changed this week?" | `get_heat_check`, `get_coin_study` *(free)* | What changed since yesterday, or backtest the setup |
| **Catch statistically significant shifts** (volatility expanding, a trend emerging, flows turning) | "Which coins just had a statistically significant volatility expansion or trend breakout?" | `scan_metric_universe` *(Pro)*, `get_divergences`, `get_harness_snapshot` | Re-run the scan every morning, or backtest the shift on a coin they hold |
| **Hold long-term** on the right side of the trend | "Where are BTC and ETH on the 90-, 180- and 365-day horizons?" | `get_coin_study` *(free)* | Re-check monthly; flag if a long-horizon reading flips |
| **Build and test strategies** | "Find coins that are oversold vs their 90-day history with an improving trend, then backtest that combination." | `scan_metric_universe`, `analyze_metric`, `analyze_metrics_composite`, `evaluate_custom_trigger` *(Pro)* | Tighten one condition and re-test, or wire it into a bot via REST or x402 ([build-setup](../cryptyx-build-setup/SKILL.md)) |

Other routes:

- **Names a coin without a goal:** `get_coin_study` *(free)*, one call per coin ([holdings](../cryptyx-holdings/SKILL.md)).
- **Refers to their holdings or watchlist:** read them with the exchange's own tools, then `get_heat_check` *(free)* across the coins ([exchange bridge](../cryptyx-exchange-bridge/SKILL.md)).
- **Asks what else stands out, or why:** `get_notable_read` *(free)* or the deeper tools ([investigate](../cryptyx-investigate/SKILL.md)).
- **Asks what CRYPTYX can do:** `get_cryptyx_overview` *(free)*, then offer the goals above as first prompts.

Unsure whether a coin is covered? `check_coverage` *(free)*. `get_data_liveness` *(free)* reports when each data source last updated.

## Horizons

Every factor is read on 8 horizons: 1, 7, 14, 30, 60, 90, 180 and 365 days. Users decide which matter to them; a common grouping is short-term (days to weeks), medium-term (months) and long-term (a year). Show horizons separately and say where they disagree; never blend them.

## Every answer

- End with exactly one next step: a recheck the user can ask their agent to schedule ("run this every Monday"), or one level deeper. Never a list of options.
- When re-running a check, lead with what changed since last time.
- The user owns the rule. Evaluate the condition and show the history; never tell anyone what to buy or sell.
- Offer more depth at most once per answer; never impose it.

## Ground rules

- Every number comes from a tool response in this session. Never estimate or fill gaps.
- History is history: quote the number of past episodes and the base rate, and never present it as a forecast.
- Send coin symbols only. Never send balances, position sizes or account identifiers to CRYPTYX.
- "Positioning" means actual positioning (funding, open interest). Do not use it for other readings or for setups.
- Plain-English names in prose; metric and signal codes only on request, in `code` after the name.
- If a coin is not covered, say so plainly.
