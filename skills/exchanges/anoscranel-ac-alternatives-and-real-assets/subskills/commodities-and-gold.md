---
name: commodities-and-gold
domain: investing/commodities-and-gold
trigger: "Evaluating commodity exposure and what a gold allocation actually does."
anti_trigger: "Not for trading commodities, and not for price forecasting."
scope: "Commodity exposure through futures, roll cost, contango and backwardation, and gold's actual behaviour."
status: seedling
---

# Commodities and gold

## Standard

Commodities are not an asset you hold; they are a series of futures contracts you roll. That distinction explains the central fact of commodity investing: the return is not the change in the spot price but the change in the spot price plus or minus the roll. In contango the roll costs money every month; in backwardation it pays. A commodity fund can lose money while the spot price rises, and that is not a malfunction.

Gold is different in mechanics and similar in confusion. It pays no cash flow, so its value rests on what others will pay; it has historically behaved as a hedge in some crises and not others, and its correlation with inflation is weaker and less stable than the marketing suggests. Recording what it actually did in the last several stress episodes is more useful than asserting what it should do.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://fred.stlouisfed.org/>.

## Decision rules

- Commodity exposure is recorded as futures with an explicit roll method, not as a spot holding.
- The current curve structure — contango or backwardation — is recorded with its annualised roll cost.
- Gold is recorded with no cash flow assumption and with its measured behaviour in the last three stress episodes.
- Commodity and gold exposures are recorded separately; they respond to different drivers.
- ETF structures are checked for whether they hold metal, futures, or equities.
- Any inflation-hedge claim is tested against the holding's own history, not asserted.

## Procedure

1. Identify the instrument and whether it holds spot, futures, or equities.
2. Record the curve structure and the annualised roll cost.
3. For gold, record the vehicle type and the custody arrangement.
4. Pull the holding's behaviour in the last three stress episodes.
5. Compare with the claimed property: hedge, inflation protection, diversification.
6. Record the finding with the vehicle and the dates.

## Anti-patterns

- Treating a commodity ETF as a spot holding.
- Assuming gold protects against inflation without checking the record.
- Ignoring roll cost because the spot price rose.
- Comparing commodity equities with commodity futures.
- Assuming a gold ETF holds metal without reading its structure.

## Done checklist

- [ ] Instrument type and structure identified.
- [ ] Curve structure and roll cost recorded.
- [ ] Gold vehicle and custody recorded.
- [ ] Stress-episode behaviour measured.
- [ ] Claims tested against the record.
- [ ] Finding recorded with dates.

## Sources

- Investor education on commodities and funds: <https://www.investor.gov/introduction-investing>
- Commodity and rate data: <https://fred.stlouisfed.org/>
- Regulatory context for fund disclosure: <https://www.sec.gov/investor>
