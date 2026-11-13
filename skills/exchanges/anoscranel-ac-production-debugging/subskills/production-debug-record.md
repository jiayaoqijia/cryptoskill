---
name: production-debug-record
domain: software-engineering/production-debug-record
trigger: "Writing the record of a production debugging episode."
anti_trigger: "Not for the blameless postmortem of the incident (that is ac-reliability)."
scope: "The written debug record: symptom, evidence, hypothesis, test, outcome."
status: seedling
---

# Production debug record

## Standard

The production debug record is the working document of one debugging episode, kept from the first evidence capture to the final change. It differs from an incident report: that is about communication and follow-ups, while this is about the investigation itself — what was suspected, what was tested against logs, what the captures showed, and what was ruled out. Investigations without a record repeat themselves when the same failure returns next month.

Its core value is the ruled-out list. A future investigator facing the same symptom inherits not only the fix but the dead ends: the hypotheses already tested, the log patterns already searched, the tools that perturbed the failure away. Writing down what did not work is what stops a team from re-running the same five searches every incident.

## Decision rules

- Record the symptom verbatim with the first timestamp it occurred.
- Attach the evidence index: which captures exist, where, and their labels.
- Record each hypothesis with the test's result including refuted and undetermined.
- Maintain the ruled-out list until the episode closes.
- Record the perturbation warning if observation changed the failure.
- At closure, record the verification that the fix caused the symptom to stop.

## Procedure

1. Write the symptom and the timeline of occurrences.
2. Index captured evidence with pointers to labelled files.
3. Log each hypothesis and its test result as it happens.
4. Add ruled-out entries as they die.
5. On closure, record the fix and the evidence that verifies it.
6. Link the record from the incident report and from future similar symptoms.

## Anti-patterns

- A record that lists only the winning hypothesis.
- Evidence left on a decommissioned host with no copy.
- "Could not reproduce" with no note of what was tried.
- Recording an observation without its perturbation warning.
- No verification step — the fix shipped, the symptom persisted, nobody logged it.

## Done checklist

- [ ] Symptom and timeline recorded.
- [ ] Evidence index with pointers.
- [ ] Hypothesis log with test results.
- [ ] Ruled-out list maintained.
- [ ] Perturbation warnings recorded.
- [ ] Closure verification recorded.

A record of this shape also compounds across incidents: the ruled-out lists of three episodes with the same signature often point at the one hypothesis nobody has tested, so the record should be findable by symptom keywords, not only by incident number.

## Sources

- Google SRE debugging practice: <https://sre.google/sre-book/debugging-tips/>
- Incident analysis writing: <https://sre.google/sre-book/postmortem-culture/>
- Evidence standards for postmortems: <https://learn.microsoft.com/en-us/azure/well-architected/>
