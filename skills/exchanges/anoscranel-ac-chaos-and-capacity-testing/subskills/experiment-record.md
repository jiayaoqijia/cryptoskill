---
name: experiment-record
domain: software-engineering/experiment-record
trigger: "Writing the record of a chaos or capacity experiment."
anti_trigger: "Not for incident postmortems, and not for test plans."
scope: "The written record: hypothesis, method, result, and follow-up."
status: seedling
---

# Experiment record

## Standard

The experiment record states the hypothesis, the method, the result, and the follow-up, with the system version and configuration it applies to. Its value is that it makes the experiment reproducible: a later team can rerun it and see whether the system still behaves as it did, which is the only way a capacity or resilience claim stays true.

The follow-up section is where the record becomes an engineering artefact rather than a report. Every experiment produces either a change to the system or a change to the expectation, and a record that names neither has produced a document. The follow-up carries an owner and a date, so the finding is either acted on or explicitly accepted.

Primary sources: <https://principlesofchaos.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the hypothesis as an observable statement written before the experiment.
- The method is recorded precisely enough to repeat.
- The result compares observation with expectation, including where they diverged.
- The system version, configuration, and date are recorded.
- The follow-up names a change to the system or an accepted expectation, with an owner.
- Review triggers are dated: system change, capacity shift, new dependency.

## Procedure

1. Record the hypothesis before running anything.
2. Record the method and the parameters.
3. Record the observations and the comparison.
4. Record the version, configuration, and date.
5. Record the follow-up with an owner.
6. Revisit at each trigger and record whether the result still holds.

## Anti-patterns

- A record written from memory after the experiment.
- A method described so loosely it cannot be repeated.
- Reporting the result without the version it applies to.
- Findings without owners.
- No triggers, so a stale result is read as current.

## Done checklist

- [ ] Hypothesis recorded before the run.
- [ ] Method and parameters recorded.
- [ ] Result compared with expectation.
- [ ] Version, configuration, date recorded.
- [ ] Follow-up with owner recorded.
- [ ] Triggers dated.

The record also serves as evidence that the experiment was authorised: a written hypothesis, a stated blast radius, and a named abort authority are what distinguish a controlled test from an unplanned production change, and the record is the artefact that shows the difference after the fact.


The record should also name what was not tested, because the boundary of an experiment is as informative as its result: a resilience claim that rests on one injected fault is a claim about that fault, and stating the untested dependencies prevents the finding from being generalised further than the evidence supports.

## Sources

- Chaos engineering principles: <https://principlesofchaos.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Reliability engineering guidance: <https://sre.google/>
