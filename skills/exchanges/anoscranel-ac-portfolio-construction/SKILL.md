---
name: ac-portfolio-construction
description: "Professional portfolio construction and risk budgeting for discretionary and systematic trading: allocating risk, not capital; correlation breakdown in stress regimes; drawdown budgeting and recovery arithmetic; capital allocation across venues and margin rails; concentration and single-point-of-failure registers; rebalancing rules; and periodic portfolio reviews. Use when asking 'portfolio construction', 'risk budgeting', 'allocate across strategies', 'correlation', 'drawdown budget', 'concentration risk'. Not for the per-trade record (ac-crypto-trading-discipline), not for venue due diligence (ac-perp-venue-diligence), not for backtest validation (ac-backtest-integrity)."
license: MIT
metadata:
  domain: crypto-trading
  status: seedling
---

# Portfolio Construction

## Overview

Portfolio construction in crypto trading defines how capital, risk, and drawdown budgets are distributed across multiple strategies, assets, and venues. Unlike traditional asset management where correlations remain relatively stable across market regimes, crypto markets exhibit regime-dependent correlation spikes during stress events and liquidation cascades. Diversification that appears effective in calm markets can vanish precisely when risk capital is most exposed.

This skill governs portfolio-level risk management, asset allocation, correlation tracking, concentration limits, and periodic reviews. It establishes deterministic rules for risk budgeting rather than capital allocation, ensuring that strategies with high leverage do not dominate total portfolio volatility or create hidden single points of failure.

## Subskills Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| [`subskills/risk-budgeting-across-strategies.md`](subskills/risk-budgeting-across-strategies.md) | crypto-trading/risk-budgeting-across-strategies | Allocating risk by loss-at-invalidation rather than capital across strategies. |
| [`subskills/correlation-regimes.md`](subskills/correlation-regimes.md) | crypto-trading/correlation-regimes | Measuring regime-dependent correlation and managing tail dependence in common shocks. |
| [`subskills/drawdown-budgeting.md`](subskills/drawdown-budgeting.md) | crypto-trading/drawdown-budgeting | Managing maximum drawdown budgets, strategy combination, and recovery arithmetic. |
| [`subskills/capital-allocation.md`](subskills/capital-allocation.md) | crypto-trading/capital-allocation | Distributing capital across venues, margin modes, lockups, and withdrawal rails. |
| [`subskills/concentration-and-single-points.md`](subskills/concentration-and-single-points.md) | crypto-trading/concentration-and-single-points | Auditing venue, stablecoin, strategy, and custody concentration points. |
| [`subskills/rebalancing-and-drift.md`](subskills/rebalancing-and-drift.md) | crypto-trading/rebalancing-and-drift | Defining drift tolerances, rebalancing rules, and transaction cost impacts. |
| [`subskills/portfolio-review.md`](subskills/portfolio-review.md) | crypto-trading/portfolio-review | Executing periodic portfolio reviews, performance attribution, and strategy sunsetting. |

## When to use

- Setting or reviewing the risk budget across several trading strategies or books.
- Deciding how much capital each strategy and venue should hold.
- Checking whether diversification still holds after a regime change or a stress event.
- Reviewing drawdown budget adherence and concentration limits at a periodic review.
- Recording why a strategy was cut or its budget changed.

Primary sources for these criteria: <https://www.fsb.org/work-of-the-fsb/market-and-institutional-resilience/crypto-assets/> and <https://www.bis.org/bcbs/publ/d589.htm>.

## When NOT to use

- For the per-trade decision record or the risk budget of one trade (use ac-crypto-trading-discipline).
- For evaluating a single venue's safety (use ac-perp-venue-diligence).
- For validating a strategy's backtest before it earns any allocation (use ac-backtest-integrity).

## Status and honest limits

The correlation and drawdown claims here are structural, not measured parameters: no portfolio-level dataset exists for crypto strategy books, so every budget is an operator-set assumption and must be recorded as one. Diversification measured in calm markets is the number that fails first in a common shock, and a cascade is a common shock by construction. Revisit the budgets at every periodic review; do not treat a past correlation matrix as a current one.

## Sources & References

- Basel Committee on Banking Supervision: https://www.bis.org/bcbs/publ/d589.htm
- National Bureau of Economic Research (NBER): https://www.nber.org/papers/w31000
- Financial Stability Board (FSB): https://www.fsb.org/work-of-the-fsb/market-and-institutional-resilience/crypto-assets/
- International Organization of Securities Commissions (IOSCO): https://www.iosco.org/
