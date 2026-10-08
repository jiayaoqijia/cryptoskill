---
name: close-an-incident-and-resume-normal
description: Use when impact has stopped and the response must stand down without loose ends. Runs a close-out checklist of residue, monitoring, comms, and followups before declaring all-clear.
---

# Close an Incident and Resume Normal Operations

Mitigation is not closure. Temporary fixes, elevated monitoring, and half-lifted freezes left in place quietly become the new normal until something else breaks. A close-out checklist prevents that drift.

## Procedure

1. Confirm the impact metric is at or below baseline for a full monitoring window, not a single sample: error rate back to `~0.1%` for 30 minutes.
2. List and schedule the residue: temporary config, raised limits, manual failovers, and their removal dates. A mitigation held in place forever is undeclared debt.
3. Decide monitoring: leave elevated alerts on for 24h, or return to normal thresholds? Record which, so nobody chases a normal-sized blip as if the incident is returning.
4. Close the comms loop: send a final stakeholder note ("impact ended 14:52 UTC, followups in OPS-3391") and set the public status page to resolved.
5. Lift the change freeze explicitly and tell the frozen teams.
6. Confirm every followup has an owner and a date (from `track-incident-followups-to-closure`), and schedule the review.
7. Only then release the bridge and archive the incident channel — which becomes the input to the review.
8. Write the closing timestamp in the timeline before anyone leaves; the end of the incident is data too.
9. Tell the on-call you are handing the system back to normal watch, so they are not surprised by the drop in alert volume.

## Pitfalls

- Declaring all-clear on one good sample while the error rate is still climbing down and flaring.
- Leaving a temporary hotfix and scaling change in place with no ticket, so it silently becomes permanent.
- Never updating the status page, so customers think it is still broken after it has ended.
- Closing the bridge before writing the last timestamp, losing the end of the timeline.
- Forgetting to lift the freeze, so the next unrelated release trips over a gate no one remembers setting.
- Skipping the handback to on-call, so a genuine alert after closure is dismissed as "we're already closing".

## Verification

```
    grep -E 'all-clear|impact ended|freeze lifted' incident/SEV*-2026-*.md
    # passes when the end time, freeze lift, and a followups ticket link are all recorded
```

Related: hand the residue list to `track-incident-followups-to-closure` so nothing survives the close quietly.
