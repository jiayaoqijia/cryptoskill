---
name: ac-rates-trading
description: "Trading government bond futures as a venue: contract specifications and the cheapest-to-deliver, DV01 and hedge ratios, net basis and the delivery option, repo financing and specials, curve and butterfly trades, central-bank and auction calendars, and the written rates trading record. It explains how the contracts and the curve work; it never recommends a rate view or predicts yields. Use when asking \"bond futures\", \"cheapest to deliver\", \"DV01\", \"hedge ratio for Treasuries\", \"2s10s\", \"net basis\", \"repo special\", \"why did my bond future track the CTD\". Not for bond price and duration mechanics in a portfolio (ac-fixed-income-and-rates), not for macro release reading (ac-macro-and-policy-reading), not for perpetual funding (ac-funding-and-basis)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Rates trading

## Overview

A government bond future is a contract on a notional bond, settled by delivering one of several eligible bonds. That design creates the two objects a rates trader actually trades: the cheapest-to-deliver, which is the bond the short will hand over, and the basis, which is the difference between the future and that bond's cash price after carry. Everything else — DV01, hedge ratios, curve spreads — is built on those two.

This skill covers that structure and the mechanics around it: contract specifications, the conversion factor that equalises delivery, the delivery option embedded in the short's choice, repo financing and its specials, and the curve trades that express a view on the shape rather than the level. Bond mathematics for a portfolio belongs to a different skill, and the boundary is stated in each leaf.

Primary sources: <https://www.cmegroup.com/> and <https://www.federalreserve.gov/>.

## When to use

- When trading or hedging with government bond futures.
- When a basis, a hedge ratio, or a delivery decision needs to be worked out.
- When repo financing or a special collateral rate affects the position.
- When a curve or butterfly trade is being structured.

## When NOT to use

- For bond price, yield, and duration mechanics in a portfolio (use ac-fixed-income-and-rates).
- For reading central-bank communication and macro releases (use ac-macro-and-policy-reading).
- For perpetual futures funding and basis on crypto venues (use ac-funding-and-basis).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/bond-futures-basics.md` | `investing/bond-futures-basics` | Notional coupon, conversion factors, eligible baskets, and invoice price. |
| `subskills/dv01-and-hedging.md` | `investing/dv01-and-hedging` | DV01, hedge ratios, and duration-weighted hedging across the curve. |
| `subskills/ctd-and-basis.md` | `investing/ctd-and-basis` | Cheapest-to-deliver, net basis, and the delivery option the short owns. |
| `subskills/repo-and-financing.md` | `investing/repo-and-financing` | Repo rates, specials, and the carry of a long or short position. |
| `subskills/curve-trades.md` | `investing/curve-trades` | Steepener, flattener, and butterfly structures with DV01-neutral weights. |
| `subskills/central-bank-and-events.md` | `investing/central-bank-and-events` | Meeting dates, auction calendar, and settlement events that move the basis. |
| `subskills/rates-trading-record.md` | `investing/rates-trading-record` | The written record: contract, CTD, DV01, financing, and curve exposure. |

## Status and honest limits

The cheapest-to-deliver changes with yields, and a hedge computed on today's CTD is not the hedge tomorrow. Delivery options, conversion factors, and repo specials are exchange- and market-specific, and they change with the contract cycle. Every number here is a measurement with a date, and a rates position that has not been re-checked against the current CTD and the current repo rate has not been measured at all.
