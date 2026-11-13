---
name: idempotency-and-reruns
domain: software-engineering/idempotency-and-reruns
trigger: "Making pipeline tasks safe to run twice."
anti_trigger: "Not for API idempotency keys, and not for backfill planning."
scope: "Idempotent tasks keyed on input partition; rerun failed tasks only."
status: seedling
---

# Idempotency and reruns

## Standard

A pipeline task is idempotent when running it twice over the same input partition produces the same result as running it once — no duplicated rows, no double-incremented metrics, no partially written outputs visible mid-run. The key is the input partition: a task that declares "process date D for source S" and writes by replacing that partition's output atomically can be rerun freely; a task that declares "process whatever is new" cannot be rerun at all without duplicating.

Write atomicity is the second half. The consumer of a pipeline stage must never observe a half-written partition: the pattern is write-to-temp then swap, or insert-then-commit within a single transaction. A task can be idempotent in intent and still corrupt data if its output is visible while being written.

Primary sources: <https://docs.getdbt.com/> and <https://airflow.apache.org/docs/>.

## Decision rules

- Give every task an explicit idempotency key: usually (source, input partition).
- Make each task replace-or-upsert by that key so a rerun is a no-op or a repair.
- Write outputs atomically: temp-then-swap or single-transaction inserts.
- Rerun granularity equals task granularity: rerunning a whole day because one task failed is a design smell.
- Test idempotency deliberately: run twice in a row in a test environment and diff the outputs.
- Treat "we always clear the output first" as a stopgap, not a design: clearing makes the window of empty output visible to consumers.

## Procedure

1. For each task, state the idempotency key out loud before writing code.
2. Choose the write pattern: partition-replace for full recompute, keyed upsert for incremental.
3. Implement the write atomically (temp+swap or transaction).
4. Add a rerun-double test to the pipeline's test suite.
5. On failure, rerun only failed tasks of the failed partition; the platform tracks the rest.
6. Record the key and write pattern per task in the pipeline record.

## Anti-patterns

- "Append on each run" tasks that duplicate on every rerun.
- Rerunning an entire date range to fix one stage because rerun granularity is coarse.
- Consumers reading a partition mid-write.
- Idempotency assumed but never tested by a double run.
- Hanging state in external systems (cache, search index) that the rerun does not clear.

## Done checklist

- [ ] Idempotency key stated per task.
- [ ] Replace-or-upsert chosen per task.
- [ ] Atomic write implemented and verified.
- [ ] Double-run test passes.
- [ ] Failed-only rerun used in practice once.
- [ ] Keys and patterns recorded.

## Sources

- dbt incremental and full-refresh models: <https://docs.getdbt.com/>
- Airflow task rerun semantics: <https://airflow.apache.org/docs/>
- Delta Lake ACID table format: <https://delta.io/>
