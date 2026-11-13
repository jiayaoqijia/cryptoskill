---
name: scenario-record
domain: investing/scenario-record
trigger: "Writing the record of a stress test and its outcome."
anti_trigger: "Not for predicting outcomes, and not for risk policy."
scope: "The written record: scenario, assumptions, result, and action."
status: seedling

---

# Scenario record

## Standard

The scenario record holds the scenario as constructed, the assumptions it rests on, the criterion it was judged against, the result, and the action attached. Written this way, a series of tests becomes comparable across reviews, and a later reader can tell whether a change in the result came from the portfolio or from a change in the scenario.

The assumptions deserve particular attention because they are where a pass is manufactured. Correlations, liquidity, and the treatment of positions that cannot be valued are the three that most often decide the outcome, and recording them explicitly means that a test which passes on generous assumptions is identifiable as such rather than appearing equivalent to one that passed on conservative ones.

Primary sources: <https://www.bis.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the mechanism and the moves with their horizon.
- Assumptions on correlations, liquidity, and valuation are recorded separately.
- The criterion is recorded with the date it was set.
- The result is recorded against the criterion, with the largest contributing positions.
- The action attached is recorded with an owner and a date.
- The record is versioned; a changed scenario produces a new entry, not an edit.

## Procedure

1. Record the scenario and its mechanism.
2. Record the assumptions separately.
3. Record the criterion and its date.
4. Record the result and the largest contributors.
5. Record the action, owner, and deadline.
6. File as a new entry on any change.

## Anti-patterns

- Recording the result without the assumptions.
- Editing the scenario after the result to make it comparable with a prior test.
- Omitting the largest contributing positions, which is where the finding lives.
- An action with no owner.
- Recording a pass without noting which assumption was generous.

## Done checklist

- [ ] Scenario and mechanism recorded.
- [ ] Assumptions recorded separately.
- [ ] Criterion and date recorded.
- [ ] Result and contributors recorded.
- [ ] Action with owner recorded.
- [ ] Entry versioned.

The series is also the artefact that makes a test useful over time: a single result describes a portfolio, while a series of comparable results describes whether the portfolio's vulnerability is changing, and only the second can inform a decision about whether to act.


A record that names the largest contributing positions also makes the next test cheaper to design, since the same exposures can be tested with a different mechanism rather than rebuilding the scenario from scratch.


## Sources

- Stress testing documentation standards: <https://www.bis.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on risk reporting: <https://www.investor.gov/introduction-investing>
