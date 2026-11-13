---
name: savepoints-and-partial-rollback
domain: software-engineering/savepoints-and-partial-rollback
trigger: "Recovering part of a failed transaction without losing all of it."
anti_trigger: "Not for workflow durability across processes, and not for retry design."
scope: "Nested work inside one transaction and recovering part of it."
status: seedling
---

# Savepoints and partial rollback

## Standard

A savepoint is a named mark inside a transaction: the work between the transaction's start and the mark stays committed-in-progress, and a rollback to the mark undoes only what came after it. The transaction continues, so a single bad row in a ten-thousand-row batch does not discard nine thousand nine hundred and ninety-nine good ones — it is skipped, the savepoint swallows its failure, and the batch proceeds.

The discipline is proportion. Rolling back to a savepoint and continuing is right when a failure is record-local and the surrounding work is still valid; a full rollback is right when the failure invalidates the unit's premise. Deciding which failures are which is a design decision made before the batch runs, and a savepoint used to swallow errors that actually poison the unit produces a committed transaction whose premise was never checked.

Primary sources: <https://www.postgresql.org/docs/current/sql-savepoint.html> and <https://www.postgresql.org/docs/current/transaction-iso.html>.

## Decision rules

- Classify per-failure behaviour: skip the record or abort the unit.
- Create the savepoint immediately before the risky per-record work.
- Roll back to it on record-local failure, log the record, and continue.
- Save the decision on the commit shape: unit or partial, before the run.
- Record the released savepoint names, and release them when passed.
- Retry never continues past a full rollback — there is nothing to continue from.

## Procedure

1. Define the batch's transaction shape and failure classes.
2. Create a savepoint before each record or sub-batch.
3. On failure, roll back to the savepoint and record the skip.
4. On unit-level failure, roll back the transaction and exit.
5. Release passed savepoints to bound the savepoint stack.
6. Record the shape and failure classes in the isolation record.

## Anti-patterns

- One savepoint for the whole batch, making it equivalent to a full rollback.
- Continuing after an error that invalidates the premise.
- Never releasing savepoints, growing the stack for a long run.
- Rolling back to a savepoint that predates already-committed-elsewhere assumptions.
- Mixing skip and abort decisions decided on the spot rather than in design.

## Done checklist

- [ ] Failure classes defined.
- [ ] Savepoints placed at the per-record boundary.
- [ ] Skip versus abort decided in advance.
- [ ] Unit-level failures given the full rollback.
- [ ] Savepoints released when passed.
- [ ] Decisions recorded.

## Sources

- Savepoint syntax and behaviour: <https://www.postgresql.org/docs/current/sql-savepoint.html>
- Transaction structure and levels: <https://www.postgresql.org/docs/current/transaction-iso.html>
- Locks held across the batch: <https://www.postgresql.org/docs/current/explicit-locking.html>
