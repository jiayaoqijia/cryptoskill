---
name: retry-5xx-with-capped-jittered-backoff
description: Use when API calls fail transiently. Retry only retryable failures, honour Retry-After, add full jitter, and cap the total so one dead endpoint cannot consume the run.
---

# Retry 5xx with capped jittered backoff

Retrying indiscriminately floods the API and hides your bugs; retrying blindly with fixed delays
aligns every client into a thundering herd. Classify, then back off with jitter and a ceiling.

## Procedure

1. Partition errors by retryability before writing the loop:
   ```python
   RETRY = {408, 429, 500, 502, 503, 504}   # everything else: do not retry
   ```
2. On 429/503 read `Retry-After` (seconds or HTTP date) and wait exactly that; only fall back to your own backoff when it is absent.
3. Use full jitter so clients do not re-synchronise:
   ```python
   import random, time
   delay = random.uniform(0, min(30, 0.5 * 2**attempt))  # base=0.5, cap=30
   time.sleep(delay)
   ```
4. Cap attempts (3-5) and total elapsed per call (e.g. 60 s); exit on whichever trips first.
5. Retry only idempotent requests (GET/PUT/DELETE) or POSTs carrying an idempotency key.
6. Log attempt number, status, and the sleep each pass so a retry storm shows up in logs.

## Pitfalls

- Retrying 400s floods the API and hides your bug; classify first, retry last.
- Client sleeps without a per-request timeout hang forever on a blackholed socket.
- Backing off on 429 without reading `Retry-After` can retry too soon and extend the ban.
- A shared retry counter across calls couples unrelated failures; count per logical call.
- A per-request timeout shorter than the backoff means the sleep is cut off and never completes.

## Verification

    grep -E 'attempt=[1-9]' run.log | wc -l
    grep -c 'status=503' run.log

Every 503 is either resolved or capped at the attempt limit; counts are bounded, not growing. Report: "1,240 calls, 12 retries all on 503, all resolved within 4 attempts."
