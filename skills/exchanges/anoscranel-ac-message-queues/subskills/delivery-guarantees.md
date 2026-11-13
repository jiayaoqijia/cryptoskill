---
name: delivery-guarantees
domain: software-engineering/delivery-guarantees
trigger: "Deciding what a queue promises about delivery."
anti_trigger: "Not for consumer idempotency design, and not for broker selection."
scope: "The ladder from at-most-once to effectively-once, and its cost at each rung."
status: seedling
---

# Delivery guarantees

## Standard

There are three rungs and no fourth. At-most-once sends a message and forgets it: fast, and a crash can lose it silently. At-least-once acknowledges after processing: a crash mid-work redelivers, so the consumer sees duplicates, and correctness moves into the consumer. Effectively-once is at-least-once plus a deduplication key the consumer checks, which is really an agreement about bookkeeping rather than a property of the pipe.

The cost climbs with the rung. At-most-once needs no coordination; at-least-once holds the message until an acknowledgement survives a consumer restart; effectively-once adds a store of seen keys with its own retention and expiry question. The honest design statement picks the rung for each queue and names who absorbs each failure — because the queue silently picks at-most-once unless someone decides otherwise.

Primary sources: <https://kafka.apache.org/documentation/> and <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html>.

## Decision rules

- Record the chosen rung per queue, and the decision's owner and date.
- Record what a broker restart does to in-flight and queued messages at that rung.
- Record what must persist across restarts for the rung to hold: the log, the ack state, or the dedup store.
- Record the duplicate rate the consumer must tolerate at at-least-once.
- Record the dedup key's scope and retention if effectively-once is claimed.
- Record the test that demonstrates the rung under a killed consumer and a killed broker.

## Procedure

1. State the rung for each queue and why that rung and not one higher.
2. Trace a message through a consumer crash at the worst moment.
3. Trace the same through a broker restart.
4. Compute or bound the duplicate exposure.
5. Define the dedup key and its expiry if used.
6. Write the guarantee with the test that evidences it.

## Anti-patterns

- Believing a queue offers exactly-once without a consumer-side mechanism.
- Choosing at-least-once and leaving the consumer without a dedup key.
- Assuming the broker's default is the safe rung; defaults are usually the cheap one.
- Claiming effectively-once with a dedup key that expires before redelivery.
- Testing delivery guarantees only when nothing crashes.

## Done checklist

- [ ] Rung recorded per queue.
- [ ] Consumer-crash trace written.
- [ ] Broker-restart trace written.
- [ ] Duplicate exposure bounded.
- [ ] Dedup key and expiry defined.
- [ ] Crash test evidencing the rung.

## Sources

- Kafka delivery semantics: <https://kafka.apache.org/documentation/>
- Managed-queue at-least-once documentation: <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html>
- Messaging patterns reference: <https://www.enterpriseintegrationpatterns.com/>
