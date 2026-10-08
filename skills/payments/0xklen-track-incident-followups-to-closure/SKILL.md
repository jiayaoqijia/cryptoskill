---
name: track-incident-followups-to-closure
description: Use when an incident is mitigated and action items would otherwise evaporate. Converts each followup into an owned, dated, verifiable ticket and tracks it from review to done.
---

# Track Incident Followups to Closure

The incident closes when the impact stops; the learning only lands if the followups survive past the next busy week. An untracked "we should add a test for that" is how the same incident recurs in three months.

## Procedure

1. At the review, extract every followup from the decision log and timeline, including the small ones (a missing runbook, a slow alert).
2. Convert each into a ticket with a single owner, a due date, and a verifiable done-condition — not a vague title:

       F-1 owner @ana due 2026-04-25: alert when checkout error rate >2% for 5m.
           Done when: alert fires in a synthetic test. Ticket: OPS-3391

3. Distinguish mitigation debt (temporary fix still in place) from prevention (stops recurrence); schedule the debt first because it is a live risk.
4. Attach a recurrence guard to each prevention item: a test, a dashboard, or a canary that would catch the same class of failure.
5. Review open followups at the next incident review: list overdue ones by name and owner, not as a count.
6. Close an item only when its done-condition is met and linked, not when the ticket is assigned.
7. If an item is repeatedly deferred, escalate the risk decision to the owner of the affected system rather than silently rolling the date.
8. Cap the open list per incident (roughly 5-7); merge or drop the rest so the ones that matter are not lost in noise.
9. Record who verified each closure, so "done" means checked, not claimed.

## Pitfalls

- "Add better monitoring" as a ticket with no metric, threshold, or window — impossible to mark done.
- Assigning followups to "the team" so no individual owns the date.
- Closing the review and never revisiting the list, so items age silently.
- Treating all items as equal when one is a live mitigation temporarily holding the system up.
- Rolling the due date without recording why, so a real risk quietly slips.
- Filing followups only in the postmortem doc, where nobody tracks them after the review.

## Verification

```
    grep -E '^F-[0-9]+ owner @\w+ due [0-9]{4}-[0-9]{2}-[0-9]{2}' incident/SEV*-2026-*.md
    # passes when every followup has an owner, a due date, and a checked done-condition
```

Related: every live mitigation's removal date belongs beside these followups, not in someone's memory.
