---
name: backfill-ordering
domain: software-engineering/backfill-ordering
trigger: "Copying existing data so the copy finishes before the switch."
anti_trigger: "Not for research-data backfills, and not for schema backfills inside one store."
scope: "Copying the old data so the backfill finishes ahead of the switch."
status: seedling
---

# Backfill ordering

## Standard

In any cutover that avoids an outage, the old data must be copied to the new store while writes continue, and the copy must converge rather than merely progress. Copy oldest data first — it is the least likely to change again — and track the lag between the copy's position and the live write frontier. The backfill is finished not when it has read the last row but when its lag reaches zero and holds, which for a busy store means incremental passes, each shorter than the last.

Three mechanics decide whether convergence is reachable. Idempotent copy operations, so a failed pass can be resumed from checkpoints rather than restarted. Version-aware writes, so the copy cannot overwrite a row that dual writes have already made newer — the classic dual-write corruption is the backfill stamping yesterday's value over today's. A progress metric defined as lag against the live frontier, so "60 percent copied" is meaningless but "forty minutes behind the frontier, shrinking" is a cutover estimate.

Primary sources: <https://www.postgresql.org/> and <https://martinfowler.com/>.

## Decision rules

- Record the copy order and the reason, oldest-first by default.
- Record the idempotency mechanism per row and the checkpoint interval.
- Record the version or timestamp rule that prevents stale overwrite of fresher writes.
- Record lag against the live write frontier per pass.
- Record the convergence criterion: lag zero, held for a stated interval.
- Never overwrite a newer row with an older read.

## Procedure

1. Size the data and the write rate.
2. Choose the copy order and checkpointing.
3. Add version or timestamp comparisons to the copy's write side.
4. Run passes and measure lag per pass.
5. Continue until lag reaches zero and holds.
6. Record total duration and the last pass length.

## Anti-patterns

- A single full pass with no resume, restarted from zero on any failure.
- Copying newest first, chasing rows that keep changing.
- A progress percentage with no lag measurement.
- Stale overwrite of dual-written rows because the copy ignored versions.
- Declaring the backfill done at "last row read" while lag is still hours.

## Done checklist

- [ ] Copy order and reason recorded.
- [ ] Idempotency and checkpoints recorded.
- [ ] Version-aware writes in place.
- [ ] Lag measured per pass.
- [ ] Convergence criterion met and held.
- [ ] Duration recorded.

## Sources

- Bulk copy mechanics: <https://www.postgresql.org/docs/>
- Migration patterns: <https://martinfowler.com/>
- Data engineering references: <https://www.distributed-systems.net/>
