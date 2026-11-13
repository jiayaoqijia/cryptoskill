---
name: webhook-reconciliation
domain: software-engineering/webhook-reconciliation
trigger: "Building processor webhooks that confirm rather than command, and reconciling without them."
anti_trigger: "Not for webhooks you send to others, and not for payment state design."
scope: "Webhooks confirm, they do not command; state must be inferable without them."
status: seedling
---

# Webhook reconciliation

## Standard

A processor webhook is the network's way of telling you something already happened. It is evidence, not instruction: the payment state machine does not take commands from webhooks; it reacts to them. The distinction shows under failure: a webhook that arrives late, duplicated, or out of order cannot corrupt state if the state machine's transitions are driven by observed facts (an authorization exists; a capture was recorded) rather than by the webhook's payload text.

Treating webhooks as commands produces the classic corruption: a duplicate webhook applied twice as two captures, an out-of-order webhook rolling state backwards, a missed webhook leaving the record silent while the customer's money moved. The defence is to make state inferable without webhooks at all: signed webhooks are an optimization for latency of truth, and reconciliation — polling the processor's API and comparing against the ledger — is the standing, scheduled verification that the internal state matches the money.

Primary sources: <https://docs.stripe.com/payments/3d-secure> and <https://docs.stripe.com/billing/subscriptions/overview>.

## Decision rules

- Every webhook is verified against a signature before any state is touched.
- Transition guards check the current state; a webhook for a transition already applied is acknowledged without double-applying it.
- Idempotent handling by event identity: redelivery of the same event can only produce a replay of the recorded transition.
- Out-of-order arrival cannot revert state; late-arriving facts are applied to the truth, not to the timestamp ordering.
- Scheduled reconciliation walks processed payments against the processor API; a mismatch is an incident in the ledger, not a silent fix.
- Webhook handling is idempotent at the layer of the operation it confirms, never at the layer of the queue-acknowledgement alone.

## Procedure

1. Verify the signature, then parse; from there treat only the facts the payload legitimately carries.
2. Identify the event identity; store it; skip redeliveries of recorded identities.
3. Map the payload's fact to the state machine's transition; only the machine transitions.
4. Acknowledge the webhook after the fact is durably recorded, not before.
5. Run schedule-based reconciliation: list processor transactions for the window, compare to ledger, log all differences.
6. Test with duplicated and out-of-order deliveries.

## Anti-patterns

- "The webhook said captured" — mark paid, no signature verification, no state check.
- Applying state transitions directly from webhook payload lines.
- Stopping the reconciliation job because webhooks "usually arrive".
- Acknowledging on receipt, before state is updated, so a crash creates a black hole.
- Idempotent only at the queue level, so replay with a new queue-id becomes a second charge.

## Done checklist

- [ ] Signature verification before state change.
- [ ] Event identity stored; redeliveries replay, never re-apply.
- [ ] Transitions driven by observed facts, not payload text.
- [ ] Reconciliation scheduled and diffing against the ledger.
- [ ] Ack-delivery ordering tested with crash scenarios.
- [ ] Duplicated and out-of-order delivery tests included.

## Sources

- 3-D Secure flows: <https://docs.stripe.com/payments/3d-secure>
- Billing lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
- PCI guidance library: <https://www.pcisecuritystandards.org/document_library/>
