---
name: ac-commodities-trading
description: "Trading commodity futures as a venue: contract specifications and tick value, curve shape and roll yield, storage and convenience yield, seasonality and inventory data, margin and delivery obligations, calendar and processing spreads, and the written commodity trading record. It explains how the contracts work; it never recommends a commodity or predicts a price. Use when asking \"contango\", \"backwardation\", \"roll yield\", \"first notice day\", \"crack spread\", \"crush spread\", \"commodity futures contract size\", \"why does my oil ETF decay\". Not for holding commodities as an asset class (ac-alternatives-and-real-assets), not for currency or rate exposure (ac-currency-and-fx-risk), not for perpetual futures funding (ac-funding-and-basis)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Commodities trading

## Overview

A commodity futures contract is an agreement about a specific grade of a physical good, at a specific location, at a specific date. Everything a trader needs to know lives in that sentence: the grade determines which deliverable qualifies, the location determines the freight and the basis, and the date determines which contract month carries the storage and the risk. Trading the curve means trading those relationships, not only the headline price.

This skill covers the mechanics of that market: contract specifications, the shape of the curve and what it pays or costs to hold a position, the physical facts that drive the curve, the margin and delivery obligations that arrive with a contract, and the spreads that express a view on processing or timing rather than on price. Holding commodities as a portfolio exposure is a different problem, and the boundary is stated.

Primary sources: <https://www.cftc.gov/> and <https://www.cmegroup.com/>.

## When to use

- When trading or analysing a commodity futures contract.
- When a curve shape, roll yield, or contract roll needs to be understood.
- When a delivery, notice, or expiry obligation is approaching.
- When a spread expresses the intended view better than an outright position.

## When NOT to use

- For commodities as an asset-class allocation (use ac-alternatives-and-real-assets).
- For perpetual futures funding on crypto venues (use ac-funding-and-basis).
- For currency exposure in commodity-exporting economies (use ac-currency-and-fx-risk).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/futures-contract-specs.md` | `investing/futures-contract-specs` | Grade, location, size, tick value, and the expiry that defines the contract. |
| `subskills/curve-shape-and-carry.md` | `investing/curve-shape-and-carry` | Contango, backwardation, roll yield, and what holding a position pays or costs. |
| `subskills/storage-and-convenience-yield.md` | `investing/storage-and-convenience-yield` | Physical stocks, storage cost, convenience yield, and why the curve can invert. |
| `subskills/seasonality-and-inventory.md` | `investing/seasonality-and-inventory` | Seasonal patterns, inventory reports, weather, and the data that moves the curve. |
| `subskills/margin-and-delivery-risk.md` | `investing/margin-and-delivery-risk` | Initial and variation margin, notice days, and the obligations of a delivered contract. |
| `subskills/commodity-spreads.md` | `investing/commodity-spreads` | Calendar spreads, crack and crush spreads, and basis versus the physical market. |
| `subskills/commodities-trading-record.md` | `investing/commodities-trading-record` | The written record: contract, curve position, roll plan, margin, and delivery avoidance. |

## Status and honest limits

Commodity markets are physical markets with financial wrappers, and the physical side can invalidate a financial analysis quickly: a pipeline outage, a harvest, a shipping constraint. Contract specifications are set by the exchange and change; margin is set by the exchange and the broker and changes more often. Any position that can reach delivery must be treated as a physical commitment until it is closed, and a trader who has not read the notice rules has not understood the position.
