---
name: ac-funding-and-basis
description: "Perpetual-futures funding and basis craft: how funding is computed and paid, funding extremes as positioning evidence (and what they cannot predict), the cash-and-carry basis trade and its arithmetic, carry economics and the full cost stack, open-interest reading across venues, the measured fact that liquidations do not cluster at funding settlement, and the carry risk register. It analyses funding and basis; it never recommends a trade, a venue, or a return. Use when asking \"funding rate\", \"basis trade\", \"cash and carry\", \"carry trade\", \"open interest\", \"is funding a signal\", \"perp funding\". Not for venue evaluation (ac-perp-venue-diligence), not for the trade record or risk budget (ac-crypto-trading-discipline), not for hunt analysis (ac-liquidation-hunt-analysis)."
license: MIT
metadata:
  domain: crypto-trading
  status: seedling
---

# ac-funding-and-basis

## Overview
The `ac-funding-and-basis` skill provides a highly rigorous, fully evidence-backed operational framework for analyzing perpetual futures funding mechanics, crowd positioning evidence, cash-and-carry basis strategies, carry return economics, open interest quadrants, liquidation cascade dynamics, and comprehensive carry risk registers. It incorporates verified empirical findings from market microstructure research, replacing market myths with measurable data to ensure precise quantitative execution across all supported derivative instruments, collateral types, asset classes, operational frameworks, execution protocols, and trading venues globally.



Primary sources used across this skill: <https://www.fsb.org/work-of-the-fsb/financial-innovation-and-structural-change/crypto-assets-and-global-stablecoins/> and <https://www.binance.com/en/support/faq/introduction-to-binance-futures-funding-rates-360033525031>.

## When to use
- Analyzing perpetual futures funding rates, premium indices, clamp functions, and exact payment calculations across major derivative exchanges.
- Constructing, executing, and monitoring cash-and-carry spot-perp or calendar basis trades with strict margin buffering and collateral management.
- Evaluating annualized carry yields, historical funding variance, capital efficiency, and total execution cost stacks.
- Interpreting open interest price quadrants, post-cascade liquidity resets, and cross-venue definition discrepancies.
- Investigating liquidation cascade timing, branching ratios, time-of-day concentration, and funding rate consequences.
- Building carry risk registers, setting automated monitoring triggers, and managing funding regime shifts or counterparty exposure.

## When NOT to use
- Evaluating perpetual futures venue safety, insurance funds, or exchange solvency (use `ac-perp-venue-diligence`).
- Recording individual live trade executions, position sizing rules, or personal risk budgets (use `ac-crypto-trading-discipline`).
- Analyzing liquidation hunt setups or stop-hunt mechanics (use `ac-liquidation-hunt-analysis`).

## Index
| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/funding-mechanics.md` | crypto-trading/funding-mechanics | Calculates funding payments, premium index, clamp mechanics, and sign conventions on perpetual futures. |
| `subskills/funding-as-positioning.md` | crypto-trading/funding-as-positioning | Evaluates perpetual funding extremes as crowd-positioning evidence, limitations, and cross-venue dispersion. |
| `subskills/basis-trade.md` | crypto-trading/basis-trade | Constructs cash-and-carry spot-perp and calendar basis trades, carry arithmetic, and risk factors. |
| `subskills/carry-economics.md` | crypto-trading/carry-economics | Analyzes annualized carry yields, funding variance, capacity constraints, and total cost stacks. |
| `subskills/open-interest-reading.md` | crypto-trading/open-interest-reading | Interprets open interest price quadrants, post-cascade resets, and cross-venue definition differences. |
| `subskills/funding-and-cascade.md` | crypto-trading/funding-and-cascade | Evaluates empirical evidence on funding settlement non-clustering, branching ratios, and funding flips. |
| `subskills/carry-risk-register.md` | crypto-trading/carry-risk-register | Registers risks, monitoring triggers, funding regime shifts, counterparty exposure, and exit liquidity. |

## Status and honest limits
Status: seedling. This skill encodes established quantitative mechanics and empirical microstructure findings. It does not provide financial advice, predict future price directions, or guarantee arbitrage returns. All carry strategies are subject to execution slippage, funding variance, margin call risks, and regime shifts. Operators must verify exchange specifications and maintain adequate collateral reserves at all times.
