---
name: baseline-pin
description: Identify the real strongest baseline, fetch it, pin an exact commit, build it with a recorded recipe, verify correctness, and record everything in baselines/MANIFEST.md with a fairness checklist. Use at P4 before any comparison is measured, and again whenever a reviewer or falsifier questions a baseline.
---
# baseline-pin

## 1. Identify the *real* baseline (before fetching anything)

- The paper you are improving on is **not automatically** the baseline. Ask these
  questions:
  - Is its construction a re-derivation of earlier work? Search for the core idea
    under other names.
  - Has a follow-up already improved on it? Check citing papers and ePrint from the
    last 24 months.
  - Is a different library much faster for the same task? For example, an
    implementation in another language or with a different backend.
- The strongest fair comparison beats the most convenient one. Write the decision in
  DECISIONS.md: "baseline = X because ..., rejected Y because ...".
- Record the **best reproducible local number** as the bar to clear. The paper's
  single-thread number may understate what the baseline achieves with trivial,
  standard optimisations such as parallelisation. If a trivial engineering change
  makes the baseline much faster, that faster version is the bar.

## 2. Fetch and pin

```bash
references/baselines/fetch.sh "$PROJECT/baselines" openfhe lattice-estimator
# -> baselines/PINNED.tsv with full SHAs
```

- Pin a **full commit SHA**. A tag or branch name is not enough, because tags can move
  and branches always do.
- Research artifacts often ship as **patches to a library** rather than as a standalone
  program. Pin both: the upstream SHA and the patched fork's SHA or patch hash.
- Never commit third-party source trees into the research repo. Commit only the
  MANIFEST row and the fetch command.

## 3. Build recipe (exact, copy-pasteable)

Record the exact configure and build commands, compiler **and version**, flags,
dependency versions (NTL/GMP, Rust toolchain, Go version), and environment variables
needed at *runtime*.

Runtime linkage is a classic trap. If several versions of a shared library are
installed, the binary may silently load the wrong one. Set `LD_LIBRARY_PATH`
explicitly, then check with `ldd`. Keep one build directory per configuration:
`build-release-native/`, `build-release-portable/`. **Never benchmark from a build
directory whose provenance you cannot state.** Stale builds from an earlier
configuration have produced wrong numbers many times. `crbench stale BIN SRC` flags
sources newer than the binary.

If a configuration misbehaves only at one optimisation level, record which level
was used for each number. An example is a code-generation problem at `-O2` that
disappears at `-O0`, or the reverse.

## 4. Verify before timing

- [ ] The library's own tests pass.
- [ ] End-to-end correctness on your parameter set: decrypt equals expected, the
      signature verifies, the proof verifies, PSI output equals the true intersection.
      Print every slot, not a sample.
- [ ] The **runtime parameters are printed and diffed** against the paper you compare
      with (ring dimension, moduli, gadget base, key distribution, failure probability,
      security level). A library preset named "128-bit" can use different concrete
      values from those in a paper citing it. If the paper's speed-up used different
      parameters from the library default, the denominator changed.
- [ ] Record the failure modes. If a configuration is infeasible, document the
      *boundary* with the exact error message, for example "parameter X too small to
      hold Y", "unsupported ring shape" or "Decrypting with too much noise". Make the
      harness catch the exception and print `FAILED (<reason>)` instead of dumping core.

## 5. MANIFEST row (the project's `baselines/MANIFEST.md`)

```markdown
| name | url | commit (full SHA) | tag | build recipe | compiler + flags | threads | bench command | parser | role | fairness notes |
|---|---|---|---|---|---|---|---|---|---|---|
| toylib | https://example.org/toylib.git | 0123456789abcdef0123456789abcdef01234567 | v1.2.0 | `cmake -B b -DCMAKE_BUILD_TYPE=Release && cmake --build b -j4` | gcc 12.3, -O3 -march=native | 1 | `b/bench --set toy128` | gbench | strongest public implementation of X | preset toy128 has n=..., log q=... (paper Table 3 quotes different n); we use the preset on both arms |
```

Add a "Practical build priority" list: which baseline to reproduce first, and why.

## 6. Fairness checklist (sign off before handing to `experimenter`)

- [ ] Same parameters and the same security estimate (see `skills/param-estimation`).
- [ ] Same threads. Report single-thread as well as parallel.
- [ ] Same compiler, flags and SIMD or accelerator backend.
- [ ] Same machine, same session, interleaved rounds.
- [ ] Same work, with the same phases timed. Offline and online are reported separately.
- [ ] Every cited baseline number has been re-measured locally. Cited and local numbers
      are never mixed in one ratio.
- [ ] The strongest known baseline is included, not only the one the target paper used.
- [ ] Build freshness is verified, and runtime library linkage is verified with `ldd`.

## Hand-off

The row is complete, every checklist box is ticked or has a written exception, and a
single-arm reference run (`crbench run -a base=...`, at least 3 repeats) is logged.
Next agent: `experimenter`.
