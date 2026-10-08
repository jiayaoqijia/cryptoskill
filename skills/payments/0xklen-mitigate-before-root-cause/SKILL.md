---
name: mitigate-before-root-cause
description: Use when an incident is active and responders start root-causing before the bleeding stops. Orders mitigation first (rollback, failover, flag off) and defers diagnosis until impact is contained.
---

# Mitigate Before Root Cause

The instinct under pressure is to understand the bug before touching anything, but every minute spent diagnosing is a minute customers stay broken. Stop the impact with the cheapest reversible action, then find out why on a stable system.

## Procedure

1. Ask "what single action removes the impact fastest and is reversible?" before "what caused this?". Usual answers: roll back the last deploy, flip the feature flag off, fail over to the secondary region, shed load, block the bad traffic.
2. Prefer the action you can undo in one step. `kubectl rollout undo deploy/checkout` beats editing three manifests live.
3. Execute the mitigation, then immediately re-measure the user-facing metric (error rate, p99 latency, failed logins). Mitigation is not done until the metric moves.
4. Only when impact is contained, start root-cause work on the now-stable system, preserving the evidence:
   - save the failing pod's logs and a heap/goroutine dump before deleting it: `kubectl logs <pod> --previous > /tmp/<id>-prev.log`
   - snapshot the DB connection count and the slow-query set.
5. If a mitigation is destructive or hard to reverse (dropping a table, force-deleting a PVC), stop and get the IC to weigh it before running it.
6. Record the mitigation and its measured effect in the decision log; "rolled back and errors fell from 12% to 0.4%" is the line the postmortem needs.
7. If the revert does not move the metric, say so and try the next cheapest lever; do not assume the first answer was wrong.
8. State the residual risk of the mitigation (e.g. "reverted a feature users were using") so comms can account for it.
9. Keep the evidence and the mitigation in separate steps so capturing logs never blocks the rollback.

## Pitfalls

- Fixing forward with a new deploy while broken, doubling the surface area instead of reverting to the last known-good release.
- Declaring mitigation done because the command succeeded, without checking the user metric moved.
- Deleting the failing pod or VM before capturing logs, destroying the only evidence of the cause.
- Confusing "the alert went away" with "users are fine" — your own monitoring can be the casualty.
- Holding a rollback for approval when the rollback is the safe default and the alternative is ongoing customer pain.
- Choosing a mitigation you cannot reverse under time pressure, turning a fix into a second incident.

## Verification

```
    grep -E 'mitigation|rolled back|flag (off|disabled)' incident/SEV*-2026-*.md
    # passes when a mitigation action and the metric delta it produced are recorded before any root-cause entry
```

Related: write the metric delta into `keep-an-incident-decision-log` while it is still fresh.
