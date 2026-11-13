---
name: blocking-and-nonblocking
domain: software-engineering/blocking-and-nonblocking
trigger: "Choosing blocking versus non-blocking semantics for a socket or file."
anti_trigger: "Not for async runtime architecture, and not for circuit-breaker policy."
scope: "What blocking promises, and what non-blocking requires in exchange."
status: seedling
---

# Blocking and non-blocking

## Standard

A blocking operation promises completion or failure before returning: the thread waits, and when the call returns the work is done or the error is real. A non-blocking operation promises immediate return with a third outcome — not ready — and the program must decide what to do about it: retry, queue, or abandon. The choice is a promise about control flow, not a performance knob, and each model's failure modes are the other's normal operation.

The consequence is where complexity lives. A blocking program's failure mode is a stuck thread, and its diagnosis is a stack trace; a non-blocking program's normal path includes not-ready, and every not-ready must be handled explicitly or the operation is silently dropped. Partial writes are the classic trap: a blocking write can still write partially, and a non-blocking one returns short routinely, so a loop that assumes all-or-nothing is wrong in both models for different reasons.

Primary sources: <https://man7.org/linux/man-pages/man7/epoll.7.html> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Record, per hot path, whether the file or socket is blocking or non-blocking.
- Under non-blocking, handle not-ready explicitly on every operation; it is a normal outcome.
- Handle partial writes in both models with a continuation that resumes from the written count.
- Record the not-ready policy: retry immediately, defer to the event loop, or shed load.
- Never mix blocking calls into a non-blocking event loop thread.
- Record what unblocks a stuck blocking thread — timeout, close, or signal — for each path.

## Procedure

1. Classify each hot descriptor's mode.
2. Write the not-ready handling for every non-blocking operation.
3. Implement partial-write continuation with a byte-count state.
4. Verify no blocking call runs on an event-loop thread.
5. Record the not-ready policy and the unblock mechanism.
6. Test with a stalled peer for both models' behaviour.

## Anti-patterns

- Treating a short write as an error in either mode.
- Assuming non-blocking makes a call faster; it changes who waits.
- A blocking call on an event loop thread.
- Not-ready handled as an exception rather than an outcome.
- No timeout on a blocking path that can stall indefinitely.

## Done checklist

- [ ] Mode recorded per hot descriptor.
- [ ] Not-ready handled explicitly.
- [ ] Partial-write continuation implemented.
- [ ] Event-loop threads audited for blocking calls.
- [ ] Not-ready policy recorded.
- [ ] Stall behaviour tested.

The trap also runs in the opposite direction when a blocking write is accepted only partially, since the next byte count must resume from the part which succeeded and not from the beginning, and a code path which retries the whole buffer duplicates bytes in both models.

## Sources

- Non-blocking readiness context: <https://man7.org/linux/man-pages/man7/epoll.7.html>
- System diagnosis: <https://www.brendangregg.com/linuxperf.html>
- Event loop integration: <https://www.kernel.org/doc/html/latest/admin-guide/index.html>
