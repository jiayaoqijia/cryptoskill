---
name: ac-equity-index-futures
description: "Trading equity index futures as a venue: contract multipliers and cash settlement, fair value and the basis, the quarterly roll, the overnight session and gap risk, hedging a portfolio with contracts, index futures versus the ETF alternative, and the written record. It explains how the contract behaves; it never recommends a position or predicts an index. Use when asking \"ES contract size\", \"fair value of the future\", \"spread between futures and cash\", \"index futures roll\", \"hedge my portfolio with futures\", \"futures or ETF\", \"overnight session liquidity\". Not for single-stock trading (ac-stock-trading), not for portfolio risk budgeting (ac-portfolio-construction), not for options on indices (ac-options-and-volatility)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Equity index futures

## Overview

An equity index future is an agreement to settle, in cash, the difference between an index level at expiry and the price agreed. There is no delivery, no basket, and no conversion factor; the contract is a pure cash settlement on a published index, and everything that makes it interesting follows from that: the basis to the cash index, the quarterly roll, the nearly continuous session, and the leverage that comes with a small margin against a large notional.

This skill covers the mechanics of trading that contract and using it as a hedge. It is not about picking a direction; it is about knowing what the price means relative to the cash market, when the contract must be rolled, how it behaves outside the cash session, and how many contracts a portfolio actually needs. Single-stock trading and options are separate skills, and the boundaries are stated.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## When to use

- When trading an index future and the basis or multiplier matters.
- When rolling from one quarterly contract to the next.
- When hedging a portfolio with futures rather than selling holdings.
- When comparing a futures position with the equivalent ETF exposure.

## When NOT to use

- For trading individual stocks (use ac-stock-trading).
- For sizing risk across a portfolio of strategies (use ac-portfolio-construction).
- For index options and volatility (use ac-options-and-volatility).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/index-futures-specs.md` | `investing/index-futures-specs` | Multiplier, tick, expiry cycle, cash settlement, and margin. |
| `subskills/fair-value-and-basis.md` | `investing/fair-value-and-basis` | Cost of carry, dividends, and the difference between fair value and the traded basis. |
| `subskills/roll-and-expiry.md` | `investing/roll-and-expiry` | The quarterly roll, roll yield, and the calendar spread between contracts. |
| `subskills/overnight-session.md` | `investing/overnight-session` | Nearly continuous trading, session liquidity, and the gap when cash opens. |
| `subskills/hedging-with-index-futures.md` | `investing/hedging-with-index-futures` | Beta, contract count, and tracking error between a portfolio and the index. |
| `subskills/futures-versus-etf.md` | `investing/futures-versus-etf` | Financing, dividends, tax, leverage, and the trade-offs between the two vehicles. |
| `subskills/index-futures-record.md` | `investing/index-futures-record` | The written record: contract, basis, roll plan, hedge ratio, and margin. |

## Status and honest limits

The basis is a financing relationship that moves with rates and dividends, so a fair value computed today is not a fair value next week. Futures are leveraged instruments: the margin is a performance bond, not a cap on loss, and a gap can require funding before the position is closed. Nothing here recommends a position, and a hedge that has not been measured against the portfolio's actual beta is a hedge with an unknown residual.
