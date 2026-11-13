---
name: priority-and-dispatch
domain: software-engineering/priority-and-dispatch
trigger: "Reading how a broker decides which consumer gets the next message."
anti_trigger: "Not for routing, and not for load balancing at the network tier."
scope: "Priority queues, prefetch, and the fairness they quietly decide."
status: seedling
---

# Priority and dispatch

## Standard

With one consumer, dispatch is trivial. With several, the broker decides who receives next, and two settings quietly make that decision. Prefetch caps how many unacknowledged messages a consumer may hold: an unbounded prefetch lets one fast-grabbing consumer starve the others; a prefetch of one round-trips every message and wastes the pipe. Priority declares which queued message is next: strict priority can starve low-priority work indefinitely, and its absence is itself a policy — first-in-first-out — that deserves to be chosen rather than defaulted into.

The subtle failure is head-of-line blocking through prefetch. A consumer holding ten messages, nine of which are quick and one slow, has taken the ten minutes of work behind the slow message away from idle peers. The fix is the window's size, and the honest number is derived from processing-time variance, not instinct: high variance wants a small window even at throughput cost.

Primary sources: <https://www.rabbitmq.com/tutorials/tutorial-one-python> and <https://kafka.apache.org/documentation/>.

## Decision rules

- Record the dispatch policy: FIFO, strict priority, or weighted fairness.
- Record the prefetch or in-flight window per consumer and its derivation.
- Record what strict priority does to the lowest class under sustained load.
- Record processing-time variance, the number that sizes the window.
- Record whether one consumer can hold a batch others could be processing.
- Record the observed starvation event and the adjustment it prompted.

## Procedure

1. State the dispatch policy and who chose it.
2. Record the prefetch window and measure the throughput it costs.
3. Measure processing-time variance per message class.
4. Simulate one slow message in a full window with idle peers.
5. Test the lowest priority class under sustained high-priority load.
6. Write the dispatch policy with the starvation behaviour stated.

## Anti-patterns

- Unbounded prefetch with competing consumers.
- A window sized by throughput alone while variance starves peers.
- Strict priority with no guarantee for the bottom class.
- Treating FIFO as not-a-policy; it is one, chosen by default.
- Priority levels that encode importance the system cannot act on.

## Done checklist

- [ ] Dispatch policy stated.
- [ ] Prefetch window and derivation recorded.
- [ ] Variance measured.
- [ ] Head-of-line case tested.
- [ ] Lowest class tested under load.
- [ ] Policy written with starvation stated.

## Sources

- Prefetch and dispatch tutorial: <https://www.rabbitmq.com/tutorials/tutorial-one-python>
- Kafka consumer grouping: <https://kafka.apache.org/documentation/>
- Queue-based load levelling pattern: <https://www.enterpriseintegrationpatterns.com/>
