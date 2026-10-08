---
name: bound-pipeline-retries-with-backoff
description: Use when a pipeline retries failed calls and risks amplifying load or hammering a recovering service. Applies bounded exponential backoff with jitter and a circuit breaker, and fails loudly past the budget.
---

# Bound Pipeline Retries with Backoff

Unbounded retries turn a brief outage into a retry storm that keeps the dependency down. Bound attempts, back off exponentially with jitter, and stop calling a service that is clearly failing.

## Procedure

1. Classify errors before retrying: retry only transient ones (timeout, 429, 5xx, connection reset). Never retry 400/422 or a validation failure.
2. Cap attempts (for example 5) and total time (for example 2 minutes). Past either, fail the job or dead-letter the record.
3. Exponential backoff with jitter: `delay = min(cap, base * 2**attempt) * random(0.5, 1.0)`. Jitter prevents synchronized retries across workers.
4. Honour server signals: `Retry-After` on 429/503, and never retry faster than it says.
5. Add a circuit breaker: after N consecutive failures, open and stop calling for a cooldown, then half-open with a single probe.
6. Make the retried operation idempotent so a retry that actually succeeded server-side does not double-write.
7. Retry at one layer only. A library retry under an HTTP-client retry under a job retry multiplies into 5x5x5 attempts.
8. Log each retry with the attempt number and the delay, so a storm is visible in the logs before it exhausts the dependency.
9. Give the job a total time budget and a cancel, so retries cannot outlive the batch window.
10. Treat a permanent failure as terminal once classified, and route it to the DLQ rather than the retry loop.

## Pitfalls

- Retrying a 400 or a schema error wastes the budget and delays the real fix.
- No jitter synchronizes retries from many workers into a spike.
- Retry amplification: three layers of retry stack multiplicatively.
- Retrying a non-idempotent write (a POST that creates) duplicates on the retry.
- Ignoring `Retry-After` extends the outage the server is trying to shed.
- Infinite retries with no total-time cap hang the job until the scheduler kills it.
- A circuit breaker that never half-opens keeps calling a recovered service down.
- Retrying a poison record burns the budget meant for the transient blip.

## Verification

```sh
grep -rn "max_retries\|retry_after\|backoff" config/
python -m pytest tests/test_retry.py -k backoff
```

Retries are bounded, delays grow and carry jitter, and a simulated 429 yields the capped attempts then a clean failure. Report the policy, attempts used, and the failure classification.