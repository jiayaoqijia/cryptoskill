---
name: make-api-writes-idempotent-with-a-key
description: Use when a POST or PUT creates or charges something over a network. Send a stable idempotency key so a timeout-and-retry cannot double-create.
---

# Make API writes idempotent with a key

The failure mode is a request that succeeds on the server, times out on the client, and gets
retried into a duplicate. A stable idempotency key collapses the retry onto the original result.

## Procedure

1. Derive a deterministic key per logical operation, not per attempt:
   ```python
   import uuid
   NAMESPACE = uuid.UUID("6f9619ff-8b86-d011-b42d-00c04fc964ff")
   key = str(uuid.uuid5(NAMESPACE, f"{user_id}:{cart_hash}"))
   ```
2. Send it in the provider's slot (`Idempotency-Key` header or a body field) and reuse the exact key on every retry of that operation.
3. Persist the key and the resulting resource id so a crash mid-request can be reconciled:
   ```sql
   CREATE TABLE idem(key TEXT PRIMARY KEY, resource_id TEXT, status TEXT);
   ```
4. On a timeout, retry with the same key; the server returns the original result instead of creating a second.
5. Treat `409 Conflict` / "already exists" as success-with-existing-id, not a hard failure.
6. Expire keys only after the provider's window (often 24h); keep them longer than the retry horizon.
7. For providers with no native key, dedupe on a client-generated id and look up before creating.

## Pitfalls

- A random key per attempt defeats the mechanism completely — every retry is a new write.
- Keys that embed the attempt number or a timestamp are per-attempt; keep them stable.
- Key scope is usually per-account and per-endpoint; reusing across endpoints collides.
- Providers cap key length (e.g. 255 chars) and reject malformed ones — hash long inputs.
- A key held only in memory is lost on restart, so the retry horizon must match persistence.

## Verification

    for i in 1 2; do curl -s -X POST "$API/v1/charges" -H "Idempotency-Key: $K" -d @body.json | jq -r .id; done

Both lines print the same id and only one resource exists. Report: "Retried a timed-out charge with key 3f2a...; single charge id returned twice."
