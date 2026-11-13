---
name: exploration-and-coverage
domain: software-engineering/exploration-and-coverage
trigger: "Deliberately exploring the catalogue to keep learning alive."
anti_trigger: "Not for the exploration-exploitation of bandits in general, and not for diversity rules."
scope: "Exploration as part of design, not an accident of randomness."
status: seedling
---

# Exploration and coverage

## Standard

Exploration is the budget the recommender spends on learning what it does not yet know, and it is bought, not found. The system's learned signals concentrate where it already serves confidently; that is efficient locally and impoverishing globally, because the measurement then cannot see what would have happened in the unvisited regions. The exploration quota — a percentage of impressions per surface reserved for under-exposed items, new candidates, or controlled probes — is the instrument that keeps the catalogue observable and the model correctable.

The design decisions are size, allocation, and honesty. Size: a percentage per surface, stated and reviewed, not an emergent behaviour of whatever the ranker happened to be uncertain about. Allocation: which items, which surfaces, how often — the exploration budget spent on genuinely informative probes, not scattered across the tail as noise. Honesty: explorations are labelled in serve context like cold-start serves are, because the purpose of the budget is to produce accurate information about under-explored regions, and unlabelled exploration poisons the very signal it exists to collect.

Primary sources: <https://en.wikipedia.org/wiki/Multi-armed_bandit> and <https://en.wikipedia.org/wiki/Collaborative_filtering>.

## Decision rules

- The exploration quota is a percentage per surface, documented and reviewed on a schedule, not residual.
- The quota's allocation rule is written: what classes of items, how often, on which surfaces.
- Exploration serves carry the label in the log; the signal is only good if it can be recognized as an exploration measurement.
- The value of exploration is measured: interactions with explored items versus the counterfactual; a range of checks confirms the budget is still informative.
- An exploration budget is never spent by silently inflating a popularity tier; that is popularity, not exploration.
- Cold-start entry channels and the exploration budget interact: their combined exposure is the policy and both are labelled.

## Procedure

1. Set the per-surface quota in percent of impressions, with its rationale, in the record.
2. Write the allocation rules that designate exploration candidates: new items, under-exposed tail, or model-uncertain regions.
3. Label explorations in the serve context, and log the assignment.
4. Measure interactions and outcomes on explored cohorts against non-explored equivalents where possible.
5. Report the catalogue coverage per unit time that the budget produces, by category, not just by count.
6. Revisit size and allocation at the product cadence; the budget ages as the catalogue ages.

## Anti-patterns

- Zero exploration because engagement dips; the regions become unobservable and the system ossifies.
- Exploration that puts everything into already-famous items; that is a popularity tier in a costume.
- Unlabelled exploration leading to the discovery of surprise results nobody can explain later.
- A budget nobody measures, because exploration outcomes disappear into aggregate engagement reports.
- The quota competing directly with the diversity rules for space rather than two named policies divided deliberately.

## Done checklist

- [ ] Quota defined per surface with rationale.
- [ ] Allocation rules written and implemented.
- [ ] Exploration serves labelled in the log.
- [ ] Outcomes measured against equivalent controls.
- [ ] Catalogue coverage per unit time reported by category.
- [ ] Quota reviewed on the product cadence.

## Sources

- Multi-armed bandits and exploration: <https://en.wikipedia.org/wiki/Multi-armed_bandit>
- Collaborative filtering: <https://en.wikipedia.org/wiki/Collaborative_filtering>
- Recommender overview: <https://en.wikipedia.org/wiki/Recommender_system>
