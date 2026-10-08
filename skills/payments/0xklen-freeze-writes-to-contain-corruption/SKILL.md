---
name: freeze-writes-to-contain-corruption
description: Use when bad data or a bad deploy is actively writing to a store you cannot roll back instantly — puts the system into a global write-freeze so corruption stops spreading while you assess and repair.
---

# Freeze writes to contain corruption

When a bug is corrupting rows, sending wrong emails or duplicating charges, the first job is to stop the bleeding, not to diagnose. A global write-freeze halts every mutation at one gate so nothing new is written while you decide how far back to repair.

## Procedure

1. Make the freeze a single runtime check on the *write* path, evaluated per request, defaulting to "frozen" when the flag store is unreachable. One gate is auditable; five scattered `if frozen` checks are not:
       if store.GetBool("writes_frozen") { w.Header().Set("Retry-After","60"); http.Error(w,"maintenance",503); return }

2. Freeze at the narrowest layer that still covers every writer: application middleware if all writes go through it, otherwise a DB role. For Postgres, remove the write privilege as the hard backstop so even a stray script is blocked:
       ALTER DATABASE app SET default_transaction_read_only = on;  -- affects new sessions
       REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public FROM app_rw;

3. Let in-flight writes *finish* rather than killing them mid-transaction. Set the flag, wait for open transactions to drain (`SELECT count(*) FROM pg_stat_activity WHERE state='idle in transaction'` is 0), then take the harder layer. A killed half-write is exactly the corruption you are trying to stop.

4. Exempt the repair channel explicitly, not by being quiet about it. Keep one narrowly-scoped writer (a maintenance role or a backfill service account) so you can restore data while the freeze is on, and log every write it makes.

5. Announce the freeze where clients can see it: return `503` with `Retry-After`, and post to the status page. Clients that retry hard against a frozen write API create a retry storm the moment you unfreeze.

6. Decide the recovery order *before* unfreezing: repair the corrupted window, replay any events captured during the freeze, run a reconciliation query, and only then lift the freeze. Lifting first and repairing later re-corrupts.

7. Unfreeze in the smallest blast radius first — one shard, one tenant — and watch the write-error rate and the reconciliation diff before widening.

## Pitfalls

- Freezing reads too, turning a write-corruption incident into a total outage that hides the progress you are making.
- Freezing only the app tier while a cron job, admin script or message consumer keeps writing; the corruption continues and the freeze looks ineffective.
- Lifting the freeze to "run a quick test write" and forgetting to re-freeze, reopening the exact hole mid-repair.
- No `Retry-After` or status-page notice, so every client retries in a tight loop and the unfreeze is immediately followed by a thundering herd.

## Verification

    # with the freeze on, every mutating request must be refused
    curl -s -o /dev/null -w '%{http_code}\n' -X POST localhost:8080/orders -d '{}'   # 503
    psql "$DATABASE_URL" -c "SHOW default_transaction_read_only;"                    # on
    psql "$DATABASE_URL" -c "INSERT INTO t(id) VALUES (1);"                          # ERROR: read-only
    # and reads still serve
    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/orders/1                # 200

Report: the layer the freeze lives at, proof that writes return 503 and the DB rejects a raw insert, reads still serving, and the repair-then-unfreeze order written down before lifting.
