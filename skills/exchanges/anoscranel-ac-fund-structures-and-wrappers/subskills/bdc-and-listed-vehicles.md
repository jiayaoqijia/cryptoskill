---
name: bdc-and-listed-vehicles
domain: investing/bdc-and-listed-vehicles
trigger: "Reading a listed private-credit vehicle and its structural constraints."
anti_trigger: "Not for private credit as an asset class, and not for manager evaluation."
scope: "Business development companies, interval funds, and listed private vehicles."
status: seedling
---

# BDC and listed vehicles

## Standard

A business development company is a listed vehicle that lends to or invests in private companies, and its structure is defined by the rules that allow it: asset coverage requirements that limit leverage, a requirement to distribute most of its taxable income, and a valuation process for assets that do not trade. The listed price and the underlying net asset value are separate numbers, and the gap between them is the market's view of the portfolio's marks.

That gap is the central analytical object. When a BDC trades below net asset value, the market is expressing doubt about the marks, the leverage, or the portfolio's credit quality, and the doubt may be right or wrong. Reading the vehicle means comparing the discount with the portfolio's composition, its non-accrual rate, and its leverage, rather than treating the discount as either an opportunity or a warning on its own.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the vehicle type: BDC, interval fund, or another listed structure.
- Record the net asset value per share and the market price, and the resulting discount or premium.
- Record the asset coverage ratio and the leverage within the permitted limits.
- Record the non-accrual rate and the portfolio's sector concentration.
- Record the valuation methodology and who performs it.
- Record the distribution rate and whether it is funded from income or from capital.

## Procedure

1. Identify the vehicle type and its structural constraints.
2. Record net asset value, market price, and the gap.
3. Record leverage and asset coverage.
4. Record non-accruals and concentration.
5. Record the valuation process.
6. Record the distribution's source and its coverage by income.

## Anti-patterns

- Treating a discount to net asset value as automatically cheap.
- Ignoring that the marks are estimates for assets that do not trade.
- Reading the distribution rate as a yield without checking its source.
- Overlooking leverage, which amplifies both the marks and the discount.
- Comparing a listed vehicle's liquidity with the underlying loans' liquidity.

## Done checklist

- [ ] Vehicle type recorded.
- [ ] Net asset value and market price recorded.
- [ ] Asset coverage and leverage recorded.
- [ ] Non-accruals and concentration recorded.
- [ ] Valuation process recorded.
- [ ] Distribution source recorded.

## Sources

- Registered closed-end and BDC disclosure: <https://www.sec.gov/investor>
- Investor education on listed vehicles: <https://www.investor.gov/introduction-investing>
- Market practice guidance: <https://www.finra.org/>
