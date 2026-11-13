---
name: write-ahead-logging
domain: software-engineering/write-ahead-logging
trigger: "Reasoning about what a write-ahead log makes durable and when."
anti_trigger: "Not for archival audit trails (ac-audit-logging)."
scope: "Log-before-overwrite, Group Commit, checkpoints, and recovery replay."
status: seedling
---

# Write-ahead logging

## Standard

A write-ahead log makes an in-place-update structure crash-safe: every change is recorded in the log and forced to stable storage before the data page it describes is allowed to be written. After a crash, recovery replays the log from the last checkpoint and re-applies the changes the pages may not have received, converting a partially written page file into a consistent one.

The log is also the engine's throughput regulator. Because each acknowledged write costs at least one log flush, batching many transactions' records into one flush — group commit — is the primary lever for write throughput, and its cost is measured in acknowledgements delayed. The checkpoint bounds recovery time by advancing the point from which replay must start, and it chooses when to run based on the recovery window it tolerates. These two settings together decide the latency and the recovery time of every acknowledged write.

Primary sources: <https://postgresql.org/docs/current/wal-configuration.html> and <https://en.wikipedia.org/wiki/Write-ahead_logging>.

## Decision rules

- Record the log's durability setting and the acknowledgement it provides.
- Record whether and when group commit batches, including the window and what causes it to close early.
- Record the buffer used for log records and what recovery loses if it is still unwritten.
- Record the checkpoint interval and follow-up recovery replay length that interval implies.
- Record what happens after a crash to a transaction whose acknowledge preceded the flush of its log record.
- Record the log's space management and how reuse might allow recovery to fail.

## Procedure

1. Record the log setting that defines an acknowledged write.
2. Measure the group commit's batch size and its acknowledgement delay.
3. Record the log buffer size and its loss window after a crash.
4. Record the checkpoint interval and the replay length it implies.
5. Trace one acknowledged write from log record to data page to checkpoint.
6. Write the record with the acknowledgement contract stated in implementation terms.

## Anti-patterns

- Assuming an acknowledgement means durable without reading the setting.
- Comparing write throughput across durability settings.
- Sizing the log buffer without recording the loss window it represents.
- Tuning the checkpoint interval without calculating the recovery time it implies.
- Treating log space as free because the log is discarded.

## Done checklist

- [ ] Durability setting and its acknowledgement recorded.
- [ ] Group commit window recorded.
- [ ] Buffer loss window recorded.
- [ ] Checkpoint interval and replay length recorded.
- [ ] Acknowledged write traced end to end.
- [ ] Contract stated in implementation terms.

## Sources

- PostgreSQL write-ahead log configuration: <https://postgresql.org/docs/current/wal-configuration.html>
- InnoDB redo log architecture: <https://dev.mysql.com/doc/refman/en/innodb-redo-log.html>
- Write-ahead logging and crash recovery: <https://en.wikipedia.org/wiki/Write-ahead_logging>
