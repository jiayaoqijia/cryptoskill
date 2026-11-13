---
name: ac-liquidity-risk
description: "Managing liquidity as its own budget rather than a property of assets: market liquidity versus funding liquidity, days-to-liquidate at portfolio level, the liquidity ladder and its haircuts, fire-sale spirals and the discount that clears them, margin calls as a liquidity event, liquidity under stress when correlations converge, and the written liquidity record. It measures what can be sold and when; it never recommends a position and never predicts a crisis. Use when asking \"liquidity risk\", \"days to liquidate\", \"liquidity budget\", \"fire sale\", \"funding liquidity\", \"liquidity ladder\", \"how much can I exit in a week\". Not for sizing a single stock position (ac-stock-trading), not for risk budgeting across strategies (ac-portfolio-construction), not for margin mechanics on one position (ac-portfolio-leverage)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Liquidity risk

## Overview

Liquidity has two meanings that are often conflated. Market liquidity is the ability to sell an asset quickly without moving its price. Funding liquidity is the ability to raise cash when it is due. A portfolio can fail on either, and the failures reinforce each other: a margin call requires cash, raising cash requires selling, and selling an illiquid asset in a stressed market produces the loss that triggers the next call.

This skill treats liquidity as a budget that is set in advance and tested against scenarios. The unit is days: how many days of normal volume it would take to exit a position at a stated participation rate, and how those days lengthen when volume falls. A portfolio whose answer changes materially between calm and stressed conditions is a portfolio with a liquidity problem that has not yet been revealed.

Primary sources: <https://www.bis.org/> and <https://www.investor.gov/introduction-investing>.

## When to use

- When a portfolio holds assets of differing liquidity and a schedule must be met.
- When a margin call or a redemption could force selling.
- When an allocation to an illiquid asset class is being sized.
- When stress conditions are being tested against the portfolio's ability to raise cash.

## When NOT to use

- For sizing a single-name equity position (use ac-stock-trading).
- For risk budgeting across strategies and venues (use ac-portfolio-construction).
- For margin mechanics and forced-sale procedure on one position (use ac-portfolio-leverage).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/market-versus-funding-liquidity.md` | `investing/market-versus-funding-liquidity` | Two different constraints that fail in different ways. |
| `subskills/days-to-liquidate.md` | `investing/days-to-liquidate` | Participation rates, volume baselines, and the portfolio-level ladder. |
| `subskills/liquidity-ladder.md` | `investing/liquidity-ladder` | Buckets by time to cash, with haircuts applied to each. |
| `subskills/fire-sale-and-discounts.md` | `investing/fire-sale-and-discounts` | What a forced seller pays, and how the discount clears the market. |
| `subskills/margin-calls-as-liquidity.md` | `investing/margin-calls-as-liquidity` | When a collateral call becomes a cash deadline. |
| `subskills/stress-liquidity.md` | `investing/stress-liquidity` | Volume that vanishes, correlations that converge, and the changed answer. |
| `subskills/liquidity-record.md` | `investing/liquidity-record` | The written record: the ladder, the assumptions, and the trigger levels. |

## Status and honest limits

Every liquidity measure here is estimated from past volume, and past volume is the least reliable guide precisely when it matters. Assets that trade heavily in calm conditions can become untradeable in a stress event, and the correlation between assets that usually offer a choice of what to sell can converge to one exactly when the choice is needed. The record states its assumptions and the stress case, and a liquidity budget that has not been tested against a stress case is an assumption rather than a budget.
