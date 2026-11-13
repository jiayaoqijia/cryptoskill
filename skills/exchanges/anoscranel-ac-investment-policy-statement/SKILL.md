---
name: ac-investment-policy-statement
description: "Writing and maintaining the investment policy statement that governs long-horizon capital: goals and horizon, risk capacity versus tolerance, the constraints register, target allocation with ranges, the rebalancing rule, monitoring cadence and review triggers, and the signed versioned record. It writes policy; it never recommends a security or predicts returns. Use when asking \"investment policy\", \"write an IPS\", \"asset allocation policy\", \"rebalancing rule\", \"how should this portfolio be governed\". Not for researching a company (ac-equity-research), not for valuing one (ac-valuation), not for trade-level risk (ac-crypto-trading-discipline)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Investment policy statement

## Overview

An investment policy statement decides, in advance and in writing, what the capital is for, what it may and may not do, and who decides when the facts change. Its value is not bureaucratic: it is the artefact that keeps a decision made in a calm month from being reversed in an anxious one, and it is the only document that can tell you whether a portfolio is behaving as intended.

The statement is written in policy language, not in market language. It names objectives, constraints, ranges, and a rebalancing rule. It does not name securities, and it does not contain a forecast.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.cfainstitute.org/>.

## When to use

- Before capital is allocated for a long horizon, whatever the size.
- When objectives, liquidity needs, or constraints change materially.
- When a portfolio has drifted outside its stated ranges.
- When someone asks whether a holding belongs in the portfolio.

## When NOT to use

- For choosing which company to own (use ac-equity-research and ac-valuation).
- For per-trade risk and journaling (use ac-crypto-trading-discipline).
- For portfolio risk budgeting across trading strategies (use ac-portfolio-construction).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/goals-and-horizon.md` | `investing/goals-and-horizon` | Objectives stated as measurable claims, with the horizon and liquidity needs that constrain them. |
| `subskills/risk-capacity-and-tolerance.md` | `investing/risk-capacity-and-tolerance` | Ability to bear loss versus willingness to bear it, and which constraint binds. |
| `subskills/constraints-register.md` | `investing/constraints-register` | Liquidity, legal, tax, and personal constraints written down as operative limits. |
| `subskills/asset-allocation-policy.md` | `investing/asset-allocation-policy` | Target weights and permitted ranges, and the separation of policy from market view. |
| `subskills/rebalancing-policy.md` | `investing/rebalancing-policy` | Calendar versus threshold rebalancing, the bands, and the cost of each choice. |
| `subskills/monitoring-and-review.md` | `investing/monitoring-and-review` | What is monitored, how often, and the triggers that reopen the policy rather than the portfolio. |
| `subskills/ips-record.md` | `investing/ips-record` | The written statement: goals, constraints, allocation, rebalancing, review, sign-off, and version. |

## Status and honest limits

A policy statement cannot make a bad allocation good, and it cannot anticipate every constraint life adds. What it can do is make decisions checkable: a portfolio that breaches its own ranges is visibly out of policy, and a decision to change policy is visibly a decision rather than a drift. Review it on schedule, not in response to a bad month; a policy revised whenever markets fall is not a policy.
