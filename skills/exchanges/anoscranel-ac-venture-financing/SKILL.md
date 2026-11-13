---
name: ac-venture-financing
description: 'The financial mechanics of venture-backed private companies: the cap table before and after each round, preference stacks and liquidation waterfalls, option pools and dilution arithmetic, term sheets as a leverage sequence, venture debt as an alternative layer, exit waterfalls for distributing proceeds across classes of stock, 409A valuations as the internal price of common stock, and the written financing record. It explains the arithmetic of ownership as investments pile up; it never recommends a security or predicts a fund raising outcome. Use when asking "cap table", "liquidation preference", "anti-dilution", "option pool", "priced round", "SAFE", "convertible note", "venture debt", "waterfall", "409A", "exit waterfall". Not for public equity analysis of the listed companies (ac-equity-research), not for fund manager diligence (ac-manager-and-vehicle-diligence), not for secondary share sales (ac-portfolio-financing secondaries coverage).'
license: MIT
metadata:
  domain: investing
status: seedling
---

# Venture financing

## Overview

A venture-backed company is a stack of financial claims, each negotiated in a sequence of financings. New investors buy a class of preferred stock with terms; employees hold options from a pool; founders hired before any of it hold common. What each person owns depends on the order of the financings, the convertibility of each into the next, and the complex liquidation waterfall that governs how exit proceeds distribute across preference stacks and participation rights. The reality is closer to structured finance than to the "percentage ownership" intuition that founders usually apply.

This skill covers the mechanics: cap table construction and projections across rounds, liquidation preferences and their waterfall dynamics, option pool arithmetic and the dilution of creating one, term-sheet sequencing as value shifts across rounds, venture debt as a less-dilutive but more rigid alternative, waterfall analysis for exit scenarios, and 409A-type valuations as the internal price of common stock. Fund diligence against a venture manager belongs to a different skill; the analysis of public listed equities belongs to another.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.law.cornell.edu/>.

## When to use

- When building or analysing a cap table across priced rounds.
- When calculating exit waterfalls and liquidation preference outcomes.
- When comparing term sheets or venture debt as financing alternatives.
- When calculating dilution from option pool creation or expansion.

## When NOT to use

- For the equity analysis of listed public companies (use ac-equity-research).
- For fund manager and vehicle due diligence (use ac-manager-and-vehicle-diligence).
- For LP secondaries and fund-level liquidity transactions (use ac-portfolio-financing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/cap-table-mechanics.md` | `investing/cap-table-mechanics` | The cap table as the single source of ownership truth across rounds. |
| `subskills/liquidation-preferences.md` | `investing/liquidation-preferences` | The preference stack, participation, and seniority in a sale. |
| `subskills/anti-dilution-and-ratchets.md` | `investing/anti-dilution-and-ratchets` | Down-round protection and the full-ratchet/blended-weighted-average spectrum. |
| `subskills/option-pool-dilution.md` | `investing/option-pool-dilution` | Creating and refreshing the pool; who bears the dilution. |
| `subskills/term-sheet-sequence.md` | `investing/term-sheet-sequence` | Pricing and terms across successive rounds; what changes and why. |
| `subskills/venture-debt.md` | `investing/venture-debt` | Debt against venture equity: warrants, covenants, and maturity. |
| `subskills/exit-waterfall.md` | `investing/exit-waterfall` | Distributing exit proceeds across preferred, common, and options. |
| `subskills/fairness-value-409a.md` | `investing/fairness-value-409a` | The internal valuation of common stock and option strike prices. |
| `subskills/venture-record.md` | `investing/venture-record` | The written financing record: rounds, terms, projections, and reality. |

## Status and honest limits

Private-company terms vary widely and change as market conditions shift; a term-sheet checklist read as universal truth will mislead. This skill states the mechanics and the arithmetic — the waterfall is deterministic, the exit value is not — and never recommends an investment or predicts whether a round closes. A cap table that has never been projected through a downside exit has not been read at all.
