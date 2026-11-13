---
name: long-transactions
domain: software-engineering/long-transactions
trigger: "Containing the cost of transactions that run for minutes or hours."
anti_trigger: "Not for stream state management, and not for batch orchestration."
scope: "Lock hold time, vacuum and snapshot age, and batching the work."
status: seedling
---

# Long transactions

## Standard

A long transaction is expensive in two compounding ways. It holds locks — or a snapshot — for its whole duration, blocking cleanup and concurrent writes in its wake. And under MVCC it pins the version horizon: every row version changed since it started must be retained for it, so a transaction open for hours grows the table's dead-tuple count until it ends, and the vacuum that would reclaim the space cannot pass the horizon it holds.

The treatment is division. A unit of work that must be all-or-nothing is not the same as a program that must run for hours: the work is broken into transactions sized so each is correct alone, the state between them lives in the data rather than in a connection, and the one truly atomic core is kept small. What cannot be divided — a migration, a bulk load — is scheduled with the cost named and an end time recorded.

Primary sources: <https://www.postgresql.org/docs/current/mvcc.html> and <https://www.postgresql.org/docs/current/explicit-locking.html>.

## Decision rules

- Record the intended duration class per transaction: interactive, batch, or maintenance.
- Verify whether an all-day process is genuinely one transaction or a sequence.
- Watch the version-age metric and the oldest-open transaction's age.
- Break batch work into committed units with resumable state in the data.
- Keep reports off primary write traffic where snapshots pin cleanup.
- Record the longest lock-hold and snapshot-hold times observed in production.

## Procedure

1. Measure current transaction durations and the age of the oldest open one.
2. Classify the long runners: genuine atomicity or an accidental giant.
3. Divide the accidental giants and move progress state into the data.
4. Schedule true maintenance work and record its window.
5. Alert on age thresholds and hold times before they bite.
6. Record the observed ranges and the changes made.

## Anti-patterns

- A weekend batch as one transaction because " rollback on failure " sounded safer.
- Measuring query time and assuming it equals lock-hold time.
- A reporting snapshot left open by a forgotten connection.
- Dividing atomic operations into units that are not correct alone.
- Treating vacuum lag as a storage problem rather than a horizon problem.

## Done checklist

- [ ] Long runners measured and classified.
- [ ] Accidental giants divided with resumable state.
- [ ] Version-age metrics watched.
- [ ] Maintenance windows recorded.
- [ ] Alerts on age and hold time.
- [ ] Findings recorded.

## Sources

- Version retention and cleanup: <https://www.postgresql.org/docs/current/mvcc.html>
- Lock hold costs: <https://www.postgresql.org/docs/current/explicit-locking.html>
- Isolation cost under long runs: <https://www.postgresql.org/docs/current/transaction-iso.html>
