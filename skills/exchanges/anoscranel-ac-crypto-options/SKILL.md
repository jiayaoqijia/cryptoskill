---
name: ac-crypto-options
description: "Trading crypto options by their own conventions: inverse coin-margined versus linear stablecoin-margined contracts, expiry grids and 08:00 UTC settlement, the volatility surface and its skew, venue structure and request-for-quote liquidity, margin and liquidation of short options, the yield-selling pattern and its tail, and the written record. It explains how the contracts behave; it never recommends a position or predicts a price. Use when asking \"inverse option\", \"coin-margined option\", \"Deribit expiry\", \"DVOL\", \"crypto option spread\", \"selling options for yield\", \"option liquidation\". Not for generic greeks and structures (ac-options-and-volatility), not for perpetual funding (ac-funding-and-basis), not for the spot venue's safety (ac-perp-venue-diligence)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Crypto options

## Overview

Crypto options differ from their listed equity cousins in three ways that decide outcomes: the collateral currency, the expiry grid, and the venue structure. A contract may be margined and settled in the underlying coin or in a stablecoin, which changes both the payoff and the risk of the collateral itself; expiries run daily, weekly, monthly, and quarterly with a fixed settlement time; and most volume trades through request-for-quote rather than a displayed book.

This skill covers those mechanics and the risks that follow: inverse contract arithmetic, settlement and mark price conventions, the surface and its persistent skew, margin and liquidation for short options, and the yield-selling pattern that dominates retail participation in this market. Generic greeks belong to the options skill and perpetual funding belongs to its own.

Primary sources: <https://www.cftc.gov/> and <https://www.sec.gov/investor>.

## When to use

- When trading an option on a crypto venue and the contract's collateral matters.
- When an inverse contract's payoff or margin needs computing.
- When the surface's skew or term structure is being read as a signal.
- When a short option position's liquidation risk needs assessing.

## When NOT to use

- For greeks, surfaces in general, and option structures (use ac-options-and-volatility).
- For perpetual futures funding and basis (use ac-funding-and-basis).
- For evaluating the venue's solvency and book (use ac-perp-venue-diligence).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/inverse-and-linear-contracts.md` | `crypto-trading/inverse-and-linear-contracts` | Coin-margined versus stablecoin-margined contracts and their P&L arithmetic. |
| `subskills/crypto-expiry-and-settlement.md` | `crypto-trading/crypto-expiry-and-settlement` | Daily to quarterly expiries, the settlement time, and the mark price. |
| `subskills/crypto-vol-surface.md` | `crypto-trading/crypto-vol-surface` | DVOL, skew, term structure, and the weekend effect. |
| `subskills/crypto-option-venues.md` | `crypto-trading/crypto-option-venues` | Order books versus request-for-quote, and where the liquidity actually is. |
| `subskills/crypto-option-margin.md` | `crypto-trading/crypto-option-margin` | Margin, portfolio offsets, and the liquidation of short options. |
| `subskills/yield-selling-and-its-tail.md` | `crypto-trading/yield-selling-and-its-tail` | Covered calls and cash-secured puts sold for yield, and the loss they concentrate. |
| `subskills/crypto-option-record.md` | `crypto-trading/crypto-option-record` | The written record: contract type, collateral, expiry, and liquidation distance. |

## Status and honest limits

Venue rules, contract specifications, and margin methodologies change, and a settlement or liquidation convention read from a marketing page may be out of date. Inverse contracts make the collateral itself a risk: a position can be correct on the option and still lose value in the margining currency. Nothing here recommends a position, and a short option position without its liquidation price computed is a position whose worst case is unknown.
