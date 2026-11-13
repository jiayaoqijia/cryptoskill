---
name: real-estate-vehicles
domain: investing/real-estate-vehicles
trigger: "Comparing REIT exposure with direct property ownership."
anti_trigger: "Not for property valuation of a specific building, and not for mortgage advice."
scope: "REITs versus direct property, cap rates, NAV arithmetic, and the leverage inside the vehicle."
status: seedling
---

# Real estate vehicles

## Standard

Real estate can be owned directly or through a vehicle, and the difference is not cosmetic. Direct ownership gives control and full exposure; a listed REIT gives daily liquidity but wraps the property in corporate leverage, management fees, and a share price that trades away from the value of the buildings. Both are real estate, but they behave differently in a crisis: the share price falls first and often further.

The arithmetic that matters is the cap rate: net operating income divided by property value. It is the property's yield before financing, and comparing it with the cost of debt explains why leverage amplifies returns in both directions. A REIT trading at a discount to its net asset value is a different proposition from one trading at a premium, and the discount is a signal about the market's view of the assets and the debt.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the vehicle type: direct, listed REIT, or unlisted fund; each has a different liquidity profile.
- For a REIT, record the premium or discount to net asset value, with the NAV's date and method.
- Cap rate is recorded alongside the cost of debt to show the leverage arithmetic.
- The leverage inside the vehicle is recorded separately from the leverage of the holding.
- Occupancy, lease duration, and tenant concentration are recorded where disclosed.
- Direct property is recorded with its transaction costs and its time-to-sale, not just its price.

## Procedure

1. Identify the vehicle and its liquidity terms.
2. Compute or collect the cap rate and the cost of debt.
3. Record NAV, its date, and the premium or discount.
4. Record occupancy, lease duration, and tenant concentration.
5. Estimate the leverage contribution to returns in both directions.
6. Write the comparison with the direct alternative.

## Anti-patterns

- Treating a REIT's share price as the property value.
- Comparing a leveraged vehicle's yield with an unleveraged one's.
- Ignoring the discount to NAV when it is large.
- Forgetting transaction costs and time-to-sale for direct property.
- Assuming daily liquidity means the underlying is liquid.

## Done checklist

- [ ] Vehicle type and liquidity recorded.
- [ ] Cap rate and cost of debt computed.
- [ ] NAV with date and premium or discount recorded.
- [ ] Occupancy and lease profile recorded.
- [ ] Leverage contribution estimated both ways.
- [ ] Direct alternative compared.

## Sources

- Regulatory context for REIT disclosure: <https://www.sec.gov/investor>
- Investor education on real-estate investing: <https://www.investor.gov/introduction-investing>
- Rate data for the cost-of-debt comparison: <https://fred.stlouisfed.org/>
