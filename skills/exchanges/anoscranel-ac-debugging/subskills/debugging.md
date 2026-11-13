---
name: debugging
domain: software-engineering/debugging
trigger: "\"Why does this fail\", \"fix this bug\", \"it crashes when\", \"this returns the wrong value\", \"race condition\", \"deadlock\", \"the agent's fix broke something else\"."
anti_trigger: "Finding the defect class or introducing commit behind a fixed bug (subskills/root-cause.md); red CI from config or infra (subskills/build-failures.md); nondeterministic tests; slowness."
scope: "Reproduce, minimise, hypothesise, test: the scientific debugging loop incl. concurrency bugs"
status: "seedling"
---

# Debugging

## Standard

- **Scientific debugging** (Zeller, *Why Programs Fail*): observe → hypothesise → predict → experiment → conclude, repeated. Four reasoning modes: deduction, observation, induction, experimentation.
- **Loop**: reproduce → minimise → hypothesise → instrument → fix → regression test.
- **Vocabulary**: IEEE 1044 separates failure (observed wrong behaviour), fault or defect (the code flaw) and problem (the report) (https://standards.ieee.org/ieee/1044/1526).
- **Sanitizers**: ASan (memory errors), TSan (data races), UBSan (undefined behaviour), MSan (uninitialised reads). ⚠️ Slowdown figures are single-source; measure per workload.
- **Agent fixes**: about 7.8% of patches that pass a tool's own checks fail the full developer suite; 29.6% diverge from the human fix (arXiv 2503.15223).

## Decision rules

1. No fix before a reliable reproduction. Pin time, randomness, locale, data and versions until it fails every time.
2. Minimise the case: smallest input, fewest steps, least code.
3. Write the hypothesis down as "X fails because Y", plus the observation that would disprove it.
4. One variable per experiment. Predict the result before you run it.
5. Observe first, change second. Logs, debugger, watchpoints and prints are all fine.
6. Concurrency suspects (timing-dependent, load-dependent, vanishes under a debugger): run under TSan or the language race detector; add ordering logs with thread IDs and timestamps; check lock order for deadlocks.
7. The fix lands with a test that fails before and passes after. Run the full suite, not only that test.
8. Never "fix" by deleting, skipping or loosening the failing test.
9. Two failed fix attempts in a row → stop patching. Re-read the evidence; your model of the bug is wrong.
10. An agent's "the cause is X" is a hypothesis. A human confirms the cause before the fix merges.

## Procedure

1. Write the bug: expected, actual, steps, environment, first-seen version.
2. Reproduce it, ideally as a failing automated test.
3. Minimise: halve input and steps until removing anything makes it pass.
4. Localise: binary-search the code path with logs or breakpoints; check inputs and outputs at each boundary.
5. For memory or undefined-behaviour symptoms:
   ```bash
   cc -fsanitize=address,undefined -g -O1 app.c && ./a.out
   go test -race ./...
   ```
6. State the hypothesis and run the experiment that could refute it.
7. Confirmed → write the smallest fix at the right layer.
8. Run the new test (now green) and the full suite.
9. Record in the bug log: reproduction, cause, fix, the test level that missed it.
10. Same mistake likely elsewhere → find the class next (subskills/root-cause.md).

## Anti-patterns

- Shotgun debugging: random changes until it passes.
- Fixing the symptom where it shows, not where it starts.
- Retries or catches that hide the failure.
- Trusting an agent's fix without the full suite.

## Done checklist

- [ ] Reliable, minimal reproduction exists.
- [ ] Cause written and confirmed by an experiment.
- [ ] Fix ships with a fails-before, passes-after test.
- [ ] Full suite green.
- [ ] Bug log entry written.

## Sources

- <https://courses.cs.duke.edu/compsci308/spring26/readings/Zeller_Scientific_Debugging.pdf>
- <https://github.com/byerlikaya/claude-starter-kit/blob/main/plugin/skills/systematic-debugging/SKILL.md>
- https://standards.ieee.org/ieee/1044/1526 · https://arxiv.org/abs/2503.15223
