---
name: verify-a-webhook-is-delivered-at-least-once
description: Use when consuming webhooks that may be retried. Dedupe by event id in durable storage, tolerate out-of-order delivery, and make the handler idempotent so a duplicate is a no-op.
---

# Verify a webhook is delivered at least once

Webhook delivery is at-least-once: the same event arrives again after a timeout or provider
retry. Without dedupe you double-charge, double-send, or double-count.

## Procedure

1. Assume the same event id arrives more than once — retries, dual regions, manual replays.
2. Extract the provider's stable id (`id`, `event.id`, `X-GitHub-Delivery`) and record it with a unique constraint:
   ```sql
   CREATE TABLE seen_events(event_id TEXT PRIMARY KEY, received_at TIMESTAMPTZ DEFAULT now());
   INSERT INTO seen_events(event_id) VALUES ($1) ON CONFLICT DO NOTHING;
   ```
3. If the insert affects 0 rows the event is a duplicate: return 200 and stop; do not reprocess.
4. Assume out-of-order delivery: key state changes on the event's own timestamp/sequence, or re-fetch current state from the API.
5. Make the side effect idempotent (upsert, not insert) as a second line of defence.
6. Return 2xx only after committing the dedupe row, so a crash lets the provider retry.
7. Expire old event ids after the provider's retry window (often 3-7 days), not immediately.

## Pitfalls

- Deduping in memory is lost on restart; use durable storage.
- Using the whole payload as the key fails when the provider adds a volatile field; use the id.
- Processing before recording lets two concurrent deliveries both proceed; record first.
- Providers differ on ordering guarantees per resource; read the docs, do not assume.
- Expiring ids too early lets a delayed retry through as a "new" event.

## Verification

    curl -s -X POST localhost:3000/hook -H "X-Event-Id: evt_1" -d @evt.json   # 200, processed
    curl -s -X POST localhost:3000/hook -H "X-Event-Id: evt_1" -d @evt.json   # 200, deduped
    psql -c "select count(*) from seen_events where event_id='evt_1'"          # 1

Report: "Duplicate evt_1 returned 200/duplicate; one row in seen_events; side effect ran once."
