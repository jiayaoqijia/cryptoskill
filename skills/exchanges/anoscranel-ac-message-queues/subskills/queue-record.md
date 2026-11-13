---
name: queue-record
domain: software-engineering/queue-record
trigger: "Writing the record for a queue's configuration and guarantees."
anti_trigger: "Not for recommending a broker, and not for the broker's documentation."
scope: "The written record of guarantees, limits, and inspection points."
status: seedling
---

# Queue record

## Standard

The queue record states, per queue, the routing contract, the delivery rung, the ack configuration, the poison path, the dispatch policy, and the bound. These six lines are what an operator needs when a queue misbehaves at 3 a.m., and their absence is why queues are re-debugged from scratch each time: the configuration lives in the broker dashboard and in one engineer's memory.

The record's second job is naming the person who absorbs each residual risk. At-least-once means the consumer absorbs duplicates; shedding means a class of senders absorbs loss; strict priority means the bottom class absorbs starvation. A queue record that does not say who pays for each guarantee is an incomplete contract, and the payment is collected at the worst possible moment.

Primary sources: <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html> and <https://osf.io/prereg/>.

## Decision rules

- The record names each queue, its exchange or topic, and its routing contract.
- The delivery rung is stated per queue with the crash test that evidenced it.
- The ack timing, scope, and timeout are recorded.
- The poison path names its limits, destination, reader, and alarm.
- The dispatch policy and prefetch window are recorded with their variance basis.
- The bound and the full-queue behaviour are recorded with the absorbed-risk owner named.

## Procedure

1. List each queue with its routing contract.
2. State the rung and attach the crash-test evidence.
3. Record ack and timeout configuration.
4. Record the poison path with its reader.
5. Record dispatch and prefetch with measurements.
6. Record the bound and the rejection owner.

## Anti-patterns

- Recording the broker's name instead of the queue's guarantees.
- No crash test attached to the claimed rung.
- A dead-letter queue in the record with no reader named.
- Stating guarantees without naming who absorbs the residual risk.
- Sizing prefetch from instinct recorded as if measured.

## Done checklist

- [ ] Queues and routing contracts listed.
- [ ] Rungs stated with evidence.
- [ ] Ack and timeout recorded.
- [ ] Poison path with reader recorded.
- [ ] Dispatch and prefetch with measurements recorded.
- [ ] Bounds and risk owners named.

The record should also state the queue's observable lag in steady state, because that is the number an alarm threshold is set against: a record with no baseline forces the first alarm threshold to be guessed during the first incident, which is the wrong time to learn what normal looks like.

## Sources

- Managed queue configuration reference: <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html>
- Stated conditions practice: <https://osf.io/prereg/>
- Messaging patterns: <https://www.enterpriseintegrationpatterns.com/>
