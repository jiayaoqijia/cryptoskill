---
name: commitments-of-traders
domain: investing/commitments-of-traders
trigger: "Reading the Commitments of Traders report for positioning."
anti_trigger: "Not for forecasting prices, and not for equities positioning."
scope: "CFTC categories, net positioning, and the commercial-versus-fund split."
status: seedling
---

# Commitments of Traders

## Standard

The Commitments of Traders report, published weekly, breaks open interest in a futures market into categories: commercial traders who use the contract for their business, and non-commercial traders who do not, often split further into funds and other reportables. The split is the report's value, because it separates hedgers from speculators and shows how each is positioned.

The report describes open interest, not price, and it is published several days after the date it covers. Its most cited transformation is net positioning — longs minus shorts in a category — and its most common misuse is treating an extreme net position as a reversal signal. A large speculative long can persist through a substantial further rally, so the record should state the position and its percentile rather than a conclusion.

Primary sources: <https://www.cftc.gov/> and <https://www.cmegroup.com/>.

## Decision rules

- Record the report date, the publication date, and the lag.
- Record open interest and the split by category.
- Record net positioning by category and its percentile over a stated window.
- Record the commercial net position separately, since it reflects hedging demand rather than a view.
- Record the contract and whether it is the aggregate across exchanges or a single venue.
- Treat an extreme reading as a description of crowding, not as a signal.

## Procedure

1. Pull the report for the market and date.
2. Record open interest and the category split.
3. Compute net positions and percentiles.
4. Record the commercial side separately.
5. Note any change in categorisation.
6. Write the summary with the percentile stated.

## Anti-patterns

- Treating an extreme net position as a reversal signal.
- Reading commercial positioning as a directional view.
- Comparing percentiles across markets with different participant mixes.
- Ignoring the lag between report and publication.
- Aggregating categories that the report keeps separate.

## Done checklist

- [ ] Report and publication dates recorded.
- [ ] Open interest and split recorded.
- [ ] Net positions and percentiles computed.
- [ ] Commercial side recorded separately.
- [ ] Categorisation changes noted.
- [ ] Summary states crowding, not forecast.

A further reading detail is the change rather than the level: a category that has added to a position for several consecutive weeks is describing a trend in participation, while a single large week can be one participant rebalancing. Recording the sequence, not only the latest number, is what lets a later reader tell the two apart without re-pulling the archive.


## Sources

- Commitments of Traders reports: <https://www.cftc.gov/>
- Exchange open interest data: <https://www.cmegroup.com/>
- Investor education on futures positioning: <https://www.investor.gov/introduction-investing>
