---
name: tail-latency
domain: software-engineering/tail-latency
trigger: "\"p99 is high\", \"some requests take seconds\", \"average looks fine but users complain\", \"long tail latency\"."
anti_trigger: "SLO definition and error budgets (ac-reliability); capacity headroom planning (ac-chaos-and-capacity-testing)."
scope: "Why the tail exists, what creates it, and how to read the latency distribution."
status: seedling
---

# Tail latency

## Standard

The average lies. A p50 of 80 ms with a p99 of 4 seconds is a system that is fast for most and broken for a few, and the few are not random — they are the requests that hit garbage collection, a cold cache, a contended lock, or a queue behind one slow request. Tail work starts by replacing the average with the distribution: percentiles over a window, plotted, not summarised.

The tail is created by specific mechanisms, each with a signature. Queueing amplifies: at high utilisation, arrival variance becomes wait variance, and the tail grows faster than the mean (the "tail at scale" observation from Dean and Barroso, https://dl.acm.org/doi/10.1145/2408776.2408804). Variance sources — background jobs, retries elsewhere, lock contention, page cache misses — land on a few requests and are invisible at p50. The fix order is diagnose-then-reduce: find which mechanism produces the tail before changing anything.

## Decision rules

1. Report p50, p95, p99 — and the max — for every critical path. Never the average alone.
2. Plot the distribution over time; a widening tail is a leading indicator the mean will not show.
3. Attribute the tail: per-request labels for cache hit/miss, GC events, queue depth at arrival.
4. Check utilisation before optimising code: a tail at 90% utilisation is a queueing problem.
5. A latency outlier that correlates with another system's behaviour is that system's problem.
6. One tenant's batch job creating everyone's tail is an isolation failure (see ac-multitenancy-and-isolation).

## Procedure

1. Collect per-request latency with enough labels to attribute the tail.
2. Compute percentiles over fixed windows; plot them.
3. Take the slowest 1% of requests and read their labels — what do they share?
4. Classify the mechanism: queueing, variance source, or genuine work.
5. Fix the mechanism, not the symptom: shed load, isolate, or remove the variance source.
6. Re-measure the tail specifically. The p50 must not regress while the p99 improves.

## Anti-patterns

- Optimising the average path while the tail is a queueing effect.
- Reporting a single "average latency" number to users or in dashboards.
- Treating the max as noise to be discarded — it is a request that happened.
- Adding capacity to fix a tail created by a lock or a background job.
- Checking the p99 only when someone complains.

## Done checklist

- [ ] Percentiles reported for every critical path.
- [ ] Distribution plotted over time.
- [ ] Slow requests attributed by label.
- [ ] Tail mechanism classified.
- [ ] Fix applied to the mechanism.
- [ ] Tail re-measured without p50 regression.

## Sources

- The tail at scale: <https://dl.acm.org/doi/10.1145/2408776.2408804>
- Percentiles and why averages mislead: <https://sre.google/sre-book/monitoring-distributed-systems/>
- Queueing and utilisation effects: <https://learn.microsoft.com/en-us/azure/architecture/>
