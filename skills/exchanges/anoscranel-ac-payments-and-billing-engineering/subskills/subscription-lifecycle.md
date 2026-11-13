---
name: subscription-lifecycle
domain: software-engineering/subscription-lifecycle
trigger: "Running subscriptions across trials, renewals, failures, and cancellation."
anti_trigger: "Not for one-time payment state, and not for proration arithmetic."
scope: "Trials, dunning cycles, and the states between paid and cancelled."
status: seedling
---

# Subscription lifecycle

## Standard

A subscription is a state machine with a calendar attached. Unlike a one-time payment, the transition sources are time-based events — period end, trial expiry, billing anchor dates — and each renewal is a new money operation that must satisfy the same state discipline as any other: idempotent, observable, and driven by recorded facts. Cancellation is not a terminal state from the money side; a cancelled subscription may still owe a final invoice, may still renew if the cancel arrives after the period was billed, and the customer's expectation of access must be modeled separately from the billing state.

Dunning is the discipline that makes failed renewals survivable. A renewal decline is not a cancellation; it enters the dunning cycle — a pre-written schedule of retries and customer notifications, ending in either recovery or an explicit terminal state. The code never improvises how many times to retry a failed renewal or when to notify the customer; the schedule was decided when the subscription was designed, and every step is applied against the payment state, not against the clock of anxiety.

Primary sources: <https://docs.stripe.com/billing/subscriptions/overview> and <https://docs.stripe.com/payments/3d-secure>.

## Decision rules

- Model billing state and access state separately; the customer's access at any moment derives from a named rule, not from a boolean.
- Trial conversion and first renewal are explicit transitions with idempotent money events of their own.
- Dunning schedule decided at design time: number of retries, notification cadence, terminal outcome; written into the subscription product definition.
- retries during dunning reuse the renewal operation's idempotency key.
- Cancellation states: immediate, at-period-end, and scheduled define different money events; which one occurred is a fact, not an inference.
- The billing calendar — period boundaries, timezone, anchor dates — is recorded data, never computed from wall-clock guesses.

## Procedure

1. Write the full state set, including the states that exist after cancellation is requested.
2. Define the time-based trigger set and where each trigger's money event comes from.
3. Write the dunning schedule with retry count, spacing, and notification pairing.
4. Trace trial → conversion → renewal → decline → dunning states end-to-end with test fixtures, verifying each money event once.
5. Separate access rules from billing rules; test the customer's access in every billing state.
6. Review the state set against the processor's lifecycle documentation for unmodelled cases.

## Anti-patterns

- Cancellation that ends billing but quietly leaves access alive forever.
- Renewal retries that mint a new charge operation each time.
- A dunning cadence decided by an on-call engineer at 2am.
- Treating the period end as \"whatever the date math says\"; the anchor date is record data.
- Access revoked because a renewal is in dunning, before the terminal state declares it.

## Done checklist

- [ ] State set written including post-cancellation states.
- [ ] Time-based triggers mapped to explicit money events.
- [ ] Dunning schedule pre-written with retry count and notifications.
- [ ] Trial → renewal path traced end-to-end.
- [ ] Access rules separated and tested per billing state.
- [ ] Lifecycle checked against processor documentation.

## Sources

- Billing subscription lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
- 3-D Secure and authentication: <https://docs.stripe.com/payments/3d-secure>
- Disputes: <https://stripe.com/docs/disputes>
