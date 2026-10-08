---
name: hand-off-incident-command-at-shift-change
description: Use when the current incident commander is going off-shift. Runs a structured handoff of roles, state, open hypotheses, and in-flight tasks, with a zero-tolerance rule against blaming the outgoing commander.
---

# Hand Off Incident Command at Shift Change

An incident spanning a shift boundary dies at the seam unless command transfers with the rigour of a surgery handover: state, open questions, and what has already been ruled out. Blamelessness here means the incoming IC inherits the situation, not a defence of it.

## Procedure

1. Freeze the outgoing IC's decision log and publish a handoff block in the incident channel:

       HANDOFF 22:00Z IC: @ana -> @ben
       State: mitigated, error rate 0.4%, cause still open.
       Open hypotheses: (1) pool leak in 4.18 (2) upstream 503s. Ruled out: DB CPU, network.
       In flight: heap dump uploading; vendor ticket 8842.
       Next update due 22:15. Do NOT restart the pool until the dump finishes.

2. Walk the incoming IC through the last three decision-log entries verbatim, not a paraphrase.
3. Transfer the pinned runbook, the comms cadence timer, and the escalation contacts.
4. The incoming IC restates the state and next action in their own words; if the restatement is wrong, the handoff is not done.
5. Keep the outgoing IC reachable for one cadence interval, then explicitly release them: "you're off, @ben owns it."
6. If the outgoing IC made an error, log it as a fact in the timeline — never as an accusation in the handoff.
7. Confirm the incoming IC knows who their deputy is and when their own shift ends.
8. State which of the three bridge roles (IC, comms, scribe) also change hands, not just the IC.

## Pitfalls

- Handing off "it's mostly under control" with no state line, so the incoming IC re-investigates ruled-out ground.
- The outgoing IC stays on the call and keeps deciding, producing two commanders and contradictory fixes.
- Losing the in-flight task list, so a heap dump or vendor ticket is forgotten at the seam.
- Blaming the outgoing shift for a mitigation that looks wrong in hindsight, which teaches everyone to hide state.
- Handing off the IC role but silently keeping the comms role, so two people post conflicting updates.
- Restating hypotheses as facts during handoff, re-infecting the new shift with a guess the old one had already doubted.

## Verification

```
    grep -A6 'HANDOFF ' incident/SEV*-2026-*.md | tail
    # passes when state, open hypotheses, in-flight tasks, and a due time all appear and the incoming IC restated them
```

Related: the incoming IC reads `keep-an-incident-decision-log` entries verbatim, not a summary.
