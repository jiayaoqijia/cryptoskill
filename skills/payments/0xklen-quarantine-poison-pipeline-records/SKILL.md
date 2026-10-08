---
name: quarantine-poison-pipeline-records
description: Use when one malformed record repeatedly crashes a batch and blocks the rest. Isolates the poison record, lets the batch proceed, and fixes the parse rather than retrying forever.
---

# Quarantine Poison Pipeline Records

One record that fails to parse can abort a whole batch, so good data starves behind it. Catch the failure per-record, quarantine the offending record, and let the batch complete.

## Procedure

1. Make parsing per-record, not per-batch: wrap the decode in a try/catch so one bad record does not fail the file.
   - Python: process row-by-row and catch `json.JSONDecodeError`, `ValueError`.
   - Spark: a UDF returning a struct of (value, error) and `filter(col('error').isNull())`.
2. On failure, write the raw bytes plus the error and the source offset to a quarantine store, then continue the loop.
3. Count and alarm: a nonzero quarantine rate on a healthy source is a signal, not a nuisance.
4. Distinguish a genuine poison record (malformed forever) from a transient one (partial write, ordering). Retry transient ones once before quarantining.
5. Never drop silently: a batch that "succeeded" with 3% quarantined must report that number.
6. Feed the quarantine into monitoring and a replay path once the parser is fixed.
7. For streaming, use a side output or dead-letter topic rather than failing the operator, which restarts from the checkpoint and hits the same record again.
8. Guard against resource-exhaustion records (a multi-GB line) with a size check before parsing; a try/catch cannot catch an OOM kill.
9. Alert when the quarantine rate exceeds a threshold, not per record, so a burst pages once.
10. Keep the quarantine store separate from the target so a target outage does not also lose the bad records.

## Pitfalls

- A whole-batch `try/except` aborts on the first bad record and blocks all others.
- Retrying the batch does nothing for a permanently malformed record; it fails identically each time.
- Dropping bad records without counting hides a rising error rate.
- Quarantining without the raw payload makes the record unrecoverable.
- A parser that crashes the JVM (OOM on a huge record) needs a size guard, not a try/catch.
- Fixing the parser but not replaying the quarantine leaves a permanent gap.
- A per-record alert on every failure floods the channel and gets muted, hiding a rising rate.
- Quarantining on parsing only, missing records that parse but fail a semantic check downstream.

## Verification

```sh
psql -c "SELECT date_trunc('hour',failed_at), count(*) FROM quarantine GROUP BY 1 ORDER BY 1 DESC"
# completeness: loaded + quarantined == input
psql -c "SELECT (SELECT count(*) FROM raw) - (SELECT count(*) FROM loaded) - (SELECT count(*) FROM quarantine)"
```

The gap is zero (every input row landed in loaded or quarantine) and the quarantine rate is under threshold. Report the poison rate, the offending keys, and whether replay is needed.