---
name: short-interest-and-fails
domain: investing/short-interest-and-fails
trigger: "Reading short interest and failure-to-deliver data."
anti_trigger: "Not for predicting squeezes, and not for short-selling mechanics."
scope: "Twice-monthly short interest, days to cover, and fail-to-deliver data."
status: seedling
---

# Short interest and fails

## Standard

Short interest is published twice a month and reports the total shares sold short as of a settlement date, aggregated across all participants. It does not say who is short, at what price, or with what hedging, and it is published days after the date it describes. Days to cover divides that figure by average volume, which makes it a measure of how long covering would take if everyone tried at once.

Failure-to-deliver data is different: it reports shares that were not delivered at settlement, which can indicate a borrow that could not be sourced. A persistent fail in a name is a sign that the borrow is scarce, and it can coexist with a falling short interest if the positions are being rolled rather than closed. Neither series forecasts a squeeze, and both are frequently cited as if they did.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the settlement date and the publication date, and compute the lag.
- Record short interest as a percentage of float, with the float source named.
- Record days to cover and the volume window used.
- Record the failure-to-deliver series separately and note persistence rather than a single reading.
- Record any known borrow constraint, which explains both series.
- Treat both as descriptions of a state rather than as predictions.

## Procedure

1. Pull short interest with its settlement and publication dates.
2. Compute the percentage of float and days to cover.
3. Pull the failure-to-deliver series for the same window.
4. Record the borrow situation for the name.
5. Compare the two series for consistency.
6. Write the summary with the state described.

## Anti-patterns

- Quoting short interest without its settlement date.
- Treating days to cover as a price forecast.
- Reading a single fail as evidence of manipulation.
- Ignoring the float definition used.
- Comparing short interest across venues with different reporting.

## Done checklist

- [ ] Settlement and publication dates recorded.
- [ ] Percentage of float computed with source.
- [ ] Days to cover recorded.
- [ ] Fails series recorded.
- [ ] Borrow situation recorded.
- [ ] Summary describes state, not forecast.

The two series are also read together for a reason that is easy to miss: a falling short interest with a rising fail series can mean positions are being closed on paper while the borrow remains strained, and a rising short interest with no fails can mean the borrow is easy and the position is being built openly. The pairing, not either series alone, is what describes the state.


## Sources

- Short sale and fail data context: <https://www.sec.gov/investor>
- Market data and trading guidance: <https://www.finra.org/>
- Investor education on short selling: <https://www.investor.gov/introduction-investing>
