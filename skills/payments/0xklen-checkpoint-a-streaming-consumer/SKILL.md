---
name: checkpoint-a-streaming-consumer
description: Use when a streaming consumer must resume without loss or duplication after a restart. Commits offsets and state atomically with output and validates that recovery replays from the right place.
---

# Checkpoint a Streaming Consumer

A consumer that loses its position on restart either reprocesses hours of data or silently skips it. Checkpointing records how far processing got, and recovery must resume exactly there.

## Procedure

1. Decide what a checkpoint means: the input offset consumed, a state snapshot, or both. Stateful operators need both.
2. Commit offsets tied to output, not on a timer.
   - Spark: `foreachBatch` plus `checkpointLocation`.
   - Flink: `env.enableCheckpointing(60000)`.
   - Kafka Connect: enable the connector's offset storage.
3. Use a durable checkpoint location on shared storage (`s3://.../checkpoints/job`), never a local disk that dies with the pod.
4. Set the interval against semantics: shorter means less reprocessing but more overhead; align it with the sink's transaction granularity.
5. On recovery, the framework resumes from the last completed checkpoint. Confirm the resumed offset matches the last committed output.
6. Watch the checkpoint as a health signal: a job that has not checkpointed in more than three intervals is stuck, even if it reports RUNNING.
7. Prune old checkpoints/snapshots so storage stays bounded, but never the latest complete one.
8. Test by killing the job (not a graceful stop) and restarting; verify no gap and no duplicate at the boundary.
9. Size the checkpoint interval so the maximum reprocessed window is within your SLO.
10. Record the source partition count in the checkpoint metadata so a resharding is visible before it corrupts state.

## Pitfalls

- Storing checkpoints on ephemeral local disk loses them on a pod reschedule.
- A checkpoint that advances even when the sink write failed turns a failure into silent data loss.
- State schema changes between deploys make old checkpoints unreadable; use state schema evolution or start fresh.
- A checkpoint interval longer than the SLO means every restart reprocesses more than the SLO allows.
- Two jobs sharing a checkpoint location corrupt each other's state.
- Treating RUNNING as healthy when checkpoints have stopped.
- Changing the number of partitions without state redistribution silently drops keyed state.
- Committing offsets manually in user code races the framework's checkpoint and reintroduces duplicates.

## Verification

```sh
ls -lt s3://bucket/checkpoints/job/ | head
kafka-consumer-groups --describe --group myjob
```

Checkpoint files are recent and consumer lag is near zero. Report the checkpoint location, interval, last offset, and the result of the kill-restart test.