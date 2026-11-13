---
name: continuous-profiling
domain: software-engineering/continuous-profiling
trigger: "\"profile production\", \"always-on profiling\", \"where does CPU go in prod\", \"sampling profiler\"."
anti_trigger: "Browser-side profiling (subskills/web-performance.md); flame-graph reading basics (subskills/performance.md)."
scope: "Sampling profilers in production, their overhead, and what the samples can and cannot tell you."
status: seedling
---

# Continuous profiling

## Standard

A one-off profile answers "where is it slow right now"; a continuous profiler answers "where did the CPU go this week", and the second question finds the regressions no benchmark noticed. Sampling profilers make this affordable: they read thread stacks at a fixed rate — hundreds of hertz — and aggregate, so a production profile costs a bounded few percent and no request interference beyond that.

What a sampling profile cannot tell you is just as defined: it shows where time was spent, not why; it misses events between samples; and on optimized code, inline frames can merge (see ac-production-debugging's stack-reading rules). It also cannot tell you about wall-clock blocking — a sampling CPU profile of a thread pool stuck on locks shows nothing, because nothing was executing. For blocking, the tool is a thread dump repeated, not a CPU sample.

## Decision rules

1. Use a sampling profiler for always-on production profiling; bounded overhead, aggregable.
2. Prefer flame-graph aggregation for the weekly view — the width comparison finds regressions.
3. Check the sample rate and the overhead budget before enabling in production.
4. For wall-clock blocking investigations (locks, I/O waits), use blocking profilers or repeated thread dumps — a CPU profile of blocked threads is empty.
5. Keep profiles keyed by build identifier; samples from different builds do not aggregate.
6. Look at diffs week over week, not absolute flame graphs — the diff is the signal.

## Procedure

1. Select a sampling profiler with a documented overhead figure.
2. Set the sample rate and confirm with a canary that latency did not move.
3. Enable on a subset; verify; roll out.
4. Aggregate by build and by service; build the weekly diff view.
5. For each regression in the diff, drill from the frame back to the code.
6. Record the finding and its fix in the performance record.

## Anti-patterns

- Instrumenting a wall-clock problem with a CPU sampling profiler.
- Aggregating samples across builds or code versions.
- Enabling at maximum sample rate in production because the option exists.
- Reading one absolute flame graph without a baseline to compare against.
- Treating an empty CPU profile as evidence of no problem.

## Done checklist

- [ ] Sampling profiler selected with overhead figure.
- [ ] Sample rate set; canary verified no latency shift.
- [ ] Aggregation keyed by build.
- [ ] Weekly diff view exists.
- [ ] Wall-clock problems routed to the blocking-tool path.
- [ ] Findings recorded.

## Sources

- Flame graphs and their reading: <https://www.brendangregg.com/flamegraphs.html>
- Continuous profiling systems: <https://learn.microsoft.com/en-us/azure/>
- CPU sampling methodology: <https://www.kernel.org/doc/html/latest/trace/>
