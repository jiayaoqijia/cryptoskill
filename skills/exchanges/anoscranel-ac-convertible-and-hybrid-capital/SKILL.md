---
name: ac-convertible-and-hybrid-capital
description: "Analysing convertible bonds and hybrid capital as one instrument class: conversion parity and premium, the bond floor and credit sensitivity, yield to worst and yield to call, the issuer's call and the holder's put, busted converts and distressed conversion, bank AT1 and contingent capital triggers, perpetual structures and call expectations, the conversion price adjustment on a corporate action, and the written hybrid record. It explains the arithmetic and the structure; it never recommends a security and never predicts a conversion. Use when asking \"convertible bond\", \"conversion premium\", \"bond floor\", \"busted convert\", \"yield to worst\", \"AT1\", \"CoCo trigger\", \"perpetual bond\", \"additional tier one\", \"why did my convertible fall with the stock\". Not for retail structured notes and reverse convertibles (ac-structured-products), not for plain bond duration and pricing (ac-fixed-income-and-rates), not for the issuer's equity case (ac-equity-research)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Convertible and hybrid capital

## Overview

A convertible bond is three instruments wearing one ISIN: a corporate bond that pays a coupon and carries credit risk, an equity option embedded in the conversion right, and a financing decision the issuer makes when it chooses the coupon and the conversion premium. A hybrid — a bank AT1, an insurance perpetual, an industrial preferred — is the same logic pushed further: equity-like loss absorption in exchange for a coupon that sits above the issuer's senior debt.

Reading either requires holding all the pieces at once. A convertible that falls with the stock and rises with credit is behaving correctly; the surprise is always that one of the three exposures has become dominant. This skill covers that arithmetic and those structures, and stops short of recommending an instrument.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## When to use

- When analysing a convertible bond and its conversion terms.
- When a convertible's price has moved against the underlying and the cause needs separating.
- When a hybrid or contingent capital instrument's trigger and coupon terms matter.
- When comparing a convertible with the equivalent stock-plus-bond combination.

## When NOT to use

- For retail structured notes and reverse convertibles (use ac-structured-products).
- For plain bond pricing, duration, and yield mechanics (use ac-fixed-income-and-rates).
- For the issuer's equity investment case (use ac-equity-research).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/conversion-parity-and-premium.md` | `investing/conversion-parity-and-premium` | Parity, conversion premium, and what the premium pays for. |
| `subskills/bond-floor-and-credit.md` | `investing/bond-floor-and-credit` | The bond floor, credit spread sensitivity, and the floor that moves. |
| `subskills/yield-to-worst-and-call.md` | `investing/yield-to-worst-and-call` | Yield to worst, the issuer's call, and the holder's put. |
| `subskills/busted-and-distressed-converts.md` | `investing/busted-and-distressed-converts` | Busted converts, distressed conversion, and workout exposure. |
| `subskills/contingent-capital.md` | `investing/contingent-capital` | AT1, CoCo triggers, coupon cancellation, and the loss path. |
| `subskills/perpetuals-and-call-expectations.md` | `investing/perpetuals-and-call-expectations` | Perpetual structures and the call the market expects. |
| `subskills/hybrid-capital-record.md` | `investing/hybrid-capital-record` | The written record: parity, floor, triggers, and the three exposures. |

## Status and honest limits

Convertible and hybrid terms are contractual and jurisdiction-specific, and the trigger mechanics in contingent capital have been tested in only a handful of real events. Valuing the embedded option requires a credit-adjusted model and a volatility input that the market supplies rather than the analyst. Nothing here recommends an instrument, and a hybrid held without its trigger, coupon-cancellation, and call terms read is a position whose loss path is assumed rather than known.
