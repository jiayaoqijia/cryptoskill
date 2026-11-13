---
name: rating-record
domain: investing/rating-record
trigger: "Writing the record of a credit's rating position and its exposures."
anti_trigger: "Not for recommending a credit, and not for the agency's own report."
scope: "The written record: rating, outlook, triggers, and exposure."
status: seedling
---

# Rating record

## Standard

The rating record states the rating by agency and scale, the outlook and any watch, the distance to each threshold that matters to the holder, and the contracts or mandates that reference a rating level. Those fields convert an opinion into a set of exposures: what must be sold, what must be posted, and what must be reviewed if the rating moves.

The record's second function is comparability. A rating quoted without its agency, its scale, and its date cannot be compared with another, and a portfolio aggregated across agencies without that discipline produces a composite that no agency would recognise. Stating each agency's view separately, rather than averaging, is what keeps the record honest about disagreement.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- Record each agency's rating, scale, and date separately.
- Record outlooks and watches with their assigned dates.
- Record the distance to every threshold the position is subject to.
- Record each contract or mandate that references a rating, with its consequence.
- Record the holder's own constraint: whether the position is eligible at each level.
- Record the review trigger for each threshold, not only the threshold itself.

## Procedure

1. Record ratings by agency with dates.
2. Record outlooks and watches.
3. Record threshold distances.
4. Record contractual references and consequences.
5. Record the eligibility constraint.
6. Set review triggers and file the record.

## Anti-patterns

- Averaging ratings into a composite.
- Recording a rating without its date.
- Omitting the contractual triggers.
- Leaving the holder's own eligibility unstated.
- Setting a threshold without a review trigger.

## Done checklist

- [ ] Ratings by agency recorded.
- [ ] Outlooks and watches recorded.
- [ ] Threshold distances recorded.
- [ ] Contractual references recorded.
- [ ] Eligibility recorded.
- [ ] Review triggers set.

The record's most useful column is the consequence beside each threshold: a threshold with no consequence is a number to watch, while one that forces a sale or a collateral posting is a date to prepare for, and conflating the two produces a watchlist where everything looks equally urgent until one of them is not.

Keeping the record for every holding rather than only for names near a threshold is what makes the aggregate visible: the exposure that matters is the sum of forced sales and collateral postings across the portfolio under a stress that hits several names at once, and that sum cannot be computed from a watchlist that only tracks the ones already close.

## Sources

- Credit rating disclosure: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Regulatory references to ratings: <https://www.bis.org/>
