---
name: page-the-correct-on-call-rotation
description: Use when an alert or incident needs a human now. Pages the rotation with severity, a runbook link, and an ack deadline, and escalates on no-ack rather than paging individuals by name.
---

# Page the Correct On-Call Rotation

Paging the wrong person, or an empty rotation, is the single most common reason a real incident sits unnoticed. Page the rotation, not a name; include enough context to act; escalate automatically if nobody acknowledges.

## Procedure

1. Page the rotation, never an individual: `oncall page --rotation checkout --sev 2 --incident SEV2-2026-04-11-checkout`. A hardcoded name is a hole when that person is asleep.
2. Include in the page: severity, one-line impact, the alert that fired, and a direct runbook link (`docs/runbooks/checkout.md`). A page that says only "checkout alerting" wastes the first five minutes.
3. Set an acknowledgement deadline (5 min for SEV1, 15 min for SEV2) and let the tooling escalate to the next tier automatically on no-ack.
4. Verify the rotation is not empty before you rely on it — an unstaffed rotation is a silent failure:

       oncall rotations list --team checkout | jq '.[] | select(.members|length==0)'

5. If the primary does not ack, the secondary is paged next; do not start paging managers out of band during the first window.
6. Record the page and ack times in the timeline; a slow ack is a followup item, not a personal failing.
7. For a suspected widespread issue, page the service owner and the org on-call simultaneously rather than discovering the scope serially.
8. Confirm the paged human actually joined before you stop the notification; a silent ack can still be someone who went back to sleep.

## Pitfalls

- Paging a person found in a README who left the team, so the page goes nowhere and the alert ages.
- A rotation with no members, discovered only when the incident is already ten minutes old.
- Pages with no runbook or impact, so the responder's first action is to ask the IC what is wrong.
- Not escalating on no-ack, so a single awake-but-away responder holds the whole incident.
- Paging everyone "just in case", so the signal is lost and half the org burns out.
- Relying on a chat message as a page, which no one sees outside working hours.

## Verification

```
    oncall rotations list --team checkout | jq '.[] | select(.members|length==0)' ; echo exit=$?
    # passes when the query returns no empty rotation and every page carries severity + runbook + ack deadline
```

Related: `escalate-an-incident-to-a-new-team` decides who to page once the first rotation is engaged.
