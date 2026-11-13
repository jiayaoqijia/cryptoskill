---
name: ac-rates-options
description: "Trading interest-rate options by their own conventions: payer and receiver swaptions, caps and floors, normal versus lognormal volatility, European Bermudan and mid-curve exercise, the volatility cube and its skew, hedging DV01 and vega, dealer liquidity and clearing, and the written record. It explains how the instruments quote and settle; it never recommends a rate view or predicts yields. Use when asking \"swaption\", \"cap floor\", \"normal vol\", \"basis point volatility\", \"Bermudan swaption\", \"mid-curve option\", \"rates vol cube\", \"why is my swaption vega not matching\". Not for generic option greeks and structures (ac-options-and-volatility), not for bond futures mechanics (ac-rates-trading), not for bond portfolio mathematics (ac-fixed-income-and-rates)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Rates options

## Overview

An interest-rate option is an option on a rate rather than on a price, and that single difference explains most of its conventions. Volatility is quoted in basis points per annum for many instruments, the underlying is a swap or a forward rate rather than a bond, and the exercise can be European, Bermudan, or a series of mid-curve expiries into the same swap. A trader arriving from equity options finds the greeks familiar and the quoting entirely different.

This skill covers the conventions and the mechanics: what a payer and a receiver swaption are, how caps and floors decompose into them, why normal volatility exists and when it is used, how the volatility cube is organised, and how a rates option book is hedged and financed. Bond futures mechanics belong to the rates trading skill, and the generic greeks belong to the options skill.

Primary sources: <https://www.cmegroup.com/> and <https://www.bis.org/>.

## When to use

- When trading swaptions, caps, floors, or mid-curve options.
- When a volatility quote in basis points needs converting or comparing.
- When a Bermudan or callable structure's exercise schedule matters.
- When hedging a rates option book's vega or DV01.

## When NOT to use

- For greeks, implied volatility surfaces in general, and structures (use ac-options-and-volatility).
- For bond futures, CTD, and basis mechanics (use ac-rates-trading).
- For bond price and duration arithmetic (use ac-fixed-income-and-rates).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/swaptions-and-caps.md` | `investing/swaptions-and-caps` | Payer and receiver swaptions, caps and floors, and how they decompose. |
| `subskills/normal-vs-lognormal-vol.md` | `investing/normal-vs-lognormal-vol` | Basis-point versus percentage volatility, and what negative rates did to the convention. |
| `subskills/exercise-styles.md` | `investing/exercise-styles` | European, Bermudan, and American exercise, and mid-curve expiries. |
| `subskills/rates-vol-surface.md` | `investing/rates-vol-surface` | The strike and expiry cube, and the skew that rates options carry. |
| `subskills/rates-option-hedging.md` | `investing/rates-option-hedging` | DV01 and vega hedging, gamma in a rates book, and rehedging cost. |
| `subskills/rates-option-liquidity.md` | `investing/rates-option-liquidity` | Dealer liquidity, clearing, and compression in rates options. |
| `subskills/rates-option-record.md` | `investing/rates-option-record` | The written record: instrument, vol convention, exercise, and hedge. |

## Status and honest limits

Rates option pricing depends on a model, and the model's assumptions matter more here than in equity options because the underlying is a curve rather than a single price. Different models produce different sensitivities for the same trade, and Bermudan structures are particularly model-sensitive. Every number in the record should name the model and the volatility convention, and a comparison between two quotes that does not is a comparison of two different things.
