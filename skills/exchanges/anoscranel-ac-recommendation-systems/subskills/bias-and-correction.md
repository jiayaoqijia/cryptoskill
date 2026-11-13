---
name: bias-and-correction
domain: software-engineering/bias-and-correction
trigger: "Recognizing that the log records the ranking you served, not preference."
anti_trigger: "Not for experiment design, and not for the scoring loss."
scope: "Position, popularity, and feedback loops; counterfactual remedies."
status: seedling
---

# Bias and correction

## Standard

The interaction log is an observation of the system's own output, and three biases distort it before any analysis begins. Position bias: items shown high are clicked more regardless of quality, so the log overstates preference for what the ranker already liked. Popularity bias: shared items collect interactions simply by being everywhere, so head items crowd the tail in every learned signal. Feedback-loop bias: the model trains on its own outputs and re-serves them, and yesterday's ranking becomes tomorrow's data — a closed loop in which the recommender converges on its own reflection.

The remedies are counterfactual in spirit: position-debiasing or inverse-propensity weighting lets training re-weight interactions by how likely each was to be shown in the first place; interleaving or counterfactual evaluation compares rankers under equivalent exposure rather than between staggered deployments; and a small reserved exploration budget keeps regions of the catalogue observable that the ranker would otherwise never visit. The correction is chosen by which bias dominates your surface, and each carries its own measurement — an uncorrected popular-item boost looks like a quality result until it is tested against equal exposure.

Primary sources: <https://en.wikipedia.org/wiki/Recommender_system> and <https://en.wikipedia.org/wiki/Collaborative_filtering>.

## Decision rules

- Name the dominant bias per surface; position dominates ranking surfaces; popularity dominates feeds and discovery; the loop dominates all.
- The propensity or weighting used for correction is itself measured; the correction applied blindly becomes a new bias.
- A reserved exploration budget exists by design, sized by stated percentage, not by an ad-hoc trial of leftovers.
- Ranker comparison uses counterfactual or interleaved evaluation where the property allows; the plain old A/B is the fallback, never the assumption.
- Every interaction carries the serve context — position, alternatives shown — so correction and analysis can happen.
- Popularity and sharing metrics are reported alongside personalization metrics; a system can look accomplished while narrowing.

## Procedure

1. Measure the biases present per surface: click rates by position, interaction concentration by item popularity, and ranking self-overlap over time.
2. Choose per-surface correction: position-debiasing, inverse-propensity weighting, or model-level correction.
3. Record the serve context with interactions so correction has its inputs.
4. Reserve an exploration percentage per surface and measure its catalogue coverage per unit time.
5. Set up a counterfactual or interleaved comparison where the product permits.
6. Re-measure after each correction ships; corrections drift as the loop adapts.

## Anti-patterns

- Reporting improved clicks after promoting a position-heavy item without position correction.
- An exploration budget of zero, because the team sees it as a cost; the catalogue becomes unobservable.
- Treating popularity as quality; a shared item is shared, not preferred.
- Interactions stripped of context at ingestion, discarding the only inputs correction needs.
- The correction itself unreviewed for multiple cycles; the model's assumptions age silently.

## Done checklist

- [ ] Dominant bias named per surface with measurements.
- [ ] Correction chosen per surface, with the correction's inputs recorded.
- [ ] Serve context stored with every interaction.
- [ ] Exploration budget exists and is measured.
- [ ] Counterfactual or interleaved comparison configured where the surface allows.
- [ ] Correction effects re-measured on a schedule.

## Sources

- Recommender system overview: <https://en.wikipedia.org/wiki/Recommender_system>
- Collaborative filtering: <https://en.wikipedia.org/wiki/Collaborative_filtering>
- Learning to rank: <https://en.wikipedia.org/wiki/Learning_to_rank>
