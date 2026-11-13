---
name: ac-credit-derivatives
description: "Trading credit as a venue: single-name credit default swaps and their mechanics, spread DV01 and hedging, credit indices and their rolls, the basis between cash bonds and derivatives, recovery and default events, liquidity and counterparty terms, and the written credit trading record. It explains how the instruments work; it never recommends a credit or predicts a default. Use when asking \"CDS spread\", \"spread DV01\", \"credit index roll\", \"CDS-bond basis\", \"credit event\", \"is my CDS hedge working\", \"IG vs HY index\". Not for analysing a borrower's credit quality (ac-bank-and-credit-analysis), not for bond price mechanics (ac-fixed-income-and-rates), not for venue due diligence (ac-perp-venue-diligence)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Credit derivatives

## Overview

A credit default swap is a contract in which one side pays a periodic premium and the other pays out if a defined credit event occurs. It is insurance with a tradable price, and the price — the spread — is quoted in basis points per year. Buying protection and selling protection are the two directions, and they are not symmetric in their mechanics: one pays premium, the other receives it against the obligation to pay out.

This skill covers the trading mechanics: how spreads convert into a sensitivity, how indices differ from single names, why the derivative and the cash bond can trade at different levels, what a credit event triggers, and what the record must contain. Judging whether a borrower will repay belongs to credit analysis; this skill assumes the view exists and asks how it is expressed and measured.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## When to use

- When trading single-name or index credit protection.
- When a hedge needs to be sized in spread sensitivity rather than notional.
- When the cash bond and the derivative imply different levels.
- When a credit event or a restructuring question affects a position.

## When NOT to use

- For assessing a borrower's ability to repay (use ac-bank-and-credit-analysis).
- For bond price, yield, and duration arithmetic (use ac-fixed-income-and-rates).
- For evaluating a trading venue's solvency (use ac-perp-venue-diligence).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/cds-mechanics.md` | `investing/cds-mechanics` | Premium legs, protection legs, quoting conventions, and settlement. |
| `subskills/spread-dv01.md` | `investing/spread-dv01` | Spread sensitivity, hedge ratios, and why notional matching misleads. |
| `subskills/credit-indices.md` | `investing/credit-indices` | Index composition, the roll, and the difference between index and single-name risk. |
| `subskills/cds-bond-basis.md` | `investing/cds-bond-basis` | Why the cash bond and the derivative diverge, and what closes the gap. |
| `subskills/credit-events.md` | `investing/credit-events` | Default, restructuring, and the auction that settles protection. |
| `subskills/credit-liquidity-and-terms.md` | `investing/credit-liquidity-and-terms` | Dealer liquidity, documentation, and counterparty terms. |
| `subskills/credit-trading-record.md` | `investing/credit-trading-record` | The written record: direction, spread, DV01, event exposure, and review. |

## Status and honest limits

Credit derivatives are documented contracts, and the documentation decides what counts as an event and what settles. A position whose economics rest on a judgement about recovery, or on a definition the trader has not read, is a position whose risk is legal as much as market. Liquidity in single names can disappear quickly, and the instruments here are not suitable for every account; where access requires eligibility, that constraint is part of the assessment.
