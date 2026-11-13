---
name: ac-saas-tax-and-geography
description: 'Charging the right tax to the right customer in the right jurisdiction: place of supply and who owes the tax, destination versus origin regimes, VAT and GST as the global default, customer location evidence from billing address to IP, business-customer reverse charge and tax IDs at checkout, tax-inclusive versus tax-exclusive display, the registration threshold decision, invoice requirements per jurisdiction, and the written tax-geography record. It explains the model a SaaS uses to decide what to charge and document; it never files a return and never names a rate for a specific sale. Use when asking "SaaS tax", "where do I collect VAT", "place of supply", "tax nexus", "tax ID validation", "B2B reverse charge", "tax exclusive versus inclusive", "geo pricing". Not for money arithmetic and rounding of the computed amount (ac-money-arithmetic), not for electronic invoicing formats (ac-business-writing), not for an individual''s tax liability (ac-trading-records-and-tax).'

license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# SaaS tax and geography

## Overview

A SaaS that sells across borders will be expected to charge each customer's tax correctly, display it properly, document it, and remit it. That means modelling the customer's tax world before payment: where the sale is deemed to occur — place of supply; who owes the tax; what evidence proves the customer's location; whether a business buyer self-assesses; and what a valid invoice for that jurisdiction requires.

This skill covers the place-of-supply model that vendors must implement, in software, to collect the right thing. SaaS tax compliance is writing code that makes the correct taxable outcome practicable; the obligation is triggered by jurisdictions, and the outcome follows from each one's place-of-supply rules for B2B and B2C sales. Everything here describes the mechanism; nothing here files returns or advises a specific sale.

Primary sources: <https://stripe.com/docs/tax> and <https://en.wikipedia.org/wiki/Value-added_tax>.

## When to use

- When a product adds billing across borders and needs to collect VAT, GST, or US sales tax.
- When an integration needs to decide whether to charge tax based on the customer's jurisdiction.
- When B2B customers provide tax IDs and need to be treated as the "reverse-charge" case.
- When a customer-facing price display needs a tax-exclusive and tax-inclusive mode from the start.

## When NOT to use

- For the arithmetic once the amount is decided — rounding rules and half-even (use ac-money-arithmetic).
- For drafting tax advice or computing liability (use ac-trading-records-and-tax for the accounting side; consult a professional for the legal side).
- For invoice documents as a writing task (use ac-business-writing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/place-of-supply.md` | `software-engineering/place-of-supply` | Which rules apply: destination versus origin, B2B versus B2C, the customer's location as the trigger. |
| `subskills/tax-id-validation.md` | `software-engineering/tax-id-validation` | VAT and EORI identifiers: checksums, registry confirmation, blocked formats, the customer's role in attestation. |
| `subskills/thresholds-and-registration.md` | `software-engineering/thresholds-and-registration` | When collecting becomes mandatory: distance-selling thresholds, currency conversion, retrospective liability. |
| `subskills/reverse-charge.md` | `software-engineering/reverse-charge` | When the buyer self-assesses: B2B services and why the VAT number is the pivotal test. |
| `subskills/tax-inclusive-and-display.md` | `software-engineering/tax-inclusive-and-display` | Tax-exclusive pricing, tax-inclusive pricing, and the line between a legal display choice and unit-of-measure confusion. |
| `subskills/invoicing-compliance.md` | `software-engineering/invoicing-compliance` | What a compliant invoice requires per jurisdiction, and why invoicing is not a cosmetic step. |
| `subskills/tax-address-evidence.md` | `software-engineering/tax-address-evidence` | Address, billing country, phone prefix, IP, and bank country as location evidence with staleness rules. |
| `subskills/tax-record.md` | `software-engineering/tax-record` | The evidence bundle: place-of-supply decision, IDs used, evidence used, amount remitted, per sale. |

## Status and honest limits

Tax law changes and rates change more often than laws do. This skill models the decision structure — location, regime, IDs, display mode, invoice requirements, thresholds — not the rates; the rates are inputs. Nothing here is tax advice; for a specific sale or filing question, professional advice is required.
