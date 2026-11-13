---
name: isolation-record
domain: software-engineering/isolation-record
trigger: "Writing the isolation and locking record for a unit of work."
anti_trigger: "Not for the database's changelog, and not for schema history."
scope: "The written record: level, assumptions, locks, and retry policy."
status: seedling
---

# Isolation record

## Standard

The isolation record states, per unit of work, the isolation level, the anomalies it assumes cannot occur, the locks it takes and in what order, its retry behaviour on abort and deadlock, and its duration class. It exists because the isolation assumptions of a code path are invisible in the code itself — a read-modify-write looks identical whether it is safe or racy — and the record is where the difference is written down.

Its second function is the audit trail for the retry policy. Deadlock and serializable aborts return errors that the application treats as retryable, and the record names what the retry does: re-reads fresh data, bounds its attempts, and jitters its waits. A unit whose retry details are recorded can be reviewed for the stampede it will cause on a hot row; one whose retries live only in a catch block cannot.

Primary sources: <https://www.postgresql.org/docs/current/transaction-iso.html> and <https://www.postgresql.org/docs/current/explicit-locking.html>.

## Decision rules

- Record the isolation level for each unit of work and the reason it suffices.
- Record the anomalies the unit tolerates and those it refuses.
- List the locks taken, their mode, and the total order they are acquired in.
- Record the retry behaviour: re-reads, caps, jitter, and failure after exhaustion.
- Record the duration class and the hooks it must hold.
- Amend by dated entries only.

## Procedure

1. Enter the unit of work, its level, and the tolerated anomalies.
2. List locks with modes and ordering.
3. Describe the retry path, including what it re-reads and its cap.
4. Note the duration class and the operations it blocks.
5. Note the test that demonstrates each removed anomaly.
6. Date and append amendments at review or change.

## Anti-patterns

- No record, so the level choice is folklore held in one person's head.
- Retry described as "handled in the catch block" instead of by behaviour.
- Tolerated anomalies decided by what the level happened to be.
- Lock order implicit in the code.
- A level change without a corresponding assumption review.

## Done checklist

- [ ] Level and rationale per unit recorded.
- [ ] Anomaly tolerance explicit.
- [ ] Lock modes and order listed.
- [ ] Retry behaviour fully described.
- [ ] Duration class noted.
- [ ] Anomaly tests referenced.

## Sources

- Isolation levels as documented behaviour: <https://www.postgresql.org/docs/current/transaction-iso.html>
- Explicit lock modes: <https://www.postgresql.org/docs/current/explicit-locking.html>
- Lock interaction with version retention: <https://www.postgresql.org/docs/current/mvcc.html>
