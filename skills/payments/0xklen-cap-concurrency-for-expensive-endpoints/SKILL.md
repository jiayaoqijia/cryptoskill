---
name: cap-concurrency-for-expensive-endpoints
description: Use when one expensive endpoint exhausts the shared pool and starves everything else — give it a dedicated bounded lane and its own connection pool.
---

# Cap concurrency for expensive endpoints

A few expensive endpoints share the same connection pool and thread budget as cheap ones. Run concurrently, they consume every connection and starve health checks and fast reads. Give expensive work its own small, bounded lane.

## Procedure

1. Identify expensive endpoints by measured cost: p99 over 1s, or query rows/CPU per call far above the mean. Cross-reference the endpoint with `pg_stat_statements` total time.
2. Give each a dedicated concurrency limit, separate from the general request limiter:
```python
REPORT_SEM = asyncio.Semaphore(4)
async def report(req):
    if not await acquire_now(REPORT_SEM):     # non-blocking try-acquire
        raise HTTPException(429, "report lane full", headers={"Retry-After": "5"})
    try:
        ...
    finally:
        REPORT_SEM.release()                  # release on every path
```
3. Or use a bulkhead: a separate connection pool or worker pool for expensive work, so it can never take the general pool's connections:
```python
report_engine = create_engine(url, pool_size=4, pool_timeout=2)
```
4. Return `429` with `Retry-After` when the lane is full, rather than queueing until everything times out.
5. Move genuinely heavy work — exports, big reports — to a background job: return `202 Accepted` with a job id and let the client poll; do not hold an HTTP connection for 30s.
6. Set a per-endpoint timeout shorter than the request budget so a runaway report is cancelled and releases its slot.
7. Watch the lane's queue depth and the general pool's wait time; if expensive endpoints still starve the general pool, the bulkhead is not actually separate.

## Pitfalls

- A global rate limiter that does not distinguish endpoints, so cheap requests are throttled while expensive ones slip through elsewhere.
- A semaphore acquired but not released on the error path, leaking slots until the lane is permanently full.
- A bulkhead that shares the same underlying connection pool, so it is not a bulkhead at all.
- `429` without `Retry-After`, so clients retry immediately and hold the lane saturated.
- Streaming a 30s report through the request path instead of making it a job.
- Setting the lane size above the database's useful concurrency, so the cap protects nothing.

## Verification

    hey -z 30s -c 50 http://localhost:8080/report &
    hey -z 30s -c 50 http://localhost:8080/ping
    curl -s localhost:9090/metrics | grep -E "report_inflight|pool_wait_seconds"
    # pass: /ping p99 unchanged, /report returns 429 past the cap, pool wait near zero

Report the endpoint's concurrency cap and pool, the 429 behavior, and the p99 of a cheap endpoint while the expensive one is saturated.
