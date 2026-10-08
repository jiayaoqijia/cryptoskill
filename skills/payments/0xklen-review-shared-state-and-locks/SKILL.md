---
name: review-shared-state-and-locks
description: Use when a diff adds mutable shared state, goroutines, threads, or lock acquisition. Checks lock ordering, access scope, and runs the race detector before approving.
---

# Review shared state and locks in the diff

Concurrency bugs pass every test on a lightly loaded laptop and fail in production under load. Review the diff for shared mutable state and prove the access is guarded.

## Procedure

1. Find new shared state in the diff: `gh pr diff 482 | grep -nE '^\+.*(sync\.Mutex|sync\.RWMutex|var .* map\[|static .*=|global |lazy_static|AtomicRef|locks?\[)'`.
2. For every mutation of shared state, confirm the write holds the lock and every read does too. A read on a fast path that skips the lock is a blocking finding.
3. Check lock ordering: if a function takes lock A then lock B, search the file for the reverse order `B then A`. Inconsistent ordering is a deadlock.
4. Confirm you copy-under-lock before iterating; ranging a map while another goroutine writes it panics with "concurrent map iteration and map write".
5. Check the lock is held for the whole compound operation, not just per-field: read-modify-write on a counter needs one lock spanning the get and the set.
6. Prefer an atomic or a channel over a mutex only when the operation is a single word; anything compound needs the lock.
7. Run the race detector and require it green as a merge condition.

## Pitfalls

- A `sync.Mutex` guarding the map but a returned slice pointing at the same backing array, mutated later without the lock.
- Using `RWMutex` where a write path takes `RLock`, allowing a write through a read lock.
- Deferring `Unlock` inside a loop, so the lock is held until the function returns.
- A pointer field shared by value-copying a struct that embeds the mutex; the copy's lock is a different lock.

## Verification

    go test -race ./... 
    # or, for C/C++/Rust with sanitizers:
    RUSTFLAGS="-Z sanitizer=thread" cargo test
    # Python: run with coverage of threading sites and assert-timeout for deadlock:
    pytest tests/ -q --timeout=30

Report each shared-state site, the lock that guards it, and the ordering pair. A green `-race` run and consistent ordering are the merge conditions.

## Worked example

A worker adds `var cache = map[string]int{}` with writes taken under `mu.Lock()`, but the metrics endpoint ranges that map with no lock. Under load it dies with `fatal error: concurrent map iteration and map write`. The fix wraps the read in `mu.RLock()` or returns a snapshot copied under the lock. `go test -race ./...` reproduced the crash before the fix and is clean after.
