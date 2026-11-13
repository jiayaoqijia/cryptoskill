---
name: false-sharing-and-padding
domain: software-engineering/false-sharing-and-padding
trigger: "Diagnosing and fixing false sharing between threads."
anti_trigger: "Not for lock contention, and not for network-level sharing."
scope: "Two threads, one cache line, and the padding that separates them."
status: seedling
---

# False sharing and padding

## Standard

False sharing is contention without logical sharing: two threads write different variables, but the variables sit in the same cache line, so the coherence protocol treats every write as a conflict. The program is correct — no race exists — but it scales backwards, and the effect worsens as more threads are added because each contributes its own invalidations.

The diagnosis is the signature: performance degrades with thread count while profiling shows no lock contention, and per-core counters show heavy coherence traffic on the affected lines. The fix is padding or a layout change that moves each thread's written field onto its own line, and the honest fix is applied only after the counters confirm the diagnosis, because padding costs memory and readability.

Primary sources: <https://www.akkadia.org/drepper/cpumemory.pdf> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Confirm the signature before padding: per-thread slowdown with no lock contention.
- Verify that the two fields are genuinely distinct, not logically shared through a hidden path.
- Record the observed line size and the padding width applied to reach separation.
- Prefer an array-of-structs to struct-of-arrays restructuring over manual padding where a per-slot layout naturally separates.
- Record how many threads the fix was measured at, since the degradation is thread-count dependent.
- Remove padding deliberately if the layout changes; never carry it as folklore.

## Procedure

1. Reproduce the slowdown and record the thread count.
2. Profile for lock contention and rule it out.
3. Measure per-core coherence traffic on the affected structure.
4. Identify the fields sharing a line.
5. Separate them with padding or a layout change.
6. Re-measure scaling across the same thread counts.

## Anti-patterns

- Padding every structure speculatively.
- Treating a slowdown under threads as a lock problem without measuring.
- Fixing true logical sharing with padding.
- Hard-coding a line size from a previous machine.
- Omitting the thread count from the measurement record.

## Done checklist

- [ ] Signature reproduced and thread count recorded.
- [ ] Lock contention ruled out.
- [ ] Coherence traffic measured.
- [ ] Fields identified and separated.
- [ ] Scaling re-measured.
- [ ] Padding width and rationale recorded.

A related trap is the reverse pattern: fields that look independent because they are separate variables can still land adjacently in the binary, since a compiler may place unrelated objects in the same line when they are declared together in one scope. The diagnosis therefore starts from the addresses, not from the source layout, and a placement that was safe under one compiler's ordering can become contended after an unrelated change to the same file.

## Sources

- Coherence theory and practice: <https://www.akkadia.org/drepper/cpumemory.pdf>
- Linux profiling tools: <https://www.brendangregg.com/linuxperf.html>
- Syscall reference for memory placement: <https://man7.org/linux/man-pages/man2/mmap.2.html>
