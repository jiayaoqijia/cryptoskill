# Reproducibility Protocol

## Claim-to-experiment matrix

| Claim/table/figure | Inputs/parameters | Command/workflow | Raw output | Processing/statistics | Expected tolerance | Status |
|---|---|---|---|---|---|---|

Claims without a row are not artifact-supported.

## Provenance manifest

Record repository/commit, dirty state, dependency locks, OS/container, compiler/runtime, libraries, hardware/microcode, CPU/GPU settings, environment variables (without secrets), dataset/version/hash, parameters, seeds, dates, and time/resource limits.

For estimators/checkers, retain version/commit, exact configuration/command, and raw output.

## Experimental validity

- define hypothesis, unit, workload, sampling, repetitions, warmup, randomization, exclusions, stopping rule;
- report distribution/uncertainty and justified statistical tests/effect sizes;
- preserve negative and failed runs;
- align security level, parameter set, implementation maturity, hardware, threading, batching, setup, and amortization for baselines;
- separate correctness tests, performance benchmarks, security estimates, and side-channel evidence.

## Replay stages

1. access/integrity check;
2. clean build/install;
3. smoke test;
4. one representative claim;
5. full or justified scaled suite;
6. independent post-processing from raw outputs;
7. compare within predeclared tolerance;
8. investigate deviations without moving criteria post hoc.

## Artifact report

State what was actually executed, by whom/environment, success/failure, deviations, and residual limitations. A successful smoke test proves functionality of that path, not reproduction of all results.

