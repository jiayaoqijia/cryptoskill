---
name: bench-protocol
description: Measurement protocol for trustworthy timings. It covers interleaved A/B rounds, medians with IQR and bootstrap CIs, at least 3 repeats, warm-up, no stale builds, an isolated and locked machine, thread pinning, and recorded environment. Use for every performance number, whether FHE, lattice attack, SAT/MILP, MPC/PSI or PQC, before it can enter EVIDENCE.md.
---
# bench-protocol

## Rules

1. **Interleave.** Run the arms in rounds with rotating order (A B, B A, ...). Never run
   all of A and then all of B. Machine state (thermal, turbo, co-tenants, page cache)
   drifts. Absolute times can swing by a factor of two across hours on a shared
   server, so **only ratios from back-to-back pairs in the same session are trusted.**
2. **Repeat.** Use at least 3 measured repeats plus at least 1 discarded warm-up round.
   Use at least 7 when the arms differ by less than 10% or the spread is large. Single
   measurements of the same binary can differ by nearly 2×.
3. **Report the median**, with the IQR and a bootstrap 95% CI. For a ratio, report
   `median(A)/median(B)` with a paired bootstrap CI. Never report the mean of a skewed
   timing distribution as the headline number. Never report the best of N unless the
   protocol states it for both arms.
4. **Lock and isolate.** Hold `crbench`'s file lock so benches never overlap. Run
   benches one at a time with low concurrency: parallel benches compete for memory
   bandwidth and inflate the arm that uses it more. Keep the machine free of other
   heavy jobs. `crbench env` warns on high load and non-`performance` governors.
5. **Control threads.** Set `OMP_NUM_THREADS`, `RAYON_NUM_THREADS`, `GOMAXPROCS` and
   the MKL/OpenBLAS thread variables explicitly (`--threads`). Pin with `taskset`
   (`--cpus`) when comparing single-thread numbers. Report the single-thread comparison
   even when the headline is parallel.
6. **No stale builds.** Build from the pinned commit into a configuration-specific
   directory. Run `crbench stale BIN SRC` before each campaign. Record the build flags.
7. **Record the environment.** `crbench run` stores CPU, governor, load, compilers,
   git commit and dirty flag of `--target`, and the performance environment variables in
   `run.json`. Keep it.
8. **Record failures.** A crash, timeout or missing output stays in the ledger as a
   failed execution with its error. It is excluded from statistics but never deleted.
   If one arm fails systematically, that is a result: document the boundary.
9. **Verify correctness in the timed binary.** The benchmark must check its output
   (decrypt and compare, verify). A fast wrong answer is not a data point.
10. **Explain surprises.** If a wall-clock speed-up exceeds the operation-count ratio,
    find the mechanism before publishing. Examples: evaluation at a lower level with a
    smaller modulus, lower depth, cache effects. Otherwise, suspect the measurement.

## Command

```bash
crbench run \
  -a base='./build-base/bench --set toy' \
  -a new='./build-new/bench --set toy' \
  -n 7 -w 1 --order alternate --parser generic --metric time \
  --threads 1 --cpus 2 --target ./src --log-dir results/2026-01-01-toy-ab
```

Outputs: `results/.../run.json` (all executions, environment, summary),
`results/.../<arm>/rNNN.log` (raw output of each execution), and a JSON summary on
stdout with the speed-up and its CI.

## Choosing the metric

| domain | primary metric | also record |
|---|---|---|
| FHE | latency per operation, or amortised per slot or bit | peak memory (`/usr/bin/time -v`), key sizes, multiplicative depth or level used |
| lattice attacks / estimators | wall time and success rate over seeds | block size β, dimension, memory |
| SAT / MILP | time to solve, median over ≥ 10 seeds or instances | timeouts (count), solver version, CNF/LP hash |
| MPC / PSI | end-to-end time per network profile | bytes sent per party, rounds, offline/online split |
| PQC | median cycles (fixed frequency) | stack and heap usage, key and ciphertext/signature sizes |

## When numbers disagree across sessions

Rerun both arms back to back in one session. If the new pair contradicts an earlier
headline, the **same-session pair wins**. Withdraw the old number explicitly in
EVIDENCE.md (strike it through and add a reason) rather than silently replacing it.
Check whether the cache is really the variable before you blame it: run a cache-isolation
experiment.

## Hand-off

`run.json` and logs are in place, with at least 3 successful repeats per arm. Then
use `skills/log-to-evidence` to create EVIDENCE rows.
