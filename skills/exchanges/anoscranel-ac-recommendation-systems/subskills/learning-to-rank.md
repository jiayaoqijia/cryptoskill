---
name: learning-to-rank
domain: software-engineering/learning-to-rank
trigger: "Choosing the scoring model and the loss it is trained toward."
anti_trigger: "Not for candidate retrieval, and not for offline metric arithmetic."
scope: "The scorer, its features, and its loss tied to the decision."
status: seedling
---

# Learning to rank

## Standard

The scoring stage turns a user, an item, and their context into an ordering, and its centre of gravity is the loss function. Pointwise losses score each item independently against a target and are easy to train but bake absolute-quality thinking into a system whose job is relative choice. Pairwise losses compare item pairs and match the ranking task better — getting the order right — while listwise losses optimize a metric over the whole slate and match the served experience best at the cost of implementation complexity. The loss is not a library default; it is a statement about which decisions the model is being asked to get right.

The honest default is the tuple that holds the whole scorer together: features (user, item, context, cross-features like "did this user interact with items like this one in this surface"), the loss, and the training window. Each member of the tuple changes the semantics of the others; a fresh feature set against a stale window is a different model wearing the same name, and cross-features computed from a different source than the one live serving reads invites skew between what was trained and what is scored.

Primary sources: <https://en.wikipedia.org/wiki/Recommender_system> and <https://en.wikipedia.org/wiki/Learning_to_rank>.

## Decision rules

- Choose the loss deliberately from pointwise, pairwise, listwise; write down which decision it is meant to get right.
- Feature computation is shared between training and serving, or skew is measured continuously; two implementations need a diff harness.
- Training window recent enough to reflect the current catalogue and behaviour; parameterized slack as a stated compromise.
- Context features which surface and position the item will appear in; a scorer blind to surface produces one list treated as everything.
- Feature version discipline: new features and removed features are model version bumps, not silent edits.
- This stage's evaluation metrics are the scorer's cross-entropy or ranking loss offline; product outcomes separately come from online experiment.

## Procedure

1. Decide the loss class and its rationale; record it in the record.
2. Design the feature set: user-side, item-side, context, cross-features; name the source and freshness of each.
3. Verify that the training pipeline and the serving path compute cross-features identically.
4. Set the training window and schedule; document the staleness compromise.
5. Train, validate on offline metrics for the loss; iterate on features and window; record each dismissible variant.
6. Ship through the online experiment; the offline result was a hypothesis.

## Anti-patterns

- Library default losses with the catalogue, timeframe, and intent unexamined.
- A one-implementation-fits-all-serve scoring layer for the whole product, with only position adjustments to help.
- Cross-features trained from batch but served from an online store; train-serve skew masquerading as model degradation.
- A window set for convenience; the model is always learning the previous catalogue.
- Offline-only validation cycles ending in a release with no experiment.

## Done checklist

- [ ] Loss chosen and its rationale recorded.
- [ ] Feature set designed with source and freshness named per feature.
- [ ] Train-serve skew measured or eliminated.
- [ ] Training window parameterized and scheduled.
- [ ] Offline evaluation attached to the loss class.
- [ ] Online experiment as the ship gate.

## Sources

- Recommender overview: <https://en.wikipedia.org/wiki/Recommender_system>
- Learning to rank: <https://en.wikipedia.org/wiki/Learning_to_rank>
- Collaborative filtering: <https://en.wikipedia.org/wiki/Collaborative_filtering>
