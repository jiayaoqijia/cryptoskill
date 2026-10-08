---
name: add-jitter-and-deadline-to-retries
description: Use when a retry loop can outlive its budget or fire in lockstep — bound the timing with exponential backoff plus full jitter and a wall-clock deadline.
---

# Add jitter and a deadline to retries

Retries without jitter re-synchronise a fleet into a thundering herd; retries without a deadline keep an outage alive after the caller gave up. Both are timing bugs, and both are fixed with arithmetic, not flags.

## Procedure

1. Give every retry loop three numbers: a base delay, a cap, and an absolute deadline:
```
base=200ms  cap=20s  deadline=start + 30s
```
2. Delay with full jitter so attempts spread out; the AWS-style formula:
```python
import random, time
def backoff(attempt, base=0.2, cap=20.0):
    return random.uniform(0, min(cap, base * (2 ** attempt)))
time.sleep(backoff(attempt))
```
3. Check the deadline *before* sleeping, and cap the sleep to what remains:
```python
remaining = deadline - time.monotonic()
if remaining <= 0: raise DeadlineExceeded
time.sleep(min(backoff(attempt), remaining))
```
4. Use a monotonic clock for the deadline so an NTP step or DST change cannot extend it (see `distinguish-duration-from-deadline`).
5. Respect `Retry-After` when the server sends it — it overrides your backoff, but not your deadline:
```python
d = float(resp.headers.get("Retry-After", backoff(attempt)))
time.sleep(min(d, max(0, deadline - time.monotonic())))
```
6. Only retry idempotent operations, or attach an idempotency key so a duplicate attempt is a no-op.
7. Log every attempt with `attempt`, `sleep`, and `remaining` so the budget is visible in production.

## Pitfalls

- Fixed-interval retries across N clients produce a synchronised spike exactly one interval after the outage — the herd that took the service down keeps it down.
- Exponential without a cap reaches hours after a few attempts; always cap, and cap at the level that still fits the deadline.
- Jittering the interval but not the *start* leaves the first retry aligned; full jitter randomises the whole delay from zero.
- A deadline in local time or wall clock can be silently extended by a clock step; monotonic cannot.
- Sleeping the full backoff when `remaining` is smaller overshoots the deadline by design — always `min(backoff, remaining)`.
- Retrying a non-idempotent POST duplicates the side effect; a 409 on the retry is a signal, not a failure.

## Verification

```
python3 -c "import random; [print(round(random.uniform(0, min(20, 0.2*2**i)),2)) for i in range(8)]"
```
Values are spread and bounded by the cap, not a fixed ladder = jitter and cap are live. Report: "retries use full-jitter exponential backoff, 30s monotonic deadline, Retry-After honoured; observed attempt spread 0.03-19.9s."
