---
name: releases-and-revisions
domain: investing/releases-and-revisions
trigger: "Reading an economic release with its definition and its revision history."
anti_trigger: "Not for forecasting the next print, and not for trading the release."
scope: "Which releases matter, how they are defined, and why the revision often outweighs the print."
status: seedling
---

# Releases and revisions

## Standard

Every economic release has a definition, a sample, and a revision schedule, and the three determine what the number can tell you. A payroll figure is a survey with a response rate and a benchmark revision; an inflation print is a basket with weights that change annually. Reading the number without the definition is reading a headline, not data.

Revisions are the part markets forget. First prints are estimates, and the cumulative revision is frequently larger than the month-to-month change that markets reacted to. A series that looked like a turning point in the first print can look like noise after the revision, which means the honest analysis uses revised data for history and treats the current print as provisional.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the release's definition, sample, and revision schedule before interpreting the number.
- Record whether the figure is a first print, a revision, or a benchmarked series.
- Compare the current print with the revised history, not only with the previous print.
- Treat the first print as provisional in any conclusion that outlives the day.
- Record the market's reaction separately from the data's content.
- When a series is rebased or redefined, record the break and do not splice without a note.

## Procedure

1. Identify the release and its definition.
2. Record whether the figure is first print or revised.
3. Pull the revised history for comparison.
4. Note the revision schedule and typical revision size.
5. Separate the data from the market's reaction.
6. Record the break where a definition changed.

## Anti-patterns

- Treating a first print as final.
- Comparing a new definition with an old series without a break note.
- Reading the market reaction as the data's meaning.
- Ignoring the sample and response rate.
- Quoting a headline figure without its definition.

## Done checklist

- [ ] Definition, sample, and revision schedule recorded.
- [ ] Print status recorded.
- [ ] Revised history compared.
- [ ] Typical revision size noted.
- [ ] Reaction separated from content.
- [ ] Definition breaks recorded.

## Sources

- Macro data series and revisions: <https://fred.stlouisfed.org/>
- Investor education on economic indicators: <https://www.investor.gov/introduction-investing>
- Regulatory context for official statistics: <https://www.sec.gov/investor>

The practical consequence is that a strategy validated on first prints is validated on data that no longer exists. Using revised history for the backtest and first prints for the live signal creates a gap between the two that looks like skill in-sample and behaves like noise out of sample.
