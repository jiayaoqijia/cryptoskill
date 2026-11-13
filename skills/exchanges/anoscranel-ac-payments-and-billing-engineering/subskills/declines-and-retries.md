---
name: declines-and-retries
domain: software-engineering/declines-and-retries
trigger: "Responding to a decline without manufacturing a duplicate charge."
anti_trigger: "Not for idempotency key design alone, and not for disputes."
scope: "The decline taxonomy, honest retries, and how to never create a duplicate charge."
status: seedling
---

# Declines and retries

## Standard

A decline is the issuer exercising judgement, and the code's first duty is to report it honestly to the customer rather than to improvise. Declines come in classes with different meanings: hard declines — stolen card, insufficient funds, do-not-honor — where an immediate retry with the same data is noise; and soft declines — timeouts, transient issuer unavailability — where a disciplined retry with the same idempotency key may still complete the customer's single intended operation. The taxonomy is not decoration; the retry policy hangs on it.

The danger of retries is not the retry itself but the new-charge risk every retry carries when the idempotency key is mishandled. A retry must reuse the customer's operation key so the network, the processor, and the merchant code converge on one money event. When the retry policy and the key policy are owned by different hands — the client's retry loop minting fresh keys while the server waits — the duplicate arrives wearing the costume of a success, and is discovered later by the customer, not by the code.

Primary sources: <https://docs.stripe.com/billing/subscriptions/overview> and <https://stripe.com/docs/disputes>.

## Decision rules

- Classify declines into hard and soft at the point of receipt; record the class with the state.
- Retries only for soft declines, with the same idempotency key, on a schedule with a stated cap.
- Hard declines surface to the customer as an action needed; the code never silently retries them into approvals.
- Exponential backoff with jitter for any client-visible retry; never a tight loop, never a Predictable-second pattern.
- Every retry attempt, successful or not, is logged with its key and its decline class.
- The customer-visible failure is honest and immediate; the state machine, not hope, tells the screen what to say.

## Procedure

1. On decline, record the processor's decline code and map it to your class table.
2. Persist the class with the payment state — never re-derive it from a screen.
3. Soft-decline path: retry with same key, schedule with backoff and cap.
4. Hard-decline path: surface the customer action; the machine holds requires_action, not failed-by-default.
5. Test the retry path with a duplicate-charge oracle: walk the sequence and assert one money event.
6. Review the class table against processor documentation at every integration review.

## Anti-patterns

- Blanket retries on any decline; the issuer reads it as card testing.
- A client-side retry loop that mints fresh idempotency keys per attempt.
- Classifying by string matching on decline messages; codes are data, prose is not.
- Retrying while the customer watches a spinner; the state decides the message.
- Treating a do-not-honor as a temporary condition; the card, not the network, decided.

## Done checklist

- [ ] Decline class table written and persisted with state.
- [ ] Retry policy: soft-only, same-key, backoff, cap.
- [ ] Hard declines surface customer action, not silent retries.
- [ ] Duplicate-charge oracle runs in tests.
- [ ] Every attempt logged with key and class.
- [ ] Class table reviewed against processor docs.

## Sources

- Subscription billing lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
- Disputes and their triggers: <https://stripe.com/docs/disputes>
- PCI guidance library: <https://www.pcisecuritystandards.org/document_library/>
