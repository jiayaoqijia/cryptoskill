---
name: ac-credit-curve
description: "Reading and trading the credit curve: the term structure of spreads for one issuer, slope and shape versus the risk-free curve, roll-down and carry along the credit curve, curve trades and their DV01 weighting, inversion and what it signals, cross-issuer relative value, and the written curve record. It explains the shape and the arithmetic of curve positions; it never recommends a credit or predicts a default. Use when asking \"credit curve\", \"spread curve\", \"roll down\", \"credit carry\", \"curve steepener\", \"inverted credit curve\", \"relative value across maturities\", \"why is the 5y wider than the 10y\". Not for single-point spread DV01 and hedging (ac-credit-derivatives), not for the risk-free yield curve (ac-fixed-income-and-rates), not for borrower analysis (ac-bank-and-credit-analysis)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Credit curve

## Overview

The credit curve is the set of spreads at which one issuer can borrow across maturities, over the risk-free curve at each point. Its shape carries information that a single spread cannot: an upward slope usually reflects increasing uncertainty and liquidity premium with time, a flat curve suggests the market prices similar risk at every horizon, and an inverted curve is a statement that the near-term risk dominates.

Trading the curve means taking a position in one maturity against another, so that a parallel move in spreads affects both legs similarly and the return comes from the change in slope. The mechanics resemble a rates curve trade but the risks differ: recovery assumptions, default probability, and liquidity vary along the credit curve in ways that have no rates analogue.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## When to use

- When an issuer's spreads across maturities need interpreting.
- When a curve trade is being structured or reviewed.
- When roll-down and carry along the credit curve are being estimated.
- When an inversion or a flattening needs explaining.

## When NOT to use

- For single-point spread DV01, indices and credit events (use ac-credit-derivatives).
- For the risk-free curve's own shape (use ac-fixed-income-and-rates).
- For assessing the issuer's ability to repay (use ac-bank-and-credit-analysis).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/curve-shape.md` | `investing/curve-shape` | Slope, curvature, and what each shape is saying. |
| `subskills/spread-versus-risk-free.md` | `investing/spread-versus-risk-free` | The credit curve as a spread over a curve that also moves. |
| `subskills/roll-and-carry-credit.md` | `investing/roll-and-carry-credit` | Roll-down, carry, and the return from an unchanged curve. |
| `subskills/curve-trade-structure.md` | `investing/curve-trade-structure` | Steepener and flattener structures with spread DV01 weights. |
| `subskills/inversion-and-stress.md` | `investing/inversion-and-stress` | Why an inverted credit curve appears, and what it implies. |
| `subskills/cross-issuer-relative-value.md` | `investing/cross-issuer-relative-value` | Comparing curves across issuers without confounding the comparison. |
| `subskills/credit-curve-record.md` | `investing/credit-curve-record` | The written record: points, shape, roll assumption, and weights. |

## Status and honest limits

Credit curves are built from a sparse set of quoted points, and interpolation between them assumes a smoothness the market does not guarantee; a single illiquid maturity can distort the shape that a trader reads. The roll and carry estimates depend on the curve staying where it is, which is the assumption most likely to fail. Nothing here recommends a credit, and a curve trade sized on one leg's liquidity without the other's is sized on the wrong constraint.
