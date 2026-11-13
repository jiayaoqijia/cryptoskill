---
name: game-days-and-hypotheses
domain: software-engineering/game-days-and-hypotheses
trigger: "Running a game day with a stated expectation and time box."
anti_trigger: "Not for incident response, and not for unplanned experiments."
scope: "A stated expectation, a time box, and what counts as a finding."
status: seedling
---

# Game days and hypotheses

## Standard

A game day is a scheduled experiment in which a team expects a specific behaviour and watches whether the system delivers it. The expectation is the point: without one, the exercise produces anecdotes about what happened rather than a comparison between what was designed and what exists, and anecdotes do not accumulate into knowledge.

The time box protects the exercise from becoming an incident. A game day has a start, a duration, a stop condition, and a debrief, and the debrief is where the value is captured — not in the injection itself but in the gap between the expected behaviour and the observed one, and in the decision about whether to change the system or the expectation.

Primary sources: <https://principlesofchaos.org/> and <https://sre.google/>.

## Decision rules

- Record the hypothesis as a specific observable statement, not a general hope.
- Record the time box and the stop condition.
- Record the participants and their roles: operator, observer, and abort authority.
- Record what would falsify the hypothesis.
- Record the debrief within a stated interval after the exercise.
- Record the follow-up as a change to the system or to the expectation, with an owner.

## Procedure

1. Write the hypothesis as an observable statement.
2. Set the time box and the stop condition.
3. Assign roles and record who holds abort authority.
4. Run the exercise and record the timeline.
5. Debrief the gap between expectation and observation.
6. Record follow-ups with owners and dates.

## Anti-patterns

- Running a game day as a surprise drill rather than a stated experiment.
- No falsification condition, so any outcome confirms the hypothesis.
- Debriefing weeks later when memory has faded.
- Recording findings without owners.
- Repeating the same exercise to watch the same behaviour.

## Done checklist

- [ ] Hypothesis recorded as observable.
- [ ] Time box and stop condition recorded.
- [ ] Roles and abort authority recorded.
- [ ] Falsification condition recorded.
- [ ] Debrief held and recorded.
- [ ] Follow-ups with owners recorded.

The exercise is also a test of the team rather than only the system: who notices, who escalates, and who has the authority to stop it are all observable during a game day, and those observations are often more actionable than the technical finding because they cannot be fixed by a code change alone.


## Sources

- Chaos engineering principles: <https://principlesofchaos.org/>
- Reliability practice: <https://sre.google/>
- Incident and exercise guidance: <https://www.cncf.io/>
