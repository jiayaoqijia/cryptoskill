---
name: queue-backpressure
domain: software-engineering/queue-backpressure
trigger: "Deciding what a queue does when it grows faster than it drains."
anti_trigger: "Not for consumer lag in event systems, and not for load shedding at the service tier."
scope: "Bounded buffers, what to reject, and where the excess is allowed to go."
status: seedling
---

# Queue backpressure

## Standard

A queue absorbs bursts, which means it can also hide a sustained imbalance: producers faster than consumers, emptied only by a crash or a purge. The two designs are bounded and unbounded. A bounded queue pushes back — rejecting or blocking producers when full, making the overload someone else's problem immediately — while an unbounded queue absorbs everything until memory, disk, or a deadline gives out, and the failure arrives without warning.

Bounded queues force the rejection decision into the open, and it has three honest answers: reject the producer with an error it must handle; shed the least valuable class of message by policy; or degrade into a slower mode that drains while admitting less. Which one a system uses is a product decision wearing an infrastructure costume, and it belongs in the record rather than in an exception handler.

Primary sources: <https://www.rabbitmq.com/tutorials/tutorial-one-python> and <https://kafka.apache.org/documentation/>.

## Decision rules

- Record the queue's bound and the units it bounds: messages, bytes, or time-to-drain.
- Record the full-queue behaviour: reject, block, shed by class, or something else.
- Record who is allowed to observe near-full and be warned before the limit.
- Record what the drain time at peak is and the number the bound implies.
- Record what is lost when the bound is hit with shedding.
- Record the purge policy and who is authorised to invoke it.

## Procedure

1. State the bound and its unit.
2. Measure the sustained drain rate against the observed arrival rate.
3. Compute drain time bound-full and compare it to the tolerance.
4. Classify message classes by what may be shed first.
5. Configure the full-queue behaviour accordingly.
6. Write the record with the rejection policy named as a product decision.

## Anti-patterns

- An unbounded queue that silently converts overload into latency.
- Rejecting without a producer that knows what to do with the rejection.
- A bound never tested against the real arrival rate.
- Shedding by accident under load rather than by declared class.
- Emergency purges with no record of what was removed.

## Done checklist

- [ ] Bound and unit stated.
- [ ] Drain rate versus arrival rate measured.
- [ ] Full behaviour configured.
- [ ] Shed classes declared.
- [ ] Rejection path owned by the producer.
- [ ] Purge authority recorded.

## Sources

- Queue limits and flow control: <https://www.rabbitmq.com/tutorials/tutorial-one-python>
- Kafka retention and consumer lag: <https://kafka.apache.org/documentation/>
- Load shedding discussion: <https://sre.google/sre-book/handling-overload/>
