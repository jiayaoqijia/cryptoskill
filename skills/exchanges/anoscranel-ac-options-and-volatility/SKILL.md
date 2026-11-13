---
name: ac-options-and-volatility
description: "Options and volatility craft for traders and investors: the greeks and what each measures, implied volatility and the surface, the common structures and when each fits, the volatility risk premium, hedging with options and its cost, execution and assignment mechanics, and the written options record. It explains mechanics and risk; it never recommends a trade, a strategy, or a direction. Use when asking \"options greeks\", \"implied volatility\", \"covered call\", \"protective put\", \"straddle\", \"volatility risk premium\", \"assignment risk\". Not for choosing the underlying instrument (ac-derivatives-instrument-selection), not for liquidation geometry (ac-liquidation-risk-management), not for hedging FX (ac-currency-and-fx-risk)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Options and volatility

## Overview

An option is a right, sold for a price, with a payoff that depends on the path and the level of the underlying. That structure gives four sensitivities — delta, gamma, theta, vega — and a market price for the right that is quoted as implied volatility rather than as a dollar amount, because the dollar price depends on inputs that change every moment.

The craft is reading those numbers honestly. Implied volatility is a price, not a forecast; the surface's shape encodes what the market pays for protection at different strikes and dates; and the volatility risk premium is a compensation for bearing risk, not a free lunch. This skill explains the mechanics and the risk; it does not pick trades.

Primary sources: <https://www.cboe.com/> and <https://www.investor.gov/introduction-investing>.

## When to use

- When an option position is being considered, opened, or reviewed.
- When implied volatility or the surface is being cited as a signal.
- When a hedge is being sized or compared with its alternatives.
- When assignment or expiry mechanics could affect the book.

## When NOT to use

- For choosing between perps, dated futures, and options at a high level (use ac-derivatives-instrument-selection).
- For liquidation distance and margin mechanics (use ac-liquidation-risk-management).
- For currency hedging with forwards (use ac-currency-and-fx-risk).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/option-greeks.md` | `crypto-trading/option-greeks` | Delta, gamma, theta, and vega, and the portfolio-level aggregation of each. |
| `subskills/implied-volatility.md` | `crypto-trading/implied-volatility` | Implied volatility, skew, and term structure, and what the surface does and does not say. |
| `subskills/option-structures.md` | `crypto-trading/option-structures` | Spreads, straddles, covered calls, and protective puts, and the exposure each creates. |
| `subskills/volatility-risk-premium.md` | `crypto-trading/volatility-risk-premium` | Implied versus realised volatility, selling versus buying volatility, and the tail that pays for the premium. |
| `subskills/hedging-with-options.md` | `crypto-trading/hedging-with-options` | Protective puts and collars, the cost of insurance, and what the hedge does not cover. |
| `subskills/option-execution.md` | `crypto-trading/option-execution` | Spreads, open interest, assignment and early exercise, and the mechanics that costs hide in. |
| `subskills/options-record.md` | `crypto-trading/options-record` | The written options record: structure, greeks, cost, maximum loss, and review triggers. |

## Status and honest limits

Options pricing models are approximations and their assumptions fail exactly when it matters: in a jump, in a liquidity hole, in a vol spike. Greeks are local derivatives that describe small moves, and a portfolio that is delta-neutral can lose heavily on a gap. Any options claim in a record should state the model and the assumption behind it, and any short-volatility position should state its maximum loss in full.
