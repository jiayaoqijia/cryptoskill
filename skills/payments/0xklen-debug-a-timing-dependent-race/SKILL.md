---
name: debug-a-timing-dependent-race
description: Use when a bug appears only at certain times, in CI but not locally, or under load. Makes the schedule deterministic with fake clocks and forced ordering instead of retrying.
---

# Debug a Timing-Dependent Race

"Passes locally, fails in CI" is a timing statement. Stop re-running and hoping; take control of the clock and the ordering so the failure becomes a decision, not a dice roll.

## Procedure

1. Classify the trigger: wall-clock (a date boundary), ordering (two async tasks), or load (a queue backing up). Each needs a different instrument.
2. Reproduce deterministically by freezing the clock. Use a fake timer (`sinon.useFakeTimers()`, `freezegun`/`time-machine` in Python, `tokio::time::pause()`) so you can advance time by hand.
3. For ordering, replace the scheduler: run with one worker (`--concurrency=1`), then deliberately interleave with a seeded scheduler or `asyncio` event-loop `debug=True`.
4. Add a barrier at the suspected interleaving point and run the two sides in both orders; if one order always fails, you have a deterministic repro.
5. For load, find the threshold: ramp concurrency (`seq 1 1 64 | xargs -n1 -P <n> ./req.sh`) until it fails, and record the number.
6. Check for the classic cause: state read before a write lands, a cache warmed by an earlier test, or a connection pool reused across tests. Confirm with a per-test isolation run.
7. Once deterministic, bisect one variable (thread, timer, await point) as in `isolate-by-changing-one-variable`.
8. Fix the ordering, not the timing: add the missing await/lock, or make the operation idempotent, rather than padding with a sleep.

## Pitfalls

- Adding sleeps to make it pass, which shrinks the window instead of closing it and ships a latency regression.
- Re-running CI until it goes green and calling the bug resolved.
- A test that depends on test execution order; running the file alone "proves" a fix that is really isolation.
- Freezing one clock while another (DB `now()`, container time) keeps moving, so half the schedule is still random.
- Tuning the CI runner's CPU or `--maxWorkers` as a fix; the race is still there, just rarer.
- Blaming the CI machine's load without measuring it (`/proc/loadavg`, runner CPU) to confirm.

## Verification

    for i in 1 2 3; do ./test --concurrency=1 --seed=$i >/dev/null 2>&1; echo "seed=$i exit=$?"; done
    # passes when one seed fails all three times (deterministic) and the fixed seed is recorded

    npx jest --runInBand path/test.spec.js
    # passes when the test is green in-band AND stays green across 20 repeated runs with a fixed clock

Report to the user: the trigger class, the frozen schedule or threshold that reproduces it reliably, and the ordering the fix closes.
