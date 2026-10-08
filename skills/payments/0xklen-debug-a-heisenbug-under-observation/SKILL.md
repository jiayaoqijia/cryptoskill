---
name: debug-a-heisenbug-under-observation
description: Use when a bug disappears when you add logging, a debugger, or a delay. Changes the observation method so the timing-sensitive race is captured instead of hidden.
---

# Debug a Heisenbug Under Observation

A bug that vanishes under a debugger is timing-sensitive: the observer altered the schedule. Stop adding pauses; capture the event from outside the race.

## Procedure

1. Confirm it is a heisenbug: run the failing case with `-O0`/no logging and again under `gdb`/`pdb`; note which one stops failing. That delta *is* the clue.
2. Replace interactive debugging with non-blocking capture: `perf`, `strace -f -tt -T`, `dtrace`, `ftrace`, or thread-sanitizer, none of which breakpoint your threads.
3. Add a timestamped ring buffer in memory and dump it *after* the crash, so logging does not slow the hot path before the bug fires.
4. Run a stress loop to amplify the window: `for i in $(seq 1 5000); do ./test || break; done`, or `-race` / `TSAN_OPTIONS=halt_on_error=1`.
5. Pin to one CPU (`taskset -c 0`) or force single-thread scheduling; if the bug then disappears, it is a concurrency bug and you can bisect which pair of threads matters.
6. Insert a deliberate, deterministic delay *at the suspect point* to widen a specific window — a controlled reproduction beats a lucky one.
7. Once you can reproduce, bisect one variable at a time (see `isolate-by-changing-one-variable`) among the threads or async tasks involved.
8. Record the schedule you needed to reproduce it, so the eventual regression test can force the same interleaving.

## Pitfalls

- Reaching for a print statement first, which is exactly the thing that perturbs the schedule and hides the bug.
- Concluding "not reproducible" after one clean run under a debugger.
- Running the stress loop without saving the failing iteration's seed or ordering, so the catch cannot be replayed.
- Chasing the delay you added as if it were part of the product code.
- Amplifying with so much load that the machine OOMs or throttles, adding unrelated failures.
- Fixing by sprinkling sleeps, which hides the race and ships the bug as latency.

## Verification

    TSAN_OPTIONS=halt_on_error=1 ./test_app 2>&1 | grep -m1 'WARNING: ThreadSanitizer'
    # passes when a concrete data race (with two stack frames) is printed

    for i in $(seq 1 2000); do ./race.sh >/tmp/r.$i 2>&1 || break; done; echo "caught at $i"
    # a caught iteration with a saved log is the reproduction to keep

Report to the user: the observation method that exposed the race, the two stacks that collide, and the schedule needed to reproduce it.
