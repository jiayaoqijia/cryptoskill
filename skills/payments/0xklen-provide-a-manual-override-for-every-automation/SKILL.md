---
name: provide-a-manual-override-for-every-automation
description: Use when an automation must run but you need to pause, skip, or force it by hand. Gives every job an operator-controlled switch that does not require a code change.
---

# Provide a manual override for every automation

Automations meet conditions their authors did not foresee. The operator needs a way to pause, skip, or force a run without editing code and redeploying — and that override must be visible and auditable.

## Procedure

1. Give every job three overrides: pause (do not run), skip-once (run nothing this time), and force (run now, out of schedule). Implement them as flags, an env var, and a small state file.
2. Read the override from a place that does not need a redeploy: an env var, a config table, or a file in a known path:
       PAUSE_FILE=/etc/automation/pause/nightly-reconcile
       [ -f "$PAUSE_FILE" ] && { echo "paused"; exit 0; }
3. Make a paused run exit 0 and log `status="paused"` — a pause is a normal, non-alarming state, not an error.
4. Record who paused and why: the state file includes the requester and timestamp, or a row in a control table, so the pause is attributable.
5. Never let a pause be silent forever: if a job is paused longer than its retention window, alert so an accidental permanent pause is caught.
6. Provide a force-run entrypoint (`./job.sh --force --unit 2026-10-07`) that respects the idempotency guard, so forcing twice is still safe.
7. Keep overrides out of the job's business logic; one gate at the top, not conditions scattered through the code.
8. Protect the control channel: only operators who may run the job may pause or force it; log the identity.
9. Test all three overrides in staging as part of the job's test, so they do not silently rot.
10. Document each override in the runbook with the exact command or file path.

## Pitfalls

- Pausing by commenting out the cron entry, which nobody remembers to restore.
- A pause that exits non-zero or alerts, so pausing triggers a page.
- A force-run that bypasses the idempotency guard and double-processes.
- Overrides implemented as code branches that require a merge and deploy to use.
- No record of who paused the job, so a stale pause is unattributed.
- An override path with world-write permissions that any process can flip.

## Verification

    touch /etc/automation/pause/nightly-reconcile && ./job.sh; echo "exit=$?"   # 0, status=paused
    ./job.sh --force --unit 2026-10-07; echo "exit=$?"                          # runs once, guard holds
    rm /etc/automation/pause/nightly-reconcile
    # pass: pause exits 0 without working; force runs; a second force is a no-op

Report the three override mechanisms, where they are stored, who may set them, and the test that exercised each.
