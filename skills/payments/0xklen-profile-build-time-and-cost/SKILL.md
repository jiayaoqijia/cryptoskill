---
name: profile-build-time-and-cost
description: Use when a build or CI pipeline is slow or expensive. Measures wall time per stage, finds the dominant cost, and quantifies savings from a change.
---

# Profile Build Time and Cost

"Slow" is a symptom; the cost is usually one stage and one resource class. Measure per-stage wall time and billed minutes before optimising, or you will shrink the part that was never the bottleneck.

## Procedure

1. Get a per-stage wall clock. Wrap each step:
   `/usr/bin/time -v ./build.sh` for max RSS and elapsed; `hyperfine './build.sh'` for repeated runs with a median.
2. For a compiled build, ask the build system for its own timings:
   `ninja -d stats` (per-edge), `cargo build --timings` (HTML flamegraph in `target/cargo-timings/`), `bazel build --profile=profile.json` then `bazel analyze-profile profile.json`.
3. Attribute CI cost: list the last 30 runs' durations and multiply by the runner's per-minute price. `gh run list --limit 30 --json databaseId,createdAt,updatedAt,conclusion`.
4. Rank stages by `duration × price-per-minute`. A 20-minute job on a 4-vCPU runner can cost more than a 5-minute job on 16 vCPU.
5. Attack the top stage first. Common wins: cache the dependency layer, shard a test suite (`--shard=1/4`), skip unaffected targets in a monorepo, or move a job off the critical path to run in parallel.
6. Quantify before/after with the same measurement — a change is only real if the median over 5 runs drops.
7. Check whether a bigger runner is cheaper than a faster build: 16-vCPU at 4× price but 3× faster is a net loss; 32-vCPU at 8× price and 6× faster is a win.

## Pitfalls

- Optimising a stage that runs once per day while a 3-minute stage runs on every push.
- Cold-cache timings masquerading as the steady state; measure the warm path that actually dominates CI.
- Parallelism that saturates I/O just moves the wait; verify with `iostat` or the build system's own utilisation report.
- Comparing a cached run to an uncached baseline and calling the difference a speedup.
- Ignoring queue time: a job that waits 4 minutes for a self-hosted runner is slower than a hosted one that starts instantly.
- Measuring on a laptop with a warm compiler cache and comparing to a cold CI runner compares two different systems, not two versions.

## Verification

    hyperfine --warmup 1 --runs 5 './build.sh' \
      && /usr/bin/time -v ./build.sh 2>&1 | grep -E 'Elapsed|Maximum resident'

Record the median elapsed and peak RSS; repeat on the branch with the fix and compare. For CI cost, recompute billed minutes over the same 30-run window.

Report: "Stage <X> is 62% of wall time (<before>→<after> after caching); billed CI minutes for 30 runs fell from <A> to <B> at $<rate>/min."
