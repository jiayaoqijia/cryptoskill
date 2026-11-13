---
name: feedback-signals
domain: software-engineering/feedback-signals
trigger: "Deciding what the interaction log can honestly tell you."
anti_trigger: "Not for retrieval mechanics, and not for online measurement of changes."
scope: "Implicit and explicit data, and what each honestly measures."
status: seedling
---

# Feedback signals

## Standard

Explicit feedback — ratings, thumbs, saves — is a direct statement of preference, and it is rare, skewed toward the extremes, and given by an unrepresentative minority of users. Implicit feedback — views, plays, clicks, dwell, purchases, skips — is abundant and everyone contributes, but each signal is a mixture: a click says the item won the ranking it appeared in, at that position, in that context, against those alternatives; it does not say the item was good, and it certainly does not say a non-click was a negative.

The design question is which mixture you are willing to model. Treating every click as a positive and every non-click as a negative bakes the ranking's own footprint into the training data. Treating clicks as weak evidence with weights, and absences as unknown rather than negative, costs more modelling effort and leaves the data slower to use; it also removes the loop where days of self-confirmation arrive dressed as learning.

Primary sources: <https://en.wikipedia.org/wiki/Recommender_system> and <https://en.wikipedia.org/wiki/Collaborative_filtering>.

## Decision rules

- Name each signal the system collects as explicit or implicit, and write down what mixture the training treats it as.
- Weighted implicit is the default posture; unweighted all-positives requires a stated reason.
- Non-interactions are unknown, not negative; treating them as negative needs a specific justification.
- Signal provenance — which surface, which impression, which position — is recorded because it carries the bias any later correction needs.
- The most recent interactions count more than old ones; decay is a stated parameter, not a tuning accident.
- The set of signals and their weights are versioned with the model; a change to weight semantics is a data change.

## Procedure

1. Inventory the collected signals; classify each as explicit or implicit.
2. For each implicit signal, write the claim it licenses: won an impression, held attention for N seconds, converted, was skipped.
3. Choose per-signal weights and the non-interaction stance; record both with reasons.
4. Attach impression context — surface, position, alternatives shown — to every stored interaction.
5. Set the decay parameter explicitly and revisit it at each model review.
6. Version the signal definition set with the model identifier.

## Anti-patterns

- One-click equals one positive, non-click equals one negative, and the loop learned its own reflection.
- Treating a thumbs-down as equally-weighted evidence against as a click is evidence for — the asymmetry is the point.
- Signals from different surfaces pooled without context, because a mobile feed's click and a search-result's click mean different things.
- A decay parameter nobody set, inherited from a library default.
- Retuning weights to chase an offline metric that rewards the loop.

## Done checklist

- [ ] Every signal classified with its licensed claim.
- [ ] Weights and non-interaction stance chosen and recorded.
- [ ] Impression context stored with interactions.
- [ ] Decay set deliberately and revisited.
- [ ] Mixture semantics versioned with the model.
- [ ] Signal inventory reviewed with the product's actual meaning.

## Sources

- Recommender system overview: <https://en.wikipedia.org/wiki/Recommender_system>
- Collaborative filtering: <https://en.wikipedia.org/wiki/Collaborative_filtering>
- Content-based filtering: <https://en.wikipedia.org/wiki/Content-based_filtering>
