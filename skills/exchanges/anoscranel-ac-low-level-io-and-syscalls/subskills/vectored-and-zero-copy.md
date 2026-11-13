---
name: vectored-and-zero-copy
domain: software-engineering/vectored-and-zero-copy
trigger: "Avoiding copies through vectored and zero-copy interfaces."
anti_trigger: "Not for protocol framing design, and not for buffer pool management."
scope: "Scatter-gather and the copies an interface can avoid."
status: seedling
---

# Vectored and zero-copy

## Standard

Ordinary writes take one contiguous buffer, so a response assembled from a header, a payload, and a trailer must either be copied into one buffer or written in three calls. A vectored interface takes a list of segments and writes them in one call: the kernel gathers the pieces, the boundary is crossed once, and the copy into a staging buffer never happens.

Zero-copy interfaces go further and eliminate the copy between kernel buffers, moving data from a file to a socket without the payload transiting user memory at all. The trade is ownership: the operation may complete asynchronously with respect to the user buffer, so a zero-copy write can still be reading the buffer when the function returns, and the caller must not modify it until completion. Interfaces that promise zero copy promise fewer copies, not none — every one keeps at least its own record of the transfer.

Primary sources: <https://man7.org/linux/man-pages/man7/epoll.7.html> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Record which hot paths assemble output from multiple segments.
- Replace assembled-then-written buffers with a vectored call where the interface allows it.
- Record the segment count limit of the vectored interface and split when exceeded.
- For zero-copy paths, record the buffer-ownership rule and when modification becomes safe.
- Count copies, not calls, when comparing: a vectored call and a copy both cross once, only one copies.
- Measure with realistic segment mixes, not a single large buffer.

## Procedure

1. Identify hot paths that copy segments into a staging buffer before writing.
2. Replace the copy-and-write with a vectored write.
3. Verify the segment count per call against the interface limit.
4. Where zero-copy applies, implement the ownership discipline for the buffer.
5. Measure copies and boundary crossings before and after.
6. Record the interface choice and both measurements.

## Anti-patterns

- Copying segments into one buffer because the write interface takes one pointer.
- Modifying a zero-copy buffer before completion.
- Exceeding segment limits silently.
- Judging by call count when copy count is the cost.
- Testing vectored paths with a single segment.

## Done checklist

- [ ] Multi-segment hot paths identified.
- [ ] Vectored calls replace copy-and-write.
- [ ] Segment limits respected.
- [ ] Zero-copy ownership implemented.
- [ ] Copies counted before and after.
- [ ] Interface choice recorded.

Segment assembly is also a lifecycle decision: the pieces described to the interface must outlive the call in most implementations, so what looked like a temporary header built on the stack becomes a use-after-return if the interface consumes it later, and the fix is an ownership rule, not a copy.

## Sources

- Scatter-gather I/O context: <https://man7.org/linux/man-pages/man7/epoll.7.html>
- System measurement: <https://www.brendangregg.com/linuxperf.html>
- Memory transfer costs: <https://www.akkadia.org/drepper/cpumemory.pdf>
