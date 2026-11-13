---
name: ac-portfolio-leverage
description: "Borrowing against a securities portfolio: margin mechanics and maintenance requirements, the cost of leverage and its break-even, forced-sale mechanics and their tax consequence, securities-backed lending on LTV and covenants, how leverage changes drawdown arithmetic, the sizing rules that keep it survivable, and the written leverage record. It explains mechanics and risk; it never recommends borrowing and never predicts returns. Use when asking \"margin loan\", \"margin call\", \"should I use leverage\", \"securities-backed lending\", \"Lombard loan\", \"maintenance margin\", \"forced sale\". Not for perpetual-futures liquidation geometry (ac-liquidation-risk-management), not for portfolio risk budgeting across venues (ac-portfolio-construction), not for broker fee comparison (ac-broker-and-custody-selection)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Portfolio leverage

## Overview

Borrowing against a portfolio changes the arithmetic of every outcome. A portfolio with a loan against it does not merely amplify gains and losses; it acquires a boundary condition, the maintenance requirement, at which the broker sells assets without asking. That boundary converts a temporary drawdown into a permanent loss if the sale happens at the bottom, and the conversion is the whole risk.

This skill covers the mechanics of that borrowing: how margin is computed, what triggers a call, how a forced sale executes, what a securities-backed loan adds through covenants, and what the drawdown arithmetic looks like once a loan is present. It does not recommend leverage, and it does not predict the market. The purpose is to make the boundary visible before it is reached.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.finra.org/>.

## When to use

- When considering borrowing against a portfolio or using margin.
- When a maintenance requirement or a call needs understanding.
- When comparing a margin loan with a securities-backed line.
- When reviewing an existing leverage position before a market move.

## When NOT to use

- For perpetual-futures liquidation price and margin mode (use ac-liquidation-risk-management).
- For allocating risk across strategies and venues (use ac-portfolio-construction).
- For comparing broker costs and custody (use ac-broker-and-custody-selection).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/margin-mechanics.md` | `investing/margin-mechanics` | Initial and maintenance requirements, equity computation, and what actually triggers a call. |
| `subskills/cost-of-leverage.md` | `investing/cost-of-leverage` | The borrowing rate, the break-even return it implies, and the drag it adds. |
| `subskills/forced-sale-mechanics.md` | `investing/forced-sale-mechanics` | What gets sold, in what order, at what price, and the tax consequence that follows. |
| `subskills/securities-backed-lending.md` | `investing/securities-backed-lending` | LTV ratios, covenants, and the difference between a margin account and a loan against assets. |
| `subskills/leverage-and-drawdown.md` | `investing/leverage-and-drawdown` | How leverage changes recovery arithmetic and why the path matters more than the average. |
| `subskills/leverage-sizing.md` | `investing/leverage-sizing` | Choosing a ratio that survives a plausible fall, with pre-committed rules for reducing it. |
| `subskills/leverage-record.md` | `investing/leverage-record` | The written record: ratio, cost, maintenance buffer, triggers, and the forced-sale scenario. |

## Status and honest limits

Margin rules are set by the broker and the regulator, and house requirements can be raised without notice, which means a position that is comfortable today may not be tomorrow. Every calculation here depends on prices that move and on rules that change, so the record carries dates, buffers, and review triggers rather than a fixed ratio. Nothing in this skill is advice to borrow, and a leveraged position large enough to matter belongs with an adviser who can see the whole balance sheet.
