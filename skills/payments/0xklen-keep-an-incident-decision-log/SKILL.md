---
name: keep-an-incident-decision-log
description: Use when responders make consequential choices during an incident. Records each decision with time, owner, options weighed, and reversibility, so the postmortem argues from facts not memory.
---

# Keep an Incident Decision Log

Memory of an incident reconstructs a tidy story that never happened. A decision log records the options that were actually on the table at the time, which is the only thing that makes a later review honest.

## Procedure

1. Add one line per decision to the incident channel or a running file:

       14:07Z @ic: chose ROLLBACK over hotfix. Rollback is one command; hotfix needs a new build.
       Reversible, ~3 min. Rejected: scaling pool (does not fix the leak).

2. Record time (UTC), decider, the decision, the alternative rejected, and why. The "why" is the part that goes missing and the part the review needs.
3. Log the reversibility and expected cost so a later reader knows whether it was a safe default or a gamble.
4. Log non-actions too: `14:12Z @ic: chose NOT to page the DB team yet; pool resizing is recovering, revisit 14:30.`
5. Capture assumptions with a shelf life: "assuming the leak is in 4.18 only — if 4.17 also leaks, escalate to SEV1."
6. Do not edit past entries to make them look correct; append a correction with the new time.
7. Keep it in the incident channel, not a private doc, so the scribe and IC both see it.
8. When the IC hands over at a shift change, the new IC reads the last three entries verbatim, not a paraphrase.
9. At close, tag each decision that needs a followup so the review can find it without re-reading the stream.

## Pitfalls

- Logging only the action taken and dropping the option rejected, so the review cannot tell a deliberate choice from an oversight.
- Timestamps from a laptop clock with no timezone, making the timeline unmergeable with server logs.
- The IC making four decisions verbally and the scribe reconstructing them an hour later from a fuzzy memory.
- Editing yesterday's entry after the fact instead of appending a dated correction.
- Recording the decision but not who made it, so no one can be asked why at the review.
- Writing the log in a personal note that leaves when the incident channel is archived.

## Verification

    grep -cE '^[0-9]{2}:[0-9]{2}Z @[a-z-]+:' incident/SEV*-2026-*.md
    # passes when every consequential action in the timeline has a matching decision entry with a rejected alternative
