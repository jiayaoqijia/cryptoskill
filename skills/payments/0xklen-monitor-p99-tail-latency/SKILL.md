---
name: monitor-p99-tail-latency
description: Use when average latency looks fine but users complain — measure the p99/p999 tail from a histogram, never a mean, and alert on the tail.
---

# Monitor p99 tail latency

An average hides the tail, and the tail is what users feel. A service with p50=10ms and p99=2s has a fine average and one request in a hundred timing out. Track percentiles from a histogram and alert on p99 and p999.

## Procedure

1. Emit a histogram, never a mean. Prometheus `http_request_duration_seconds_bucket`, a Datadog distribution, or a StatsD timer; never `avg`.
```python
REQ = Histogram("http_request_duration_seconds", "req",
                buckets=[.005,.01,.025,.05,.1,.25,.5,1,2.5,5,10])
REQ.labels(endpoint=ep).observe(elapsed)
```
2. Choose buckets around the SLO. For a 200ms SLO you need buckets at 100/150/200/250ms, not a spread that cannot resolve the boundary.
3. Query the tail from the histogram:
```
histogram_quantile(0.99,
  sum by (le, endpoint) (rate(http_request_duration_seconds_bucket[5m])))
```
4. Graph p50, p99, and p999 together: a widening gap between p50 and p99 is a queueing or contention problem, not uniformly slow code.
5. Track the *count* of slow requests, not only the percentile: p99 is computed from few samples at low traffic and is noisy, so require a minimum request rate before alerting on it.
6. Alert on the tail exceeding the SLO error budget (a burn-rate alert), not on a single spike that self-clears.
7. Correlate the tail with GC pauses, lock waits, pool waits, and cold caches by overlaying those metrics on the same axis.

## Pitfalls

- Averaging across endpoints, so one slow endpoint vanishes into a fast global mean.
- Bucket resolution coarser than the SLO — 100ms and 1s buckets cannot tell 150ms from 900ms.
- Averaging percentiles over time (the mean of p99s) instead of computing from the histogram.
- Alerting on p99 at low traffic, where it is a single request.
- Measuring client-side, including the network to the user, then blaming the server.
- Unbounded label cardinality (user id, URL with ids) exploding the histogram's memory.

## Verification

    curl -s localhost:9090/api/v1/query --data-urlencode \
      'query=histogram_quantile(0.99,sum by(le)(rate(http_request_duration_seconds_bucket[5m])))'
    # pass: p99 returned as a number, buckets fine enough near the SLO

Report p50/p99/p999 for the endpoint, the bucket set relative to the SLO, and the slow-request count per minute.
