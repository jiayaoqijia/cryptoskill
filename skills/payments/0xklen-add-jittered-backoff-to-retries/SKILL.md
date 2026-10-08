---
name: add-jittered-backoff-to-retries
description: Use when services retry failed dependencies — replaces fixed retry delays with capped exponential backoff and full jitter to prevent synchronised retry storms.
---

# Add jittered backoff to retries

Synchronised retries turn a blip into an outage: every client retries at the same instant and re-crushes the recovering dependency. Cap the attempts, space them exponentially, and randomise each delay.

## Procedure

1. Make retries opt-in per call, never a global default. A `GET` may retry; a `POST /charge` may not unless the endpoint is idempotent via an idempotency key.

2. Use full jitter, the AWS-recommended form:
       delay = random_between(0, min(cap, base * 2**attempt))
   with `base=100ms`, `cap=5s`, `max_attempts=4`. Full jitter beats equal jitter at the tail when many clients retry together.

3. Budget the total time: `timeout = sum(delays) + per_attempt_timeout`. Wrap the loop in a context/deadline so a request cannot wait 4×5 s; cap the outer deadline at the caller's SLA minus its own work.

4. Retry only retryable errors: connection reset, `503` carrying `Retry-After`, and timeouts. Never retry `400`, `401`, `403`, `404`, `422`. Honour a `Retry-After` header instead of your own delay.

5. Add a retry budget to bound amplification: allow retries only up to 10% of the request rate (gRPC `retryThrottling`, or a per-client token bucket). That caps fan-out at ~1.1×.

6. Emit `retry_attempts_total{outcome}` and alert when attempts/original exceeds 0.1 sustained — that is a dependency degrading, not a transient blip.

7. Stagger fan-out by instance: offset the first attempt by `hash(instance_id) % base` so a thousand pods do not align at t=0.

## Pitfalls

- A fixed `sleep(1s)` in a loop across 500 instances — a synchronised retry storm hits the dependency at exactly 1 s, 2 s, 3 s and blocks its recovery.
- Retrying a write without an idempotency key, double-charging the customer.
- Retrying a slow-but-succeeding timeout, multiplying load on an already-saturated dependency. Prefer retrying only on connection failure, not on the whole timeout.
- No outer deadline, so stacked retries hold connections until the pool is exhausted.

## Verification

    python tools/simulate_retries.py --clients 1000 --base 100 --cap 5000 --jitter full
    # histogram of first-attempt times shows a spread, not a single spike
    curl -s 'localhost:9090/api/v1/query?query=rate(retry_attempts_total[5m])' | jq

Report: base/cap/max_attempts used, the jitter histogram showing spread, and the retry-budget threshold (10%) with the amplification bound (≤1.1×).
