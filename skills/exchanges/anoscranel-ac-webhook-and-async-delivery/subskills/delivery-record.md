---
name: delivery-record
domain: software-engineering/delivery-record
trigger: "Writing the record of a webhook delivery contract."
anti_trigger: "Not for API documentation, and not for event schema design."
scope: "The written record: schedule, signature scheme, ordering, and disable policy."
status: seedling
---

# Delivery record

## Standard

The delivery record states the retry schedule and horizon, the signature scheme and its timestamp window, the ordering property, the disabling policy, and the fetch path for missed events. Those five items are what a receiver needs in order to build an endpoint that behaves correctly, and each of them is a promise the sender may fail to keep silently.

Its second function is to make the contract's limits explicit. A record that states a three-day horizon and a fetch endpoint has told the receiver what to build against; one that describes the payload and omits the horizon has left the receiver to discover the loss during an outage. The limits are the more useful half.

Primary sources: <https://www.rfc-editor.org/rfc/rfc9110> and <https://osf.io/prereg/>.

## Decision rules

- The record states the envelope and the event identifier used for deduplication.
- The retry schedule, horizon, and success codes are recorded.
- The signature scheme records the signed material, algorithm, and timestamp window.
- The ordering property is recorded with its stream definition.
- The disabling threshold and re-enablement path are recorded.
- The fetch endpoint for missed events is recorded with its retention.

## Procedure

1. Record the envelope and identifier.
2. Record the retry schedule, horizon, and success codes.
3. Record the signature scheme and window.
4. Record ordering and its stream.
5. Record the disabling policy and recovery.
6. Record the fetch endpoint and retention.

## Anti-patterns

- Documenting the payload and omitting the horizon.
- A signature described without the signed material.
- Ordering claimed without its stream definition.
- A fetch endpoint with no retention stated, so a receiver cannot know how far back to look.
- A disabling policy that exists in code but not in the contract.

## Done checklist

- [ ] Envelope and identifier recorded.
- [ ] Schedule, horizon, success codes recorded.
- [ ] Signature scheme and window recorded.
- [ ] Ordering and stream recorded.
- [ ] Disabling and recovery recorded.
- [ ] Fetch endpoint and retention recorded.

The record should also state what the sender does with an event that fails permanently, since a malformed payload or a deleted resource produces an error that no retry will fix, and the record should say whether that event is dropped, retained, or surfaced to the receiver.


The record should also state the sender's own capacity per receiver, since a delivery system that retries one endpoint aggressively can slow delivery to every other: a per-endpoint concurrency limit is part of the contract's fairness, not an implementation detail hidden in the sender.

## Sources

- HTTP delivery semantics: <https://www.rfc-editor.org/rfc/rfc9110>
- Pre-registration practice for stated terms: <https://osf.io/prereg/>
- Security controls for signing: <https://csrc.nist.gov/>
