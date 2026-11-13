---
name: levels-and-anomalies
domain: software-engineering/levels-and-anomalies
trigger: "Choosing an isolation level by the anomalies the code can tolerate."
anti_trigger: "Not for consensus across nodes, and not for schema design."
scope: "The isolation levels, the anomaly each permits, and the one it removes."
status: seedling
---

# Levels and anomalies

## Standard

An isolation level is defined by what it lets through. Read uncommitted permits dirty reads — seeing another transaction's uncommitted work. Read committed removes dirty reads but permits non-repeatable reads, where a row read twice returns different committed values. Repeatable read freezes a row's reads but permits phantoms, where a predicate query returns a different set of rows — and snapshot-family levels permit write skew, where two transactions each read a consistent snapshot, each check a condition that is true in their own snapshot, and each write in a way that makes the combined result violate the condition neither saw broken. Serializable allows none of these, at the price of aborting work that would violate the ordering.

The engineering meaning is that each level encodes an assumption the application must either meet or enforce itself. Code that reads a balance, decides, then writes assumes nothing else changed between read and write — at read committed that assumption is false and the level will not defend it. Choosing a level is therefore writing down the concurrency contract the queries rely on, not picking a number from a tuning guide.

Primary sources: <https://www.postgresql.org/docs/current/transaction-iso.html> and <https://jepsen.io/consistency>.

## Decision rules

- Record the isolation level per transaction type, not per database default.
- List the anomalies each critical path can tolerate and those it cannot.
- Treat read-modify-write sequences as claiming repeatable-read-or-stronger assumptions.
- Include the write skew test: two snapshot transactions making decisions the combination invalidates.
- Verify the engine's actual behaviour for the named level, not the standard's text.
- Record the abort-and-retry behaviour for the level that can fail on conflict.
- State who owns enforcement when a lower level is chosen for throughput.

## Procedure

1. Classify each transaction by the anomalies it must not observe.
2. Map the requirement onto the weakest level that satisfies it.
3. Verify the engine's documented behaviour for that level.
4. Implement the retry path for levels that abort on conflict.
5. Write a concurrency test that demonstrates the removed anomaly.
6. Record level, rationale, and test per transaction type.

## Anti-patterns

- Running everything at the database default without a per-path decision.
- Assuming a level name means the same across engines.
- Choosing serializable without a retry path for its aborts.
- Choosing read uncommitted for writes because reads elsewhere tolerate it.
- No test demonstrating the tolerable anomaly is actually tolerated.

## Done checklist

- [ ] Levels decided per transaction type.
- [ ] Anomaly tolerance classified.
- [ ] Engine behaviour verified.
- [ ] Abort and retry path implemented.
- [ ] Concurrency test in place.
- [ ] Decisions recorded.

## Sources

- Isolation levels and their anomalies, from the engine: <https://www.postgresql.org/docs/current/transaction-iso.html>
- Anomaly taxonomy across consistency models: <https://jepsen.io/consistency>
- Explicit locking as the enforcement companion: <https://www.postgresql.org/docs/current/explicit-locking.html>
