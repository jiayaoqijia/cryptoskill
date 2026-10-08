---
name: budget-your-request-rate-against-quota
description: Use when an integration has a hard rate limit or quota. Track remaining budget from headers, reserve headroom, and pace requests so the client throttles itself before the server does.
---

# Budget your request rate against quota

Waiting for a 429 to discover you are over budget means you already are. Pace client-side,
read the remaining-quota headers, and reserve headroom for retries and interactive calls.

## Procedure

1. Learn the quota from docs plus the reporting headers: `X-RateLimit-Limit`, `-Remaining`, `-Reset`.
2. Enforce a rate below the allowance (e.g. 80%) with a token bucket:
   ```python
   import time
   class Bucket:
       def __init__(self, rate, burst):
           self.rate, self.tokens, self.burst, self.t = rate, burst, burst, time.time()
       def take(self):
           now = time.time()
           self.tokens = min(self.burst, self.tokens + (now - self.t) * self.rate); self.t = now
           if self.tokens < 1:
               time.sleep((1 - self.tokens) / self.rate); self.tokens = 0
           else:
               self.tokens -= 1
   ```
3. Read `Remaining`/`Reset` after each call; if the server says you are near the floor, slow down immediately rather than waiting for 429.
4. Reserve a slice (e.g. 10%) of budget for retries and user-triggered calls.
5. Plan batch windows explicitly: 1000 calls at 5/s is 200 s; do not fire them all at once.
6. Persist the counter across restarts so a crash-restart loop does not re-consume the hourly quota.
7. Alert when remaining drops below a threshold, before exhaustion.

## Pitfalls

- Limits are per-key, per-IP, or per-endpoint; a single global counter under-counts and still trips 429.
- Burst allowances mean a steady 80% can still 429 at the top of a window; pace within the second too.
- Counting only HTTP calls misses websocket frames or batch sub-requests that also count.
- Relying on 429s to throttle is reactive and already over budget.
- A rate limiter across processes needs a shared store (Redis); per-process state race-drifts.

## Verification

    grep -c 'X-RateLimit-Remaining' run.log; tail -1 run.log

Report: "Ran 5,000 calls at 8/s; peak remaining 20%; zero 429s."
