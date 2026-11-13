---
name: mmap-versus-read
domain: software-engineering/mmap-versus-read
trigger: "Deciding between mapping a file and reading it."
anti_trigger: "Not for shared-memory IPC design, and not for swap policy."
scope: "Mapping a file versus reading it, and each one's failure mode."
status: seedling
---

# mmap versus read

## Standard

Reading a file copies bytes from the kernel's cache into the program's buffer. Mapping a file pages its contents into the program's address space on demand: no explicit read call, no copy on access, and page faults become the fetch mechanism. For random access into a large file, mapping avoids reading what is not touched; for a full sequential read, the explicit read amortizes better and avoids fault-per-page overhead.

The failure modes differ in kind. A mapped file's I/O errors arrive as signals at access time, not as return values at call time, so error handling moves from the call site to a handler — a structural change, not a wrapper. A mapped region also holds the mapping open until unmapped, and a large mapping constrains address space; a program that maps many large files can exhaust a resource a reader would never notice.

Primary sources: <https://man7.org/linux/man-pages/man2/mmap.2.html> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Record the access pattern: random sparse, full sequential, or repeated random.
- Reserve mapping for sparse random access where untouched pages are never paid for.
- Prefer read for full sequential passes and for streams where copy cost is minor.
- Record the error-handling path for mapped I/O failures — signal handler, not return code.
- Count live mappings and their total size against address-space limits.
- Record whether mapped pages are locked, since eviction turns faults into stalls.

## Procedure

1. Classify the access pattern over the file.
2. Estimate pages touched versus file size for sparse access.
3. Choose mapping or read and record the reason.
4. Implement the error path appropriate to the choice.
5. Measure with the same residency conditions.
6. Record the choice, the reason, and both measurements.

## Anti-patterns

- Mapping for a full sequential read.
- Treating a mapped file like a buffer with no error-handler plan.
- Keeping large mappings alive beyond their use.
- Comparing a mapped sparse read to an unmapped full read.
- Assuming mapping removes the page cache — it uses it.

## Done checklist

- [ ] Access pattern classified.
- [ ] Choice made with a stated reason.
- [ ] Error path matches the model.
- [ ] Mapping count and size recorded.
- [ ] Residency measurements taken.
- [ ] Decision recorded.

A further consideration is that the two models interact with the page cache differently under write traffic: a write to a mapped page is visible to every other mapper of the file at once, while a written buffer reaches other readers only at flush, so a shared writable file pushes the choice toward read unless coherence-on-write is precisely what is wanted.

## Sources

- mmap semantics and errors: <https://man7.org/linux/man-pages/man2/mmap.2.html>
- Faults and measurement: <https://www.brendangregg.com/linuxperf.html>
- Memory placement context: <https://www.akkadia.org/drepper/cpumemory.pdf>
