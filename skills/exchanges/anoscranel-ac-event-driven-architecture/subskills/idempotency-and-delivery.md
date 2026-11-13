---
name: idempotency-and-delivery
domain: software-engineering/idempotency-and-delivery
trigger: "Making a consumer safe under at-least-once delivery."
anti_trigger: "Not for broker configuration, and not for exactly-once marketing claims."
scope: "At-least-once delivery, the exactly-once illusion, and idempotent consumers."
status: seedling
---

# Idempotency and delivery

## Standard

Most brokers deliver at least once, which means a message can arrive more than once and the consumer must produce the same result either way. Exactly-once delivery is not a property of a network: what exists is exactly-once processing, achieved by making the consumer's effect idempotent and recording what it has already processed, or by making the write conditional on a deduplication key.

The engineering is therefore in the consumer, not the broker. A consumer that increments a counter without recording the message identifier will double-count on a redelivery; one that writes with a unique constraint on the message identifier, or compares a version, will not. The record states which mechanism is used and what it costs.

Primary sources: <https://www.cncf.io/> and <https://www.enterpriseintegrationpatterns.com/>.

## Decision rules

- Record the delivery guarantee of the broker and its configuration.
- Record the deduplication mechanism: unique constraint, version comparison, or a processed-message table.
- Record the window in which duplicates are detected, since a table that is truncated loses the guarantee.
- Record the side effects that are not idempotent, such as sending an email or calling a payment provider.
- Record how those side effects are made safe, usually by an idempotency key passed downstream.
- Record the consumer's offset commit timing relative to its effect.

## Procedure

1. Record the delivery guarantee.
2. Choose a deduplication mechanism and record its window.
3. Identify non-idempotent side effects and give each an idempotency key.
4. Align offset commit with the effect, recording the ordering.
5. Test by delivering the same message twice.
6. Record the duplicate rate observed in production.

## Anti-patterns

- Assuming exactly-once delivery from a broker setting.
- Deduplicating in memory, which fails on restart.
- An external call without an idempotency key.
- Committing the offset before the effect, which loses messages on failure.
- A deduplication table with no retention policy, so it grows or silently truncates.

## Done checklist

- [ ] Delivery guarantee recorded.
- [ ] Deduplication mechanism and window recorded.
- [ ] Non-idempotent side effects listed with keys.
- [ ] Offset commit ordering recorded.
- [ ] Duplicate delivery tested.
- [ ] Duplicate rate measured.

The duplicate rate is worth measuring for a second reason beyond correctness: a rate that is far above what the broker's guarantees would suggest points to a consumer restarting frequently or a rebalance storm, which is an operational signal that the message semantics alone would not reveal.


## Sources

- Messaging semantics guidance: <https://www.cncf.io/>
- Integration pattern reference: <https://www.enterpriseintegrationpatterns.com/>
- Distributed systems reference: <https://martinfowler.com/>
