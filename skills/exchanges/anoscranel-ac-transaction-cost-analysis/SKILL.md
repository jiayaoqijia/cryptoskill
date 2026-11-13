---
name: ac-transaction-cost-analysis
description: "Measuring what trading actually costs across a book rather than on one order: implementation shortfall and arrival-price benchmarks, VWAP and participation benchmarking, the cost decomposition into spread impact and delay, broker and venue scorecards, transition management and its risks, research payment and soft-dollar governance, and the written cost record. It measures execution cost and its attribution; it never recommends a broker and never predicts a price. Use when asking \"implementation shortfall\", \"arrival price\", \"VWAP benchmark\", \"transaction cost analysis\", \"TCA\", \"broker scorecard\", \"transition management\", \"soft dollars\", \"commission recapture\", \"why is my trading costing so much\". Not for placing a single order (ac-order-execution), not for slippage on one trade (ac-order-execution), not for broker fee schedules and custody (ac-broker-and-custody-selection)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Transaction cost analysis

## Overview

The cost of trading is not the commission. It is the difference between the price a portfolio would have achieved with no trading and the price it achieved, and that difference includes the spread paid, the impact of the order on the market, the delay between deciding and executing, and the opportunity cost of what was not filled. Measured per order these components are noisy; measured across a book and over time they become a stable estimate of what a strategy pays to exist.

This skill covers that measurement: the benchmarks available and what each assumes, the decomposition of cost into its parts, how to score brokers and venues on evidence rather than on relationship, what transition management involves and where its risks sit, and how research payment is governed once it is no longer bundled into commission. It measures cost; it does not choose a broker.

Primary sources: <https://www.cfainstitute.org/> and <https://www.sec.gov/investor>.

## When to use

- When establishing what a strategy costs to trade over time.
- When comparing execution quality across brokers or venues.
- When a portfolio transition or a large rebalance is being planned.
- When research payment arrangements are being reviewed or documented.

## When NOT to use

- For order type selection and placement on a single order (use ac-order-execution).
- For slippage measurement on one trade or one name (use ac-order-execution).
- For broker fee schedules, custody, and account structure (use ac-broker-and-custody-selection).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/implementation-shortfall.md` | `investing/implementation-shortfall` | Decision price to execution price, and the components in between. |
| `subskills/vwap-and-participation-benchmarks.md` | `investing/vwap-and-participation-benchmarks` | VWAP, participation rate, and the benchmarks that flatter a strategy. |
| `subskills/cost-decomposition.md` | `investing/cost-decomposition` | Spread, impact, delay, and opportunity cost as separate measurements. |
| `subskills/broker-scorecards.md` | `investing/broker-scorecards` | Scoring brokers and venues on evidence, and the sample size problem. |
| `subskills/transition-management.md` | `investing/transition-management` | Moving a portfolio between managers, and where the cost and risk sit. |
| `subskills/research-payment-governance.md` | `investing/research-payment-governance` | Unbundling, soft dollars, and the governance of research spend. |
| `subskills/cost-record.md` | `investing/cost-record` | The written cost record: benchmark, decomposition, and review triggers. |

## Status and honest limits

Cost measurement is only as good as the data behind it: a benchmark computed from a reference price that was not observable at the decision time measures something other than what it claims. Samples are small for any single strategy in any single quarter, and the difference between two brokers is often inside the noise. Nothing here recommends a broker, and a cost figure quoted without its benchmark and its sample is a number rather than a measurement.
