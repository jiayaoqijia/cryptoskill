---
name: continuous-profiling-in-production
description: Use when a slowdown only appears under real production traffic — run a low-overhead continuous profiler and read the flamegraph from the slow window, not a synthetic benchmark.
---

# Continuous profiling in production

A laptop benchmark does not reproduce production's data shapes, cache state, and contention. A continuous profiler samples every process at low overhead and keeps per-window flamegraphs, so when p99 spikes you can open the profile from that exact minute.

## Procedure

1. Pick a whole-system profiler: Grafana Pyroscope, Parca, Datadog Continuous Profiler, or an internal pprof endpoint. All sample at roughly 1-10% CPU overhead.
2. Deploy the per-language agent behind a flag so it can be disabled fast. Go: `pyroscope.Start(pyroscope.Config{ServerAddress: addr, ApplicationName: "api"})`; Python: `pyroscope.configure(application_name="api")`.
3. Label profiles by the dimensions you investigate with — `service`, `version`, `region`, `endpoint` — but never by user id or trace id, which explode storage.
4. When latency degrades, open the profile for that time window and read the flamegraph; compare against the same service an hour earlier.
5. Read both CPU and wall-clock profiles: a node with high wall time but low CPU is blocked on I/O, a lock, or GC, and a CPU profile alone misses it.
6. Correlate the profile with deploys by overlaying a deploy marker; a flamegraph shape change that begins at a release is a regression, not organic growth.
7. Keep retention long enough to cover a slow-burn leak (days to weeks), and cap sampling so the profiler never appears as a top frame itself.
8. Paste the flamegraph link into the incident thread so the slow window is reproducible after the fact; a profile you cannot reopen is trivia.

## Pitfalls

- Profiling without a baseline: a hotspot at 20% means nothing until compared with the same path a day earlier.
- Retaining profiles for minutes only, so a regression that builds over days is gone before anyone looks.
- Profiling only CPU on an I/O-blocked service and concluding there is no hotspot — the wait is the cost.
- High-cardinality labels (user id, trace id) exploding the profile store.
- Leaving the profiler's HTTP debug endpoint bound to `0.0.0.0` in production — it leaks memory and is a DoS vector.
- Sampling so aggressively it perturbs the latency being measured.
- Reading an aggregate flamegraph over a long window and missing a two-minute spike.
- Trusting a single instance's profile when only one replica carries the bad config.

## Verification

    curl -s "http://pyroscope:4040/render?query=api.cpu%7Bversion%3D%22v3%22%7D&from=now-15m&format=json" | jq '.flamebearer'
    curl -s localhost:6060/debug/pprof/profile?seconds=30 -o cpu.pb.gz   # internal port only
    # pass: per-window profiles resolve; top frame is application code, not the profiler

Report the profiler, its sampling rate and overhead, the window showing the regression, and the named function with its share of wall time.
