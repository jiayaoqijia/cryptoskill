---
name: shed-load-gracefully-under-overload
description: Use when a service saturates and latency explodes — adds admission control, bounded queues and priority shedding so the service degrades instead of collapsing.
---

# Shed load gracefully under overload

Past the knee of the latency curve, more concurrency yields less throughput: queued requests wait while tail latency grows without bound. Shed early, shed by priority, and shed with the right status code.

## Procedure

1. Find the concurrency limit empirically. Sweep load and plot throughput against in-flight requests; the knee is where throughput flattens while p99 rises. Set max concurrency to about 70% of the knee.

2. Enforce it with a bounded semaphore acquired before any expensive work:
       sem := make(chan struct{}, 200)
       select { case sem <- struct{}{}: defer func(){ <-sem }()
       default: http.Error(w, "overload", 503); return }

3. Bound the queue hard: max wait 50 ms and max depth equal to the concurrency limit. A request that waits longer than its admission budget is already outside its SLA — reject it rather than serve it late.

4. Shed by priority: interactive (checkout) before batch and reporting. Keep separate semaphores or weighted admission (checkout gets 8 of 10 slots). Return `503` with `Retry-After: 1` so clients back off.

5. Return `503`, not `500`, for shed requests and exclude them from the error-SLO numerator: shedding is a capacity statement, not a bug. Still alert on a shed ratio above 1% for 5 min — that is the capacity signal.

6. Degrade features instead of the whole service: serve cached responses, drop the recommendation panel, compute a cheaper aggregate. Gate each with a flag toggled from a load signal.

7. Protect downstreams with bulkheads: cap outbound concurrency per dependency so one slow peer cannot consume the inbound budget.

## Pitfalls

- An unbounded queue converts overload into memory growth and a 30 s p99, then an OOM. A queue is only useful if it is bounded and short.
- Shedding at random kills checkout while batch jobs survive; always prioritise by business value.
- Counting shed `503`s as errors in the SLO burns the error budget during a legitimate capacity event and hides the real cause.
- Setting the limit from a dev-box benchmark (8 cores, no TLS) rather than production hardware and traffic mix.

## Verification

    vegeta attack -rate 5000 -duration 60s -targets targets.txt | vegeta report
    # shed 503s rise but served p99 stays under SLO; throughput plateaus, no collapse
    curl -s 'localhost:9090/api/v1/query?query=rate(http_requests_total{code="503"}[1m])' | jq

Report: the knee concurrency, the 50 ms admission budget, the shed ratio at 5000 rps, and served-request p99 remaining under SLO.
