---
maturity: experimental
name: extension-profiling
description: Compare browser extension performance between branches using WDYR, React DevTools Profiler, and E2E benchmarks with statistical rigor.
---

# Browser Extension Profiling

Methodology for profiling and comparing extension performance across branches or commits.

## When To Use

- Validating that a refactor reduces unnecessary re-renders (needs before/after comparison)
- Establishing baseline metrics for a performance initiative
- Investigating a reported UI slowdown in the extension

## Do Not Use When

- Single-run comparisons — statistical significance requires ≥10 runs per scenario
- The change touches only non-render paths (background scripts, network with no UI impact)
- Target behavior is server-side latency, not UI rendering

## Workflow

1. **Build both branches** on the same machine and Chrome version: `yarn build:test` for the E2E benchmarks, and a development build (`yarn start` or `yarn build:test:dev`) for the React DevTools Profiler. For a PR, build the PR's merge-base as the baseline, not main's tip. The merge-base is the build the PR actually changed.

2. **WDYR profiling** (unnecessary re-render counts)
   ```bash
   ENABLE_WHY_DID_YOU_RENDER=true yarn start
   ```
   Flags to watch:
   - `different objects that are equal by value` → object recreation
   - `different functions with the same name` → callback recreation
   - `props object itself changed but values equal` → parent cascade

3. **React DevTools Profiler** for flame graphs and commit timings, on a development build. `yarn build:test` passes `--mode production`, which sets `NODE_ENV=production`, and React's production build records no profiling data.
   ```bash
   yarn devtools:react
   ```

4. **E2E benchmarks** for scenario durations
   ```bash
   yarn test:e2e:benchmark
   ```

5. **Collect ≥10 runs** per scenario. Discard top/bottom 10%. Report mean, median, stddev, p75, p95.

6. **Effect size:** report the difference in the metric's own units alongside Cohen's d. Cohen's d is the difference divided by the benchmark's own spread, so the difference worth acting on comes from product impact, fixed before the runs.

## Common Pitfalls

| Mistake | Correct Approach |
|---------|-----------------|
| Running branches on different machines or Chrome versions | Same machine, same Chrome, no other apps running |
| Pooling all runs including noisy late-session ones | Fix the primary analysis, and any rule for dropping a round, before the runs. Report per-round stats as sensitivity, with explicit round attribution |
| Reporting absolute re-render counts without scenario context | Normalize per-action; cascade fixes show multiplied impact at root |
| Skipping cache and state reset between runs | Clear browser cache, reset extension state for each run |

## Pre-Profiling Checklist

- [ ] Both branches built with `yarn build:test` (benchmarks) and a development build (React DevTools Profiler)
- [ ] Same machine, same Chrome version
- [ ] No other tabs or applications running
- [ ] WDYR enabled: `ENABLE_WHY_DID_YOU_RENDER=true`
- [ ] Cache and extension state cleared between runs
- [ ] Wallet state sized for the scenario: `yarn start:with-state` runs `yarn start` with a generated fixture wallet (30 accounts by default). A null on an empty wallet is a fact about the fixture, not the code
