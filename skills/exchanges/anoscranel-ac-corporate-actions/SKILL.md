---
name: ac-corporate-actions
description: "Handling corporate actions correctly in a portfolio and in data: splits and consolidations, dividends and distributions, mergers and acquisitions, spin-offs and rights, the price and volume adjustment that keeps history comparable, the accounting and tax treatment, and the written corporate-actions record. It explains mechanics and record-keeping; it never recommends a security or predicts an outcome. Use when asking \"stock split\", \"dividend adjustment\", \"merger arbitrage\", \"spin-off\", \"rights issue\", \"adjusted prices\", \"corporate action\". Not for valuation (ac-valuation), not for equity research (ac-equity-research), not for tax computation (ac-trading-records-and-tax)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Corporate actions

## Overview

A corporate action changes the terms of a holding, and the change arrives through a mechanism — a split ratio, a dividend record date, a merger consideration, a spin-off distribution — each with its own timetable and its own effect on the data. Most portfolio accounting errors trace back to one of these, and most backtest errors trace back to a price series that was never adjusted.

This skill is the mechanics and the record. It does not judge whether an acquisition is good or bad; it makes sure the position, the cost basis, the adjusted history and the tax record all agree once the action has happened.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## When to use

- When a holding announces a split, dividend, merger, spin-off, or rights issue.
- When a historical price series is being used and its adjustment is unknown.
- When cost basis must be recalculated or documented.
- When reconciling a portfolio against a broker statement.

## When NOT to use

- For valuing a company before or after an action (use ac-valuation).
- For the annual tax pack and jurisdiction questions (use ac-trading-records-and-tax).
- For order timing around an event (use ac-equity-market-structure).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/splits-and-consolidations.md` | `investing/splits-and-consolidations` | Ratios, the share count change, and why the price is not a return. |
| `subskills/dividends-and-distributions.md` | `investing/dividends-and-distributions` | Ex-dates, record dates, withholding, and the difference between income and total return. |
| `subskills/mergers-and-acquisitions.md` | `investing/mergers-and-acquisitions` | Cash, stock, and mixed consideration, and what each does to the position and the basis. |
| `subskills/spin-offs-and-rights.md` | `investing/spin-offs-and-rights` | Distributed shares and rights issues, and the basis allocation problem. |
| `subskills/price-and-volume-adjustment.md` | `investing/price-and-volume-adjustment` | Adjusting history so a chart is comparable, and the difference between adjusted and total-return series. |
| `subskills/corporate-action-accounting.md` | `investing/corporate-action-accounting` | Cost basis, proceeds, and the treatment questions a professional must answer. |
| `subskills/corporate-actions-record.md` | `investing/corporate-actions-record` | The written record: action, terms, dates, effects on position, basis, and data. |

## Status and honest limits

Terms and timetables are set by the issuer and the exchange, and they change: a deal can be revised, a record date can move, and a distribution can be reclassified. Every fact here is a structure to verify against the issuer's own announcement before relying on it, and the record should name the document it was verified against.
