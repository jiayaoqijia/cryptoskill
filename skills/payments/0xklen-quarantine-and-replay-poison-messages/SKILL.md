---
name: quarantine-and-replay-poison-messages
description: Use when one malformed message crashes the consumer and blocks the queue — diverts it to a quarantine store after N failures with full context, then replays it once the fix lands.
---

# Quarantine and replay poison messages

A single malformed message that crashes or hangs the consumer blocks every message behind it: the queue stalls, guaranteed ordering is broken, and on some brokers the message is redelivered forever. Move the poison aside with enough context to fix and replay it, and keep the queue flowing.

## Procedure

1. Detect poison by *attempt count*, not by one failure. Transient errors (timeout, connection reset) look identical to poison on the first try. Use a per-message attempt counter keyed on the message id, stored with a TTL longer than the max backoff:
       attempts = redis.incr(f"att:{msg.id}"); redis.expire(f"att:{msg.id}", 3600)
       if attempts > 5 { quarantine(msg) }

2. On quarantine, *stop retrying* the message and move it to a dead-letter/quarantine queue with the original payload plus context, not just the payload:
       {"id":..., "body":<base64 original>, "error":str(e), "stack":trace,
        "consumer":"orders-v3", "attempts":6, "first_seen":..., "quarantined_at":...}

3. Never drop on quarantine and never ack without storing. An ack that discards the only copy of a message is data loss, and the bug that produced it becomes unobservable.

4. Alert on quarantine *rate*, not volume: one poison message in a million is normal bad data; ten per minute is a producer bug shipping bad payloads. Page above 5/min for 5 min.

5. Build a replay path that reads the quarantine store, applies the decoded payload through the *same* consumer handler with retries disabled, and marks the record replayed (or re-quarantined on repeat failure). Keep replay idempotent so a re-run does not double-apply side effects:
       python tools/replay.py --queue quarantine-orders --since 2026-01-01 --dry-run
       python tools/replay.py --queue quarantine-orders --since 2026-01-01 --apply

6. Keep quarantined payloads for the retention the data requires (often 30 days) and purge on schedule — a quarantine store full of PII is a compliance liability, not just disk.

7. Watch the *source*: group quarantined messages by producer and by schema version. Clustering on `schema_version` or `producer` points at the fix far faster than reading individual errors.

## Pitfalls

- Quarantining on the first failure, so a brief broker hiccup diverts thousands of perfectly good messages into the DLQ.
- Storing only `{"error": ...}` without the original body, so the message can never be replayed and its data is gone.
- A redrive policy with no `maxReceiveCount`, so the message loops through the main queue forever instead of ever reaching quarantine.
- Replaying the whole quarantine store without `--dry-run` first, double-applying charges or emails when the original attempt actually succeeded before the crash.

## Verification

    # inject a malformed message and confirm it lands in quarantine without blocking
    aws sqs send-message --queue-url $Q --message-body '{"broken":'
    aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages
    aws sqs receive-message --queue-url $QUARANTINE --max-number-of-messages 1 | jq '.Messages[0].Body'
    # main queue drains; quarantine holds the one bad message with full context

Report: the attempt threshold, the quarantine payload schema (with original body), the alert rule on quarantine rate, and a replay run in `--dry-run` that reconstructed the failing message and named the producer/schema to fix.
