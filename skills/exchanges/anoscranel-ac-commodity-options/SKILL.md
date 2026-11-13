---
name: ac-commodity-options
description: "Trading commodity options by their own mechanics: options on futures and their expiry before the future, American exercise and early assignment, supply-driven skew and seasonal volatility, average-price and spread options, exercising into delivery risk, hedging physical exposure, and the written record. It explains how the contracts behave; it never recommends a commodity or predicts a price. Use when asking \"options on crude futures\", \"commodity option expiry\", \"early exercise commodity option\", \"average price option\", \"Asian option\", \"crack spread option\", \"why is the skew so wide in gas\". Not for generic greeks and structures (ac-options-and-volatility), not for commodity futures mechanics (ac-commodities-trading), not for commodity allocation (ac-alternatives-and-real-assets)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Commodity options

## Overview

Most commodity options are options on futures, not options on the spot commodity. Their expiry comes before the underlying future's first notice day, their exercise delivers a futures position rather than a good, and their volatility is shaped by supply conditions rather than by a single index. Those three facts decide most of what is different about trading them.

This skill covers that structure: the timing of expiry against delivery, the consequences of American exercise, the skew that a physical market produces, the seasonal pattern in volatility, and the average-price structures that hedgers use. Commodity futures mechanics belong to their own skill, and the generic greeks belong to the options skill; this one is about what changes when the underlying is a physical market.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## When to use

- When trading options on commodity futures.
- When expiry, exercise, or assignment could create a futures or delivery obligation.
- When the volatility skew or term structure looks unusual and needs explaining.
- When a hedger needs an average-price or spread structure.

## When NOT to use

- For greeks, implied volatility surfaces in general, and structures (use ac-options-and-volatility).
- For futures contract specifications, margin, and delivery (use ac-commodities-trading).
- For commodity exposure as an asset class (use ac-alternatives-and-real-assets).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/options-on-futures.md` | `investing/options-on-futures` | The option's expiry, the future's expiry, and the gap between them. |
| `subskills/american-exercise.md` | `investing/american-exercise` | Early exercise, assignment into a futures position, and the resulting margin. |
| `subskills/commodity-vol-skew.md` | `investing/commodity-vol-skew` | Supply-driven skew, and why the wings are priced where they are. |
| `subskills/seasonal-volatility.md` | `investing/seasonal-volatility` | Volatility that follows the crop or heating calendar, and the term structure it creates. |
| `subskills/average-and-spread-options.md` | `investing/average-and-spread-options` | Asian and average-price options, and options on processing spreads. |
| `subskills/commodity-option-hedging.md` | `investing/commodity-option-hedging` | Hedging a physical exposure with options, and what the hedge does not cover. |
| `subskills/commodity-option-record.md` | `investing/commodity-option-record` | The written record: contract, expiry gap, exercise terms, and delivery avoidance. |

## Status and honest limits

Commodity options can be exercised into a futures position that then carries delivery obligations, and the timing of that chain is exchange-specific and changes with each contract cycle. Volatility in these markets is driven by events that no model anticipates, and the skew reflects real physical scarcity. Nothing here recommends a position, and any structure that can end in delivery must be planned for from the day it is opened.
