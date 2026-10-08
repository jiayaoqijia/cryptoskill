---
name: delegate-investigation-tasks-under-command
description: Use when the incident commander must task responders without joining the debugging. Assigns bounded, time-boxed investigation threads with a defined return format so command stays unblocked.
---

# Delegate Investigation Tasks Under Command

An IC who starts grepping logs has stopped commanding. Delegation keeps command on the decision layer while responders work bounded threads — but only if each task has an owner, a timebox, and a defined form of answer.

## Procedure

1. Frame each task as a question with a test, not an activity: not "look at the DB" but "in 10 minutes tell me whether active DB connections stay high after traffic drops — that distinguishes leak from load."
2. Give every task an owner and a timebox: "@ben, 10 minutes, report by 14:25."
3. Specify the return format so the answer is usable: "one line: connections after the drop, and whether that supports the leak."
4. Keep the IC out of the thread; if the IC must investigate, they hand command to a deputy first.
5. Limit parallelism: 3-4 open threads max; more and the IC cannot hold the state and handoffs degrade.
6. Close each thread explicitly when answered — "leak confirmed, thanks, drop it" — so responders are not left digging in a dead end.
7. Track threads somewhere visible (the channel) so a handoff at shift change does not strand one.
8. Write the outstanding threads into the handoff block when the IC changes, or they are lost.
9. Give the responder the evidence they need to start (log path, dashboard link) rather than making them hunt.

## Pitfalls

- Assigning an activity ("investigate the cache") with no question, so the responder returns raw data and no conclusion.
- Timeboxes that are never checked, so a 10-minute task runs an hour and blocks the branch that depended on it.
- The IC picking up a keyboard "just to check", silently abandoning command.
- Six parallel threads the IC cannot reconcile, so the same hypothesis is tested twice and two others are dropped.
- Never closing threads, so the responder keeps working on a question the team already answered.
- Delegating without the return format, so five people answer in five shapes the IC must translate.

## Verification

```
    grep -E '@\w+, [0-9]+ min, report by' incident/SEV*-2026-*.md
    # passes when every delegated thread names an owner, a timebox, and a specific return question
```

Related: `run-an-incident-call-bridge` covers how the IC voices these tasks without cross-talk.
