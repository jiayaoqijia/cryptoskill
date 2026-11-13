---
name: threat-hunting
domain: security-hardening/threat-hunting
trigger: "Hunting for adversary activity that no alert has caught."
anti_trigger: "Not for alert triage, and not for scoping a confirmed incident."
scope: "Hypothesis-driven hunts over telemetry, distinct from alert waiting."
status: seedling
---

# Threat hunting

## Standard

Hunting is the deliberate search for activity that the detections did not fire on, driven by a hypothesis about what an adversary would have had to do in this estate. The hypothesis is what separates hunting from browsing logs: a hunt states an assumed behavior, the telemetry that would show it, and what evidence would confirm or exclude it before the query runs. A hunt without a stated hypothesis is a tour, and tours find what searches always find.

The other half of the discipline is the negative result. Most hunts exclude the hypothesis, and an exclusion is a finding only if the telemetry actually covers the behavior — a hunt that found nothing over a log source that was never collected has not excluded anything. Recording what the hunt could and could not see is what makes its negative results usable and its coverage gaps into collection requirements.

Primary sources: <https://attack.mitre.org/> and <https://www.cisa.gov/>.

## Decision rules

- State the hypothesis as a behavior in this environment, not a generic threat.
- Name the telemetry that would evidence it and verify that telemetry is collected.
- Define the confirming and excluding evidence before querying.
- Record the hunt's result either way, with the time window searched.
- Convert every coverage gap found into a collection requirement.
- Feed confirmed hunts into new detections so the next occurrence alerts.

## Procedure

1. Write the hypothesis and its assumed behavior.
2. List the required telemetry and verify each source exists and retains.
3. Define confirmation and exclusion criteria.
4. Run the queries over a stated window.
5. Record result, evidence, and coverage limits.
6. Turn confirmations into detections and gaps into requirements.

## Anti-patterns

- Hunting without a hypothesis, by browsing.
- Treating a no-find as clean when the telemetry was missing.
- One-off hunts with no record of what was searched.
- Confirmed findings left as anecdotes instead of detections.
- Hypotheses copied from threat reports without mapping to this estate.

## Done checklist

- [ ] Hypothesis stated as estate-specific behavior.
- [ ] Telemetry verified collected and retained.
- [ ] Confirmation and exclusion criteria defined.
- [ ] Window searched recorded.
- [ ] Result recorded with coverage limits.
- [ ] Detections or collection requirements filed.

A hunt calendar is the complement to hypothesis discipline: recurring hunts against the techniques most likely for this estate keep the program from chasing only what last week's report mentioned, and the calendar itself documents what the program believes its threat space is.

## Sources

- Adversary behavior reference: <https://attack.mitre.org/>
- Hunting program guidance: <https://www.cisa.gov/>
- Telemetry standards context: <https://csrc.nist.gov/>
