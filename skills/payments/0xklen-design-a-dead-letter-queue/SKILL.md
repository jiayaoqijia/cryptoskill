---
name: design-a-dead-letter-queue
description: Use when records fail validation or processing and must not be silently dropped or block the pipeline. Captures each failure with payload, error, and origin so it can be inspected and replayed.
---

# Design a Dead-Letter Queue

A record that fails processing should leave the pipeline with everything needed to understand and re-run it, not vanish into a log line. A DLQ is a durable store plus the metadata that makes a replay possible.

## Procedure

1. Store the full original payload, serialized as received, not just the error message. Without the payload there is nothing to replay.
2. Attach metadata: `job_name`, `source`, `partition_or_window`, `failed_at`, `attempt_count`, `error_class`, `error_message`, and the record's natural key.
3. Key on natural key plus arrival time so a repeated failure of the same record shows as a rising `attempt_count`, not endless duplicate rows.
4. Separate transient failures (timeout, rate limit) from permanent ones (schema invalid, referential failure). Only permanent failures belong in the DLQ; retry transient ones first.
5. Set a max attempt count; past it, move the record to a terminal state and alert.
6. Make replay first-class: a tool that reads DLQ rows, re-runs them through the same validation and load, and clears each on success.
7. Bound the queue: a retention policy and an alarm when depth grows past a threshold (for example >100 rows or +20% per hour).
8. Never let growth be silent. A pipeline that always succeeds while dropping 5% of records is worse than one that fails.
9. Include a `state` column (`pending`, `retrying`, `terminal`) so consumers of the DLQ can filter what is actionable.
10. Store the schema version of the payload, so a replay months later parses it with the code that produced it.

## Pitfalls

- Logging the error but not the payload makes the DLQ useless for replay.
- A DLQ with no consumer grows forever and is discovered only when a table is missing rows.
- Retrying a permanently malformed record to max attempts wastes the budget meant for transient errors.
- No dedupe key means a record that fails every run fills the queue with duplicates.
- Storing only the error string loses the field values that caused it.
- Treating the DLQ as a graveyard: nothing is fixed, the gap just becomes permanent.
- A DLQ on the same storage as the target means a target outage also loses the failures.
- Storing a PoC payload without its schema version makes replay impossible after the code moves on.

## Verification

```sh
kafka-consumer-groups --bootstrap-server $BROKER --describe --group dlq-inspector
psql -c "SELECT count(*), max(failed_at) FROM dead_letters"
```

Depth is under threshold and the oldest entry is recent, meaning someone is draining it. Report DLQ depth, the top error classes, and the path of the replay tool.