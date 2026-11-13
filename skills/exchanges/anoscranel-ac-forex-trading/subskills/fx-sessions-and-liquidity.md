---
name: fx-sessions-and-liquidity
domain: investing/fx-sessions-and-liquidity
trigger: "Choosing when to trade FX and what liquidity to expect at that hour."
anti_trigger: "Not for predicting price direction, and not for portfolio hedging."
scope: "Session overlaps, fixing windows, liquidity holes, and intervention risk."
status: seedling
---

# FX sessions and liquidity

## Standard

FX liquidity follows the sun. The Tokyo session, the London session, and the New York session overlap in pairs, and the overlap between London and New York is the deepest part of the day. Outside those windows — late New York, the hours before Asia opens, holidays — spreads widen and depth thins, so the same order costs more and moves the price further.

Two scheduled events concentrate flow beyond the ordinary session pattern. The daily fixing windows, above all the London four o'clock, attract large orders that are executed around a benchmark, which produces a characteristic pattern of volatility into and after the fix. And central-bank intervention is an event with no schedule, which is why positions held through it carry a risk that ordinary stop-loss levels do not bound.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the session in which the strategy trades and the typical spread at that hour.
- Record the fixing windows relevant to the pairs traded and the behaviour observed around them.
- Record the hours when liquidity is thin and avoid market orders there.
- Record the days when holidays in either currency's home market reduce liquidity.
- Record intervention risk for the pairs where it is plausible, and treat stops as indicative.
- Record the time zone of every timestamp used, since FX has no single close.

## Procedure

1. Map the sessions and overlaps for the pairs traded.
2. Sample spreads by hour across a week and record the shape.
3. Note the fixing windows and any pattern around them.
4. Note holiday calendars for both currencies.
5. Record intervention history and the venue's behaviour in it.
6. Write the timing rules the strategy will follow.

## Anti-patterns

- Trading thin hours because that is when there is time to trade.
- Treating a stop as guaranteed through an intervention.
- Ignoring the fixing window when sizing an order near it.
- Comparing spreads across hours without recording the hour.
- Forgetting that a holiday in one currency's market changes liquidity in the pair.

## Done checklist

- [ ] Sessions and overlaps mapped.
- [ ] Spreads sampled by hour.
- [ ] Fixing windows recorded.
- [ ] Holiday calendars noted.
- [ ] Intervention risk recorded.
- [ ] Timing rules written.

## Sources

- Foreign exchange liquidity and turnover surveys: <https://www.bis.org/>
- Central bank operations and rates: <https://www.federalreserve.gov/>
- Market volatility and rate data: <https://fred.stlouisfed.org/>
