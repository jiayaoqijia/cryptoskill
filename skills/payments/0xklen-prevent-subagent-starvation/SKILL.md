---
name: prevent-subagent-starvation
description: Use when several agents share a pool of workers, locks, or rate-limited resources. Guarantees every queued child eventually runs by bounding how long one child can hold a shared slot.
---

# Prevent Subagent Starvation

Starvation is a queued child that never runs because others keep grabbing the shared resource. Bound hold times, use a fair queue, and prove every child got a turn.

## Procedure

1. Identify the contended resource: worker slots, a file lock, an API rate budget, or a single-writer path.
2. Give the queue a FIFO discipline for equal-priority work so a new arrival cannot jump an older child.
3. Cap how long any child may hold a slot: a lock TTL (e.g. 120s) or a max task duration, after which the slot is reclaimed.
4. Reserve capacity for the tail: keep at least one slot free for the oldest waiting child, not the newest.
5. Add an aging rule — a child waiting longer than `2 × avg_task_time` is promoted ahead of newcomers.
6. Instrument queue depth and wait time per child in `notes/queue.log` (`child-id enqueue_ts start_ts end_ts`).
7. Alarm when any child's wait exceeds a threshold (e.g. 300s) even if throughput looks fine.
8. Detect a lock leak: a slot held with no active child, visible as a TTL expiry with no `end_ts`.
9. Re-dispatch any child that expired its turn rather than dropping it silently.
10. After the run, assert every enqueued child has a start time: `awk 'NF && $3==""' notes/queue.log` must be empty.

## Pitfalls

- A lock with no TTL, so one hung child holds the resource forever and the rest starve.
- LIFO or random scheduling that lets fast newcomers repeatedly overtake a slow-but-waiting child.
- Fair-looking round-robin that still starves a child needing two slots at once under contention.
- Measuring throughput (jobs/sec) as health while one child sits unstarted.
- Dropping a waiting child at shutdown to "finish the batch" and calling the run complete.

## Verification

```bash
awk 'NF && $3==""{print "starved: "$1}' notes/queue.log; awk 'NF{print $3-$2}' notes/queue.log | sort -n | tail -1
# passes when no starved lines print and max wait is under the starvation threshold
```

Report to the user: queue depth, the longest wait, and any child that expired its slot and was re-queued.
