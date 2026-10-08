---
name: keep-capacity-headroom-above-peak
description: Use when traffic approaches the point where latency explodes — size capacity left of the knee of the utilization curve and alarm on leading indicators, not saturation.
---

# Keep capacity headroom above peak

Throughput does not degrade linearly with load; past a knee it collapses as queues grow and everything contends. Size for the peak plus headroom so you sit to the left of the knee, and alarm on the leading indicators.

## Procedure

1. Find the knee empirically: load-test at rising rates and plot throughput and p99 against utilization. Past roughly 70-80% of the saturation point, p99 rises steeply — that is the knee.
2. Provision so peak sustained load lands at about 50-60% utilization of the bottleneck resource, leaving room for a spike, a lost instance, or a slow dependency.
3. Identify the true bottleneck first: it may be DB connections, a downstream rate limit, or a lock, not CPU. Measure the resource whose queue is longest.
4. Run capacity at N+1: a deployment with N instances must survive losing one, so target `N/(N-1)` headroom on top of the peak figure.
5. Alarm on leading indicators, not saturation: queue depth, in-flight requests, connection-pool wait time, and a rising p99. CPU at 100% is already too late.
6. Re-derive headroom per release: a change that adds a query per request raises per-request cost and shrinks effective capacity even at constant traffic.
7. For autoscaling, keep a warm floor above the minimum that serves base load instantly; scale-out lag during a spike arrives after the queue has formed.
8. Record the knee and the peak utilization per release in a runbook line, so headroom is a checked figure rather than folklore.

## Pitfalls

- Sizing to the average and hoping peaks are brief — the peak is exactly when downtime happens.
- Confusing average utilization with peak; a service at 40% mean can still saturate every day at 14:00.
- Using CPU alone as utilization for an I/O-bound service, which can sit at 20% CPU and be saturated on connections.
- Autoscaling from a cold floor with a slow boot; the spike is over before new instances are ready.
- Removing the headroom "temporarily" for a big batch and forgetting to restore it before peak.
- Monitoring only the resource you scaled last, missing a new bottleneck that shifted elsewhere.
- Treating a downstream's rate limit as elastic; it is a hard ceiling that returns 429s.
- Measuring capacity in the test environment, which seldom mirrors production data volume.

## Verification

    vegeta attack -rate=1500/s -duration=5m -targets=targets.txt | vegeta report -type=hdrplot
    psql -c "SELECT count(*) FROM pg_stat_activity WHERE state='active';"
    # pass: at peak, bottleneck utilization < 60%, p99 flat, pool wait near zero

Report the measured knee, the utilization at peak, the N+1 target, and the leading-indicator alarm threshold.
