---
name: ac-forex-trading
description: "Trading spot foreign exchange as a venue: quoting conventions and pip value, venue types and spread quality, rollover and swap points, session liquidity and fixing windows, leverage and weekend gap risk, a repeatable trade process, and the written FX trading record. It explains the mechanics of the market you trade in; it never recommends a currency pair or predicts an exchange rate. Use when asking \"how do pips work\", \"forex lot size\", \"rollover swap\", \"ECN or market maker\", \"forex leverage\", \"trading the London fix\", \"why is my EURUSD spread wide at night\". Not for hedging a portfolio's currency exposure (ac-currency-and-fx-risk), not for emerging-market convertibility (ac-currency-and-fx-risk), not for general order placement (ac-order-execution)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Forex trading

## Overview

Spot foreign exchange is an over-the-counter market with no single venue, no consolidated tape, and no closing price. What a trader sees is a price stream from one liquidity provider or aggregator, and what a trader pays is that price plus a spread, a commission, or a markup embedded in the rate. Understanding that structure explains most of the surprises: spreads that widen at the session change, fills that differ from the screen, and a funding charge that appears on the statement.

This skill covers the mechanics of trading the market rather than the case for any currency view. It deals with quotation, sizing, venue quality, rollover, sessions, leverage, and the process and record that make FX trading reviewable. Currency risk inside an investment portfolio is a different problem with a different skill, and the boundary between them is stated in every leaf.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## When to use

- When trading spot FX and the mechanics of the quote or the position need to be exact.
- When comparing FX venues, spread quality, and execution.
- When rollover, swap, or financing charges appear on a statement.
- When sizing a position across pairs with different quotation conventions.

## When NOT to use

- For hedging foreign holdings in a portfolio (use ac-currency-and-fx-risk).
- For convertibility and devaluation risk in emerging markets (use ac-currency-and-fx-risk).
- For generic order types and slicing (use ac-order-execution).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/fx-quoting-and-pip-value.md` | `investing/fx-quoting-and-pip-value` | Base and quote conventions, pip, lot size, and profit in the account currency. |
| `subskills/fx-venues-and-spreads.md` | `investing/fx-venues-and-spreads` | ECN, market maker, prime brokerage, last look, and what a quoted spread really includes. |
| `subskills/fx-rollover-and-swap.md` | `investing/fx-rollover-and-swap` | Tom-next, swap points, carry, and the triple swap that arrives weekly. |
| `subskills/fx-sessions-and-liquidity.md` | `investing/fx-sessions-and-liquidity` | Session overlaps, fixing windows, liquidity holes, and intervention risk. |
| `subskills/fx-leverage-and-margin.md` | `investing/fx-leverage-and-margin` | Retail leverage caps, margin computation, and the weekend gap. |
| `subskills/fx-trade-process.md` | `investing/fx-trade-process` | The repeatable decision process: thesis, event calendar, sizing, invalidation. |
| `subskills/fx-trading-record.md` | `investing/fx-trading-record` | The written record: pair, size, rate, carry, invalidation, and review. |

## Status and honest limits

FX is a zero-sum, dealer-dominated market with no central exchange, and retail participants trade a fraction of its volume through intermediaries whose interests are not identical to theirs. The mechanics here are stable; the costs and the venue behaviour are not, and they change with volatility. Nothing in this skill is a view on any currency, and a strategy that has not been measured net of spread, commission, and swap is a strategy that has not been measured.
