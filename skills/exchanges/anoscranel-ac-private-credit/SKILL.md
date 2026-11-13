---
name: ac-private-credit
description: "Analysing private credit as an asset class rather than a borrower: direct lending structure, unitranche and first-out/last-out splits, covenant-lite terms and what a covenant gives up, PIK and amortisation, sponsor dynamics and the lender's position, mark and valuation in an illiquid book, distress and lender-on-lender conflict, and the written private-credit record. It explains the structure and the arithmetic; it never recommends a fund or predicts a default. Use when asking \"private credit\", \"direct lending\", \"unitranche\", \"covenant lite\", \"PIK interest\", \"how is my private credit fund marked\", \"lender on lender violence\", \"sponsor backed lending\". Not for assessing a single borrower's ability to repay (ac-bank-and-credit-analysis), not for the allocation decision (ac-alternatives-and-real-assets), not for private fund financing and continuation vehicles (ac-portfolio-financing)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Private credit

## Overview

Private credit is lending negotiated directly between a lender and a borrower, usually a company owned by a private-equity sponsor, and held to maturity rather than traded. The asset class grew because it offered borrowers speed and certainty and lenders a spread above syndicated loans. The risk it carries is not primarily credit analysis; it is structure, liquidity, and marking.

Those three are the subject of this skill. A direct loan's protection lives in its covenants and its position in the capital structure; its liquidity is a contractual lock rather than a market; and its valuation, in the absence of trades, is a mark the manager produces. Each of those is a discipline of its own, and each is where the losses in this asset class have actually come from.

Primary sources: <https://www.federalreserve.gov/> and <https://www.sec.gov/investor>.

## When to use

- When evaluating a private credit allocation or a direct lending fund.
- When a loan's structure, covenants, or subordination need reading.
- When a fund's mark or its valuation policy is being questioned.
- When a borrower is in distress and the lender group's incentives matter.

## When NOT to use

- For assessing one borrower's ability to repay (use ac-bank-and-credit-analysis).
- For the allocation decision across asset classes (use ac-alternatives-and-real-assets).
- For fund-level financing and continuation vehicles (use ac-portfolio-financing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/direct-lending-structure.md` | `investing/direct-lending-structure` | The loan agreement, the lender group, and how a direct deal is negotiated. |
| `subskills/unitranche-and-splits.md` | `investing/unitranche-and-splits` | Unitranche, first-out and last-out, and the agreement among lenders. |
| `subskills/covenants-and-protection.md` | `investing/covenants-and-protection` | Covenant-lite, maintenance versus incurrence, and what a covenant buys. |
| `subskills/pik-and-amortisation.md` | `investing/pik-and-amortisation` | Payment-in-kind, deferred interest, and the cash flow illusion. |
| `subskills/sponsor-dynamics.md` | `investing/sponsor-dynamics` | The sponsor's incentives, the lender's position, and where they diverge. |
| `subskills/private-credit-marks.md` | `investing/private-credit-marks` | Valuation without trades, and how a mark is produced. |
| `subskills/private-credit-record.md` | `investing/private-credit-record` | The written record: structure, covenants, marks, and the exit path. |

## Status and honest limits

Private credit marks are estimates produced by the manager and audited by an accountant, not prices discovered in a market, so a reported volatility understates the risk the position carries. Structural features differ by jurisdiction and by deal, and the terms in a marketing summary are not the terms in the credit agreement. Nothing here recommends a fund or a loan, and an allocation measured by a mark nobody traded is a measurement of the manager's judgement as much as of the asset.
