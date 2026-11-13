---
name: margin-mechanics
domain: investing/margin-mechanics
trigger: "Working out equity, maintenance requirements, and what triggers a margin call."
anti_trigger: "Not for predicting prices, and not for perp margin modes."
scope: "Initial and maintenance requirements, equity computation, and what actually triggers a call."
status: seedling
---

# Margin mechanics

## Standard

Margin is computed from equity, not from the size of the position. Equity is the market value of the securities minus the loan; the maintenance requirement is a minimum equity expressed as a percentage of the position's value, and a call occurs when equity falls below it. That structure means the trigger moves with prices: a falling market reduces the asset value and the requirement together, but the loan stays fixed, so equity falls faster than the portfolio.

The details that decide the outcome are the ones least often read: which securities are eligible and at what percentage, whether the requirement is a flat percentage or a schedule by concentration, and how the broker computes value for thinly traded holdings. A house requirement above the regulatory minimum is common, and it is the one that applies.

Primary sources: <https://www.finra.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the maintenance requirement per holding and the house requirement where it differs.
- Compute equity as market value minus loan, and the buffer as equity minus the requirement.
- Record concentration rules, since a single large position may carry a higher requirement.
- Record which holdings are ineligible as collateral.
- Record the broker's right to raise requirements without notice.
- Convert the buffer into a percentage fall the portfolio can absorb before a call.

## Procedure

1. List holdings with their market values and loan balance.
2. Record the applicable requirement per holding.
3. Compute equity and the buffer above the requirement.
4. Calculate the percentage decline that exhausts the buffer.
5. Check concentration and eligibility rules.
6. Write the mechanics summary with the calculated decline.

## Anti-patterns

- Computing margin from the portfolio's total value rather than per holding.
- Using the regulatory minimum when the house requirement is higher.
- Ignoring concentration schedules.
- Treating a buffer as fixed when requirements can be raised.
- Assuming ineligible collateral counts at full value.

## Done checklist

- [ ] Requirements recorded per holding.
- [ ] Equity and buffer computed.
- [ ] Buffer expressed as a percentage decline.
- [ ] Concentration rules recorded.
- [ ] Eligibility recorded.
- [ ] Right to raise requirements noted.

The buffer calculation is the single most useful number here, because it converts a percentage requirement into a market move: a portfolio with a ten percent buffer is one that survives a ten percent fall without a call, and stating it that way makes the risk legible without any model.

## Sources

- Margin requirements and investor guidance: <https://www.finra.org/>
- Investor education on margin: <https://www.investor.gov/introduction-investing>
- Market data for scenario testing: <https://fred.stlouisfed.org/>
