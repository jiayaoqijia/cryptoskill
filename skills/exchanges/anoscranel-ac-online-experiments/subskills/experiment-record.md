---
name: experiment-record
domain: software-engineering/experiment-record
trigger: "Writing the record that makes an experiment auditable after the fact."
anti_trigger: "Not for the launch decision, and not for analytics implementation."
scope: "The written record: design, analysis plan, result, and the decision it drove."
status: seedling
---

# Experiment record

## Standard

The experiment record holds what an auditor needs to reconstruct what was measured and what was decided: the decision the experiment served, the hypothesis and OEC, the MDE and power, the assignment rule, the ramp history, the horizon, the guardrails with their states, every look that occurred, the analysis as planned, the result as measured, and the decision as taken. Written before launch and appended as the experiment runs, it converts an argument about what happened into a reading of what was recorded.

Its value compounds across the fleet. The record that captures "our click-through OEC moved but the pre-declared secondary metrics contradicted it" teaches the next design to add a broader OEC; a body of such records is how a platform learns which of its metrics lie. A record that captures only the final number teaches nothing.

Primary sources: <https://experimentguide.com/> and <https://www.exp-platform.com/>.

## Decision rules

- Record the decision, hypothesis, OEC, and decision rule before launch.
- Record MDE, power, horizon, and ramp schedule as declared.
- Append ramp steps, guardrail states, and every interim look with timestamps.
- Record the analysis as planned before running it, then the result as measured.
- Record the decision taken and whether it followed the pre-declared rule.
- Record the nulls and the reversals — the negative records teach the most.

## Procedure

1. Enter the design fields at launch approval.
2. Append each ramp change, guardrail state, and look at its own timestamp.
3. Freeze the analysis plan before the horizon completes.
4. Run the planned analysis; append the result and any pre-declared segment reads.
5. Append the decision taken, with the rule it followed or the reason it diverged.
6. Close with a one-paragraph retrospective: what the record teaches the next experiment.

## Anti-patterns

- Writing the record after the decision, from memory.
- Recording the result but not the looks that preceded it.
- Omitting the nulls or the reversed decisions.
- A record whose analysis section was written after seeing the data.
- Storing the launch facts separately from the outcome, so neither can be audited together.

## Done checklist

- [ ] Design fields recorded pre-launch.
- [ ] Ramp, guardrails, looks appended with timestamps.
- [ ] Analysis plan frozen before the horizon ended.
- [ ] Result and segment reads appended.
- [ ] Decision and rule recorded.
- [ ] Retrospective paragraph closed the record.

## Sources

- Experimentation records at platform scale: <https://experimentguide.com/>
- Experimentation platform history: <https://www.exp-platform.com/>
- Overview: <https://en.wikipedia.org/wiki/A/B_testing>
