---
name: ac-equity-options
description: "Trading listed equity options by their own mechanics: single-name versus index contracts, expiry and settlement conventions including AM-settled index options, dividends and early exercise, borrow and put-call parity distortions, index volatility versus component volatility and dispersion, corporate actions that adjust contracts, and the written record. It explains how the contracts behave; it never recommends a position or predicts a price. Use when asking \"SPX AM settlement\", \"weekly options expiry\", \"early exercise before dividend\", \"hard to borrow put\", \"dispersion trading\", \"index vol versus single stock vol\", \"option adjustment after a split\". Not for generic greeks and structures (ac-options-and-volatility), not for trading the underlying stock (ac-stock-trading), not for single-name event sizing (ac-stock-trading)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Equity options

## Overview

Listed equity options look standardised and are not uniform: a single-name contract settles differently from an index contract, expiries range from daily to multi-year, exercise is American for most single names and European for most indices, and corporate actions adjust the contract in ways that change what it delivers. The conventions decide the payoff, and the payoff is what the position owns.

This skill covers those mechanics: the single-name versus index distinction, the settlement conventions that decide which price an option settles against, dividend-driven early exercise, borrow effects on puts, the relationship between index and component volatility, and the adjustments triggered by corporate actions. Generic greeks and structures belong to the options skill; trading the underlying belongs to the stock trading skill.

Primary sources: <https://www.cboe.com/> and <https://www.sec.gov/investor>.

## When to use

- When trading listed equity or index options and the settlement convention matters.
- When assignment or early exercise could occur before a dividend.
- When a hard-to-borrow name's options price inconsistently with parity.
- When an index position's volatility depends on correlation rather than on components.
- When a corporate action may have adjusted a contract.

## When NOT to use

- For greeks, surfaces in general, and option structures (use ac-options-and-volatility).
- For trading the underlying stock and its events (use ac-stock-trading).
- For sizing a position into an earnings release (use ac-stock-trading).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/single-name-vs-index.md` | `investing/single-name-vs-index` | Two contract families with different settlement, liquidity, and risk. |
| `subskills/expiry-and-settlement.md` | `investing/expiry-and-settlement` | AM versus PM settlement, weekly expiries, and the price an option settles against. |
| `subskills/dividends-and-early-exercise.md` | `investing/dividends-and-early-exercise` | Dividend-driven exercise of calls, and assignment timing. |
| `subskills/borrow-and-put-parity.md` | `investing/borrow-and-put-parity` | Hard-to-borrow names, parity distortions, and what they imply. |
| `subskills/index-vol-and-dispersion.md` | `investing/index-vol-and-dispersion` | Index volatility as a function of correlation, and what dispersion trades. |
| `subskills/corporate-actions-and-options.md` | `investing/corporate-actions-and-options` | Splits, mergers, and special dividends, and the contract adjustment they trigger. |
| `subskills/equity-option-record.md` | `investing/equity-option-record` | The written record: contract family, settlement, dividends, borrow, and assignment plan. |

## Status and honest limits

Contract specifications are set by the exchange and adjusted by its rules, and the adjustment for a given corporate action is published rather than inferred. Settlement conventions differ between products that share a name, which is why the contract's own specification is the only authority. Nothing here recommends a position, and an option held through an event without its settlement and adjustment rules read is a position whose payoff is being assumed rather than known.
