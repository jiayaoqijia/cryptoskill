---
name: ac-currency-and-fx-risk
description: "Managing currency exposure in an investment portfolio: FX spot and forward mechanics, quoting and settlement conventions, carry and interest-rate differentials, hedging foreign holdings and its cost, currency as a portfolio exposure, emerging-market convertibility and devaluation risk, operational conversion costs, and the written FX record. It explains mechanics and risk; it never recommends a currency or predicts exchange rates. Use when asking \"currency risk\", \"hedge the euro exposure\", \"FX carry\", \"currency conversion costs\", \"devaluation risk\", \"should I hedge currency\". Not for portfolio policy (ac-investment-policy-statement), not for fixed-income duration (ac-fixed-income-and-rates), not for crypto stablecoins (ac-stablecoin-collateral-risk)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Currency and FX risk

## Overview

A foreign holding carries two exposures: the asset and the currency. The second is easy to forget because it does not appear in the price you watch, and it can dominate the first over a year. Managing it is mostly a matter of deciding, in writing, which exposure you intend to own and what you will pay to remove the other.

This skill covers the mechanics and the decision frame. It does not forecast exchange rates, and it treats every hedge as a cost with a purpose rather than a free improvement.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://fred.stlouisfed.org/>.

## When to use

- When a portfolio holds assets denominated in another currency.
- When a hedge ratio is being set or reviewed.
- When converting between currencies at size.
- When exposure to an emerging-market currency is being assessed.

## When NOT to use

- For the underlying asset's own risk (use the relevant asset skill).
- For portfolio policy and constraints (use ac-investment-policy-statement).
- For stablecoin collateral risk on crypto venues (use ac-stablecoin-collateral-risk).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/fx-mechanics.md` | `investing/fx-mechanics` | Spot and forward quotes, conventions, settlement, and what a forward price contains. |
| `subskills/carry-and-differentials.md` | `investing/carry-and-differentials` | Interest-rate differentials, carry, and the parity conditions that describe the trade-off. |
| `subskills/hedging-currency-exposure.md` | `investing/hedging-currency-exposure` | Hedge ratios, instruments, the cost of hedging, and what hedging does not remove. |
| `subskills/currency-as-exposure.md` | `investing/currency-as-exposure` | Currency as its own exposure: correlation, diversification claims, and the evidence. |
| `subskills/em-convertibility-and-devaluation.md` | `investing/em-convertibility-and-devaluation` | Capital controls, convertibility, and the mechanics of a devaluation. |
| `subskills/fx-operational-costs.md` | `investing/fx-operational-costs` | Spreads, conversion timing, and the cost stack of moving money between currencies. |
| `subskills/fx-record.md` | `investing/fx-record` | The written record: exposure, hedge, cost, and falsifiers. |

## Status and honest limits

Exchange rates are prices of two economies' policies, and no framework here predicts them. The parity conditions describe long-run relationships that can be violated for years; hedging costs change with rate differentials; and an emerging-market currency can become inconvertible in ways no hedge in a domestic account can reach. The record therefore states the exposure and the decision, not a view.
