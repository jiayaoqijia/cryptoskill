---
name: ac-fx-options
description: "Trading foreign exchange options by their own conventions: premium quoted in volatility points, spot versus forward versus premium-adjusted delta, ATM straddle and risk reversal and butterfly quotes, expiry cuts and settlement, barrier and digital structures, delta hedging, and the written record. It explains how the FX option market quotes and settles; it never recommends a position or predicts a rate. Use when asking \"FX option premium in vol points\", \"25 delta risk reversal\", \"butterfly quote\", \"premium-adjusted delta\", \"FX barrier option\", \"10am New York cut\". Not for generic greeks and structures (ac-options-and-volatility), not for spot FX trading (ac-forex-trading), not for currency risk in a portfolio (ac-currency-and-fx-risk)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# FX options

## Overview

An FX option is quoted in a way that surprises anyone arriving from listed equity options. The premium is often expressed in volatility points rather than in currency, the strike may be given as a delta rather than a price, and the volatility itself is quoted through a convention — at-the-money straddle, risk reversal, butterfly — rather than as a single number per strike. Each of those conventions exists because the market trades volatility as the primary object and the option as its wrapper.

This skill covers those conventions and the mechanics that follow: how a premium in vol points becomes an amount of currency, how spot, forward, and premium-adjusted deltas differ, how a risk reversal and butterfly describe the skew, when the expiry cuts, and how barrier structures behave near their triggers. The generic greeks and option structures belong to another skill, and the boundary is stated in each leaf.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## When to use

- When pricing or trading an FX option and the quote conventions matter.
- When a risk reversal, butterfly, or ATM straddle quote needs interpreting.
- When settlement, expiry cut, or delivery mechanics decide the outcome.
- When a barrier or digital structure's behaviour near the trigger matters.

## When NOT to use

- For greeks, implied volatility surfaces in general, and option structures (use ac-options-and-volatility).
- For spot FX trading mechanics (use ac-forex-trading).
- For hedging a portfolio's currency exposure with forwards or options (use ac-currency-and-fx-risk).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/fx-option-conventions.md` | `investing/fx-option-conventions` | Premium in vol points, expiry cuts, and settlement conventions. |
| `subskills/fx-delta-conventions.md` | `investing/fx-delta-conventions` | Spot, forward, and premium-adjusted delta, and why three exist. |
| `subskills/fx-vol-quotes.md` | `investing/fx-vol-quotes` | ATM straddle, 25-delta risk reversal, and butterfly as the market's volatility quote. |
| `subskills/fx-exercise-and-delivery.md` | `investing/fx-exercise-and-delivery` | European and American exercise, delivery versus cash settlement, and NDF options. |
| `subskills/fx-barriers-and-digitals.md` | `investing/fx-barriers-and-digitals` | Knock-ins, knock-outs, one-touch, and the behaviour near the trigger. |
| `subskills/fx-option-hedging.md` | `investing/fx-option-hedging` | Delta hedging in spot, vega management, and the cost of rehedging. |
| `subskills/fx-option-record.md` | `investing/fx-option-record` | The written record: pair, strike or delta, vol, premium, and barrier terms. |

## Status and honest limits

FX option conventions are market-specific and vary between currency pairs, between counterparties, and over time; a quote that is standard for one pair may be ambiguous for another. Premium-adjusted delta exists precisely because the naive conventions produce inconsistent hedges. Nothing here recommends a position, and a structure whose payoff depends on a barrier, a fixing, or an expiry cut must be read in the confirmation rather than inferred from the term sheet's summary.
