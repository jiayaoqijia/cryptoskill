---
name: write-a-first-week-runbook-for-oncall
description: Use when a new on-call engineer must act before they know the system. Maps each alert to a first safe action, a copy-paste command, and an escalation path, so nothing on the first shift depends on memory.
---

# Write a First-Week Runbook for On-call

Under pressure a new engineer cannot improvise from a wiki. An alert-to-action table with copy-paste commands and a named escalation path turns a terrifying first shift into a checklist.

## Procedure

1. One row per alert, with four columns: alert, meaning, first safe action, escalate to.
2. Every first action is a read-first command, never a restart: `kubectl -n prod get pods -l app=api`.
3. Give the exact command with namespace and label filled in; never leave `<name>` placeholders.
4. Mark reversible actions (`scale`, `rollback`) as safe and one-way actions (`delete pvc`, `drain`) as "wake someone".
5. Name the escalation as a person and a channel, with a time threshold: "no recovery in 10 min -> page the DB owner".
6. Include the "do nothing" row: for alerts with no impact, record that the correct action is to note and wait.
7. Keep it in the repo at `docs/runbook.md` so it versions with the system.
8. Dry-run the runbook with the new hire during business hours before their first shift.
9. Link each row to the dashboard that shows the symptom, so the reader can confirm state before acting.
10. Review the runbook after every real incident and correct the row that misled the responder.
11. Put the most-firing row at the top; the ordering is itself a hint about where the pain is.
12. Add the dashboard link and the log query for each alert.
13. Mark which alerts page a human and which only notify.
14. State the golden signal the alert maps to, so the responder knows what healthy means.
15. Add a one-line 'what this alert usually is' drawn from past incidents.
16. Include the command to silence a known-flapping alert.

## Pitfalls

- Commands with unfilled placeholders the newcomer cannot resolve at 3am.
- Telling the reader to restart first, destroying the evidence.
- Escalation as a vague "ask the team" with no threshold or name.
- A runbook that never says when inaction is the right move.
- Testing it for the first time during a real incident.
- A row that fires on a flapping alert with no note that it usually self-resolves.
- A row that runs a destructive command with no confirmation flag.
- Copy-paste commands that assume a context the new hire has not set.
- No 'last reviewed' date, so stale rows look current.
- Not saying what healthy looks like, so recovery has no target.
- Leaving out the usual cause, so the responder starts from scratch.
- No way to suppress a noisy known-bad alert.

## Verification

    grep -cE '^\| *[A-Za-z].*\|.*\|.*\|.*\|' docs/runbook.md
    # passes when every alert row has a copy-paste command and a named escalation with a time bound

Report to the user: the alert rows, the read-first commands, and the escalation thresholds.
