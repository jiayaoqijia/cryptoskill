---
name: write-a-stakeholder-status-update
description: Use when composing an update for leadership, adjacent teams, or support during an incident. Fills a fixed impact-action-ETA-ask template so the reader gets what they need without pinging the IC.
---

# Write a Stakeholder Status Update

Stakeholders do not need the debugging narrative; they need to know what is broken, what is being done, when they will hear again, and whether they must act. Writing to that shape removes the follow-up questions that steal the IC's attention.

## Procedure

1. Lead with impact in the reader's terms: not "Redis is hot" but "checkout has been failing for ~40% of users since 13:50 UTC".
2. State the current action, not the whole hypothesis list, and name the owner: "Ops is rolling back release 4.18."
3. Give a next-update time as a clock time, not "soon" — "next update 14:30 UTC".
4. Add an explicit ask or a clear "no action needed from you". Support needs to know whether to point customers at a workaround.
5. Keep it under about 120 words; long updates get skimmed and the ETA is missed.
6. Put the incident id in the subject or first line so it threads: `[SEV2-2026-04-11-checkout]`.
7. Never speculate on root cause here: "the cause of the connection-pool exhaustion is under investigation" is fine; naming a suspect that turns out innocent damages trust.
8. If you do not know the ETA, say so and commit to the next-update time instead of inventing one.
9. Separate "customers affected" from "internal teams blocked" so support and engineering each read the part they need.
10. For leadership, add the trend (improving/stable/worsening) in one word after the impact line.

## Pitfalls

- Burying the impact under three paragraphs of investigation detail so the reader reaches "we're on it" and stops.
- Promising a fix time to look decisive and missing it — a missed ETA costs more trust than "unknown, next update 14:30".
- Sending the update only to the person who asked, so the other five stakeholders each ask separately.
- Using internal shorthand ("the LB is flapping") that the support team cannot relay to customers.
- Mixing the customer notice and the internal update into one message, so it is wrong for both audiences.
- Writing in the passive voice so no owner is visible and no one knows who to follow up with.

## Verification

```
    grep -Ei 'impact|next update|no action|action needed' incident/SEV*-2026-*-update.txt
    # passes when impact, a next-update time, and an explicit action/no-action line all appear
```

Related: `run-a-comms-cadence-during-an-incident` sets when these updates are due.
