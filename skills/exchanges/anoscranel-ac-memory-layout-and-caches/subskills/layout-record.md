---
name: layout-record
domain: software-engineering/layout-record
trigger: "Writing the record of memory-layout decisions and their measurements."
anti_trigger: "Not for performance reports in general, and not for the profiling record."
scope: "The written record: layout decisions and the measurements behind them."
status: seedling
---

# Layout record

## Standard

The layout record states the structure layouts on the hot path, the alignment and padding decisions, the access patterns each was designed for, and the measurements that justified the choices. Its purpose is to let a later reader change a layout without undoing an intentional fix or carrying an accidental one — padding without a record is folklore that survives every refactor.

The record's second function is hardware honesty. Cache behaviour is per-SKU: a padding decision measured on one processor may be neutral or harmful on another, and the record carries the hardware and date of every measurement so a future port knows which decisions to re-verify. A layout tuned on a single-socket machine needs re-measurement on NUMA, and the record is where that dependency is visible.

Primary sources: <https://www.akkadia.org/drepper/cpumemory.pdf> and <https://osf.io/prereg/>.

## Decision rules

- The record lists each hot structure with its field order, offsets, and padding widths.
- Every padding or alignment decision carries the measurement that justified it.
- Every measurement carries the hardware, thread count, and date.
- Access-pattern classifications (stream, stride, irregular) are recorded per hot loop.
- NUMA and huge-page policies are recorded with their measurements.
- The record is append-only; removing padding is a new dated entry, not an edit.

## Procedure

1. List the hot-path structures with their offsets and padding.
2. Attach the before-and-after measurements for each layout change.
3. Record hardware, thread count, and date for each measurement.
4. Record the access-pattern classification per loop.
5. Record NUMA and huge-page policies where they apply.
6. Add a dated entry for every subsequent change.

## Anti-patterns

- Padding with no recorded reason.
- Measurements without hardware and date.
- Deleting padding during a refactor without a record entry.
- Recording end-to-end time without the relevant counter.
- Treating a single-machine result as portable.

## Done checklist

- [ ] Structures with offsets and padding recorded.
- [ ] Measurements attached per change.
- [ ] Hardware, thread count, date recorded.
- [ ] Access patterns recorded.
- [ ] NUMA and huge-page policies recorded.
- [ ] Changes appended with dates.

The record should also carry the rejected options: where a layout change was considered and not made, the reason belongs beside the measurements, because the most expensive repetition is re-deriving an argument that was already won once. A record of what was not changed prevents a future tuning pass from re-opening a question the data already settled.

## Sources

- Layout and hierarchy reference: <https://www.akkadia.org/drepper/cpumemory.pdf>
- Pre-registration practice: <https://osf.io/prereg/>
- Measurement tools: <https://www.brendangregg.com/linuxperf.html>
