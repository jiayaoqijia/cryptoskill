---
name: handle-batch-endpoints-with-partial-failure
description: Use when one request carries many items. Chunk to the documented batch limit, read per-item results, and reconcile successes and failures instead of treating the batch as atomic.
---

# Handle batch endpoints with partial failure

Batching is a performance win until one bad item makes you retry the whole batch and duplicate
the 489 that already succeeded. Read the per-item result and retry only what failed.

## Procedure

1. Find the documented batch cap (e.g. 100 ids) and chunk to it, never over:
   ```python
   for chunk in [ids[i:i+100] for i in range(0, len(ids), 100)]:
       r = post("/v1/batch", json={"items": chunk})
   ```
2. Expect a per-item result array even on 200/207 and map results back by id, not array position.
3. On `207 Multi-Status`, split the results into ok and err lists.
4. Re-queue only the failed items, with a bounded retry count, never the whole batch.
5. Watch total payload bytes as well as item count — some APIs cap bytes too.
6. Preserve input order for reporting by joining on id, since servers may reorder.
7. If the API is not atomic, make each item individually idempotent so a mid-batch crash is safe.

## Pitfalls

- Treating a 200 carrying per-item errors as full success silently drops failed writes.
- Positional mapping breaks the moment the server omits or reorders results.
- Retrying the whole batch on one failure duplicates all the successes.
- A batch over the cap can fail the whole request, not just the surplus items.
- 207 is not universal; some APIs return 200 with an `errors` map — read the body.

## Verification

    jq '[.[] | select(.status=="error")] | length' out/batch.json    # equals items re-queued
    jq '[.[] | select(.status=="ok")]    | length' out/batch.json    # equals ok + errored total

Report: "Batch of 500 in 5 chunks: 487 ok, 13 errored (9 invalid, 4 rate-limited) and re-queued."
