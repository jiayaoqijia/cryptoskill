---
name: seasonality-and-inventory
domain: investing/seasonality-and-inventory
trigger: "Using seasonal patterns and inventory data without over-reading them."
anti_trigger: "Not for forecasting weather or prices, and not for allocation."
scope: "Seasonal patterns, inventory reports, weather, and the data that moves the curve."
status: seedling
---

# Seasonality and inventory

## Standard

Agricultural and energy markets have calendars: planting and harvest, heating and driving seasons, maintenance turnarounds, and the annual cycle of storage fills and draws. These patterns show up in the curve because they are known in advance, which is precisely why a seasonal pattern that everyone can see is already priced and is a poor basis for a trade on its own.

The useful use of seasonality is conditional. A crop that is planted late, a drawdown that is larger than the five-year average for that week, or a storage level that is unusually low for the time of year changes the distribution around the seasonal expectation. The record should therefore compare the current observation with the seasonal norm, not with last year's price, and it should state which report the observation came from and when it was released.

Primary sources: <https://www.usda.gov/> and <https://www.eia.gov/>.

## Decision rules

- Record the seasonal pattern and the source that documents it.
- Record the current observation alongside the same-week five-year average.
- Record the release date of every data point, since revisions are common.
- Record the revision history where it matters: an initial print is not the final number.
- Treat a deviation from the seasonal norm as a question, not as a signal.
- Record which scheduled releases fall inside the holding period.

## Procedure

1. Identify the seasonal series relevant to the commodity.
2. Collect the current observation and the comparable five-year values.
3. Record release dates and any revision to the prior print.
4. Compare the deviation with the normal range for that week.
5. List the releases due during the intended holding period.
6. Record the analysis and the questions it raises.

## Anti-patterns

- Trading a seasonal pattern that is already priced.
- Comparing this year's stock level with last year's rather than with the seasonal norm.
- Using a preliminary print as final.
- Ignoring a release scheduled inside the holding period.
- Treating weather forecasts beyond their skill horizon as information.

## Done checklist

- [ ] Seasonal pattern documented with source.
- [ ] Current observation and five-year norm recorded.
- [ ] Release dates recorded.
- [ ] Revision history noted.
- [ ] Release calendar for the holding period listed.
- [ ] Questions recorded rather than conclusions.

## Sources

- Agricultural supply and demand reports: <https://www.usda.gov/>
- Energy inventory and production data: <https://www.eia.gov/>
- Positioning and market data: <https://www.cftc.gov/>
