---
name: ac-insurance-linked-securities
description: "Evaluating catastrophe bonds and insurance-linked securities as a risk class rather than a yield: trigger types and basis risk in parametric versus indemnity structures, collateral and the special-purpose reinsurer, expected loss and the spread over it, modelled versus realised loss experience, perils and their correlation, hurricane season and reset dynamics, and the written ILS record. It explains the structure and the loss arithmetic; it never recommends a bond and never predicts an event. Use when asking \"catastrophe bond\", \"cat bond spread\", \"insurance linked securities\", \"ILS\", \"parametric trigger\", \"indemnity trigger\", \"expected loss\", \"reinsurance sidecar\", \"industry loss warranty\", \"why did my cat bond lose money\". Not for insurance coverage decisions (ac-insurance-and-risk-transfer), not for securitisation waterfalls (ac-securitisation-and-tranches), not for pension transfers (ac-pension-risk-transfer)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Insurance-linked securities

## Overview

A catastrophe bond transfers a defined set of insurance losses from a sponsor to capital-market investors. The investor receives a floating coupon and loses principal, in whole or in part, if a specified event triggers the structure. The trigger is the product: two bonds covering the same peril can have entirely different risk because one pays on the sponsor's actual losses and another on an industry index or a physical measurement.

This skill covers that structure: trigger design and the basis risk it creates, the collateral arrangement and the special-purpose reinsurer, expected loss and how the spread should be read against it, the difference between modelled and realised experience, the correlation between perils and the seasonality that concentrates it, and the record that makes a position reviewable.

Primary sources: <https://www.sec.gov/investor> and <https://www.artemis.bm/>.

## When to use

- When evaluating a catastrophe bond or other insurance-linked instrument.
- When comparing trigger designs and the basis risk each carries.
- When reading expected loss, spread, and modelled loss metrics.
- When a portfolio's exposure to a single peril or season needs assessing.

## When NOT to use

- For general insurance coverage decisions (use ac-insurance-and-risk-transfer).
- For reinsurance company equity analysis (use ac-equity-research).
- For structured-credit waterfalls (use ac-securitisation-and-tranches).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|
| `subskills/trigger-design.md` | `investing/trigger-design` | Indemnity, industry loss, parametric, and modelled loss triggers. |
| `subskills/collateral-and-spv.md` | `investing/collateral-and-spv` | The special-purpose reinsurer, collateral quality, and counterparty terms. |
| `subskills/expected-loss-and-spread.md` | `investing/expected-loss-and-spread` | Expected loss, the multiple of it, and what the spread compensates. |
| `subskills/modelled-versus-realised.md` | `investing/modelled-versus-realised` | Model assumptions, their revisions, and the realised record. |
| `subskills/perils-and-correlation.md` | `investing/perils-and-correlation` | Peril definitions, secondary perils, and the correlation a portfolio carries. |
| `subskills/seasonality-and-reset.md` | `investing/seasonality-and-reset` | Season windows, reset dates, and the pricing around them. |
| `subskills/ils-record.md` | `investing/ils-record` | The written record: trigger, peril, expected loss, and season exposure. |

## Status and honest limits

Catastrophe loss models are structural simplifications of physical processes, and their estimates have historically been revised after events that the models underweighted. Expected loss is a model output, not a frequency observed in the data. Nothing here recommends a bond, and a position held through a season without the correlation to the rest of the portfolio stated has not been measured.
