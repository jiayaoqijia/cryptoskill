---
name: concurrent-execution
domain: software-engineering/concurrent-execution
trigger: "Running many suites against stages without interference."
anti_trigger: "Not for application concurrency, and not for CI runner provisioning."
scope: "Parallel suites against shared stages."
status: seedling
---

# Concurrent execution

## Standard

Two suites pointed at the same environment at the same time interfere, and the interference looks like flakiness: a test fails, a rerun passes, and the cause — the other suite's data, its load, its paused service — is invisible in the failing test's own trace. A suite that is deterministic in isolation and flaky under concurrency is not a bad suite; it is a suite sharing a stage with another suite, and the fix is isolation or ordering, not test rewrites.

The options are ordered. Isolation — separate environments or separate data per run — removes the interference class entirely and is the default where it is affordable. Resource partitioning — separate schemas, separate namespaces, separate ports — gives most of isolation on one stage. Ordering — never two suites on one stage at once — is a queue, and it trades interference for wall-clock time, which is its own cost when the queue is the release bottleneck.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Record which suites share a stage and which are isolated per run.
- Partition by schema, namespace, or port wherever a shared stage must serve many suites.
- Make each run's identifier flow through its data, so leftover rows are attributable.
- Record the concurrency policy per stage: isolated, partitioned, or serialised.
- Treat cross-suite flakiness as an environment diagnosis, not a test-quality diagnosis.
- Clean per-run data on teardown, and verify the cleanup with a concurrent-run test.

## Procedure

1. Map suites to the stages they run against.
2. Identify stages serving more than one suite concurrently.
3. Choose isolation, partitioning, or serialisation per shared stage.
4. Add run identifiers to all per-run data.
5. Prove interference is gone by running the previously conflicting suites together.
6. Record the policy per stage and the concurrency test result.

## Anti-patterns

- Retrying flaky tests instead of isolating their runs.
- A shared stage with no partitioning and no queue.
- Unattributable leftover data from failed runs.
- Cleanup that runs only on success, so failures poison the next run.
- Debugging a failing suite without checking what else was on the stage.

## Done checklist

- [ ] Suite-to-stage map recorded.
- [ ] Shared stages identified.
- [ ] Policy chosen per stage.
- [ ] Run identifiers in data.
- [ ] Interference test run and clean.
- [ ] Failure-path cleanup verified.

## Sources

- CI parallelisation practice: <https://martinfowler.com/articles/continuousIntegration.html>
- Shared-stage isolation: <https://martinfowler.com/bliki/DeploymentPipeline.html>
- Container isolation mechanics: <https://docs.docker.com/>
