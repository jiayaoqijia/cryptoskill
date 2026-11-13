---
name: ac-fund-selection
description: "Evaluating funds and ETFs as vehicles: expense ratios and the total cost stack, tracking difference versus tracking error, index methodology, structure and counterparty risk, liquidity and spreads, tax efficiency, and the written fund record. It evaluates vehicles; it never recommends a fund or predicts returns. Use when asking \"which ETF\", \"fund fees\", \"tracking error\", \"index fund\", \"should I use this fund\", \"fund structure\", \"mutual fund or ETF\". Not for choosing the asset allocation (ac-investment-policy-statement), not for evaluating a company (ac-equity-research), not for alternatives vehicles (ac-alternatives-and-real-assets)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Fund selection

## Overview

A fund is a wrapper around an exposure, and the wrapper has costs, mechanics, and risks of its own. Two funds tracking the same index can deliver different returns because of fees, sampling, securities lending, and tax treatment, and a fund can fail in ways the index does not — through counterparty exposure, liquidity mismatch, or a closure that forces a sale at the wrong time.

Fund selection is therefore a vehicle decision, separate from the asset decision. This skill evaluates the vehicle: what it costs in total, how closely it tracks, what its structure exposes the holder to, and how it behaves when the underlying market is stressed.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.sec.gov/investor>.

## When to use

- When two or more funds provide the same exposure and a choice must be made.
- When a held fund changes its index, fee, or structure.
- When a fund's tracking has drifted from its benchmark.
- When liquidity or counterparty questions arise about a vehicle.

## When NOT to use

- For the allocation decision itself (use ac-investment-policy-statement).
- For evaluating alternative-asset vehicles such as REITs or private funds (use ac-alternatives-and-real-assets).
- For security-level research (use ac-equity-research).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/cost-stack.md` | `investing/cost-stack` | Expense ratio plus spreads, commissions, and taxes: the total cost of holding a fund. |
| `subskills/tracking-difference.md` | `investing/tracking-difference` | Tracking difference versus tracking error, and what each reveals about implementation quality. |
| `subskills/index-methodology.md` | `investing/index-methodology` | What the index actually holds, how it rebalances, and where the methodology creates risk. |
| `subskills/structure-and-counterparty.md` | `investing/structure-and-counterparty` | Physical versus synthetic replication, securities lending, and the counterparty chain. |
| `subskills/fund-liquidity.md` | `investing/fund-liquidity` | Premiums and discounts, creation and redemption, and what happens to spreads in stress. |
| `subskills/tax-efficiency.md` | `investing/tax-efficiency` | Distributions, turnover, and the tax drag that differs between otherwise identical funds. |
| `subskills/fund-record.md` | `investing/fund-record` | The written fund record: exposure, cost, tracking, structure, liquidity, and review triggers. |

## Status and honest limits

Fund documentation describes a vehicle as it is today, and vehicles change: indices are redefined, fees are cut or raised, structures are merged. A selection that is not revisited is a decision that decays. The record therefore carries review triggers, and every cost figure carries its date, because a fund comparison with stale numbers is a comparison of history rather than of choices.
