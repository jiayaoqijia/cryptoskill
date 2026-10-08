---
name: document-why-an-automation-exists
description: Use when an automation's purpose is not obvious from its code and a new reader cannot tell if it is safe to change. Records the why, the owner, and the blast radius next to the job.
---

# Document why an automation exists

Code says what a job does; it rarely says why, who owns it, or what breaks if it stops. A short, explicit record next to the job prevents the next reader from guessing — or deleting the wrong thing.

## Procedure

1. Put a header block at the top of the job's entry file, or a sibling `JOB.md`, with fixed fields:
       # JOB: nightly-reconcile
       why:           detect drift between ledger and gateway settlements
       owner:         payments-oncall (see CODEOWNERS)
       trigger:       cron 03:00 UTC, concurrencyPolicy Forbid
       input:         gateway_settlements, ledger_entries (last 36h)
       output:        reconciliations table; alert on drift > 0.01%
       blast_radius:  insert/update only; never deletes
       runbook:       https://wiki/runbooks/nightly-reconcile
       retire_when:   gateway retires the settlement feed (Q3 2027)
2. State the why as the failure it prevents: "catches stuck settlements", not "runs a SQL join".
3. Name the owner as a rotation or role, not an individual, and point at where ownership is recorded.
4. State the blast radius explicitly: what it can read and write, and whether it is reversible. This is the field reviewers forget to check.
5. Record the `retire_when` condition so the job has an end-of-life, not just a start.
6. Keep the doc next to the code so a change to the job lands in the same review as the doc.
7. Add a lint or CI check that the header's required fields exist, so a new job cannot ship undocumented.
8. Link the runbook and the alert rules so the reader can find operational context in one hop.
9. Update the doc when the trigger or output changes; a stale header is worse than none because it is trusted.
10. For config-as-code jobs, store the doc as metadata in the same object so the schedule and the why travel together.

## Pitfalls

- A doc that restates the code ("it reads rows and writes rows") instead of the purpose.
- Ownership that names someone who left two teams ago.
- No blast radius field, so a reviewer cannot judge the risk of a change.
- Docs in a wiki disconnected from the code, drifting apart within a month.
- A purpose so vague ("maintenance") that it justifies anything.
- No end-of-life condition, so the job has no natural retirement path.

## Verification

    for f in jobs/*/JOB.md; do grep -qE '^(why|owner|trigger|blast_radius|runbook):' "$f" || echo "MISSING $f"; done
    # pass: prints nothing; every live job has the required header fields

Report the header fields, the owner, the blast radius, and the retire_when condition for the job in question.
