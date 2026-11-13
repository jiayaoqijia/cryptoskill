---
name: delivery-contract
domain: software-engineering/delivery-contract
trigger: "Defining what a webhook sends and how often it retries."
anti_trigger: "Not for event payload schema design, and not for queue configuration."
scope: "What is sent, the retry schedule, and the timeouts the sender applies."
status: seedling
---

# Delivery contract

## Standard

The delivery contract states what the sender will do, so that a receiver can build against it rather than guess. It covers the payload envelope, the request timeout, the retry schedule with its backoff and jitter, the total attempt horizon, the response codes that count as success, and what happens when the horizon is exhausted.

The horizon is the part receivers most often misunderstand. A retry schedule that runs for three days is generous only if the receiver's own recovery can happen within three days; an endpoint down for a week receives nothing after the third day and has no way to know what it missed. Stating the horizon and offering a fetch endpoint for missed events is what makes the guarantee honest.

Primary sources: <https://www.rfc-editor.org/rfc/rfc9110> and <https://csrc.nist.gov/>.

## Decision rules

- Record the envelope: event type, identifier, timestamp, and payload reference.
- Record the request timeout the sender applies per attempt.
- Record the retry schedule: attempt count, backoff curve, and jitter.
- Record the total horizon and the response codes treated as success.
- Record what happens at exhaustion, including whether a dead-letter is available to the receiver.
- Record the fetch endpoint that lets a receiver recover missed events.

## Procedure

1. Record the envelope fields and the event identifier.
2. Record the per-attempt timeout.
3. Record the retry schedule and horizon.
4. Record success codes and the treatment of redirects.
5. Record exhaustion behaviour and the fetch path.
6. Write the contract as the receiver would read it.

## Anti-patterns

- A retry horizon shorter than the receiver's plausible outage.
- Treating any 2xx as success without checking the receiver acknowledged processing.
- No fetch endpoint, so missed events are unrecoverable.
- A timeout longer than the receiver's own processing time, causing duplicate work.
- Documenting the schedule without the jitter, so receivers cannot predict arrival.

## Done checklist

- [ ] Envelope recorded.
- [ ] Timeout recorded.
- [ ] Retry schedule and horizon recorded.
- [ ] Success codes recorded.
- [ ] Exhaustion behaviour recorded.
- [ ] Fetch path recorded.

The success code deserves a note of its own, since a receiver that returns 200 before persisting has told the sender the event is handled and will never see it again: the contract should state that a success response is a durability claim, which is an obligation on the receiver rather than a formality.


## Sources

- HTTP semantics for request and response handling: <https://www.rfc-editor.org/rfc/rfc9110>
- Security control guidance for transport: <https://csrc.nist.gov/>
- Reliability practice: <https://sre.google/>
