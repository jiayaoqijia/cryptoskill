---
name: golden-path
domain: software-engineering/golden-path
trigger: "Defining the recommended path through a platform and proving it is shorter."
anti_trigger: "Not for toolchain selection, and not for pipeline design."
scope: "The recommended path, what it shortens, and how adoption is measured."
status: seedling
---

# Golden path

## Standard

A golden path is the one way through the platform that the platform team recommends, supports, and keeps working. It is not a restriction on other approaches; it is a promise that this path is maintained, documented, and faster than assembling the pieces yourself. Its value depends entirely on that comparison being true.

The comparison is measurable. Walking the path from an empty repository to a deployed service takes a number of steps, a number of decisions, and an amount of waiting, and the alternative can be measured the same way. A golden path that saves two steps while forcing a migration is not shorter in practice, and stating the measurement is what prevents the platform from being designed for its own convenience.

Primary sources: <https://dora.dev/> and <https://sre.google/>.

## Decision rules

- Record the path's start and end states, precisely enough to be walked.
- Record the steps and decisions it removes compared with the alternative.
- Record the time from start to deployed service, measured on a real attempt.
- Record who has walked it outside the platform team, since their experience is the test.
- Record what the path does not cover, so its boundary is known.
- Record the maintenance commitment: what breaks the path and who fixes it.

## Procedure

1. Record the start and end states.
2. Walk the path and record each step and each decision required.
3. Measure the elapsed time on a clean attempt.
4. Have someone outside the team walk it and record their friction.
5. Record the omitted scope and the maintenance commitment.
6. Write the path with its measured comparison.

## Anti-patterns

- A path defined by the platform team's own workflow.
- Measuring the path only after the environment is already configured.
- Assuming adoption because the path exists.
- A path that covers the easy half and leaves the hard decisions open.
- No maintenance commitment, so the path decays into documentation.

## Done checklist

- [ ] Start and end states recorded.
- [ ] Steps and decisions recorded.
- [ ] Elapsed time measured.
- [ ] Outside walk recorded.
- [ ] Omitted scope recorded.
- [ ] Maintenance commitment recorded.

The path should also be walked by someone who did not help design it, because the platform team's own familiarity hides the steps that require implicit knowledge: the environment variable nobody documented, the permission granted months ago, the tool installed personally. Recording where the outside walker got stuck is the most useful output of the exercise.


## Sources

- Software delivery performance research: <https://dora.dev/>
- Reliability and platform practice: <https://sre.google/>
- Developer productivity context: <https://dora.dev/research/>
