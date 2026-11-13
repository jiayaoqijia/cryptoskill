---
name: ac-structured-products
description: "Reading structured notes and packaged retail products: payoff architecture and capital protection, autocalls and reverse convertibles, participation notes, the issuer credit and the embedded derivative, pricing and the cost stack including decomposition into a bond and option components, suitability and mis-selling patterns, and the written product record. It explains mechanics and risk; it never recommends a product or predicts an outcome. Use when asking \"structured note\", \"autocallable\", \"capital protected note\", \"reverse convertible\", \"participation note\", \"barrier\", \"is this structured product worth it\". Not for fund and ETF vehicles (ac-fund-selection), not for plain options (ac-options-and-volatility), not for bond mechanics (ac-fixed-income-and-rates)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Structured products

## Overview

A structured product is a bond issued by a bank whose return is replaced by the payoff of an embedded derivative. The holder is therefore taking two exposures at once: to the issuer's ability to pay, and to a rule set that determines the payoff. That combination is why these products are hard to compare and easy to mis-describe — the marketing shows the participation, and the documentation holds the barriers, the averaging, and the issuer credit.

The craft is decomposing the note. Almost every retail structure can be read as a bond plus one or more options, and once it is read that way the cost becomes visible: the difference between the issue price and the value of the components is the distribution and structuring margin. This skill teaches that decomposition and the questions that follow; it does not judge whether a note will pay.

Primary sources: <https://www.sec.gov/investor> and <https://www.esma.europa.eu/>.

## When to use

- When a structured note, autocall, or capital-protected product is offered.
- When comparing a structured product with buying the components directly.
- When a barrier or autocall condition needs reading before a decision.
- When a product's suitability or its cost is being questioned.

## When NOT to use

- For fund and ETF vehicles (use ac-fund-selection).
- For plain listed options (use ac-options-and-volatility).
- For bond price and duration mechanics (use ac-fixed-income-and-rates).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/payoff-architecture.md` | `investing/payoff-architecture` | Capital protection, participation, barriers, and the payoff diagram the note actually promises. |
| `subskills/autocalls-and-reverse-convertibles.md` | `investing/autocalls-and-reverse-convertibles` | Early redemption triggers, coupon conditions, and the short-volatility profile they create. |
| `subskills/capital-protection.md` | `investing/capital-protection` | What "protected" means, at what level, from what, and subject to whose credit. |
| `subskills/issuer-and-embedded-derivative.md` | `investing/issuer-and-embedded-derivative` | The bank's credit, the hedge, and the two exposures a note bundles into one line. |
| `subskills/structured-product-pricing.md` | `investing/structured-product-pricing` | Decomposition into bond plus options, the issue-price gap, and the secondary-market spread. |
| `subskills/suitability-and-mis-selling.md` | `investing/suitability-and-mis-selling` | Who the product is for, the disclosure failures that recur, and the questions that expose them. |
| `subskills/structured-product-record.md` | `investing/structured-product-record` | The written record: payoff, issuer, cost, scenarios, and the review triggers. |

## Status and honest limits

Payoff documents are legally binding and marketing summaries are not; the gap between them is where most losses in this category begin. Pricing a note requires a model and inputs that a retail buyer does not have, so the honest approach is comparative and qualitative: decompose what is offered, price the visible components as far as public data allows, and treat the unmeasurable remainder as a cost to be justified. Nothing here is investment advice, and a note that cannot be explained in plain sentences should not be bought on the strength of a summary.
