---
name: open-an-incident-and-assign-roles
description: Use when starting incident response and no one has formally taken command. Names the incident, assigns the four core roles, and opens the single log every later update reads from.
---

# Open an Incident and Assign Roles

An incident without a named commander drifts: two people chase the same hypothesis, no one talks to customers, and the fix depends on whoever is loudest. Declaring the incident and its roles in the first two minutes prevents that drift.

## Procedure

1. Open one channel or thread and give it a stable id: `<sev>-<yyyy-mm-dd>-<short-slug>`, e.g. `SEV2-2026-04-11-checkout-500s`. Every later artefact references this id.
2. Assign exactly three roles, even if one person wears two:
   - **Incident Commander (IC)** — decides and delegates, never debugs. If the IC touches a keyboard to fix, command is unowned.
   - **Comms Lead** — writes stakeholder and customer updates on the cadence from `run-a-comms-cadence-during-an-incident`.
   - **Scribe** — keeps the timeline and the decision log (`keep-an-incident-decision-log`).
3. State the initial severity with `set-incident-severity-levels` and a one-line impact: who is affected and what they cannot do.
4. Pin the runbook for the affected service at the top of the channel: `docs/runbooks/<service>.md`. If none exists, note it as a followup.
5. Post a single roll-call message: roles, severity, impact, next update time. Updates must not fan out into DMs.
6. Start the cadence timer now, not after the next finding — every 15 min for SEV1/SEV2.
7. Name a deputy IC before anyone leaves the bridge, so command never lapses at a shift gap.
8. Announce the incident to the on-call channel and the service owner; everyone else is a reader, not a decider.
9. Set the channel topic to the incident id and the next-update time so late joiners orient without scrolling.
10. Log the declaration time in the channel — the postmortem's duration maths starts here.

## Pitfalls

- The senior engineer silently becomes the debugger and the IC role evaporates; freeze their hands or hand off command explicitly.
- Two channels — one in chat and a bridge call — where updates happen in only one and stakeholders miss both.
- Naming the incident after a symptom that turns out wrong ("redis-OOM") so the logs are mislabelled when the cause differs.
- Assigning roles without saying who relieves them, so command lapses at shift change with no handoff.
- Broadcasting the roll call to the whole company, so the IC is buried in replies from people who cannot help.
- Letting the IC also be the scribe, which guarantees the decision log stops the moment the incident gets busy.

## Verification

    grep -E '^(IC|Comms|Scribe):' incident/SEV*-2026-*.md
    # passes when all three roles have a named owner and an impact line exists

Report the incident id, severity, named roles, and the wall-clock time the next update is due.
