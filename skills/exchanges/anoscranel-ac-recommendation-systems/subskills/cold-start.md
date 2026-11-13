---
name: cold-start
domain: software-engineering/cold-start
trigger: "Making the system work for users and items it has never seen."
anti_trigger: "Not for the scoring loss, and not for content retrieval internals."
scope: "The bootstrap sequence for new users and new items."
status: seedling
---

# Cold start

## Standard

A new user has no history and a new item has no interactions, and both arrive constantly in a live catalogue. The recommender's answer cannot be "wait until the data exists", because the first session decides whether there will be a second. Cold start is therefore a designed bootstrap sequence, not a fallback: for new users, start from declared signals — onboarding choices, entry-point context, popularity within a peer segment — and narrow toward personalization as interactions accumulate; for new items, start from content signals, editorial placement, controlled exploration traffic, and structured metadata until co-occurrence data accrues.

The critical discipline is transitional honesty: the system should know which regime it is in. A user in their first session is being served exploratory and popular content, and the record of that fact is what prevents the interaction log from being read later as if those were personalized endorsements. Cold-start serve decisions are labelled at serve time so downstream analysis and correction can distinguish preference from placement.

Primary sources: <https://en.wikipedia.org/wiki/Collaborative_filtering> and <https://en.wikipedia.org/wiki/Content-based_filtering>.

## Decision rules

- A user or item is in a cold-start regime until a stated interaction threshold is passed; the regime is recorded at serve time.
- New users see declared-signal and segment-popularity content, with the mix specified; nothing pretends to be personalized before it is.
- New items get entry channels by design: content retrieval, structured placement, reserved exploration quota.
- Each serve during a cold-start regime is labeled in the log with the regime name so later interpretation can account for it.
- The transition out of cold start is a deliberate handover, not a drift: rules for when content weighting shifts from entry channels to interaction-driven.
- Items that stay cold after their entry window are reviewed, not stranded silently.

## Procedure

1. Write the definition of the cold regimes: which interactions count and what threshold ends each.
2. For new users, define the serve mix by source and weight; declare the onboarding and entry-context signals it uses.
3. For new items, write their entry channels with the exploration quota they receive and for how long.
4. Label every serve with the regime it was in; log it with the interaction.
5. Write the handover rules from entry channels to interaction-driven sources; verify by category.
6. Review stranded items and non-converting cold users as a product signal, not as model noise.

## Anti-patterns

- Serving blank or error states because the model found "no signal".
- Pretending top-popularity content is personalized; the user's inferred taste is quietly miscalibrated by what they clicked in that regime.
- New items launched with zero reserved traffic; they never accrue data and the catalogue narrows.
- No serve-time labels, so a later analysis cannot tell placement-driven clicks from preference-driven ones.
- A cold-start threshold so high that personalization never engages for the median user.

## Done checklist

- [ ] Cold regimes defined with thresholds.
- [ ] New-user serve mix stated and implemented.
- [ ] New-item entry channels with exploration quota.
- [ ] Serve-time regime labels in the log.
- [ ] Handover rules written and verified by category.
- [ ] Stranded-item reviews scheduled.

## Sources

- Collaborative filtering limits: <https://en.wikipedia.org/wiki/Collaborative_filtering>
- Content-based signals: <https://en.wikipedia.org/wiki/Content-based_filtering>
- Recommender overview: <https://en.wikipedia.org/wiki/Recommender_system>
