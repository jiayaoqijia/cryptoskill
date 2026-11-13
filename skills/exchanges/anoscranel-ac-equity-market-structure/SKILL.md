---
name: ac-equity-market-structure
description: "How equity markets actually execute: opening and closing auctions, halts and circuit breakers, short-selling mechanics and borrow, venue routing and dark pools, tick and lot mechanics, settlement and clearing, liquidity measurement, and the written market-structure record. It explains mechanics and risk; it never recommends a security or a venue. Use when asking \"how do auctions work\", \"circuit breaker\", \"short selling mechanics\", \"dark pools\", \"order routing\", \"settlement\", \"market structure\". Not for order-type selection on a single trade (ac-order-execution), not for crypto venue diligence (ac-perp-venue-diligence), not for equity research (ac-equity-research)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Equity market structure

## Overview

An equity order does not go to "the market"; it goes to a venue, at a time, under rules that determine what price you get and whether the order fills at all. The opening and closing auctions set the day's reference prices. Halts stop trading when the rules say so, not when it would be convenient. Short selling requires a borrow that can be recalled. And most retail orders never reach an exchange at all.

This skill is the mechanical layer beneath any equity decision. It does not pick stocks or venues; it tells you what the mechanism will do to your order, and which features of the mechanism are worth recording before you rely on them.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## When to use

- When order timing matters: auctions, halts, and thin periods.
- When a short position is being opened and the borrow terms matter.
- When execution quality or routing is being assessed.
- When settlement timing affects cash availability.

## When NOT to use

- For choosing an order type on one trade (use ac-order-execution).
- For crypto venues and perp mechanics (use ac-perp-venue-diligence, ac-funding-and-basis).
- For company fundamentals (use ac-equity-research).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/auctions-and-halts.md` | `investing/auctions-and-halts` | Opening and closing auctions, limit-up and limit-down halts, and circuit breakers. |
| `subskills/short-selling-mechanics.md` | `investing/short-selling-mechanics` | Borrow, recall, short interest, and the mechanics of a squeeze. |
| `subskills/venues-and-routing.md` | `investing/venues-and-routing` | Exchanges, alternative venues, dark pools, and how retail orders are routed and paid for. |
| `subskills/tick-and-lot-mechanics.md` | `investing/tick-and-lot-mechanics` | Tick sizes, lot sizes, minimum increments, and price improvement. |
| `subskills/settlement-and-clearing.md` | `investing/settlement-and-clearing` | Settlement cycles, clearing, fails to deliver, and the counterparty in the middle. |
| `subskills/liquidity-measurement.md` | `investing/liquidity-measurement` | Quoted versus traded liquidity, spreads, depth, and impact proxies. |
| `subskills/market-structure-record.md` | `investing/market-structure-record` | The written record: venue, timing, mechanics relied on, and what could invalidate them. |

## Status and honest limits

Market structure changes: rules are amended, venues merge, and settlement cycles shorten. Every mechanic here is described as a structure to verify against current rules before relying on it in a live decision. The skill's value is the list of questions and the record of what was assumed, not a permanent description of any exchange's behaviour.
