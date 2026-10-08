---
name: retire-an-automation-nobody-uses
description: Use when an automation may no longer be needed because its output is unread, its alert ignored, or its task obsolete. Confirms, then removes it cleanly.
---

# Retire an automation nobody uses

Automations outlive their purpose and keep costing upkeep and attention. Retire them deliberately: confirm nobody uses the output, remove the code and schedule, and leave a record.

## Procedure

1. Find candidates mechanically, not by opinion: jobs with no consumer, no alert actioned in 90 days, or an owner that has changed three times.
2. Confirm the output has no downstream: search code, dashboards, and other jobs for the artifact it produces (the table, file, message, or endpoint).
       grep -r "nightly_recon_summary" --include='*.sql' --include='*.py' .
3. Check the alert history: an alert fired for 90 days and never actioned is evidence the job's signal is unwanted.
4. Ask the recorded owner once, with a deadline: "Retiring X on the 15th unless you object" — a silent owner is consent, but the notice must exist.
5. Quiesce before deleting: pause the job for one full cadence and watch for the complaints that prove it was used.
6. Remove in order: disable the schedule and alert first (reversible), then delete the code and config after the quiet period.
7. Clean up what it created: its status row, its runbook, its resources (containers, output buckets, cron entries), so no orphans remain.
8. Leave a tombstone: a one-line record of what it was, why removed, and the date, in the changelog or a `retired.tsv`.
9. Revoke its credentials and any allowlisting tied to it, so a retired job's keys do not linger.
10. If a consumer surfaces after retirement, bring the job back from version control rather than from memory.

## Pitfalls

- Deleting on suspicion without a search for consumers or a notice period.
- Retiring the job but leaving its credentials, alert, and status row alive.
- A quiet period too short to catch a monthly consumer.
- Removing a job whose output feeds a compliance or audit requirement.
- No tombstone, so a future engineer re-adds the same job in six months.
- Turning off the alert only, so the job keeps running invisibly and burning cost.

## Verification

    # no references to the retired artifact remain
    grep -rn "nightly_recon_summary" --include='*.sql' --include='*.py' . | wc -l   # 0
    crontab -l | grep -c nightly-reconcile                                          # 0
    # pass: no consumers, no schedule, credentials revoked, tombstone written

Report the job, the consumers or their absence, the notice sent and its deadline, what was removed, and the tombstone line.
