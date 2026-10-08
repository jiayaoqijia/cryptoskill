---
name: prevent-deadlocks-with-lock-ordering
description: Use when two mutexes can be taken in either order — imposes a global lock rank, forbids holding a lock across outbound calls, and proves the cycle is gone with a canary test.
---

# Prevent deadlocks with lock ordering

A deadlock needs two mutexes acquired in opposite order by two threads. Eliminate the cycle structurally: rank every lock, always acquire ascending, and never hold a lock across a call that can take another.

## Procedure

1. Enumerate every mutex in the component: `rg -n 'sync.Mutex|sync.RWMutex|\.Lock\(\)' internal/`. Record them in `docs/lock-order.md` with an explicit integer rank.

2. Rank by containment: account (10) < order (20) < item (30). The rule: while holding rank N you may only acquire a lock with rank > N, never ≤.

3. Enforce the rule in debug builds with a tiny rank tracker:
       type Ranked struct { mu sync.Mutex; rank int }
       func (r *Ranked) Lock() { assertRank(r.rank); r.mu.Lock(); held.push(r.rank) }
   `assertRank` panics when the new rank is ≤ the top of the held stack.

4. Remove the commonest second-order case: never make a network call, fire a callback, or publish while holding a lock. Snapshot, release, then act:
       mu.Lock(); snap := s.snapshot(); mu.Unlock(); publish(snap)

5. Use `TryLock` with a deadline on any lock contended across subsystems; a failed `TryLock` converts an indefinite hang into a retry or a typed error.

6. Run the deadlock detector. Go prints `fatal error: all goroutines are asleep - deadlock!`; for a JVM use `jstack <pid>` and look for a cycle where thread A is `BLOCKED` waiting on a lock held by thread B, which waits on A.

7. Add a canary test that hammers both orders concurrently for 60 s. Before the fix it hangs; after, it must finish in under 2 s.

## Pitfalls

- Documenting an order the code does not follow — the doc drifts. Enforce with the rank tracker or a linter, never a comment alone.
- Holding a lock across an `await` or channel receive; the holder blocks on the caller while the caller blocks on the mutex.
- `RWMutex` upgrade: taking `RLock` and then calling `Lock` on the same mutex self-deadlocks.
- Declaring the deadlock gone because the canary passed once; run it under `-race -count=20` and on a 2-core box where the scheduler interleaves differently.

## Verification

    go test -race -run TestNoDeadlock -timeout 90s ./...
    rg -n '\.Lock\(\)' internal/ | wc -l    # every site covered by the rank tracker

Report: the lock graph and ranks, the call site that violated order and was restructured, and the canary finishing in under 2 s under `-race`.
