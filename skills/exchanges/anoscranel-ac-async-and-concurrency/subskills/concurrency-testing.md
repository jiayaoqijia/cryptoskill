---
name: concurrency-testing
domain: software-engineering/concurrency-testing
trigger: "Making nondeterministic failures reproducible enough to fix."
anti_trigger: "Not for general test strategy, and not for flaky-test triage alone."
scope: "Making races reproducible: stress, interleaving injection, and model checks."
status: seedling
---

# Concurrency testing

## Standard

A race's signature is that the sequence fails only sometimes, so the test design's job is to make "sometimes" happen often and, when it does, to preserve the interleaving that failed. Three techniques do this. Stress tests multiply the schedule lottery: many iterations, many task combinations. Interleaving tests remove the luck by injecting scheduling at chosen yields, forcing the rare schedules deliberately. Model checks catch the logic separately from the schedule by comparing the concurrent structure against a sequential specification.

The infrastructure matters as much as the technique. A race's evidence disappears when the process exits — the interleaving lives nowhere — so the failing test must capture the schedule, whether through seed recording for the scheduler, a log of acquire and release order, or a runtime detector that dumps the holders at the moment of failure. A concurrency test that fails with only a stack trace is a guess; one that fails with the interleaving is a bug report written by the machine.

Primary sources: <https://martinfowler.com/> and <https://dl.acm.org/>.

## Decision rules

- Test the concurrency unit, not only the whole system: pinned task pairs around one shared structure.
- Attempt a seed-reproducible scheduler, and record the schedule, not only the seed value.
- Run stresses at a stated iteration count and under varied CPU load, not only at one load.
- Add deliberate schedule injection at yields near shared invariants.
- Add a runtime race or deadlock detector to the test build, not only to production monitoring.
- Treat "flaky" as a suspect classification: re-run before blaming randomness.

## Procedure

1. Write one test per shared structure, exercising two tasks around each invariant.
2. Add stress runs at a fixed iteration count, and vary the load between runs.
3. Add interleave injection at the yields near the invariant transitions.
4. Wire a detector that dumps state at failure.
5. Record the failing interleaving when one is found, and attach the schedule to the bug.
6. Keep the found schedules as regression tests at the exact interleaving.

## Anti-patterns

- Only whole-system load tests, too coarse to name the racing structure.
- A stress test that fails only under full production hardware, so it never runs.
- Failures triaged as flaky after one passing re-run.
- No recorded schedule, so each investigation starts over.
- Found races fixed without a regression test at the same interleaving.

## Done checklist

- [ ] Per-structure two-task tests.
- [ ] Stress at a stated count and varied load.
- [ ] Interleaving injection added.
- [ ] Failure-state dump wired.
- [ ] Schedule recorded and preserved.
- [ ] Regression tests at the found interleavings.

## Sources

- Testing concurrent code: <https://martinfowler.com/>
- Concurrency verification literature: <https://dl.acm.org/>
- Systems testing references: <https://www.distributed-systems.net/>
