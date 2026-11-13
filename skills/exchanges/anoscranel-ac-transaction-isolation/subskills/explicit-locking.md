---
name: explicit-locking
domain: software-engineering/explicit-locking
trigger: "Using explicit row locks and surviving the deadlocks they cause."
anti_trigger: "Not for application-level mutex design, and not for schema changes."
scope: "Row locks, lock ordering, and the deadlock the engine reports back."
status: seedling
---

# Explicit locking

## Standard

Explicit locking is the pessimistic choice: a transaction locks the rows it will touch and holds them until it commits, keeping other writers out rather than gambling on rare conflicts. It actualizes its dependencies — a session that locks row A then row B will battle any session that locks B then A — and the engine notices the cycle, aborts one side, and hands the application a failure to retry.

Ordering is the cure, and a total order is the discipline. Lock rows in a determinate order determined by a criterion such as the primary key, and a cycle becomes impossible because no transaction ever waits on someone who waits on an earlier resource. The other tool is the lock's scope: hold locks for the shortest interval that satisfies correctness, and lock the minimal set, because every extra row held is concurrency foregone for its duration.

Primary sources: <https://www.postgresql.org/docs/current/explicit-locking.html> and <https://www.postgresql.org/docs/current/mvcc.html>.

## Decision rules

- Record the lock modes each statement takes and the access they permit.
- Lock rows in a deterministic total order such as primary-key order.
- Lock the minimal set and hold it for the shortest defensible interval.
- Collect all rows first, lock in a sorted batch, and compute second.
- Implement the deadlock-abort retry with jitter and an attempt cap.
- Monitor deadlocks per period; a rising rate is an ordering bug in production.

## Procedure

1. List the statements and the locks each takes.
2. Determine the total order and verify concurrent paths follow it.
3. Batch-lock the rows and sort them before locking.
4. Add the deadlock retry with fresh reads and an attempt cap.
5. Test the worst concurrent pair — two sessions racing the same rows.
6. Record lock modes, the order, and the retry policy.

## Anti-patterns

- Locking rows in application-traversal order rather than key order.
- Multiple lock points spread through the transaction instead of one gathering step.
- Retrying the deadlock without re-reading the data.
- Unbounded retries with no cap or jitter.
- Assuming deadlocks are rare without monitoring them.

## Done checklist

- [ ] Lock modes recorded.
- [ ] Total order defined and followed.
- [ ] Locks batched before compute.
- [ ] Retry implemented with jitter and cap.
- [ ] Adversarial pair tested.
- [ ] Deadlock monitoring in place.

## Sources

- Explicit locking levels and modes: <https://www.postgresql.org/docs/current/explicit-locking.html>
- Lock interaction with multiversion reads: <https://www.postgresql.org/docs/current/mvcc.html>
- Isolation behaviour of locked reads: <https://www.postgresql.org/docs/current/transaction-iso.html>
