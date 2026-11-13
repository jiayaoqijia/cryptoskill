---
name: filtering-and-diversity
domain: software-engineering/filtering-and-diversity
trigger: "Final ranking rules beyond the score: coverage, repetition, and fatigue."
anti_trigger: "Not for the scorer, and not for exploration policy."
scope: "Final ranking: coverage, repetition, and fatigue as explicit rules."
status: seedling
---

# Filtering and diversity

## Standard

The output of the scorer is an ordering by predicted engagement, and it is not yet a feed. Left alone, an engagement-maximizing ordering concentrates: the same strong items repeat, near-duplicates of whatever recently performed cluster together, and one taste dimension captures the slate. The final ranking layer applies explicit rules — eligibility filters, freshness, repetition windows, category quotas, creator or source caps, similarity anti-clustering — and each rule is a deliberate product decision recorded with its parameters, not a patch quietly added when someone complained.

Diversity rules are where the most confusion lives, because there are two distinct goals wearing the same word. Calibration means the slate reflects the user's broad taste distribution rather than its modal point; coverage means the user encounters categories they rarely engage. Both trade raw session engagement for long-horizon value, and both fail invisibly when they are implemented as a tuning knob rather than as a set of written rules with parameters someone owns. The wall clock of fatigue: repetition rules decide whether the user sees the same item twice in a week, and their absence is why every feed eventually feels like a corridor.

Primary sources: <https://en.wikipedia.org/wiki/Recommender_system> and <https://en.wikipedia.org/wiki/Collaborative_filtering>.

## Decision rules

- Hard filters and soft rules are separated: eligibility is never a score adjustment; score is never a policy smuggle.
- Every post-scoring rule has a parameter set, an owner, and a place in the record; nothing silent in the last mile.
- Repetition windows per surface are explicit: how soon an item may return, and what counts as the same item.
- Category and creator quotas are recorded with the diversity goal they serve — calibration versus coverage — because they are different arguments.
- The rules are evaluated: their effect on the final slates is measured with the same discipline as the scorer.
- Rules ship and change through the same experiment path as the scorer; no rule sneaks into production as either a quick fix or a launch-day reflex.

## Procedure

1. Separate the hard eligibility layer from the rest; review its business rules for encoded product decisions that belong in the record.
2. Design the repetition, quota, and novelty-carry rules per surface; write their parameters.
3. State which diversity goal each rule serves: calibrated taste reflection or novel coverage.
4. Run the rules over recent scorer outputs; measure the composition changes they produce.
5. Ship rules through the same experiment and review path as model changes; read their slates' measured effect.
6. Review the rules on the product cadence; fatigue parameters age like everything else.

## Anti-patterns

- An eligibility check that quietly re-ranks; a score threshold that quietly filters.
- Repetition windows nobody wrote; identical slates across sessions and the user wanders off.
- Category quotas tuned to chase engagement, destroying the coverage argument that justified them.
- Rules editing outputs in production as a hotfix, invisible to the record.
- Different rule sets across surfaces with nobody able to say why.

## Done checklist

- [ ] Eligibility layer separated from ranking rules.
- [ ] Per-surface repetition and quota parameters written and owned.
- [ ] Each diversity rule's goal type stated.
- [ ] Rule effects measured on real slates.
- [ ] Rules ship through experiments like any change.
- [ ] Review cadence set for fatigue parameters.

## Sources

- Recommender overview: <https://en.wikipedia.org/wiki/Recommender_system>
- Collaborative filtering: <https://en.wikipedia.org/wiki/Collaborative_filtering>
- Learning to rank: <https://en.wikipedia.org/wiki/Learning_to_rank>
