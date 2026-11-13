---
name: randomisation-and-bucketing
domain: software-engineering/randomisation-and-bucketing
trigger: "Assigning users to arms so the comparison is valid."
anti_trigger: "Not for outcome analysis, and not for deployment rollout."
scope: "Units, hash assignment, and the leakage that breaks an experiment."
status: seedling
---

# Randomisation and bucketing

## Standard

Assignment maps each experiment unit to an arm through a hash of the unit's identifier and the experiment's salt, bucketed into equal shares. The unit is the entity that experiences the treatment and is measured — usually a user, sometimes a session, a page, or a request when users cannot be identified. Two arms are comparable only when assignment depends on nothing but the hash: any path where the treatment Experience correlates with assignment reintroduces exactly the selection bias the randomisation was built to remove.

The craft is in the failure modes. Assignment must be stable — a user who sees the treatment on Monday and the control on Tuesday measures noise, not the treatment. It must be immediate — assignment at first exposure, recorded then, even if the treatment renders later. And it must be complete — every unit that experiences the treatment appears in the experiment's logs, because a dashboard that only counts units that rendered is conditioning on the treatment working.

Primary sources: <https://experimentguide.com/> and <https://en.wikipedia.org/wiki/A/B_testing>.

## Decision rules

- Choose the randomisation unit to match how the treatment is experienced and measured.
- Assign by hashing a stable identifier with the experiment salt; never by mod of an unstable count.
- Pin assignment from first exposure and persist it for the experiment's life.
- Log every assignment, including units that never render the treatment.
- Verify with a sample ratio check: arms should be equal within sampling error, and a skew is a bug.
- Isolate interference: if units interact (marketplaces, messaging), choose a unit that does not leak across arms.

## Procedure

1. Select the randomisation unit and justify it against the treatment's blast radius.
2. Implement hash-based assignment with the experiment salt and equal bucket share.
3. Store assignment at first exposure with the assignment timestamp.
4. Instrument logging before the first exposure can occur.
5. Run the sample ratio check on the first day's traffic and at scale.
6. Document the assignment rule in the experiment record.

## Anti-patterns

- Assigning by time of day, request order, or any user-visible property.
- Re-randomising on each visit and calling it a fresh sample.
- Counting only rendered units and accepting a selection-biased comparison.
- Sharing treatment across a social graph that crosses arm boundaries.
- Fixing an assignment bug mid-experiment without restarting the analysis.

## Done checklist

- [ ] Randomisation unit justified.
- [ ] Hash assignment with salt implemented.
- [ ] Assignment persisted from first exposure.
- [ ] All assignments logged.
- [ ] Sample ratio check run and passed.
- [ ] Interference isolation documented.

## Sources

- Assignment and validity: <https://experimentguide.com/>
- Experiment design overview: <https://en.wikipedia.org/wiki/A/B_testing>
- Book companion site: <https://www.exp-platform.com/>
