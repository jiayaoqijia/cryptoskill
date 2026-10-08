---
name: plan-capacity-from-load-data
description: Use when sizing infrastructure for expected traffic. Derives required replicas from measured p95 throughput and latency, leaving explicit headroom over the saturation point.
---

# Plan Capacity from Load Data

Capacity plans built on averages fail at the p99. Size from the worst realistic peak latency, the throughput one instance sustains before saturation, and an explicit headroom factor.

## Procedure

1. Measure per-instance saturation throughput: the requests per second at which p99 latency starts climbing. Ramp with `k6 run --vus 50 --duration 2m script.js` and plot RPS vs p99 — the knee is your ceiling, not the peak RPS you reached.
2. Take the load model from real data, not a guess: peak RPS from access logs over 7 days, e.g. `awk '{print $4}' access.log | cut -c2-15 | sort | uniq -c | sort -rn | head`.
3. Apply Little's Law to check concurrency: `concurrency = RPS × latency`. 500 RPS at 40 ms needs ~20 in-flight requests per instance.
4. Compute replicas: `replicas = ceil(peak_RPS / per_instance_RPS / (1 - headroom))`. Use headroom 0.3 for steady services, 0.5 for spiky ones so a lost instance or a rolling deploy is survivable.
5. Add N+1 for failure: a service that must tolerate one instance down sizes to `replicas + 1` per zone if failures are zone-scoped.
6. Test the plan: `k6 run --vus <planned> --duration 10m` against the planned fleet size and confirm p99 stays under the SLO at peak × 1.3.
7. Set autoscaling on the leading indicator (RPS, queue depth, CPU at ~70%) with a scale-up cooldown shorter than the traffic ramp, and a floor that survives a zone loss.
8. Record the assumptions (per-instance RPS, headroom, SLO) in a doc — a capacity number without its inputs cannot be revisited.

## Pitfalls

- Sizing on average latency; the p99 drives timeouts and retries, which multiply load.
- Ignoring retry amplification: a client retrying 3× turns a 20% overload into 60%.
- Autoscaling on CPU for I/O-bound work never triggers; scale on concurrency or queue length instead.
- A load test from one region does not exercise the cross-region latency real users see.
- Forgetting the database: app replicas scale horizontally, one primary does not, so the DB becomes the ceiling.
- Cold start and connection-pool warmup make the first minute after scale-out slower than steady state; factor it into the ramp.
- A capacity plan without a cost line is half a plan; multiply replica count by instance price per hour before committing.

## Verification

    k6 run --out json=result.json --vus <n> --duration 10m load.js && \
      jq '[.metrics.http_req_duration.values["p(99)"]][0]' result.json

p99 stays below the SLO threshold at 130% of forecast peak with one instance removed.

Report: "Per instance <N> RPS before the p99 knee; peak <P> RPS → <R> replicas at 30% headroom; verified p99 <X>ms at 1.3× peak with a faulted instance."
