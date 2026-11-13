---
name: dilution-per-year
domain: investing/dilution-per-year
trigger: "Measuring the annual transfer from holders to employees."
anti_trigger: "Not for predicting the share price, and not for the investment case."
scope: "The annual transfer to employees and what it costs a holder."
status: seedling
---

# Dilution per year

## Standard

The annual dilution rate is the increase in the fully diluted count over a year, excluding issuance for acquisitions or capital raising. It is the number that describes what a holder gives up each year to the compensation programme, and it compounds: two percent a year is roughly eighteen percent over a decade, which is a material share of the business transferred without any cash leaving the company.

Computing it correctly means separating the sources. Compensation issuance is the recurring transfer; option exercises add to it in proportion to the spread; acquisitions paid in stock are episodic; and a capital raise is a deliberate sale rather than a transfer. Only the first two belong in the rate, and a rate that includes the others overstates the recurring cost while one that excludes option exercises understates it.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the opening and closing fully diluted counts.
- Record the shares issued for compensation and for option exercises separately.
- Exclude shares issued for acquisitions and for capital raising, and record the exclusion.
- Compute the dilution rate as a percentage of the opening count.
- Record the multi-year trend, since a single year can be distorted by vesting cliffs.
- Compute the cumulative effect over five years at the current rate.

## Procedure

1. Record the counts at both ends of the period.
2. Separate the sources of increase.
3. Exclude episodic issuance and record why.
4. Compute the rate on the opening count.
5. Record the trend across at least three years.
6. State the cumulative effect at the current rate.

## Anti-patterns

- Using the basic count, which excludes the claims that will become shares.
- Including acquisition issuance, which overstates the recurring transfer.
- Measuring one year and treating it as the rate.
- Ignoring option exercises, which are dilution even when the expense was recognised earlier.
- Reporting the rate without its cumulative effect.

## Done checklist

- [ ] Opening and closing diluted counts recorded.
- [ ] Sources separated.
- [ ] Episodic issuance excluded and recorded.
- [ ] Rate computed.
- [ ] Trend recorded.
- [ ] Cumulative effect stated.

The rate is also more useful when compared with the buyback's cost than with the compensation expense, because the two are the same transaction viewed from opposite sides: cash spent to remove shares and shares issued to pay employees net against each other, and the residual is what the holder actually experiences.


## Sources

- Share count and compensation disclosure: <https://www.sec.gov/investor>
- Investor education on dilution: <https://www.investor.gov/introduction-investing>
- Market data for context: <https://fred.stlouisfed.org/>
