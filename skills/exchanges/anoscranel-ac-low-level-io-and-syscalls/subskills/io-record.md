---
name: io-record
domain: software-engineering/io-record
trigger: "Writing the record of I/O model choices and their measurements."
anti_trigger: "Not for the layout record, and not for general performance notes."
scope: "The written record: I/O model choices and their measurements."
status: seedling
---

# I/O record

## Standard

The I/O record states, for each hot path, the I/O model in use — blocking, readiness-driven, or submission-queued — the cache policy, the batching policy, and the measurements that justify each. I/O decisions are the most platform-sensitive choices in this pack: the same program can be syscall-bound on one kernel and copy-bound on another, and the record's function is to make the numbers' provenance visible so a port knows what to re-measure.

Its second function is semantic honesty. Batching, buffering, and zero-copy all change failure semantics — a buffered write that fails later, a zero-copy buffer still owned by the kernel — and a record that captures only the throughput numbers hides the semantic changes that later debugging needs. The record states what each choice promises about ordering, durability, and error delivery.

Primary sources: <https://man7.org/linux/man-pages/man7/epoll.7.html> and <https://osf.io/prereg/>.

## Decision rules

- The record lists each hot path with its I/O model and cache policy.
- Every model choice carries its measurement: syscall counts, copies, end-to-end time.
- Every measurement carries kernel version, hardware, and date.
- Buffering and batching policies are recorded with their flush and failure semantics.
- Zero-copy ownership rules are recorded where they apply.
- Changes are appended with dates, including reversions to simpler models.

## Procedure

1. List the hot paths and their current models.
2. Attach the measurements that justify each model.
3. Record kernel, hardware, and date per measurement.
4. Record buffering policies with their flush and failure semantics.
5. Record zero-copy ownership where used.
6. Append every change with its date and both measurements.

## Anti-patterns

- Recording throughput without syscall and copy counts.
- Measurements without kernel version and hardware.
- Buffering with no recorded flush policy.
- Zero-copy with no recorded ownership rule.
- Deleting an entry when a model is changed back.

## Done checklist

- [ ] Hot paths with models listed.
- [ ] Measurements attached per model.
- [ ] Platform provenance recorded.
- [ ] Flush and failure semantics recorded.
- [ ] Zero-copy ownership recorded.
- [ ] Changes appended with dates.

The record also serves porting in the other direction: an interface adopted because it was fastest on the development kernel may be mediocre after an upgrade, and the platform-anchored measurements let the next person see whether the gap between the current kernel and the recorded one is large enough to re-run the comparison rather than trust it.

## Sources

- I/O interface semantics: <https://man7.org/linux/man-pages/man7/epoll.7.html>
- Pre-registration practice: <https://osf.io/prereg/>
- System measurement: <https://www.brendangregg.com/linuxperf.html>
