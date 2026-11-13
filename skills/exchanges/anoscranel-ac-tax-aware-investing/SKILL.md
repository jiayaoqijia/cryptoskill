---
name: ac-tax-aware-investing
description: "Making investment decisions with tax as a design constraint: asset location across account types, loss harvesting and wash-sale traps, gain deferral and the step-up question, charitable vehicles as disposition routes, the interaction of rebalancing with realised gains, withdrawal ordering, and the written tax-aware policy record. It frames the decisions and the arithmetic; it is not tax advice and never computes a liability. Use when asking \"asset location\", \"tax-loss harvesting\", \"wash sale\", \"capital gains deferral\", \"donor-advised fund\", \"which account should hold this\", \"rebalancing without triggering gains\", \"tax-efficient withdrawal order\". Not for record-keeping and tax pack assembly (ac-trading-records-and-tax), not for retirement withdrawal arithmetic (ac-retirement-and-drawdown), not for jurisdiction rules presented as advice."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Tax-aware investing

## Overview

Tax is not a separate topic from portfolio construction; it is a constraint on every decision that involves selling, holding, or choosing where an asset lives. Two portfolios with identical holdings can deliver materially different after-tax outcomes depending on which account holds what, when gains are realised, and how losses are used — and those choices are made before the return is known.

This skill frames those choices and the arithmetic behind them. It does not compute a liability, does not interpret a jurisdiction's rules, and does not replace a professional. What it does is make the trade-offs explicit: the value of deferral, the cost of a wash-sale reset, the price of liquidity in a taxable account, and the fact that a tax decision is a portfolio decision with a deadline.

Primary sources: <https://www.irs.gov/> and <https://www.investor.gov/introduction-investing>.

## When to use

- When deciding which account should hold which asset.
- When a loss is available and harvesting is being considered.
- When rebalancing would realise gains.
- When a disposition is being planned and the route matters.

## When NOT to use

- For assembling records and a tax pack (use ac-trading-records-and-tax).
- For retirement withdrawal arithmetic (use ac-retirement-and-drawdown).
- For a specific jurisdiction's rules presented as advice: consult a professional.

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/asset-location.md` | `investing/asset-location` | Which assets belong in taxable, deferred, and exempt accounts. |
| `subskills/loss-harvesting.md` | `investing/loss-harvesting` | Realising losses, the wash-sale trap, and the basis reset. |
| `subskills/gain-deferral.md` | `investing/gain-deferral` | Holding period effects, deferral value, and the step-up question. |
| `subskills/charitable-routes.md` | `investing/charitable-routes` | Donating appreciated assets and the vehicles that hold them. |
| `subskills/rebalancing-with-tax.md` | `investing/rebalancing-with-tax` | Rebalancing with new money, in-kind, and the realised-gain cost. |
| `subskills/withdrawal-ordering.md` | `investing/withdrawal-ordering` | Which account to draw from, and the bracket interaction. |
| `subskills/tax-aware-policy.md` | `investing/tax-aware-policy` | The written policy: location rules, harvesting rules, and review triggers. |

## Status and honest limits

Tax rules are jurisdictional, change with legislation, and depend on facts a skill cannot see. Every figure here is arithmetic on assumptions rather than a liability, and a decision that matters should be checked with a professional who can see the whole position. The wider caution is that tax should not drive an investment into a worse one: a deferral that requires holding an unsuitable asset is a saving measured against a larger loss.
