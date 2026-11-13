---
name: thread-pool-saturation
domain: software-engineering/thread-pool-saturation
trigger: "Diagnosing a thread pool where every worker is busy and requests queue forever."
anti_trigger: "Not for choosing pool sizes in advance (that is limits-from-evidence)."
scope: "When all threads are busy, what queued requests experience, and what blocks them."
status: seedling
---

# Thread pool saturation

## Standard

A thread pool has a queue discipline and a bounded size, and saturation is the state where every worker is occupied and newcomers wait. What the caller experiences depends on the queue: unbounded queues grow silently until memory fails, bounded queues reject visibly, and no-queue configurations fail fast in a way callers must be built to expect. The observable "thread pool exhausted" is therefore a description of the queue's policy as much as the load.

The diagnostic question is what the threads are doing, and the only honest answer comes from repeated thread dumps. A saturated pool whose stacks are all in one blocking call has a downstream problem — the pool is the symptom. A pool whose threads are all executing useful work at full speed has a capacity problem. A pool with threads waiting on each other has a deadlock or a fan-in design error that more threads will not fix.

## Decision rules

- Capture the pool's queue depth and rejection policy as configured, not as documented.
- Take at least three thread dumps seconds apart; a single snapshot cannot show movement.
- Group stack traces by top application frame; a single dominant frame points downstream.
- Distinguish blocked on lock, blocked on I/O, and running — each means a different fix.
- Record the rejection path's behaviour as the caller experiences it.
- Check the queue bound: saturating an unbounded queue surfaces as memory, not pool errors.

## Procedure

1. Record pool size, queue bound, and rejection policy.
2. Sample queue depth over a load period.
3. Capture three or more full thread dumps.
4. Group stacks by state and by top frame.
5. Classify: downstream blockage, genuine capacity, or intra-pool contention.
6. Record the verdict tied to the stack evidence.

## Anti-patterns

- Increasing the pool size before reading the stacks.
- Treating an unbounded queue's silence as health.
- Averaging the dumps instead of grouping them; the modes matter more.
- Blaming the pool for a downstream outage it absorbed.
- Rejection policy changed without telling the callers.

## Done checklist

- [ ] Pool configuration recorded.
- [ ] Queue depth sampled.
- [ ] Three-plus dumps captured.
- [ ] Stacks grouped by state and frame.
- [ ] Verdict classified from the groups.
- [ ] Caller-visible rejection behaviour recorded.

## Sources

- JVM thread dump analysis: <https://docs.oracle.com/en/java/javase/21/troubleshoot/>
- Thread synchronization and states: <https://docs.microsoft.com/en-us/dotnet/standard/threading/>
- Executor queue policies: <https://docs.oracle.com/en/java/javase/21/core/>
