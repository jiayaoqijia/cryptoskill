---
name: payment-state-machine
domain: software-engineering/payment-state-machine
trigger: "Designing money movement as explicit states rather than as hopes."
anti_trigger: "Not for UI checkout flow, and not for processor product selection."
scope: "The intent as a state machine; states as money-positions, not screen labels."
status: seedling
---

# Payment state machine

## Standard

A payment is not an event; it is a state machine the merchant briefly believes it controls. The money takes a journey through the acquiring and issuing banks and at each hop can rest somewhere the merchant did not expect: authorized but never captured, captured but flagged for review, reversed by the issuer, eaten by a network decline after your screen said success. The code's job is to hold the true position, not the desired one.

The intent record is the seat of truth. It looks at the network and asks what has actually happened to this money; screen states derive from it and never the other way around; every state that follows creates a recorded fact with its evidence. When the truth comes from webhooks, reconciliation, or polling, what the code does with the truth is a transition; nobody improvises.

Primary sources: <https://docs.stripe.com/billing/subscriptions/overview> and <https://stripe.com/docs/disputes>.

## Decision rules

- Name the states after money positions: requires_action, authorized, captured, refunded, voided, disputed, failed; not after page names.
- Write the transition table before the first webhook, not after; a transition is rejected, not invented, in the moment.
- State the fact as external truth observed, not an action to take; the network is not your API caller.
- Every state change is immutable history; there is no in-place update to a payment row.
- Overwrite the previous state; the record's history is the audit.
- State persists before the customer sees anything the state implies; read state after any process restart.

## Procedure

1. List every state the money can occupy, from creation to terminal.
2. Draw the legal transitions and name the evidence that permits each.
3. Represent the machine in the persistence layer, not in the screen flow.
4. Build the side-effects (email, accounting, entitlement) on transitions, not scattered.
5. Test by driving the machine with the network's responses as fixtures.
6. Review the table against the processor's documentation of the lifecycle.

## Anti-patterns

- Screens as states, so a refresh decides whether the customer paid.
- A boolean \"paid\" that means three different money positions.
- Improvised state edits during an incident.
- Side effects issuing from a screen's response rather than a transition.
- No record of which state a payment was in when a dispute arrived.

## Done checklist

- [ ] State enum = money positions only.
- [ ] Transition table written and reviewed.
- [ ] Writes to state are immutable with history.
- [ ] Side effects bound to transitions.
- [ ] Network fixtures test the machine.
- [ ] Process docs reviewed for unmodelled states.

## Sources

- Billing subscription lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
- Dispute lifecycle: <https://stripe.com/docs/disputes>
- EMVCo 3-D Secure: <https://www.emvco.com/emv-technologies/3-d-secure/>
