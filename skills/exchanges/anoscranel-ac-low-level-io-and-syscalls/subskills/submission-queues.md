---
name: submission-queues
domain: software-engineering/submission-queues
trigger: "Working with submission and completion queues for dense I/O."
anti_trigger: "Not for message queues between services, and not for event-bus design."
scope: "io_uring-style submission and completion for dense I/O."
status: seedling
---

# Submission queues

## Standard

A submission-queue interface moves the boundary from per-call to per-batch: the program enqueues many operations into a shared ring the kernel consumes, and completions arrive on a completion ring. The syscall count per operation falls toward one per batch, and the model becomes asynchronous — submission and completion are separate events, so latency measurement and error handling are restructured around completion entries rather than return values.

The design trade is complexity for density. The loop must track in-flight operations by identifier, handle completions out of submission order, and decide re-submission policy on failure. For sparse I/O the machinery buys nothing and the extra state is a liability; for dense I/O — thousands of small operations, network or storage — the batch amortization is the difference between a syscall-bound and a capacity-bound program.

Primary sources: <https://man7.org/linux/man-pages/man7/epoll.7.html> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Measure the operation density before adopting a submission model; sparse I/O gains nothing.
- Record the submission batch policy: fixed count, size, or adaptive.
- Track each in-flight operation by its completion identifier, and count them against a limit.
- Handle completions out of order, and never assume submission sequence implies completion sequence.
- Record the failure policy per operation: re-submit, fail the request, or drain.
- Cap in-flight operations so a stalled target cannot exhaust queued work.

## Procedure

1. Measure the current operation density and syscall ratio.
2. Decide the batch policy for submissions.
3. Implement in-flight tracking with an explicit limit.
4. Implement out-of-order completion handling.
5. Define the per-operation failure policy.
6. Measure syscalls per operation and end-to-end time after adoption.

## Anti-patterns

- Adopting a submission model for sparse I/O.
- Assuming completions return in submission order.
- Unbounded in-flight operations against a stalled device.
- Treating a completion error as a queue-wide failure.
- Dropping the in-flight counter, which is correctness, not bookkeeping.

## Done checklist

- [ ] Density measured before adoption.
- [ ] Batch policy recorded.
- [ ] In-flight tracking with a limit.
- [ ] Out-of-order completion handled.
- [ ] Failure policy defined.
- [ ] Syscalls per operation re-measured.

Cancellation is the submission model's least obvious obligation: an operation that is queued but no longer wanted must still be cancelled by identifier, not abandoned, since an abandoned in-flight write against a reused buffer is a correctness failure the completion ring will eventually deliver as a successful write to the wrong data.

## Sources

- Event-driven I/O context: <https://man7.org/linux/man-pages/man7/epoll.7.html>
- System measurement: <https://www.brendangregg.com/linuxperf.html>
- Queue-backed memory interfaces: <https://man7.org/linux/man-pages/man2/mmap.2.html>
