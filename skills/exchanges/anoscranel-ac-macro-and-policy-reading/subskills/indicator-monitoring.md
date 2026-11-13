---
name: indicator-monitoring
domain: investing/indicator-monitoring
trigger: "Building a small macro monitoring set with a cadence and revision discipline."
anti_trigger: "Not for forecasting, and not for trading every release."
scope: "A small monitoring set, its update cadence, and the revisions that change a reading."
status: seedling
---

# Indicator monitoring

## Standard

A monitoring set is a small number of series that together describe the economy the portfolio is exposed to, updated on a schedule, with revisions tracked. The value is in the consistency: the same series, read the same way, across time, so that a change in the reading is a change in the economy rather than a change in the dashboard.

The failure mode is the expanding dashboard: indicators are added after each surprise until nothing is comparable and everything confirms something. A set of five to ten series, chosen before the surprises, is more useful than fifty chosen after them.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Choose the series before the next surprise, and record why each is included.
- Record the update frequency and the revision schedule per series.
- Read the same transformation each time: level, change, or year-over-year.
- Track revisions to past readings and note when a revision changes a conclusion.
- Cap the set; an addition requires removing something or a written reason.
- Record the reading with its date and the data's vintage.

## Procedure

1. Choose five to ten series with a reason each.
2. Record frequency and revision schedule per series.
3. Fix the transformation used for each.
4. Record readings on a schedule with the vintage.
5. Track revisions and flag changes to conclusions.
6. Review the set annually, with additions requiring a removal or a reason.

## Anti-patterns

- Adding indicators after each surprise.
- Comparing readings taken with different transformations.
- Ignoring revisions to past readings.
- Reading every release as a trading signal.
- Using a series whose definition changed without a break note.

## Done checklist

- [ ] Series chosen with reasons.
- [ ] Frequency and revision schedule recorded.
- [ ] Transformation fixed per series.
- [ ] Readings recorded with vintage.
- [ ] Revisions tracked with conclusion changes.
- [ ] Annual review with the addition rule.

## Sources

- Macro series and vintages: <https://fred.stlouisfed.org/>
- Investor education on economic indicators: <https://www.investor.gov/introduction-investing>
- Regulatory context for official statistics: <https://www.sec.gov/investor>

Recording the vintage matters because a later reader cannot tell whether a conclusion was drawn from data available at the time or from data revised afterwards. Without the vintage, every historical reading looks prescient, and the record stops being evidence of anything.

A small set also makes the revisions visible. With five series, a revision to one is a notable event; with fifty, it disappears into the noise of the dashboard, and the conclusions built on the revised series quietly stop matching the ones built before it.
