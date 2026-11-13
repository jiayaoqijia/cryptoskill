---
name: ac-fixed-income-and-rates
description: "Fixed-income and interest-rate craft for investors: bond price and yield mechanics, duration and convexity, reading the yield curve, credit spreads and their limits, inflation-linked instruments, liquidity and vehicle choice, and the written rates record. It explains mechanics and risk; it never recommends a bond, a fund, or a rate view. Use when asking \"bond math\", \"duration\", \"yield curve\", \"credit spread\", \"inflation-linked\", \"how do rates affect my portfolio\". Not for equity research (ac-equity-research), not for portfolio policy (ac-investment-policy-statement), not for crypto funding (ac-funding-and-basis)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Fixed income and rates

## Overview

A bond is a set of promised cash flows sold at a price, and almost everything in fixed income follows from the arithmetic between that price and those promises. Yield is the discount rate that equates the two; duration is the sensitivity of the price to a change in that rate; credit spread is the extra yield demanded for the risk that the promises are not kept. Understanding these four relationships is most of the craft.

The second half is judgement under uncertainty: what a curve shape means, what a spread says about the market's view of default, and where the liquidity of the instrument is worse than the liquidity of the vehicle that holds it. This skill covers both, and it is explicit that a yield is not a return unless you hold to maturity and the promises are kept.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## When to use

- When a portfolio holds or is considering bonds, bond funds, or rate-sensitive instruments.
- When interest-rate changes are affecting portfolio value and the exposure is not understood.
- When a credit spread or a curve shape is being used as a signal.
- When an inflation-linked instrument is being considered.

## When NOT to use

- For equity research or valuation (use ac-equity-research, ac-valuation).
- For policy constraints and allocation (use ac-investment-policy-statement).
- For perp funding and basis in crypto (use ac-funding-and-basis).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/yield-and-price-mechanics.md` | `investing/yield-and-price-mechanics` | The inverse relationship between price and yield, the arithmetic of a bond's cash flows, and what a yield does not tell you. |
| `subskills/duration-and-convexity.md` | `investing/duration-and-convexity` | Duration as rate sensitivity, convexity as its curvature, and the portfolio arithmetic that follows. |
| `subskills/yield-curve.md` | `investing/yield-curve` | Curve shapes, what they have historically signalled, and the limits of the signal. |
| `subskills/credit-spreads.md` | `investing/credit-spreads` | Spread as the price of default risk, ratings and their limits, and how spreads behave in stress. |
| `subskills/inflation-linked.md` | `investing/inflation-linked` | Real versus nominal yields, inflation-linked mechanics, and the breakeven arithmetic. |
| `subskills/liquidity-and-vehicles.md` | `investing/liquidity-and-vehicles` | Direct bonds versus funds and ETFs, and the liquidity mismatch that appears in stress. |
| `subskills/rates-record.md` | `investing/rates-record` | The written rates record: exposure, sensitivity, assumptions, and review triggers. |

## Status and honest limits

The mechanics are arithmetic and can be verified; the judgements are not. A curve shape is not a forecast, a spread is not a probability, and duration is a local approximation that fails for large moves. Every position in this area carries interest-rate risk, credit risk, and liquidity risk simultaneously, and the record must separate them because the responses differ.
