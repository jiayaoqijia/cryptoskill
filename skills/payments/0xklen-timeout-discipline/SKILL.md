---
name: timeout-discipline
description: Use when a command, network call, or wait could hang indefinitely. Bounds every external operation with a deadline and a partial-result plan, so a stall surfaces as a timeout instead of a frozen task.
---

# Timeout Discipline

An unbounded wait is an unbounded risk: the task freezes and no output arrives. Every external operation gets a deadline, and a timeout is treated as a finding to diagnose, not a thing to ignore.

## Procedure

1. Bound every network call: `curl --connect-timeout 5 --max-time 20 https://api.example/x`. Never rely on default timeouts, which can be minutes or infinite.
2. Bound every shell command that could hang: `timeout 300 <cmd>` on Linux, `gtimeout 300 <cmd>` on macOS (`brew install coreutils`). Wrap prompts and servers explicitly.
3. Wrap interactive tools so they cannot block on input: pipe from `/dev/null` (`tool < /dev/null`) or pass a non-interactive flag (`-y`, `--batch`, `--no-pager`).
4. For polling, use a deadline loop, not an unbounded one: `for i in $(seq 1 30); do ok && break; sleep 2; done` — 60 seconds total, then fail.
5. Match the timeout to the task: a health check gets 5s, a test suite gets 600s, a package install gets 300s. A single value for all calls is a smell.
6. On timeout, capture partial output before retrying: redirect to a file so the half-finished result is inspectable (`<cmd> > out.txt 2>&1 || true`).
7. Ensure a killed command does not leave orphans: use process groups (`timeout --kill-after=10 300 <cmd>`) and check for leftover children (`pgrep -f <cmd>`).
8. Record the timeout value and the observed duration for each operation, so a too-short limit is distinguishable from a genuine hang.
9. When a timeout is expected on a long job, run it as a tracked background process and poll, rather than blocking a foreground call for the full duration.
10. Set the timeout from the observed p99 of the operation, not a guess; measure once, then reuse the number.
11. Give connect and total separate limits: a 5s connect and a 60s total for a download, not one number.
12. On repeated timeouts at the same value, record whether the limit is wrong or the target is degraded.

## Pitfalls

- A `git clone` or `npm install` with no timeout hanging on a dead mirror for the whole session.
- An interactive CLI waiting for a password prompt that will never come, with no TTY.
- A retry loop with an attempt cap but no wall-clock deadline, running for a very long time.
- Treating a timeout as a transient error and retrying the same unbounded call.
- Killing a parent process while its children keep the port open, so the next run fails to bind.
- A parent timeout without `--kill-after`, leaving children holding the port after the parent is killed.
- Reusing a health-check timeout for a bulk API call, killing a legitimately slow write mid-flight.

## Verification

    timeout 5 sleep 30; echo "exit=$?"   # expect exit=124
    # passes when the wrapper returns 124 for a hung command, proving the deadline fires

Report to the user: the timeout used per external operation, any operation that hit it, and the partial output captured at that point.
