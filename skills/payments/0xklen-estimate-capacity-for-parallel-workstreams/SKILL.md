---
name: estimate-capacity-for-parallel-workstreams
description: Use when several projects share the same people and each has a confident solo estimate. Accounts for context-switch loss and contention so the parallel plan is not the sum of optimistic solo plans.
---

# Estimate capacity for parallel workstreams

Three projects each "estimated at 50%" do not each get a third of a person and finish on time. Switching costs and partial attention mean parallel work converges slower than serial, and the losses compound with each added stream.

## Procedure

1. Start from real capacity: people × working days × focus factor, in person-days.

       python3 -c "people=3; days=20; focus=0.7; print('capacity', people*days*focus)"
       capacity 42.0

2. Apply a coordination penalty for the number of concurrent streams. Every extra concurrent project a person touches costs roughly 10–20% of their throughput. Model it:

       python3 -c "base=42; streams=3; loss=0.15; print('effective', round(base*(1-loss*(streams-1)),1))"
       effective 29.4

3. Cap concurrency in `notes/capacity.md`. A person on three projects produces less than a person on two; the asymptote is real. Prefer two streams per person, one if the work is deep.
4. Sum each stream's requirement and compare to effective capacity. If the total exceeds it, something is over-committed — name which stream is starved rather than spreading thin.
5. Watch for shared scarce resources (the one person who knows the schema, a single test environment). Contention on these serializes work that looked parallel.
6. Re-derive after any stream is added or dropped; capacity is per-configuration, not fixed.

## Pitfalls

- Adding streams without reducing per-stream expectations, so everyone is nominally 33% and effectively less.
- Ignoring the shared-resource bottleneck (reviewer, DBA, signing key) that serializes the "parallel" work.
- Assuming a person's two projects each get 50% when in reality each gets the leftover after switching.
- Counting person-days as interchangeable; a day from someone unfamiliar with the stream is worth less.
- Planning near 100% allocation with no reserve, so any interruption starves every stream at once.

## Verification

    python3 -c "print(round(42*(1-0.15*2),1))"
    # 29.4 — effective capacity is well under 42 once 3 streams contend; compare totals against this

Report total capacity, the concurrency penalty applied, effective capacity, and which streams fit within it.
