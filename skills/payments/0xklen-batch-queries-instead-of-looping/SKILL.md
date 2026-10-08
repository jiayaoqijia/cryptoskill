---
name: batch-queries-instead-of-looping
description: Use when a job opens a database or API round trip per item in a loop — replace per-item calls with batched statements or bulk endpoints and measure the round-trip reduction.
---

# Batch queries instead of looping

A loop that issues one statement per row multiplies network latency by the row count. Batching the same work into set-based statements or bulk endpoints cuts wall time by roughly the round-trip factor without changing the result.

## Procedure

1. Count the round trips before changing anything: instrument the loop with a counter and log per-iteration time. At 1ms RTT, 10k rows is 10s of pure latency before any real work.
2. For inserts, use a multi-row `INSERT`, or `COPY` for bulk loads:
```sql
INSERT INTO events (id, ts, kind) VALUES ($1,$2,$3),($4,$5,$6);
COPY events (id, ts, kind) FROM STDIN WITH (FORMAT csv);
```
   `COPY` is an order of magnitude faster than batched `INSERT` for large loads.
3. For reads, use `WHERE id = ANY($1)` / `IN (...)` with a bounded array, chunked at ~1000 (Postgres caps parameters near 65535):
```python
for chunk in chunks(ids, 1000):
    rows = cur.execute("SELECT * FROM t WHERE id = ANY(%s)", (chunk,))
```
4. Chunk to bound statement size and memory; one giant `IN` of 100k ids builds a huge plan and can exceed limits.
5. Wrap a batch in one transaction so it commits once and applies atomically; per-row commits pay an fsync each time.
6. For APIs, use the provider's bulk endpoint (`/batch`, bulk index) and respect its batch-size cap.
7. Benchmark before and after with the same item count and report rows per second, not just wall time.

## Pitfalls

- Chunking so large the statement exceeds the driver's parameter limit and errors only at runtime.
- One transaction over a ten-minute batch holds locks and bloats WAL; commit per chunk for long jobs.
- `executemany` in some drivers still issues one round trip per row unless `execute_batch` or a batch mode is used.
- Bulk endpoints with partial-failure semantics: a whole-batch failure loses the good items unless per-item errors are handled.
- Batching changes idempotency granularity — a retried batch re-applies some rows unless keyed.
- Batching a query that returns `RETURNING` rows out of order, breaking positional assumptions.

## Verification

    time python job.py --rows 10000
    psql -c "SELECT calls FROM pg_stat_statements WHERE query LIKE 'INSERT INTO events%';"
    # pass: round trips ~ ceil(rows/chunk), wall time reduced by the RTT factor

Report rows, chunk size, round-trip count before and after, and wall time for the same input.
