---
name: ac-performance
description: "Making software fast, server and browser: measure-first performance budgets, percentile targets and tail latency, profiling, flame graphs and continuous profiling in production, memory profiling and heap snapshot diffs, controlled benchmarking with warmup and variance, latency budget allocation across the call chain, load and soak tests, N+1 and caching fixes, plus Core Web Vitals — LCP, INP, CLS — bundle cost and field versus lab data. Use when asking \"this is slow\", \"profile this\", \"p99 latency is too high\", \"set a performance budget\", \"memory leak\", \"heap snapshot diff\", \"benchmark this\", \"latency budget\", \"load test this API\", \"improve LCP\", \"fix layout shift\", \"pass Core Web Vitals\", \"the bundle is too big\". Not for SLO definition and alerting (ac-reliability), not for resource exhaustion diagnosis and OOM kills (ac-resource-exhaustion-diagnosis), not for failure injection and capacity headroom (ac-chaos-and-capacity-testing)."
license: MIT
metadata:
  domain: software-engineering
---

# Performance

## Overview

Seven leaves make software fast. Two are the original halves: the server side — written budgets, measurement before change, profiling, load and soak tests, fix order from algorithm to cache — and the browser side — Core Web Vitals targets, bundle and render cost, the field-versus-lab evidence split. Five deepen the measurement craft: the tail of the latency distribution and what creates it; continuous sampling profiles in production and the diffs that find regressions; memory profiling, where allocation profiles find churn and heap snapshot diffs find leaks; controlled benchmarking with warmup, result consumption, and variance reported; and latency budget allocation, which divides a user-facing budget across the call chain so each layer owns its share.

## When to use

- Slowness suspects: setting a budget, reproducing with realistic data, profiling.
- Hot spots: widest stacks, slow queries, N+1 loops, caching with invalidation.
- Load, stress, spike and soak tests; CI thresholds that fail the build.
- Tail work: p99 attribution, queueing at high utilisation, variance sources landing on a few requests.
- Production profiling: always-on sampling, weekly flame-graph diffs, blocking investigations.
- Memory: allocation profiles for churn, snapshot diffs for leaks.
- Benchmarks: isolated comparative measurement, warmup, spread reported with the claim.
- Budget allocation: dividing a user-facing latency budget across layers.
- Web vitals work: LCP, INP, CLS, bundle splitting, third-party script cost.

## When not to use

- Setting SLOs, error budgets or alert rules — outside this skill.
- Adding telemetry so the system can be measured — outside this skill.
- Component structure and state placement — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/performance.md` | Measure-first server speed work | "this is slow" |
| `subskills/web-performance.md` | Core Web Vitals and bundle cost | "improve LCP" |
| `subskills/tail-latency.md` | The p99 and what creates it | "p99 is high" |
| `subskills/continuous-profiling.md` | Always-on sampling and weekly diffs | "profile production" |
| `subskills/memory-profiling.md` | Allocation profiles and heap snapshot diffs | "memory leak" |
| `subskills/benchmarking.md` | Controlled comparative measurement | "benchmark this" |
| `subskills/latency-budget-allocation.md` | Dividing the budget across layers | "budget the call chain" |

## See also

- `subskills/performance.md` — measure, then move the needle.
- `subskills/web-performance.md` — the p75 the user actually feels.
- `subskills/tail-latency.md` — the average lies; the tail is where users live.
- `subskills/continuous-profiling.md` — where the CPU went this week.
- `subskills/memory-profiling.md` — churn versus growth, profile versus snapshot diff.
- `subskills/benchmarking.md` — a benchmark is a comparison, not a number.
- `subskills/latency-budget-allocation.md` — every millisecond has an owner.
