---
name: ac-retirement-and-drawdown
description: "The decumulation side of investing: withdrawal arithmetic and portfolio longevity, sequence-of-returns risk, withdrawal policies with guardrails, asset allocation while spending, longevity and inflation uncertainty, account ordering and tax, and the written drawdown policy with its triggers. It frames decisions and arithmetic; it never gives retirement, tax, or product advice. Use when asking \"withdrawal rate\", \"safe withdrawal\", \"sequence of returns\", \"retirement drawdown\", \"how much can I spend\", \"decumulation\". Not for accumulating a portfolio (ac-investment-policy-statement), not for tax computation (ac-trading-records-and-tax), not for equity research (ac-equity-research)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Retirement and drawdown

## Overview

Accumulation asks how much to save; decumulation asks how much to spend, in what order, and what to do when the market disagrees. The second question is harder because the answers interact: a withdrawal policy changes the portfolio's survival, and a market fall early in retirement changes what any given withdrawal rate means.

This skill frames the arithmetic and the policy choices. It does not tell anyone what they can afford to spend, does not compute tax, and does not recommend products. Those depend on facts — health, other income, jurisdiction — that a skill cannot see, and a professional should be involved where the stakes are large.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.irs.gov/>.

## When to use

- When planning the transition from saving to spending.
- When a withdrawal policy needs writing or reviewing.
- When a market fall raises the question of whether to change the spending plan.
- When deciding which account to draw from in which order.

## When NOT to use

- For accumulation-stage policy and allocation (use ac-investment-policy-statement).
- For computing tax on withdrawals (use ac-trading-records-and-tax or a professional).
- For product selection or annuity purchase decisions (consult a professional).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/decumulation-arithmetic.md` | `investing/decumulation-arithmetic` | Withdrawal rates, portfolio longevity, and the arithmetic that connects spending to horizon. |
| `subskills/sequence-of-returns.md` | `investing/sequence-of-returns` | Why the order of returns matters when money is leaving the portfolio, and how the risk is managed. |
| `subskills/withdrawal-policy.md` | `investing/withdrawal-policy` | Fixed real versus dynamic withdrawals, guardrails, and the written spending rule. |
| `subskills/allocation-in-drawdown.md` | `investing/allocation-in-drawdown` | How allocation changes when spending is funded from the portfolio, and the limits of bucket approaches. |
| `subskills/longevity-and-inflation.md` | `investing/longevity-and-inflation` | Horizon uncertainty, inflation protection, and what cannot be known in advance. |
| `subskills/account-ordering.md` | `investing/account-ordering` | The order in which accounts are drawn, and the tax and access considerations that drive it. |
| `subskills/drawdown-record.md` | `investing/drawdown-record` | The written drawdown policy: spending rule, guardrails, review triggers, and the record of changes. |

## Status and honest limits

Every projection here is arithmetic on assumptions, and the assumptions — return, inflation, longevity, spending — are the least reliable inputs in personal finance. A withdrawal rate that survives one historical period may fail in another, and a policy that works on average can fail for a particular person. The record should therefore state assumptions and triggers rather than a single spending number, and large decisions belong with a professional who can see the whole picture.
