---
name: ac-performance-measurement
description: "Measuring investment results honestly: time-weighted versus money-weighted returns, benchmark selection and the policy benchmark, Brinson attribution into allocation and selection, information and Sharpe ratios with their failure modes, drawdown depth, duration and the recovery arithmetic a fall requires, peer-group comparison traps, and the written performance record. It measures outcomes and attributes them; it never claims skill from a single period or recommends a strategy. Use when asking \"time-weighted return\", \"money-weighted return\", \"Brinson attribution\", \"information ratio\", \"did I beat the benchmark\", \"performance attribution\", \"drawdown duration\", \"peer group comparison\". Not for validating a backtest (ac-backtest-integrity), not for risk budgeting across strategies (ac-portfolio-construction), not for tax reporting (ac-trading-records-and-tax)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Performance measurement

## Overview

A return figure is the start of the work rather than the end. The same portfolio has several correct returns depending on the question — a time-weighted return for judging the strategy, a money-weighted return for judging the investor's experience — and reporting the wrong one flatters or penalises the wrong party. Attribution then asks where the result came from, which is a different question again.

This skill covers that measurement layer: which return to compute, which benchmark to measure against, how to attribute the difference, how to state ratios without overclaiming, and how to describe a drawdown in terms of both depth and duration. It deliberately separates measuring from judging; a single period rarely supports a conclusion about skill, and the record is built to accumulate rather than to settle.

Primary sources: <https://www.cfainstitute.org/> and <https://www.investor.gov/introduction-investing>.

## When to use

- When a portfolio's return needs to be computed and reported.
- When a result is being attributed to decisions rather than to the market.
- When a benchmark or a peer comparison is being chosen or questioned.
- When a ratio is cited as evidence of skill.

## When NOT to use

- For deciding whether a backtest is trustworthy (use ac-backtest-integrity).
- For allocating risk across strategies and venues (use ac-portfolio-construction).
- For computing tax liabilities or assembling a tax pack (use ac-trading-records-and-tax).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/time-weighted-vs-money-weighted.md` | `investing/time-weighted-vs-money-weighted` | Two correct returns that answer different questions. |
| `subskills/benchmark-selection.md` | `investing/benchmark-selection` | The policy benchmark, investable alternatives, and benchmark drift. |
| `subskills/brinson-attribution.md` | `investing/brinson-attribution` | Allocation, selection, and interaction, and what each reveals. |
| `subskills/risk-adjusted-ratios.md` | `investing/risk-adjusted-ratios` | Sharpe, information ratio, and the assumptions each carries. |
| `subskills/drawdown-depth-and-duration.md` | `investing/drawdown-depth-and-duration` | Depth, duration, recovery, and why two drawdowns of equal size differ. |
| `subskills/peer-group-traps.md` | `investing/peer-group-traps` | Survivorship, classification, and the median that hides everything. |
| `subskills/performance-record.md` | `investing/performance-record` | The written record: return type, benchmark, attribution, and period. |

## Status and honest limits

Every measure here is a description of a period, and periods are short. A ratio computed over two years has a confidence interval wide enough to include both skill and luck, and a peer ranking is a statement about a universe that has been defined by someone else. The record should state the period, the return type, and the benchmark alongside every figure, because a return quoted without them is not a measurement but a number.
