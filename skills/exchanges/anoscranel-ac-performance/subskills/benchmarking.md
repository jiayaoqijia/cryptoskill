---
name: benchmarking
domain: software-engineering/benchmarking
trigger: "\"benchmark this\", \"is this version faster\", \"microbenchmark\", \"how do I prove the improvement\"."
anti_trigger: "Load and soak tests against a deployed system (subskills/performance.md); statistical experiment design for A/B (ac-testing)."
scope: "Controlled comparative measurement: isolated microbenchmarks, warmup, and honest reporting of variance."
status: seedling
---

# Benchmarking

## Standard

A benchmark is a comparison, not a number. Its purpose is to say whether one code state is faster than another under a declared load, and everything about the method follows from keeping the comparison honest: the same inputs, the same machine class, enough iterations to see past noise, and variance reported alongside the claim. A single run proves nothing; a difference smaller than the run-to-run spread is not a result.

Microbenchmarks add their own traps. Runtimes optimise different parts of the code the longer they run, so a benchmark needs warmup before it measures steady state. The optimiser may remove the benchmarked computation entirely if its result is never used — the classic dead-code elimination escape. And the loop around the measured work can dominate: always measure the harness's own cost and subtract it from the claim.

## Decision rules

1. State the comparison before running: what change, what expectation, what threshold counts as a win.
2. Warm up before measuring: report steady-state numbers, with the warmup period declared.
3. Consume the benchmark's result: a computation whose output is never read will be optimised away.
4. Run enough iterations for the run-to-run spread to stabilise; report that spread with the claim.
5. Report the environment: machine, load, version — a number without its context is not reusable.
6. Prefer a harness result published as "difference with confidence interval" over "faster by 12%".

## Procedure

1. Define the comparison, the inputs, and the winning threshold.
2. Build the harness with warmup, result consumption, and iteration control.
3. Measure the harness's own overhead on the target platform.
4. Run the baseline and the candidate, alternating to cancel drift.
5. Report the difference with the observed spread, and the environment.
6. If the difference is within spread, the honest result is "no measurable change".

## Anti-patterns

- A "benchmark" of one run, on the developer's laptop, reported to two decimals.
- Publishing a mean without the variance.
- Letting the optimiser delete the measured work by ignoring the result.
- Comparing a warm number for the new version against a cold number for the old.
- Trusting a difference smaller than the harness's own noise.
- An isolated microbenchmark's win that reverses under real call-site data volumes.

## Done checklist

- [ ] Comparison, inputs, and threshold declared before running.
- [ ] Warmup included and stated.
- [ ] Result consumed, preventing elimination.
- [ ] Spread measured and reported with the claim.
- [ ] Environment reported.
- [ ] Result stated honestly within noise or without.

## Sources

- Java microbenchmarking hazards: <https://docs.oracle.com/en/java/javase/21/>
- Statistical assessment of benchmarks: <https://dl.acm.org/doi/10.1145/2725072>
- Measurement methodology: <https://learn.microsoft.com/en-us/visualstudio/>
