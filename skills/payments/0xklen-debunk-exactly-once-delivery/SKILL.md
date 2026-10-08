---
name: debunk-exactly-once-delivery
description: Use when a design assumes exactly-once delivery end to end. Separates at-least-once transport from exactly-once effects and makes the sink idempotent instead of trusting a broker flag.
---

# Exactly-Once Is an Effect, Not a Delivery

Transport guarantees are at-most-once or at-least-once. Exactly-once is a property you build at the sink by making effects idempotent or transactional, not something a broker config hands you for free.

## Procedure

1. Ask where the guarantee must hold: the effect on the target table, or the number of messages on the wire. These are different problems.
2. Assume at-least-once by default: every consumer sees duplicates after a rebalance, a restart, or a network retry. Design the sink to tolerate that.
3. Make the sink idempotent: upsert on a natural key, or record processed ids and skip ones already applied.
4. Where the sink is transactional, use two-phase commit to write output and commit offsets atomically.
   - Kafka: `processing.guarantee=exactly_once_v2` with a transactional producer.
   - Flink: checkpointing plus a transactional sink such as the Kafka sink with `EXACTLY_ONCE`.
5. Where it is not transactional, use the dedupe-key column plus `MERGE` / `ON CONFLICT`.
6. Do not confuse framework state with the external side effect. A Flink exactly-once pipeline writing to a plain JDBC sink still double-writes on recovery unless the write is idempotent.
7. Test by killing the consumer mid-batch and restarting; the target must not gain duplicates.
8. Keep a dedupe table keyed on the message id with a retention at least as long as the maximum redelivery window.
9. Make downstream aggregation replace-based (recompute the window) rather than additive, so a duplicate that slips through is a no-op.
10. Document the actual guarantee per hop, not one label for the whole path.

## Pitfalls

- Exactly-once advertised by a connector often means at-least-once with a dedupe key; read which one.
- Emitting side effects (email, HTTP POST, charge) inside a retried operator sends them twice; make the effect idempotent or move it out.
- A dedupe window of 24h admits duplicates older than the window.
- Offsets committed before the write cause data loss on crash; after, cause duplicates. Pick sink-side dedupe, not offset timing.
- Testing only the happy path never exercises the rebalance path where duplicates appear.
- Assuming a message id is globally unique when it is unique only per partition.
- A dedupe table pruned too aggressively reintroduces duplicates exactly during a long outage.
- Trusting the flag without a crash test means the guarantee is asserted, not verified.

## Verification

```sh
psql -c "SELECT natural_key, count(*) c FROM target GROUP BY 1 HAVING c>1"
psql -c "SELECT (SELECT count(*) FROM source) - (SELECT count(DISTINCT natural_key) FROM target)"
```

Both return zero. Report the delivery semantics actually achieved (at-least-once plus an idempotent sink), the dedupe key, and the crash-test result.