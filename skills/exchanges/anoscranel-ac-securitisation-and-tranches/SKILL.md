---
name: ac-securitisation-and-tranches
description: "Reading a securitisation as structure rather than as a bond: special-purpose vehicles and true sale, the cash-flow waterfall and subordination, credit enhancement through overcollateralisation and excess spread, tranche attachment and detachment, triggers and early amortisation, servicer behaviour and commingling, prepayment and weighted average life, and the written structure record. It explains how the structure distributes cash and loss; it never recommends a tranche and never predicts default. Use when asking \"securitisation\", \"tranche\", \"waterfall\", \"credit enhancement\", \"overcollateralisation\", \"excess spread\", \"subordination\", \"servicer\", \"weighted average life\", \"CLO\", \"RMBS\", \"why did my AAA tranche lose money\". Not for credit index tranches as a trade (ac-credit-derivatives), not for corporate bond spreads (ac-fixed-income-and-rates), not for bank balance sheets (ac-bank-and-credit-analysis)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Securitisation and tranches

## Overview

A securitisation pools assets into a special-purpose vehicle and issues claims against the pool's cash flow in a defined order. The order is the product. Two investors holding claims on the same pool can have entirely different risk because one is paid first and the other is paid last, and the rules that decide who absorbs the first loss are written in the waterfall, the enhancement structure, and the trigger tests.

This skill covers that structure: how the vehicle is separated from its originator, how cash moves through the waterfall, how enhancement is built from subordination and overcollateralisation, what triggers change the distribution, and why the servicer's behaviour is a risk the documents address but cannot eliminate. It is about reading a structure, not about choosing a tranche.

Primary sources: <https://www.sec.gov/investor> and <https://www.federalreserve.gov/>.

## When to use

- When reading an offering document for an asset-backed or mortgage-backed security.
- When a tranche's position in the waterfall needs establishing.
- When triggers, early amortisation, or servicer behaviour could change cash flow.
- When weighted average life and prepayment assumptions need stress-testing.

## When NOT to use

- For index tranches as a credit trade (use ac-credit-derivatives).
- For plain corporate bond pricing and duration (use ac-fixed-income-and-rates).
- For the originator's own credit (use ac-bank-and-credit-analysis).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/spv-and-true-sale.md` | `investing/spv-and-true-sale` | Bankruptcy remoteness, true sale, and what happens if the originator fails. |
| `subskills/waterfall-and-subordination.md` | `investing/waterfall-and-subordination` | The order in which cash and losses are allocated across tranches. |
| `subskills/credit-enhancement.md` | `investing/credit-enhancement` | Overcollateralisation, excess spread, reserve accounts, and how much loss they absorb. |
| `subskills/tranche-attachment.md` | `investing/tranche-attachment` | Attachment, detachment, and the loss window a tranche actually occupies. |
| `subskills/triggers-and-amortisation.md` | `investing/triggers-and-amortisation` | Performance triggers, early amortisation, and the redistribution they cause. |
| `subskills/servicer-and-operations.md` | `investing/servicer-and-operations` | Servicing standards, commingling, replacement, and the operational risk in the pool. |
| `subskills/prepayment-and-wal.md` | `investing/prepayment-and-wal` | Prepayment assumptions, weighted average life, and why stated maturity misleads. |
| `subskills/securitisation-record.md` | `investing/securitisation-record` | The written structure record: tranche, enhancement, triggers, and servicer terms. |

## Status and honest limits

Structures are documented in offering materials that run to hundreds of pages, and the summary a distributor provides is not the document. Triggers, definitions of default, and servicing standards are where the losses actually occur, and they change between deals for the same asset class. Nothing here recommends a tranche, and a structure analysed from a term sheet rather than the indenture has not been analysed.
