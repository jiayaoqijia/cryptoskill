---
name: seasonal-volatility
domain: investing/seasonal-volatility
trigger: "Reading the term structure of commodity volatility against the calendar."
anti_trigger: "Not for forecasting weather or prices, and not for option theory."
scope: "Volatility that follows the crop or heating calendar, and the term structure it creates."
status: seedling
---

# Seasonal volatility

## Standard

Commodity volatility has a calendar. Natural gas is more volatile in the winter and around storage reports, grains around planting and harvest, and refined products around the driving season and refinery maintenance. Because those patterns are known, they appear in the term structure of implied volatility before they appear in price, and a flat term structure in a seasonal market is itself information.

The trading consequence is that an option's expiry relative to the season matters as much as its strike. A position that spans a seasonal transition carries a volatility exposure that changes without any move in the underlying, and a roll from one expiry to another can change the position's risk profile even when the underlying price is unchanged.

Primary sources: <https://www.eia.gov/> and <https://www.usda.gov/>.

## Decision rules

- Record the seasonal pattern relevant to the commodity and its source.
- Record the implied volatility term structure across the expiries in scope.
- Record where each expiry sits relative to the seasonal transition.
- Record the effect of a roll on the volatility exposure.
- Record any scheduled report inside the option's life.
- Where the pattern is documented only anecdotally, record that and lower the confidence.

## Procedure

1. Identify the seasonal drivers for the commodity.
2. Collect implied volatility across the front expiries.
3. Map each expiry onto the seasonal calendar.
4. Record the term structure's shape and its slope.
5. Record the reports inside each option's life.
6. Write the seasonal map with its dates.

## Anti-patterns

- Treating a seasonal volatility pattern as a forecast of price.
- Ignoring the term structure when choosing an expiry.
- Rolling an option without noting the volatility change.
- Assuming a pattern holds every year.
- Missing a scheduled report inside the option's life.

## Done checklist

- [ ] Seasonal drivers recorded with source.
- [ ] Term structure across expiries recorded.
- [ ] Expiries mapped to the calendar.
- [ ] Roll effect recorded.
- [ ] Reports inside the life recorded.
- [ ] Confidence recorded.

The term structure also carries the market's expectation of the season's severity: a winter curve in gas that is unusually flat suggests the market is not pricing a severe season, and a steep one suggests it is, so reading the slope is a way of reading the expectation without forecasting weather.


## Sources

- Energy market and inventory data: <https://www.eia.gov/>
- Agricultural supply reports: <https://www.usda.gov/>
- Exchange option data: <https://www.cmegroup.com/>
