---
name: score-tests-with-mutation-testing
description: Use when a green suite might be asserting nothing — run a mutation score to find code the tests execute but never check, then kill the survivors with real assertions.
---

# Score tests with mutation testing

Line coverage counts execution; mutation score counts detection. Break the source on purpose and keep only mutants your tests kill — survivors mark the assertions you never wrote.

## Procedure

1. Pick the language tool: Python `mutmut` or `cosmic-ray`, JS/TS `npx stryker run`, Rust `cargo mutants`, Java `pitest`, Go `go-mutesting`.
2. Scope the run to one module to keep it under ~10 minutes. With mutmut:
```
pip install mutmut
mutmut run --paths-to-mutate=src/billing/ --tests-dir=tests/ --runner="pytest -q"
```
3. Read the score, not just the failures. `mutmut results` prints killed vs survived — survivors are the work list.
4. Inspect a survivor to judge it:
```
mutmut show <mutant-id>
```
A survivor is either (a) untested behavior — write an assertion; or (b) an equivalent mutant that cannot change observable output (e.g. `x * 1` → `x * 2` in dead code) — exclude it with a pragma comment.
5. For each real survivor add the smallest test that pins the behavior, then re-run the module. Target **≥80% mutation score**; below that the module is under-asserted.
6. Commit the added tests and record the delta:
```
git commit -am "kill 7 mutants in billing; score 68% -> 87%"
```
7. Enforce a floor in CI so it cannot regress: wire Stryker's `thresholds: {high: 80, low: 60, break: 60}` in `stryker.conf.json`, or fail the job when `mutmut results` shows survivors above a count.

## Pitfalls

- Chasing 100% means fighting equivalent mutants forever. 80% with every survivor triaged beats 100% with untriaged survivors.
- Mutation testing costs O(mutants × test runtime); scope it to changed modules or a nightly job or CI time explodes.
- A high mutation score over unit-tested code still misses wiring bugs. Pair with at least one end-to-end test.
- `--runner="pytest -x"` stops at the first unrelated failure and can mislabel a mutant as killed. Use the full test command.

## Verification

```
mutmut results | grep -E "Killed|Survived"
```
Passes = mutation score ≥80% and every `Survived` line is paired with a new test or annotated `# equivalent`. Report: "billing mutation score 87% (68→87 after 7 tests), 3 survivors triaged equivalent."
