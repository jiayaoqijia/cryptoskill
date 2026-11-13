---
name: state-and-size
domain: software-engineering/state-and-size
trigger: "Bounding what a stream computation must remember."
anti_trigger: "Not for recommending a state backend, and not for workflow state."
scope: "What a stream computation must remember, and its growth."
status: seedling
---

# State and size

## Standard

Every non-trivial stream computation remembers something: per-key counters, open windows, partial aggregates, the last value seen. That state is where correctness lives, and its size is where the system dies. A per-user average is bounded by the user count; a per-user-per-hour counter is bounded by users times hours; a distinct-count over an unbounded stream is bounded by nothing at all until the design gives it a bound.

The arithmetic must be done in advance, per operator: keys, key cardinality, state per key, and retention per key. The two usual killers are unbounded key cardinality — a per-device key over a growing device fleet — and unbounded retention — state kept for a key that will never return. Bloom filters, time-bounded retention, and keyed state eviction each trade exactness for space, and the trade must be named because "approximately distinct users" and "distinct users" are different products.

Primary sources: <https://nightlies.apache.org/flink/flink-docs-stable/> and <https://martinfowler.com/>.

## Decision rules

- List every stateful operator with its key, per-key state, and retention.
- Compute the worst-case total state from key cardinality, not the observed startup count.
- Record the exactness each output requires, and where approximation is acceptable.
- Record the eviction rule for state that will not be revisited.
- Record the checkpoint behaviour and the cost of restoring state after a restart.
- Measure actual state size at peak, and its growth across a week.

## Procedure

1. Enumerate stateful operators and their keys.
2. Compute per-key size and total worst case.
3. State the exactness requirement per output.
4. Choose retention and eviction rules.
5. Record checkpoint and restore behaviour.
6. Measure peak state and its growth trend.

## Anti-patterns

- A per-key map with no eviction, growing with the fleet forever.
- Distinct counts presented as exact when the state was approximated silently.
- State sized from day-one traffic and never revisited.
- Checkpointing so heavyweight that operators disable it, losing exactly-once claims.
- Retention extended "temporarily" during an incident and never restored.

## Done checklist

- [ ] Operators, keys, and retention enumerated.
- [ ] Worst-case total computed.
- [ ] Exactness requirement stated.
- [ ] Eviction rule recorded.
- [ ] Checkpoint and restore recorded.
- [ ] Peak state measured with trend.

A useful habit keeps state honest between deployments: recompute the worst case after every cardinality change — a new customer segment, a new device type — because the operator that was comfortable at a million keys is the same code dying at ten million, and nothing in the pipeline errors on the way down; it simply slows, checkpoints longer, and fails at restore.

## Sources

- Stateful stream processing: <https://nightlies.apache.org/flink/flink-docs-stable/>
- Stream systems design: <https://martinfowler.com/>
- Stream processing references: <https://dataintensive.net/>
