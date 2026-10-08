---
name: wrap-remote-calls-in-circuit-breakers
description: Use when one slow dependency is dragging down callers — wraps each remote call in a breaker with closed/open/half-open states, explicit thresholds and bounded probes.
---

# Wrap remote calls in circuit breakers

A retry policy keeps hammering a dead dependency; a breaker stops calling it and fails fast, giving it room to recover. Wrap every cross-process call in one, with thresholds set per dependency rather than per call site.

## Procedure

1. Standardise on one breaker library per language: Go `sony/gobreaker` or `failsafe-go`; Java Resilience4j; Python `pybreaker`. Do not hand-roll a state machine at each call site.

2. Configure four numbers per dependency:
       gobreaker.Settings{ Name: "payments",
         MaxRequests: 3,             // probes allowed while half-open
         Interval:    60*time.Second,// rolling window that resets closed counters
         Timeout:    30*time.Second, // how long to stay open before probing
         ReadyToTrip: func(c gobreaker.Counts) bool { return c.ConsecutiveFailures >= 5 } }

3. Fail fast when open: return a typed `DEPENDENCY_OPEN` error immediately, never wait, so callers shed load instead of piling up slow requests.

4. Bound the half-open probe: allow exactly `MaxRequests` (3) concurrent probes; all succeed → close, any fail → reopen and lengthen `Timeout` modestly (×1.5, capped).

5. Count the right events as failures: transport errors, timeouts and 5xx. A `404` or business `4xx` is a success for breaker purposes, or a legitimate not-found rate trips the breaker.

6. Prefer per-instance breakers. A per-instance breaker lets every replica discover the outage independently, which is acceptable; a global breaker needs a shared store and inherits its failure modes.

7. Export `breaker_state{name}` (0=closed, 1=half-open, 2=open) and `breaker_trips_total`, and alert on `state == 2` for more than a minute.

## Pitfalls

- Threshold too low (2 failures), so one unlucky pod trips the breaker and it flaps forever.
- Counting `4xx` as failures: a client sending bad ids trips the breaker and takes the service down for good callers too.
- No per-attempt timeout under the breaker, so the call still hangs 30 s before counting as a failure and the breaker never protects latency.
- A "global" breaker held in the very store that is the dependency going down.

## Verification

    toxiproxy-cli toxic add -t latency -a latency=5000 payments
    curl -s 'localhost:9090/api/v1/query?query=breaker_state{name="payments"}' | jq '.data.result[0].value'
    # expect state 2 within ~5 failures, then fail-fast p99 < 5ms

Report: the four settings used, the observed closed→open→half-open→closed transition under fault injection, and the fail-fast path's p99 (< 5 ms).
