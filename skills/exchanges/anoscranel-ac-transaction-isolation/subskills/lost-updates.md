---
name: lost-updates
domain: software-engineering/lost-updates
trigger: "Preventing concurrent updates from overwriting each other."
anti_trigger: "Not for distributed consensus, and not for cache invalidation."
scope: "The lost update anomaly and optimistic versus pessimistic prevention."
status: seedling
---

# Lost updates

## Standard

A lost update happens when two transactions read a value, compute against what they read, and both write — the second write overwrites the first silently, and the first update never happened as far as the row shows. It is the classic anomaly of read-modify-write at read committed: each writer believes it acted on current data, and the row's final value reflects only one of them.

Prevention takes one of two philosophies. Pessimistic locks first — the row is taken with an explicit lock, the second writer waits, and the arithmetic is safe at the cost of blocking. Optimistic assumes conflict is rare — write with a version check that aborts if the row changed, and retry the whole unit on failure. Banking increments avoid both with a single atomic statement, the strictest and cheapest form: never read, only add.

Primary sources: <https://www.postgresql.org/docs/current/transaction-iso.html> and <https://www.postgresql.org/docs/current/explicit-locking.html>.

## Decision rules

- Classify each write as independent-set, increment, or read-modify-write.
- Use a single atomic statement for increments; never read-then-write them.
- Use an explicit row lock for read-modify-write under contention.
- Use a version column and abort for low-contention read-modify-write.
- Implement the aborted transaction's retry with fresh reads.
- Record which philosophy each update path uses and why.

## Procedure

1. Inventory the read-modify-write sequences in the work.
2. Convert pure increments to atomic statements.
3. Choose pessimistic or optimistic per path based on contention.
4. Implement the abort path and verify the retry re-reads.
5. Test with two concurrent writers and confirm none of the work is lost.
6. Record the choice and the test for each path.

## Anti-patterns

- Read a balance, compute in the application, then write it back.
- A blind retry loop that always retries the same stale input without re-reading.
- Every path pessimistic even when conflicts are vanishingly rare.
- Optimistic checks on a column that is not actually the decision input.
- No concurrency test in the suite for updates, only sequential ones.

## Done checklist

- [ ] Writes classified by type.
- [ ] Increments converted to atomic statements.
- [ ] Philosophy chosen per path.
- [ ] Abort and retry paths implemented.
- [ ] Two-writer test proves no work is lost.
- [ ] Choices recorded.

A missing row in this inventory is worth stating plainly: a lost update that has already shipped does not announce itself. The row simply ends up with the last writer's value, and the anomaly is found only by reconciling against a source that kept the whole history — which is why the record asks for a two-writer test rather than trusting a review.

## Sources

- Anomaly definitions and their levels: <https://www.postgresql.org/docs/current/transaction-iso.html>
- Explicit row locking mechanics: <https://www.postgresql.org/docs/current/explicit-locking.html>
- Consistency anomalies under concurrency: <https://jepsen.io/consistency>

