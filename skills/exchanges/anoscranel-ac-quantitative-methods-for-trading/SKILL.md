---
name: ac-quantitative-methods-for-trading
description: "The statistical toolkit behind systematic trading: mean reversion and pairs, cointegration and spread construction, momentum and trend measurement, realized versus implied volatility, GARCH-style volatility models, variance and volatility swaps, signal decay net of costs, and the written quant record. It explains how these methods are built and measured; it never recommends a signal and never promises a return. Use when asking \"pairs trading\", \"cointegration\", \"mean reversion\", \"spread construction\", \"realized vol\", \"GARCH\", \"variance swap\", \"vol swap\", \"signal decay\", \"half life\", \"stationary series\", \"trend following\", \"statistical arbitrage\". Not for validating a backtest of these methods (ac-backtest-integrity), not for funding and basis carry (ac-funding-and-basis), not for factor construction for portfolios (ac-factor-investing)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Quantitative methods for trading

## Overview

Systematic trading methods are built from a small set of statistical objects: a spread between two co-moving prices, a volatility measured from returns, a trend measured over horizons. The craft is not in the formulas — they are standard — but in what each one assumes and how those assumptions fail on live data: spreads that were never cointegrated, volatility that clusters differently than modeled, signals whose decay eats the cost of trading them.

This skill covers the construction and the failure modes: how a pairs spread is built and tested for cointegration rather than correlation, what momentum actually measures across horizons, how realized and implied volatility differ and when each is the right object, how GARCH-style models estimate persistence, how variance and volatility swaps pay out, and how signal decay is separated from transaction cost. Each leaf states its assumptions; none promises that a method works.

Primary sources: <https://quant.stackexchange.com/> and <https://www.quantconnect.com/docs/>.

## When to use

- When building or evaluating a mean-reversion, pairs, or momentum strategy at the method level.
- When constructing or reading a volatility estimate — realized, implied, or modeled.
- When pricing or reading a variance or volatility swap.
- When deciding whether a signal's decay survives its costs.

## When NOT to use

- For validating whether a backtest of these methods is believable (use ac-backtest-integrity).
- For funding, basis, and carry arithmetic on perpetuals (use ac-funding-and-basis).
- For portfolio-level factor construction (use ac-factor-investing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/mean-reversion-and-pairs.md` | `crypto-trading/mean-reversion-and-pairs` | Spread construction, the stationarity assumption, and when mean reversion is wishful. |
| `subskills/cointegration-testing.md` | `crypto-trading/cointegration-testing` | Tests, in-sample traps, and what a passing test does and does not license. |
| `subskills/momentum-and-trend.md` | `crypto-trading/momentum-and-trend` | What trend measures, horizon choice, and why momentum crashes happen. |
| `subskills/realized-versus-implied.md` | `crypto-trading/realized-versus-implied` | Two volatilities, two estimators, and the premium between them. |
| `subskills/garch-style-volatility.md` | `crypto-trading/garch-style-volatility` | Clustering, persistence, and what the model assumes about tails. |
| `subskills/variance-and-vol-swaps.md` | `crypto-trading/variance-and-vol-swaps` | Payoff mechanics, the concavity correction, and the volatility risk premium. |
| `subskills/signal-decay-and-costs.md` | `crypto-trading/signal-decay-and-costs` | Half-life, capacity, and the cost line a signal must clear. |
| `subskills/quant-record.md` | `crypto-trading/quant-record` | The written record: method, assumptions, decay, costs, and falsifiers. |

## Status and honest limits

Every method in this skill has a published failure mode: pairs diverge permanently, momentum reverses in clusters, volatility models underestimate tails, and signals decay as they are known. The mathematics is stable; the edge is not, and nothing here helps predict which methods will keep working. A position taken on any of these methods belongs with its own risk budget and falsifier, and the record leaf exists to force those into writing before the trade.
