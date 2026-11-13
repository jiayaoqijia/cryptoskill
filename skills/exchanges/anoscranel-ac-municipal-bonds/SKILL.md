---
name: ac-municipal-bonds
description: "Reading the municipal bond market on its own terms: general obligation versus revenue pledges, tax-equivalent yield and the tax status that drives it, call features and refunding arithmetic, insurer wraps and their residual value, official statements and continuing disclosure, pension and OPEB liabilities behind a credit, and the written municipal record. It explains the pledge, the tax treatment and the credit arithmetic; it never recommends a bond and never predicts a default. Use when asking \"municipal bond\", \"general obligation\", \"revenue bond\", \"tax equivalent yield\", \"muni call\", \"refunding\", \"bond insurer\", \"official statement\", \"muni pension liability\", \"why is the muni yield lower\". Not for corporate credit analysis (ac-bank-and-credit-analysis), not for sovereign debt restructuring (ac-sovereign-debt), not for the taxable bond curve (ac-fixed-income-and-rates)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Municipal bonds

## Overview

A municipal bond is a loan to a state, a city, or an authority, and the two things that distinguish it are the pledge behind the payment and the tax treatment of the interest. The pledge decides the credit: a general obligation bond is backed by the issuer's taxing power, while a revenue bond is backed by the cash flow of a specific project and nothing else. The tax treatment decides the yield comparison: tax-exempt interest is worth more to a taxable investor than its stated rate, and the conversion is the first arithmetic in the market.

This skill covers those mechanics and the ones that follow: how call features and refundings change the expected life, what a bond insurer's wrap does and does not do, how to read an official statement and its continuing disclosure, and how pension and other post-employment obligations sit behind a credit. The taxable curve and corporate credit belong to other skills.

Primary sources: <https://www.msrb.org/> and <https://www.sec.gov/investor>.

## When to use

- When evaluating a municipal bond and its pledge structure.
- When comparing a tax-exempt yield with a taxable alternative.
- When a call, a refunding, or an insurer's rating change affects the position.
- When an issuer's pension or OPEB liability needs reading.

## When NOT to use

- For corporate credit analysis (use ac-bank-and-credit-analysis).
- For sovereign debt and its restructuring process (use ac-sovereign-debt).
- For taxable bond price, yield, and duration mechanics (use ac-fixed-income-and-rates).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/go-versus-revenue.md` | `investing/go-versus-revenue` | Taxing power versus project cash flow, and what each pledge actually reaches. |
| `subskills/tax-equivalent-yield.md` | `investing/tax-equivalent-yield` | Tax-exempt versus taxable comparison, and the investor's own bracket. |
| `subskills/calls-and-refunding.md` | `investing/calls-and-refunding` | Call schedules, refunding logic, and the yield to call that matters. |
| `subskills/insurer-wraps.md` | `investing/insurer-wraps` | What a wrap guarantees, its cost, and its residual value after a downgrade. |
| `subskills/disclosure-and-official-statements.md` | `investing/disclosure-and-official-statements` | Official statements, continuing disclosure, and where the gaps are. |
| `subskills/pension-and-opeb-liabilities.md` | `investing/pension-and-opeb-liabilities` | Unfunded obligations and how they compete with bondholders. |
| `subskills/municipal-record.md` | `investing/municipal-record` | The written record: pledge, tax status, call schedule, and credit findings. |

## Status and honest limits

Municipal disclosure is uneven: official statements are filed at issuance, continuing disclosure arrives annually at best, and the financial information may be a year old by the time it is read. Tax treatment depends on the investor's jurisdiction and circumstances, and this skill does not compute a liability. Nothing here recommends a bond, and an insured municipal is only as strong as the weaker of the issuer and the insurer, which is the comparison the wrap leaf exists to make explicit.
