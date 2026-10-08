---
name: retry-vs-switch
description: Use when a command, request, or API call fails. Classifies the failure as transient, deterministic, or unknown to decide between bounded retry and changing approach.
---

# Retry vs Switch

Retrying a deterministic failure just spends the same money again. Retrying a transient one is free progress. Classify the failure from its signal before you touch it again.

## Procedure

1. Read the failure signal: exit code, HTTP status, and the message text. Do not retry before reading all three.
2. Classify:
   - Transient: `429`, `503`, `504`, connection reset, `ETIMEDOUT`, DNS blip, lock contention. → retry.
   - Deterministic: `400`, `401`, `403`, `404`, syntax error, `No such file`, type error, validation failure. → fix the input; do not retry the same call.
   - Unknown: anything else. → retry once, then switch to inspection.
3. Retry with a bounded backoff and a cap: at most 3 attempts, delays 1s, 2s, 4s (add jitter: `sleep $((2**n + RANDOM%2))`). Give up and report if all three fail.
4. Respect the server's own signal: on `429`, read `Retry-After` and wait that long instead of guessing.
5. Before retrying anything that mutates state, confirm it is idempotent, or use an idempotency key, or check whether the first attempt actually landed. Retrying a payment or an email sends it twice.
6. On switching, change the class of approach, not a parameter (see `detect-sunk-cost-trap`): different endpoint, different library, cached data, a manual step.
7. Cap total time too: a retry loop needs a deadline (`timeout 120 bash -c '...'`), not just an attempt count.
8. Log each attempt with its layer: `attempt=2 layer=network status=503 action=backoff`.
9. Distinguish "the call failed" from "the call succeeded but the response was empty"; the second is not retryable without investigating.
10. On a `429`, back off to at least the `Retry-After` value and reduce concurrency rather than resuming the same rate.
11. Record the final outcome per call (`ok`, `fixed-input`, `switched`, `gave-up`) so repeats become visible later.

## Pitfalls

- Retrying a `404` or a `400` three times, which cannot succeed by repetition.
- Retrying a non-idempotent write after a timeout when the first write probably succeeded — now there are two.
- Exponential backoff with no cap, sleeping minutes on the third try.
- Retrying the same layer (network) when the fault is a schema mismatch the server keeps rejecting.
- Treating a `429` as permission to hammer harder rather than to slow down.
- Wrapping a whole request sequence in one retry, redoing the successful early calls each time.
- Retrying under a new connection to dodge a rate limit that is keyed on the account, not the socket.

## Verification

    # Attempts appear in the log with distinct layers/statuses, and total wall time is bounded
    grep -n "attempt=" notes/attempt-ledger.tsv | tail -10
    # passes when no single call shows >= 3 retries of the same deterministic error

Report to the user: the failure class per attempt, the retry policy used, and the switch that was made (or why the call was abandoned).
