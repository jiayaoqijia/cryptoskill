---
name: write-a-runbook-for-a-3am-incident
description: Use when writing a runbook or operational procedure someone executes under pressure. Orders steps as check, act, verify, with exact commands and the rollback written next to each step.
---

# Write a Runbook for a 3AM Incident

A runbook is read by a tired on-call who did not write the system. Every step must be a single command with an expected result, so the reader knows whether to continue.

## Procedure

1. Title the runbook with the trigger, not the system: "Runbook: payments queue depth over 50k". Put the alert name and its link at the top.
2. Open with a three-line summary: what is broken, the user-visible impact, and the urgency (minutes vs hours).
3. Write each step as check, act, verify, with the exact command and the result that means proceed:
   `kubectl -n prod exec deploy/worker -- queue-depth` expecting `< 1000`.
4. Include a decision point as a branch, never as prose: "If depth is still rising after the drain, go to the Restore section."
5. Record the rollback for each mutating step next to it, not in an appendix, e.g. `kubectl rollout undo deploy/worker`.
6. Name the dashboards and the two or three panels that matter, with their exact URLs.
7. Add an escalation block: who to page, their handle, and the criteria that trigger it (e.g. over 30 min to mitigation).
8. Note what NOT to do, especially destructive shortcuts: "Do not restart the leader; it triggers a failover storm."
9. Put copy-paste commands in fenced blocks so nothing is retyped from memory.
10. Date the runbook and the last drill; runbooks that were never rehearsed hide wrong commands.
11. State the blast radius of each mutating command: this affects one worker, this drains the whole queue.
12. Test it in a staging game-day and fix every command that errored or needed a missing step.

## Pitfalls

- "Investigate the issue" with no command, the exact failure mode runbooks exist to remove.
- Assuming access the on-call may not have, such as a VPN or a prod kubectl context.
- Steps that mutate state without a stated rollback.
- Referencing a dashboard that was renamed two quarters ago.
- Hidden prerequisites: the reader must know which cluster, region, or account first.
- A runbook that only works once, because it assumes the alert already fired and the cache is warm.
- Copy-pasted commands with a hardcoded hostname that is wrong in the failing region.

## Verification

    grep -c 'expect' runbooks/payments-queue.md
    # each mutating step must pair a command with an expected result and a rollback line

Have a second engineer run the runbook against a game-day scenario and confirm they reach mitigation without asking a question.
