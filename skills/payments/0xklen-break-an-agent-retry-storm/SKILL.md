---
name: break-an-agent-retry-storm
description: Use when many steps or subagents are retrying the same failing dependency at once. Add backoff and a circuit breaker so the retries do not amplify the outage.
---

# Break an agent retry storm

Simultaneous retries turn a slow dependency into a downed one. When a wave of calls fails together, the agent's instinct to retry all of them is the exact move that makes it worse.

## Procedure

1. Detect the storm: more than N failures against one endpoint within a window — e.g. 5 failures in 10s.
2. Pause all callers to that endpoint, not just the failing one. One retrying child is a blip; a hundred is a stampede.
3. Apply exponential backoff with jitter: `delay = min(cap, base * 2**attempt) * random(0.5, 1.5)`, base 200ms, cap 30s.
4. Add a circuit breaker per endpoint: `closed -> open` after 5 consecutive failures, `open -> half-open` after 20s.
5. In `open` state, fail fast without calling — return a clear `circuit_open` error so callers stop queuing.
6. In `half-open`, let exactly one probe through; success returns to `closed`, failure re-opens with a longer cooldown.
7. Cap total attempts per step (commonly 3) and surface the failure rather than retrying until the budget dies.
8. Log state transitions: `endpoint=api.data circuit=open reason=5_fails cooldown=20s` so the storm is visible in the timeline.

```python
import time, random
def backoff(attempt, base=0.2, cap=30):
    return min(cap, base * 2 ** attempt) * random.uniform(0.5, 1.5)
time.sleep(backoff(attempt))
```

## Pitfalls

- Retrying immediately on failure, which multiplies load exactly when the dependency is weakest.
- Backing off without jitter, so all retries resume on the same tick and re-form the stampede.
- Letting each subagent keep its own breaker, so ten children each retry with no shared view of the outage.
- Retrying non-idempotent writes, turning a storm into duplicated side effects.
- Setting the cap high "to be safe", so the breaker never protects anything before the budget is gone.
- Clearing the breaker on the first success without a half-open probe, snapping back to full load.

## Verification

    grep -E 'circuit=(open|half-open)' notes/action.log | tail -3   # shows the open transition and a single half-open probe

Report the failing endpoint, the backoff schedule applied, and the breaker state at the end of the run.
