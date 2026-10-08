---
name: write-the-first-incident-notification
description: Use when an incident is just detected and the first message must go out fast. Sends a short known-unknown-doing-next template within minutes so stakeholders get facts before rumour does.
---

# Write the First Incident Notification

The first notification is the hardest because you know the least. Sending a short, honest, correctly-scoped note within minutes beats a perfect one after twenty, and it sets the tone for every update that follows.

## Procedure

1. Send within 5 minutes of declaring, tagged with the incident id: `[SEV2-2026-04-11-checkout]`.
2. Use a four-line shape:
   - **Known**: what is observably broken, with numbers and scope ("checkout failing, ~40% of requests, EU and US").
   - **Unknown**: the cause, stated as unknown if it is ("cause not yet identified").
   - **Doing**: the first action in flight ("rolling back release 4.18").
   - **Next**: the next update time ("next update 14:20 UTC").
3. Send to the smallest audience that needs to act now — on-call, support lead, the affected service owner — not the whole company.
4. Mark it explicitly provisional: "early information, details may change." This buys room to be wrong about a theory without looking like a flip-flop.
5. Route it through the one channel the cadence uses so it becomes update #1, not a stray DM.
6. Do not name a cause you have not confirmed: "we see 500s on checkout" is safe; "the new ORM broke it" is a guess that will follow you.
7. Include the incident channel name so anyone who needs in can join without asking.
8. Note the current severity so recipients know whether to wake anyone.

## Pitfalls

- Waiting for a diagnosis before sending anything, losing the first ten minutes to silence.
- Blasting the whole company so fifty people respond, none of whom the IC needs.
- Writing "everything is fine but we're looking" when users are visibly broken, which reads as denial.
- Naming an unconfirmed cause that the review later disproves, undermining the whole update stream.
- Sending a DM instead of posting to the channel, so the first notice is invisible to the team.
- Omitting the next-update time, so stakeholders immediately start pinging for one.

## Verification

```
    grep -A4 'First notice' incident/SEV*-2026-*.md | head
    # passes when Known, Unknown, Doing, and Next all appear and the notice is timestamped within 5 min of declaration
```

Related: `set-incident-severity-levels` fixes the severity this notice must state.
