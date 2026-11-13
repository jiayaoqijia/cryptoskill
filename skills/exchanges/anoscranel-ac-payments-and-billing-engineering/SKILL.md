---
name: ac-payments-and-billing-engineering
description: "Moving money: the payment intent as the durable state machine, idempotency keys scoped to the money operation, authorization versus capture as two liability moments, decline handling that never doubles a charge, webhooks as confirmation, the double-entry ledger behind every balance, dunning and subscription lifecycle states, proration and metered billing, dispute evidence, PCI scope and card boundaries, and the payments record. It never recommends a processor. Use when asking \"charge a card\", \"payment state machine\", \"idempotency key\", \"authorization versus capture\", \"webhook signature verification\", \"double entry bookkeeping\", \"trial then charge\", \"failed renewal\", \"dunning\", \"proration\", \"metered billing\", \"chargeback evidence\", \"PCI scope\", \"why was the customer charged twice\". Not for general API design and idempotency (ac-api-design), not for webhook delivery to consumers (ac-webhook-and-async-delivery), not for money representation and rounding (ac-money-arithmetic)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Payments and billing engineering

## Overview

Payments engineering is transaction integrity under adversarial conditions. The bank network may approve, decline, or time out; the customer may dispute; the network may retry on its own schedule. Every design decision that matters comes from one fact: a money operation cannot be undone by the code that performed it — reversal is a second operation with its own failure modes. The craft is building so every outcome has a definite state.

The core instrument is the ledger: an append-only double-entry record where every movement has a matching movement. Balances, invoices, and payouts are derived views, never the source of truth. Payment state lives in explicit machines — intent, authorization, capture, refund, dispute — and transitions are written before the webhooks arrive: a webhook confirms a state change; it never carries the authority to make one.

Primary sources: <https://docs.stripe.com/billing/subscriptions/overview> and <https://www.pcisecuritystandards.org/document_library/>.

## When to use

- When charging cards, collecting subscriptions, or metering usage.
- When building checkout, renewal, dunning, or refund flows.
- When storing or touching card data.
- When reconciling processor reports against internal records.

## When NOT to use

- For general idempotency and API-shape design (use ac-api-design).
- For webhook delivery when you are the sender (use ac-webhook-and-async-delivery).
- For money representation and rounding arithmetic (use ac-money-arithmetic).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/payment-state-machine.md` | `software-engineering/payment-state-machine` | The intent as a state machine; states as money-positions, not screen labels. |
| `subskills/idempotent-charging.md` | `software-engineering/idempotent-charging` | Idempotency keys scoped to the operation the customer believes is one. |
| `subskills/authorization-and-capture.md` | `software-engineering/authorization-and-capture` | Two liability moments, the delay between them, and void versus refund. |
| `subskills/declines-and-retries.md` | `software-engineering/declines-and-retries` | The decline taxonomy, honest retries, and how to never create a duplicate charge. |
| `subskills/webhook-reconciliation.md` | `software-engineering/webhook-reconciliation` | Webhooks confirm, they do not command; state must be inferable without them. |
| `subskills/the-ledger.md` | `software-engineering/ledger-double-entry` | Double entry as the invariant; balances as aggregates, never updates-in-place. |
| `subskills/subscription-lifecycle.md` | `software-engineering/subscription-lifecycle` | Trials, dunning cycles, and the states between paid and cancelled. |
| `subskills/proration-and-metering.md` | `software-engineering/proration-and-metering` | Prorate as arithmetic you can show; metering as an aggregation pipeline. |
| `subskills/disputes-and-chargebacks.md` | `software-engineering/disputes-and-chargebacks` | Evidence assembly as a designed output; the economics of represent-or-accept. |
| `subskills/pci-and-card-boundaries.md` | `software-engineering/pci-and-card-boundaries` | Card data boundaries: what you never store and what remains out of scope. |
| `subskills/payments-record.md` | `software-engineering/payments-record` | The written payments record: state rules, boundary, metrics, and incident history. |

## Status and honest limits

Payment systems fail in ways that only become visible during settlement, which makes \"it seems to work\" worthless as evidence. The honest position is that the processor provider's peculiarities and the card network rules change and vary by region, so the leaf content is the layer that survives those changes: state discipline, idempotency, reconciliation, and defensible boundaries. Nothing here is legal or compliance advice about your obligations under PCI DSS — the skill draws the engineering boundary; your posture is a professional question.
