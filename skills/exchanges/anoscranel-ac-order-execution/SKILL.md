---
name: ac-order-execution
description: "Use when asking how to execute orders, manage slippage, select order types, place stops, slice large orders, or audit fills. Covers order types, cascade execution, slippage and market impact, tactical order placement, slicing and timing, execution records, and failure modes. Not for the venue evaluation (ac-perp-venue-diligence), not for the trade record or journal (ac-crypto-trading-discipline), not for liquidation risk geometry (ac-liquidation-risk-management)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

Primary sources for the claims here: <https://bybit-exchange.github.io/docs/derivatives/v5/order/create-order> and <https://binance-docs.github.io/apidocs/futures/en/#trade-s-endpoints>.

## Overview

`ac-order-execution` provides rigorous engineering standards, decision rules, and procedures for executing trades in digital asset perpetual futures and spot markets. It governs order primitive selection, behavior during systemic liquidation cascades, slippage and transaction cost measurement, tactical stop and exit placement, optimal time-slicing and liquidity-seeking algorithms, execution recordkeeping, and failure-mode recovery protocols across centralized and decentralized exchanges to ensure institutional-grade operational reliability and capital protection against market friction and routing failures.

## Subskills Index

| Leaf File | Domain | Scope |
|---|---|---|
| `subskills/order-types.md` | `crypto-trading/order-types` | Order types and execution primitives in perpetual futures and spot markets |
| `subskills/execution-in-cascades.md` | `crypto-trading/execution-in-cascades` | Order execution tactics and tape interpretation during forced liquidation cascades |
| `subskills/slippage-and-impact.md` | `crypto-trading/slippage-and-impact` | Measuring and auditing execution slippage, market impact, and fee drag against benchmarks |
| `subskills/order-placement-tactics.md` | `crypto-trading/order-placement-tactics` | Tactical order placement, stop positioning, and defensive exit routing rules |
| `subskills/slicing-and-timing.md` | `crypto-trading/slicing-and-timing` | Order slicing, participation rate management, and liquidity-seeking algorithms |
| `subskills/execution-record.md` | `crypto-trading/execution-record` | Detailed execution logging, TCA metrics, and fill benchmark attribution |
| `subskills/execution-failure-modes.md` | `crypto-trading/execution-failure-modes` | Handling execution failures, order rejections, exchange halts, and self-trade prevention |

## Core Principles

- Execution cost is a first-order P&L driver: unmitigated slippage and transaction fees can eliminate strategy alpha entirely across quantitative trading operations and market cycles.
- Market orders are catastrophic during liquidation cascades; passive or sliced limit execution is mandatory when liquidity thins.
- Every exit must carry a Reduce-Only modifier to prevent accidental position inversion during volatile fills across exchange matching engines.
- Arrival midpoint benchmarking and TCA auditing reveal true execution quality and expose anomalous flat slippage curves.

## Operational Workflows

Operators utilize these subskills sequentially or in parallel depending on order size and market volatility conditions. Routine flow begins with primitive selection via `order-types.md`, followed by tactical stop placement under `order-placement-tactics.md`. Large institutional block allocations engage `slicing-and-timing.md`, while high-volatility regimes require adherence to `execution-in-cascades.md` and `execution-failure-modes.md`. All executions conclude with logging governed by `execution-record.md` and `slippage-and-impact.md`.

## Sources

- Binance Futures API Documentation: https://binance-docs.github.io/apidocs/futures/en/#trade-s-endpoints
- Bybit API Documentation: https://bybit-exchange.github.io/docs/derivatives/v5/order/create-order
- NBER Working Paper on Market Impact and Transaction Costs: https://www.nber.org/papers/w27431
- CFA Institute Transaction Cost Analysis Standards: https://www.cfainstitute.org/en/research/foundation/2020/transaction-cost-analysis


## Additional Guidance

When deploying execution algorithms across decentralized exchanges and automated market makers, operators must additionally account for gas fee volatility, MEV (Miner Extractable Value) sandwich attack vectors, and asynchronous block confirmation delays. These factors introduce non-linear execution costs that require dynamic slippage tolerance adjustments and private RPC routing integrations.