---
name: ac-credit-rating-mechanics
description: "Reading credit ratings as a mechanism rather than an opinion: what a rating measures and what it excludes, agency methodologies and the factors that drive a notch, outlooks and watches, rating migration and default tables, fallen angels and forced-seller flows, the contract triggers a rating level activates, and the written rating record. It explains how ratings are produced and what they set off; it never recommends a credit and never predicts a downgrade. Use when asking \"credit rating\", \"rating agency\", \"downgrade risk\", \"fallen angel\", \"rating trigger\", \"notch\", \"outlook versus watch\", \"why did my bond get downgraded\", \"investment grade threshold\", \"rating migration\". Not for assessing a borrower's ability to repay (ac-bank-and-credit-analysis), not for spread levels and curve shape (ac-credit-curve), not for CDS mechanics (ac-credit-derivatives)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Credit rating mechanics

## Overview

A credit rating is an agency's opinion about the likelihood of default and, for some scales, about recovery, expressed on an ordinal scale. It is not a probability, not a recommendation, and not a valuation. What makes ratings consequential is not their accuracy but the contracts and mandates that reference them: a downgrade can force a sale, raise a borrowing cost, or trigger a collateral call, regardless of whether the agency's opinion was right.

This skill covers that mechanism: what each scale measures and excludes, how methodologies turn factors into a notch, what outlooks and watches mean operationally, how migration and default tables should be read, and which contract provisions a rating level activates. It explains the machinery and its consequences; it does not judge a particular credit.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## When to use

- When a rating, outlook, or watch is being reported or relied on.
- When a mandate, covenant, or collateral agreement references a rating level.
- When a portfolio holds names near an investment-grade threshold.
- When a downgrade has occurred or is being assessed for its consequences.

## When NOT to use

- For analysing whether a borrower can repay (use ac-bank-and-credit-analysis).
- For spread levels, curve shape, and relative value (use ac-credit-curve).
- For CDS spreads, DV01, and credit events (use ac-credit-derivatives).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/what-a-rating-measures.md` | `investing/what-a-rating-measures` | The scales, what each measures, and what a rating explicitly excludes. |
| `subskills/agency-methodologies.md` | `investing/agency-methodologies` | How factors become a notch, and where the methodologies differ. |
| `subskills/outlooks-watches-and-notches.md` | `investing/outlooks-watches-and-notches` | Outlook, watch, and the operational meaning of each. |
| `subskills/migration-and-default-tables.md` | `investing/migration-and-default-tables` | Transition matrices, default rates, and how to read them honestly. |
| `subskills/fallen-angels-and-forced-selling.md` | `investing/fallen-angels-and-forced-selling` | The investment-grade threshold and the flow a downgrade creates. |
| `subskills/rating-triggers-in-contracts.md` | `investing/rating-triggers-in-contracts` | Mandates, covenants, and collateral terms that reference a rating. |
| `subskills/rating-record.md` | `investing/rating-record` | The written record: rating, outlook, triggers, and exposure. |

## Status and honest limits

Agencies publish methodologies, and methodologies are models: they simplify, they lag, and they have historically been slow to react at the point where it mattered most. Ratings are also paid for by issuers in most markets, which is a structural conflict that disclosure does not remove. Nothing here recommends a credit, and a rating quoted without its date, its agency, and the scale it belongs to is not comparable with anything.
