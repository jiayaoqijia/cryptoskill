---
name: readiness-and-event-loops
domain: software-engineering/readiness-and-event-loops
trigger: "Designing around readiness notification rather than blocking calls."
anti_trigger: "Not for async runtime design at the language level, and not for connection pooling."
scope: "epoll, edge versus level triggering, and the thundering herd."
status: seedling
---

# Readiness and event loops

## Standard

A blocking read waits; a readiness interface asks the kernel which descriptors are ready and returns the ready set. The event loop built on the second model handles many connections in one thread: it asks once for all descriptors, serves the ready ones, and sleeps when nothing is ready, paying no thread-per-connection cost. The kernel interface is scalable precisely because the question is batched — one readiness call replaces one poll per descriptor.

The trigger mode is the decision that shapes correctness. Level-triggered readiness repeats the notification while the condition holds, so a partially drained socket is reported again; edge-triggered readiness reports the transition only, so the reader must drain until the socket would block or events are lost. Edge triggering is cheaper under high load and demands drain-to-completion discipline; level triggering forgives partial reads and pays repeated wakeups. Neither is a performance claim in itself — the choice decides what the loop must promise.

Primary sources: <https://man7.org/linux/man-pages/man7/epoll.7.html> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Record the trigger mode and the drain obligation it creates.
- Under edge triggering, drain each ready descriptor until the would-block error.
- Register descriptors once where the interface allows, not per event.
- Distribute wakeups for shared listening sockets, or accept the herd cost knowingly.
- Record the event budget per loop iteration and the overflow policy.
- Measure wakeup counts, not only loop iterations, when evaluating a loop change.

## Procedure

1. Choose the trigger mode and write the drain rule that follows from it.
2. Implement registration appropriate to the mode.
3. Define the per-iteration event budget and overflow behaviour.
4. Decide the shared-listener wakeup policy.
5. Measure wakeups and served events per iteration.
6. Record the mode, the drain rule, and the measurements.

## Anti-patterns

- Mixing trigger modes without recording which applies where.
- Edge-triggered reads that stop before the would-block error.
- Re-registering descriptors every loop.
- One readiness call per descriptor, rebuilding the poll the interface exists to avoid.
- Unbounded event batches that starve other work.

## Done checklist

- [ ] Trigger mode recorded.
- [ ] Drain rule implemented to match.
- [ ] Registration strategy recorded.
- [ ] Event budget defined.
- [ ] Wakeup policy decided.
- [ ] Measurements taken and recorded.

The loop's own fairness is also a readiness decision: a batch of ready events processed to exhaustion can starve the timer queue behind it, so the iteration budget is not an optimization constant but a scheduling statement about which latency the loop honors first.

## Sources

- epoll semantics and modes: <https://man7.org/linux/man-pages/man7/epoll.7.html>
- Event-loop system measurement: <https://www.brendangregg.com/linuxperf.html>
- Submission-queue interfaces: <https://man7.org/linux/man-pages/man2/mmap.2.html>
