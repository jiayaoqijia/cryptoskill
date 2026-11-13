---
name: idempotent-charging
domain: software-engineering/idempotent-charging
trigger: "Charging a customer exactly once regardless of how the network behaves."
anti_trigger: "Not for general idempotency in APIs, and not for retry policy in general."
scope: "Idempotency keys scoped to the operation the customer believes is one."
status: seedling
---

# Idempotent charging

## Standard

A customer never attempts a retry; the network does. Clicking twice, a phone that loses signal mid-request, a support staff member repeating the action — from the customer's side, all of these are the same charge. The idempotency key is the name the merchant code gives to the customer's intent so that any number of technical attempts against that key can only produce one money event.

The critical decision is key scope. Making a key per click, per request, or per attempt produces exactly the duplicate-charge failure the key exists to prevent. The correct scope is the customer's operation: this subscription, this cart, this invoice. A retry with a new key must be prevented; a genuine new purchase with the old key must be prevented too — the key stores the result of the first execution and returns that result for the lifetime of the operation.

Primary sources: <https://stripe.com/docs/disputes> and <https://docs.stripe.com/billing/subscriptions/overview>.

## Decision rules

- Key scope is the customer's operation, not the technical request: one cart, one renewal, one invoice adjustment.
- Store the result with the key; a replay returns the stored result and performs nothing new.
- The key has to change when the customer genuinely wants a second, new operation; state which operations are new by writing it down.
- Lifetime long enough for a disputable later arrival: a replay months later returns the same money position, not a new charge.
- Retries of a network failure reuse the same key; only auth-level failures that need re-authorization, as decided by the state machine, may mint a new one.
- Every replay is logged with its result; a replay burst is a signal about the calling system.

## Procedure

1. Identify the customer-visible operations that move money.
2. Assign each a stable key derived from the operation identity, not the request timing.
3. Store the operation result alongside the key before any user-visible confirmation.
4. Map the network's own retry semantics onto the key; processor-side retries replay the key, they do not mint.
5. Walk the incident list: dropped connection, click-twice, support-desk replay; test each produces one money event.
6. Log every replay with the reason it arrived.

## Anti-patterns

- A key per request; duplicates still possible and now invisible.
- Deleting keys after order completion; the late replay becomes a new charge.
- Keying on a hash of a request body; the genuine correction is now a collision.
- A retry policy that mints a new key after a timeout \"just in case\".
- Confirming on the client before committing the result.

## Done checklist

- [ ] Key scope is the customer's operation.
- [ ] Result stored before user-visible confirmation.
- [ ] Replay returns stored result; no new money event.
- [ ] New-operation rule written down.
- [ ] Network retry semantics mapped to the key.
- [ ] Replays logged with reasons.

## Sources

- Disputes and duplicate charges: <https://stripe.com/docs/disputes>
- Subscription lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
- PCI standards library: <https://www.pcisecuritystandards.org/document_library/>
