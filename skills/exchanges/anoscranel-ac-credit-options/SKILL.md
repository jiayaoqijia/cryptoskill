---
name: ac-credit-options
description: "Trading credit options by their own mechanics: payer and receiver options on single-name CDS, expiry against the underlying swap, spread volatility and recovery assumptions, options on credit indices, exercise and settlement into protection, dealer liquidity, hedging with credit options, and the written record. It explains how the instruments quote and settle; it never recommends a credit or predicts a default. Use when asking \"CDS option\", \"credit spread volatility\", \"option on CDS index\", \"swaption on credit\", \"credit vol quote\", \"how does a CDS option settle\". Not for generic greeks and structures (ac-options-and-volatility), not for CDS mechanics and basis (ac-credit-derivatives), not for assessing a borrower (ac-bank-and-credit-analysis)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Credit options

## Overview

A credit option gives the right to enter a credit default swap at a stated spread on a stated date. It is quoted in spread volatility rather than in a price, and its underlying is the swap's spread rather than a bond's yield. Those two facts place it between the CDS market and the options market, and they mean that a trader who understands both still has to learn the conventions that connect them.

This skill covers those conventions: the structure of payer and receiver options, how expiry relates to the underlying swap, how spread volatility is quoted and why recovery matters, how options on credit indices differ from single-name options, and how these instruments are hedged and settled. CDS mechanics belong to the credit derivatives skill, and the generic greeks belong to the options skill.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## When to use

- When trading or pricing an option on a single-name CDS.
- When an option on a credit index is being used to hedge or express a view.
- When a spread volatility quote needs interpreting or comparing.
- When exercise and settlement into protection need to be planned.

## When NOT to use

- For greeks, surfaces in general, and option structures (use ac-options-and-volatility).
- For CDS mechanics, spread DV01, and the basis (use ac-credit-derivatives).
- For analysing a borrower's ability to repay (use ac-bank-and-credit-analysis).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/cds-options-mechanics.md` | `investing/cds-options-mechanics` | Payer and receiver options, expiry against the swap, and the upfront. |
| `subskills/credit-spread-volatility.md` | `investing/credit-spread-volatility` | Spread volatility, quoting conventions, and the role of assumed recovery. |
| `subskills/index-options-and-tranches.md` | `investing/index-options-and-tranches` | Options on credit indices, and the correlation that tranches carry. |
| `subskills/credit-option-settlement.md` | `investing/credit-option-settlement` | Exercise into protection, cash settlement, and the documentation. |
| `subskills/credit-option-liquidity.md` | `investing/credit-option-liquidity` | Dealer liquidity, size, and the bid-offer in spread terms. |
| `subskills/hedging-with-credit-options.md` | `investing/hedging-with-credit-options` | Vega and spread DV01, and what a delta hedge in credit does not cover. |
| `subskills/credit-option-record.md` | `investing/credit-option-record` | The written record: reference, expiry, spread, recovery, and settlement. |

## Status and honest limits

Credit options are a dealer market with documentation that defines both the option and the swap it delivers into, so a position's risk depends on clauses a summary does not carry. Liquidity is thin outside the major indices, and a quote may not be executable at the size that would matter. Nothing here recommends a position, and a credit option held without its exercise and settlement terms read is a position whose payoff is assumed rather than known.
