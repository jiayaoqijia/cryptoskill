---
name: dag-dependencies
domain: software-engineering/dag-dependencies
trigger: "Declaring a pipeline's dependency graph honestly."
anti_trigger: "Not for stream topologies, and not for a single job's schedule."
scope: "Declaring the graph, sensors versus polling, and what the DAG must not know."
status: seedling
---

# DAG dependencies

## Standard

A pipeline's dependency graph is its correctness contract: task B runs after task A because B reads A's output. Declared as an explicit graph, the platform can rerun exactly the failed subgraph and skip what succeeded. Buried in script order or sleep-based sequencing, a failure forces either rerunning everything or hand-picking tasks — both of which corrupt data on the second run more often than on the first.

Two dependencies differ in kind: data dependencies (B reads A's output — the platform must order them) and external dependencies (A needs a source to publish today's file — the platform can only wait). Data dependencies belong in the graph; external ones belong in explicit sensors or wait-tasks that poll a stated condition, never in a magic sleep whose duration encodes a guess about the outside world.

Primary sources: <https://airflow.apache.org/docs/> and <https://docs.getdbt.com/docs/build/building-models>.

## Decision rules

- Declare every data dependency explicitly; the graph is the source of truth for ordering.
- Represent external readiness as a sensor with a stated condition and a timeout, never a sleep.
- Keep task bodies ignorant of the graph: a task validates its own inputs, it does not query the scheduler.
- Record the declared graph in the pipeline record; any hand-edit during an incident is an amendment.
- Detect cycles at declaration time, not at run time.
- Prefer few coarse tasks over many tiny ones: task overhead is paid per task, and a graph with a thousand nodes is a graph nobody reads.

## Procedure

1. List the pipeline's transformations and the data each consumes.
2. Draw the dependency edges; mark external readies as sensors.
3. Size tasks so each is a meaningful rerun unit with its own idempotency key.
4. Validate the graph acyclicity and coverage: every consumed dataset has a producing task or a sensor.
5. Record the graph, sensors, and timeouts in the pipeline record.
6. Review on every transformation change; an undeclared edge is a bug found at failure time.

## Anti-patterns

- Ordering by task-list position or sleeps.
- A task that shells out to the scheduler API to check other tasks' state.
- Undeclared dependencies discovered when the output is silently stale.
- Graphs with hundreds of nodes per day; the rerun unit has become the line of code.
- Hand-editing the graph mid-incident and leaving no record.

## Done checklist

- [ ] Every data dependency declared.
- [ ] External readies are sensors with conditions and timeouts.
- [ ] Tasks sized as meaningful rerun units.
- [ ] Graph validated acyclic and complete.
- [ ] Graph recorded and reviewed on change.
- [ ] Incident edits recorded as amendments.

## Sources

- Airflow DAG concepts: <https://airflow.apache.org/docs/>
- dbt model dependencies: <https://docs.getdbt.com/docs/build/building-models>
- PostgreSQL partitioning for pipeline tables: <https://www.postgresql.org/docs/current/ddl-partitioning.html>
