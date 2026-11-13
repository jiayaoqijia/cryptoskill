---
name: ac-stock-trading
description: "Trading individual equities as a venue: session structure and the overnight gap, single-name liquidity screening, earnings and event risk, halts and news, index and flow events, borrow and short-sale constraints, and the written stock trading record. It covers the recurring process of trading one name; it never recommends a stock or predicts a price. Use when asking \"should I trade this stock\", \"earnings gap risk\", \"pre-market trading\", \"LULD halt\", \"index rebalance\", \"hard to borrow\", \"position size for one stock\". Not for market-structure mechanics (ac-equity-market-structure), not for order placement tactics (ac-order-execution), not for the investment case (ac-equity-research)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Stock trading

## Overview

Trading a single stock is a different activity from owning one. The owner is exposed to the business; the trader is exposed to the order book, the calendar, and the crowd around a name. Those exposures have their own mechanics: the opening auction and the overnight gap, the spread and depth that vary enormously between a mega-cap and a small-cap, the earnings date that resets the distribution, the halt that suspends trading mid-position, and the borrow that decides whether a short can be held at all.

This skill covers those mechanics as a recurring process. It assumes the trading idea exists and asks how to express it without being surprised by the plumbing. The investment case belongs to equity research, the market's structure belongs to its own skill, and the placement of a single order belongs to execution; each is named where the boundary matters.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## When to use

- When trading an individual stock and the session, event, or liquidity mechanics matter.
- When sizing a single-name position from its liquidity rather than from conviction.
- When a halt, an earnings date, or an index event changes the plan.
- When the short side requires a borrow that may not exist or may be recalled.

## When NOT to use

- For auction, halt, and settlement mechanics in general (use ac-equity-market-structure).
- For order types, slicing, and slippage measurement (use ac-order-execution).
- For the fundamental case for a company (use ac-equity-research).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/session-structure.md` | `investing/session-structure` | Pre-market, opening auction, intraday, closing auction, and the overnight gap. |
| `subskills/single-name-liquidity.md` | `investing/single-name-liquidity` | Spread, depth, and average volume per name, and the position size they permit. |
| `subskills/earnings-and-event-risk.md` | `investing/earnings-and-event-risk` | Earnings dates, implied move, and sizing a position into a binary event. |
| `subskills/halts-and-news.md` | `investing/halts-and-news` | LULD and news-pending halts, resumption, and trading around them. |
| `subskills/index-and-flow-events.md` | `investing/index-and-flow-events` | Rebalances, lockups, offerings, and buybacks, and the flow they create. |
| `subskills/borrow-and-short-constraints.md` | `investing/borrow-and-short-constraints` | Locates, hard-to-borrow names, recall risk, and borrow cost. |
| `subskills/stock-trading-record.md` | `investing/stock-trading-record` | The written record: name, size, event plan, borrow, and review. |

## Status and honest limits

Liquidity, borrow, and halt behaviour change daily and differ by venue and by name, so every figure here is a measurement with a date rather than a property of the stock. A name that is liquid in calm conditions can be untradeable in a halt, and a borrow that costs a little today can be recalled tomorrow. Nothing here recommends a stock, and a trading process that has not accounted for these mechanics is measuring the idea rather than the trade.
