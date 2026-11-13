---
name: time-policy-record
domain: software-engineering/time-policy-record
trigger: "Writing the system's time policy so decisions do not get re-argued."
anti_trigger: "Not for the presentation-layer formatting (ac-i18n-and-localisation)."
scope: "The written record: clock choices, formats, zones, and update ownership."
status: seedling
---

# Time policy record

## Standard

A time policy is a short written document that answers, once, the questions every team otherwise answers repeatedly: which clock for durations, what format for storage and transport, which zone everywhere except the edge, who updates the zone database and how often, what the leap-second posture is, and what tolerance cross-machine comparisons carry. Without it, each service makes its own call and the disagreements surface as bugs — a zoneless timestamp here, a wall-clock duration there.

The record's test is whether a new service can be built compliant without asking anyone. If a new module can read the policy and produce timestamps that interoperate with every existing one, the policy works. If it needs tribal knowledge — what the database was "really" configured to, which services ignore the standard — the policy is incomplete and the gaps must be named.

## Decision rules

- State the clock rule: monotonic for durations, wall for timestamps.
- State the storage and transport format with an explicit offset.
- State the zone rule: UTC everywhere, conversion at the presentation edge only.
- Name the owner and cadence for the zone database update.
- State the leap-second posture and its justification.
- State the measured cross-machine tolerance and the drift alert threshold.

## Procedure

1. Draft the policy from the leaf decisions of this skill.
2. Audit existing services against each rule and list the exceptions.
3. Fix or explicitly register the exceptions.
4. Publish the policy where the code lives, not where documents go to die.
5. Test: build or review one module against the policy alone, no tribal knowledge.
6. Amend with dates when a rule changes.

## Anti-patterns

- A policy with an unstated exception list that only the seniors know.
- Stored in a wiki nobody visits since the migration.
- No owner for the zone database update, so it happens on incident.
- Recorded tolerance from a guess rather than a measurement.
- Silent amendments without dates.

## Done checklist

- [ ] Clock rule stated.
- [ ] Format stated with offset.
- [ ] Zone rule stated.
- [ ] Database update owner and cadence named.
- [ ] Leap posture stated.
- [ ] Exceptions registered with dates.

One more finding earns a line of its own in the audit trail: any table or column found storing timestamps without a zone, because those are silent landmines that no future policy can reach retroactively — each needs a conversion with a documented assumption about what the writer meant, and that assumption is itself a decision to record.

## Sources

- RFC 3339 timestamp profile: <https://www.rfc-editor.org/rfc/rfc3339>
- NTP precision background: <https://www.rfc-editor.org/rfc/rfc5905>
- IANA time zone database governance: <https://www.iana.org/time-zones/>
