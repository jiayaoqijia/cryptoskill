---
name: ac-crypto-trading-discipline
description: "The documented decision process of discretionary crypto trading. It governs how a trade decision is made, sized, invalidated, recorded, and reviewed. It never says what to buy, which direction to take, what size to use, or when to enter: every threshold in this skill is the operator's own stated parameter. Use when asking 'trade journal', 'pre-trade memo', 'risk budget', 'position sizing', 'when to exit a position', 'review my trades', 'trading discipline'. Not for recommending assets or directions (this skill records decisions, it does not make them), not for personal financial planning, not for portfolio construction theory."
license: MIT
metadata:
  domain: crypto-trading
---

# Crypto Trading Discipline

## Overview

The documented decision process of discretionary crypto trading. It governs how a trade decision is made, sized, invalidated, recorded, and reviewed. It never says what to buy, which direction to take, what size to use, or when to enter: every threshold in this skill is the operator's own stated parameter. The record is the deliverable; the decision is the operator's. Craft, not advice.

## When to use

- Establishing a structured pre-trade memo and audit trail before entering any market exposure.
- Setting account risk budgets, aggregate open risk caps, and drawdown preservation reserves.
- Deriving position size mathematically from invalidation distance and risk budgets rather than conviction.
- Pre-committing invalidation conditions and kill criteria across price, time, thesis, and data dimensions.
- Journaling trades and conducting outcome versus process reviews on a structured periodic cadence.
- Implementing mechanical behavioral rails against revenge trading, size escalation, thesis drift, and action bias.
- Running a one-person desk routine with clear role separation between analyst and risk manager personas.

## When NOT to use

- Recommending specific assets, directions, or entry targets; this skill records decisions and enforces discipline, but it never makes trading choices.
- Personal financial planning, wealth management advisory, or retirement capital allocation.
- Academic portfolio construction theory or quantitative asset pricing model development.

## Subskill index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/pre-trade-memo.md` | crypto-trading/pre-trade-memo | The decision record written before exposure: thesis, evidence, invalidation, size, and book state |
| `subskills/risk-budget.md` | crypto-trading/risk-budget | The account-level budget: maximum fraction per decision, aggregate cap across correlated risk, and drawdown reserve |
| `subskills/position-sizing.md` | crypto-trading/position-sizing | Deriving size from invalidation distance and risk budget rather than conviction; volatility and liquidity adjustments |
| `subskills/invalidation-and-kill.md` | crypto-trading/invalidation-and-kill | Pre-committed invalidation conditions (price, time, thesis, data); kill criteria closing positions; review triggers |
| `subskills/journal-and-review.md` | crypto-trading/journal-and-review | The journal as audit trail: memo reference, execution, exit reason, evidence; outcome vs process review; periodic cadence |
| `subskills/behavioral-rails.md` | crypto-trading/behavioral-rails | Documented failure modes and mechanical rails: revenge trading, size escalation, thesis drift, sunk-cost holding, action bias |
| `subskills/desk-routine.md` | crypto-trading/desk-routine | Operating rhythm of a one-person desk: daily brief, weekly review, periodic audit, role separation, record preservation |

Additional trading discipline considerations ensure that risk is bounded mathematically, emotional biases are neutralized by pre-committed mechanical rails, and every decision leaves an immutable audit trail for objective review.

Furthermore, maintaining crisp separation between the analytical thesis and the risk management boundaries ensures that operational decisions reflect rigorous discipline rather than unverified impulse.

## Status and limits

Status: seedling. Limits: governs the decision process, risk sizing, invalidation, journaling, and operational routines of discretionary trading; does not provide market predictions, asset selections, financial planning, or automated execution software.
