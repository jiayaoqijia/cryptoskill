---
name: cap-subagent-concurrency
description: Use when launching many subagents at once against a shared backend or machine. Limits in-flight children to a fixed number so the host, API, or rate budget is not overwhelmed.
---

# Cap Subagent Concurrency

Unbounded fan-out turns a rate limit into a wall of 429s and a local machine into swap death. Fix a maximum in-flight count and queue the rest.

## Procedure

1. Find the binding limit first: API requests/sec, provider concurrent-request cap, CPU cores, or memory per child.
2. Derive the cap from that limit with headroom — with a 10 req/s budget and one request per child per second, run at most 6-8 children.
3. Implement the cap as a semaphore or queue, not by splitting the roster by eye: keep `inflight < MAX` before starting the next child.
4. Start with a conservative default (4) and raise it only after a wave completes with no 429 or 502 responses in logs.
5. Log in-flight count over time in `notes/concurrency.log` with `ts inflight queued`.
6. Alarm on rate-limit responses (`grep -c '429' child-*.log`) and cut the cap whenever the count is nonzero.
7. Watch local resources: `ps -axo pid,rss,command | grep child` and total RSS against available memory.
8. On a bound host, prefer a lower cap with more retries over a high cap that triggers OOM and loses whole children.
9. Reset the cap to the proven value for the next wave; do not leave it at a one-off experiment number.
10. When the queue grows past a couple of waves' worth, stop accepting new work and report backpressure rather than letting wait times explode.

## Pitfalls

- Launching all fifty children and letting the provider's 429 handler act as your limiter, wasting the retries.
- Setting MAX from CPU cores alone when the real constraint is the remote API's per-second quota.
- Forgetting memory per child (a browser or a model load), so a cap that fits cores still exhausts RAM.
- Raising the cap after one clean wave on a tiny roster, then re-running a large one that collapses.
- Counting started children rather than finished ones, so the queue drains slower than expected and looks stuck.

## Verification

```bash
sort -k2 -n notes/concurrency.log | tail -1 | awk '{print "peak-inflight=" $2}'; grep -c 429 child-*.log
# passes when peak in-flight <= MAX and the 429 count is zero
```

Report to the user: the chosen MAX, the peak in-flight observed, and any rate-limit or OOM event that forced a cut.
