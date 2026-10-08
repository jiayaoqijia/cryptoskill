---
name: route-alerts-by-severity-and-owner
description: Use when alerts pile into one channel and nobody knows who should pick them up. Assigns a severity and a responsible owner so each alert routes to the right queue.
---

# Route alerts by severity and owner

A shared channel makes every alert everyone's problem and therefore nobody's. Each alert must carry a severity that sets the urgency and an owner that sets the responsibility.

## Procedure

1. Define severity levels once, in a committed file, so they are not re-argued per alert:
       # alerts/severity.yaml
       sev1: user-facing outage, page now        # page
       sev2: degraded, page during hours         # ticket + page
       sev3: internal, next business day         # ticket
       sev4: informational, digest               # log
2. Assign an owner per alert, not per team: a service, a rotation, or a named role. Ownership is a field on the alert rule, not folklore.
3. Route by `(severity, owner)` to a destination: sev1 and sev2 to the owning on-call rotation, sev3 to the owner's project board, sev4 to a weekly digest.
4. Make ownership discoverable: keep a `CODEOWNERS`-style map and let the alert reference it:
       labels: {severity: sev1, owner: payments-oncall}
5. Keep a fallback route for `owner: none` so an unlabeled alert lands somewhere visible rather than vanishing — and treat a new unowned alert as a defect.
6. Set escalation: if a sev1 is unacknowledged for 5 minutes, escalate to the backup rotation, then to the engineering lead. Record the chain in the runbook.
7. Route to rotations and queues, not individuals, so holidays and handovers do not break delivery.
8. Separate real-user impact from internal impact when setting severity; an internal job backlog is sev3 even if it is noisy.
9. Review routing monthly: which queue received what, which alerts were misrouted, which owner field was empty.
10. When a service is handed to a new team, update the owner mapping in the same change as the code, not later.

## Pitfalls

- One channel where a production outage competes with a nightly backup warning.
- Owners named as individuals, so alerts go nowhere during leave.
- Severity assigned by the alert author's anxiety rather than user impact.
- No fallback, so an unlabeled alert silently drops.
- Escalation paths that exist on paper but were never tested.
- Changing ownership in a wiki page that the alert routing never reads.

## Verification

    # every rule has a severity and a resolvable owner
    yq '.[] | select(.labels.owner == null or .labels.severity == null)' alerts/*.yaml
    # pass: prints nothing; spot-check that each owner maps to a real rotation

Report the severity table, the owner map, the routes, and the escalation chain with the time you last tested it.
