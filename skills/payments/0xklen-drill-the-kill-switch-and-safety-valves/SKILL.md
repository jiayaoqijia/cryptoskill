---
name: drill-the-kill-switch-and-safety-valves
description: Use when safety mechanisms (kill switches, breakers, read-only mode, bulkheads) have never been exercised — runs them in a scheduled drill so a control that looks wired is proven to actually stop the thing.
---

# Drill the kill switch and safety valves

A safety mechanism that has never been pulled is a belief, not a control. Switches rot: the flag is read from a stale cache, the breaker trips but nothing consumes it, the read-only path still lets a cron write. Drill each one on a schedule, in a controlled window, and record the result.

## Procedure

1. Inventory the safety controls and who owns each: kill switches, circuit breakers, bulkheads, read-only mode, bulkheads, budget caps, the degrade ladder, the feature-off for the risky path. Each needs an owner and a runbook link.

2. For each control, write the *expected* observable effect as a testable statement: "pulling `writes_frozen` makes POST /orders return 503 within 10s and stops the consumer group." If you cannot state the observable, you cannot drill it.

3. Schedule the drill in a written window with the on-call informed, on staging first, then a low-traffic production window, then a real control. Announce start and end.

4. Pull the control *for real* — set the actual flag or revoke the actual permission, do not simulate it in a test harness. Then measure with the same query the runbook uses:
       curl -s -o /dev/null -w '%{http_code}\n' -X POST localhost:8080/orders -d '{}'   # expect 503
       # time from "flag set" to "effect observed across all replicas"
       grep -h 'writes_frozen' /var/log/app/*.log | tail -1

5. Record the *time to effect* and the *coverage* (how many replicas/regions obeyed). A switch that takes 90s to propagate because of a 90s flag cache is a switch that fails under a fast-moving incident.

6. Restore and confirm full recovery — writes flowing, errors back to baseline — with the same evidence you would want after a real incident. A drill that leaves the system degraded is a self-inflicted outage.

7. File the result: control, date, time-to-effect, coverage, anomalies. Any control that failed, was too slow, or had no effect becomes a tracked fix with an owner. Re-drill after the fix.

## Pitfalls

- Drilling only in staging: production has the real cache TTLs, the real multi-region propagation and the real background writers, and behaves differently.
- Testing the control by *simulating* it (mocking the flag) rather than pulling it, which validates the mock, not the switch.
- Forgetting to restore, or restoring in the wrong order, so the drill leaves stale flags that cause a later incident.
- A drill with no recorded time-to-effect, so a slow control passes the drill and fails the real incident.

## Verification

    # the drill log must show a measured time-to-effect inside the target
    cat drills/2026-01-writes_frozen.md
    #   control: writes_frozen | effect: POST 503 within 4s | coverage: 6/6 replicas | restored: yes
    ls drills/ | wc -l                       # every control drilled at least once this quarter
    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/orders/1   # post-drill: 200, healthy

Report: the control inventory with owners, the drill log with time-to-effect and coverage per control, and the list of controls that failed and are now tracked fixes.
