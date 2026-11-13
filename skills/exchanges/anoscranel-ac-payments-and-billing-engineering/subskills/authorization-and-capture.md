---
name: authorization-and-capture
domain: software-engineering/authorization-and-capture
trigger: "Separating the moment the customer's limit is checked from the moment the money moves."
anti_trigger: "Not for subscription billing states, and not for disputes."
scope: "Two liability moments, the delay between them, and void versus refund."
status: seedling
---

# Authorization and capture

## Standard

An authorization and a capture are two money events with different liability. The authorization holds funds against the customer's limit; the customer sees a pending line; liability has not yet moved. The capture completes the charge, moves the liability, and starts the clock on settlement and on refund rights. The delay between them can be minutes or days, and each phase carries its own failure mode: an authorization can expire while you wait; a capture can be declined even after an authorization succeeded.

Void and refund are the mirror operations of the pair, and conflating them is the classic mistake. A void cancels an uncaptured authorization; the customer never sees a charge, and it costs nothing beyond the hold's disappearance. A refund returns a captured charge to the customer; it carries its own processing time, fee treatment, and customer-perception consequences. Choosing between them requires knowing which side of the capture boundary the payment currently sits on — which is a fact about the payment state, not a preference.

Primary sources: <https://docs.stripe.com/billing/subscriptions/overview> and <https://www.emvco.com/emv-technologies/3-d-secure/>.

## Decision rules

- Treat the authorization as a reservation with an expiry; state the expiry and the state that results.
- Treat the capture as the liability moment; from here, reversal is a refund, not a void.
- Decide void versus refund from the payment state; write the rule into the state machine's transitions.
- Never capture without an item-shipped confirmation where physical goods are involved; do not let the hold expire while you wait.
- Delayed captures are modeled as a policy with a range; state the range and the expiry risk honestly.
- Every authorization response is persisted; a capture that will be attempted later needs its own retry tied to the state machine.

## Procedure

1. Record the authorization with its expiry window and response data.
2. On fulfillment, capture deliberately — one event when ready.
3. If the customer cancels pre-capture, void and log.
4. If post-capture, refund; record the two events as distinct and the reason for each.
5. Test both expiry and capture-decline paths.
6. Report the money position each transition left.

## Anti-patterns

- Capturing at checkout, then refunding when the order cancels.
- A void retrofitted onto a captured charge — impossible and quietly results in a double event.
- Authorization records with no expiry; the late capture becomes a decline surprise.
- Treating the authorization response as a success screen once, twice; state, not hope, is what you show.
- No persistence between auth and capture, so the capture cannot find its authorization.

## Done checklist

- [ ] Expiry window recorded at authorization.
- [ ] Capture as a deliberate, persisted event.
- [ ] Void-versus-refund rule tied to state, written down.
- [ ] Expiry and capture-decline paths tested.
- [ ] Both mirror operations logged with reasons.
- [ ] Money position reported per transition.

## Sources

- Subscription and auth lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
- 3-D Secure and liability shift: <https://www.emvco.com/emv-technologies/3-d-secure/>
- Dispute flows: <https://stripe.com/docs/disputes>
