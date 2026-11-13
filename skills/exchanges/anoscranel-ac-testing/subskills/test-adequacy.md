---
name: test-adequacy
domain: software-engineering/test-adequacy
trigger: "\"Are my tests good enough\", \"coverage is high but bugs escape\", \"run mutation testing\", \"add property-based tests\", \"fuzz this parser\"."
anti_trigger: "Setting coverage policy and gates (subskills/test-strategy.md); writing one example test (subskills/writing-tests.md); nondeterministic failures (subskills/flaky-tests.md)."
scope: "Property-based, mutation and fuzz testing to find what coverage misses"
status: "seedling"
---

# Test Adequacy

## Standard

- **Property-based testing**: QuickCheck (Claessen & Hughes, ICFP 2000). State an invariant, generate inputs, shrink failures to a minimal counterexample. Tools: Hypothesis (Python), fast-check (JS), jqwik (JVM), proptest (Rust), FsCheck (.NET).
- **Mutation testing**: DeMillo, Lipton & Sayward (1978). Mutation score = share of seeded mutants killed. Tools: PIT (Java), Stryker (JS/.NET/Scala), mutmut and cosmic-ray (Python). Runs cost 10–100× a normal suite.
- **Fuzzing**: coverage-guided fuzzing via AFL++, libFuzzer, Go native fuzzing (Go 1.18+), cargo-fuzz, ClusterFuzzLite; OSS-Fuzz at scale.
- **Why**: line coverage proves reach, not assertion strength. Mutation score is the more honest signal. One study: a green suite detected 8.7% of mutants. ⚠️ Single study.

## Decision rules

1. Property tests when an invariant generalises: round-trip (`decode(encode(x)) == x`), idempotence, ordering, commutativity, model equivalence, metamorphic relations.
2. Fuzz anything that parses untrusted bytes: file formats, protocols, codecs, deserialisers, CLI argument parsers.
3. Mutation test critical modules and diffs, not the whole repo. Run on the PR diff or nightly.
4. Mutation target on critical code: ⚠️ no standard threshold exists. Set a baseline, then forbid regressions. Investigate every surviving mutant on changed lines.
5. A surviving mutant means one of: missing assertion, missing case, or an equivalent mutant. Mark equivalents; do not chase them.
6. Every shrunk counterexample or fuzz crash becomes a fixed example test in the regular suite.
7. Fuzz time box per run: minutes in CI, hours nightly. ⚠️ House convention.
8. Pin seeds in CI property runs so a failure reproduces; log the seed on failure.

## Procedure

1. Pick the target: the module where escaped defects cluster, or the newest parser.
2. Property test:
   ```python
   from hypothesis import given, strategies as st

   @given(st.lists(st.integers()))
   def test_sort_is_ordered_and_permutation(xs):
       out = my_sort(xs)
       assert all(a <= b for a, b in zip(out, out[1:]))
       assert sorted(xs) == out
   ```
3. Mutation run (scoped):
   ```bash
   mutmut run --paths-to-mutate src/billing/
   mutmut results
   npx stryker run --mutate "src/billing/**/*.ts"
   ```
 For each survivor on changed lines: add or sharpen an assertion, or mark equivalent.
4. Fuzz target (Go example):
   ```go
   func FuzzParse(f *testing.F) {
       f.Add([]byte("a=1"))
       f.Fuzz(func(t *testing.T, b []byte) { _, _ = Parse(b) })
   }
   ```
 Run `go test -fuzz=FuzzParse -fuzztime=60s`. Commit the corpus; keep crashers as regression inputs.
5. Record results: mutation score per module, open survivors, fuzz crashes found and fixed.
6. Wire scoped mutation and short fuzz runs into the nightly pipeline.

## Anti-patterns

- Treating 90% line coverage as proof of quality.
- Whole-repo mutation on every PR; the pipeline stalls and gets disabled.
- Chasing equivalent mutants.
- Properties that restate the implementation.
- Fuzz crashes fixed with no regression input kept.

## Done checklist

- [ ] Target module chosen from defect data.
- [ ] At least one property or fuzz target where invariants or untrusted input exist.
- [ ] Survivors on changed lines killed or marked equivalent.
- [ ] Counterexamples and crashers saved as example tests.
- [ ] Nightly job runs scoped mutation and fuzz.

## Sources

- <https://alastairreid.github.io/RelatedWork/papers/claessen:icfp:2000>
- <https://beefed.ai/en/prioritize-regression-tests-impact-analysis> (T6)
- <https://google.github.io/eng-practices/review/reviewer/looking-for.html>
- https://hypothesis.readthedocs.io · https://go.dev/doc/security/fuzz/
