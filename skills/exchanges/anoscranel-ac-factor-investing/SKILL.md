---
name: ac-factor-investing
description: "Building and evaluating factor exposures: what a factor is and how factors are constructed, cross-sectional standardisation and neutralisation, the value and size and momentum and quality families, portfolio sorts versus regression, capacity and crowding, factor timing and its poor record, and the written factor record. It explains construction and measurement; it never recommends a factor or predicts its return. Use when asking \"factor investing\", \"factor construction\", \"cross-sectional\", \"neutralise a factor\", \"momentum\", \"value factor\", \"factor crowding\", \"smart beta\", \"should I time factors\". Not for judging whether a backtest is real (ac-backtest-integrity), not for fund vehicle comparison (ac-fund-selection), not for portfolio risk budgeting (ac-portfolio-construction)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Factor investing

## Overview

A factor is a characteristic that is associated with returns across a broad cross-section of securities, persistent enough to be studied and simple enough to be constructed into a portfolio. Building one means choosing a definition, transforming the raw data into a comparable score, neutralising the exposures that are not intended, and sorting or weighting to express the view.

This skill covers that construction work and its measurement. It is deliberately silent on which factors will work next: the evidence for any factor is historical, the premiums have compressed as capital has arrived, and timing them has a poor record that is worth understanding before dismissing. The record documents the definition and the choices, so that a later review measures the factor that was actually built.

Primary sources: <https://www.nber.org/> and <https://www.investor.gov/introduction-investing>.

## When to use

- When a factor exposure is being constructed or evaluated.
- When a cross-sectional measure needs standardising or neutralising.
- When factor crowding or capacity is being assessed.
- When factor timing is being considered.

## When NOT to use

- For judging whether a backtest is trustworthy (use ac-backtest-integrity).
- For comparing funds that implement factors (use ac-fund-selection).
- For allocating risk across a portfolio (use ac-portfolio-construction).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/what-a-factor-is.md` | `investing/what-a-factor-is` | Characteristics, premiums, and the difference from a style label. |
| `subskills/factor-construction.md` | `investing/factor-construction` | Definitions, transformations, and the choices that change results. |
| `subskills/standardisation-and-neutralisation.md` | `investing/standardisation-and-neutralisation` | Winsorising, z-scores, and removing unintended exposures. |
| `subskills/sorts-and-regressions.md` | `investing/sorts-and-regressions` | Portfolio sorts versus cross-sectional regression, and what each shows. |
| `subskills/capacity-and-crowding.md` | `investing/capacity-and-crowding` | Turnover, market impact, and what happens when everyone holds it. |
| `subskills/factor-timing.md` | `investing/factor-timing` | Why timing has a poor record, and what would be required to change that. |
| `subskills/factor-record.md` | `investing/factor-record` | The written record: definition, construction, and capacity assumption. |

## Status and honest limits

Factor returns are estimated from historical samples and the estimates carry wide error bars; a premium measured over fifty years is a handful of independent observations once overlapping periods are accounted for. Definitions are chosen by the researcher, and small choices — a winsorising threshold, a neutralisation, a rebalancing frequency — change reported results materially. Nothing here recommends a factor, and a factor portfolio that has not stated its construction choices cannot be replicated or evaluated.
