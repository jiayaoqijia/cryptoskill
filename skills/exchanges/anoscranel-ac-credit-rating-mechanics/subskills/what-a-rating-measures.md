---
name: what-a-rating-measures
domain: investing/what-a-rating-measures
trigger: "Establishing what a rating does and does not say about a credit."
anti_trigger: "Not for assessing repayment capacity, and not for spread analysis."
scope: "The scales, what each measures, and what a rating explicitly excludes."
status: seedling
---

# What a rating measures

## Standard

A long-term issuer rating speaks to the likelihood of default on the obligor's debt, on a scale that is ordinal and not linear: the gap between two adjacent notches is not a constant change in probability, and the gap between investment grade and high yield is a boundary of convention rather than of risk. A rating is also forward-looking over a stated horizon, typically several years, which means it can be right about the long run and wrong about the next quarter.

What it excludes is the part most often forgotten. A rating says nothing about expected loss when recovery differs between instruments, which is why senior secured debt can carry a better instrument rating than the issuer's own; nothing about liquidity or price volatility, which is why an investment-grade bond can fall sharply; and nothing about the price paid, which is why a highly rated instrument can be a poor investment.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the agency, the scale, and whether the rating is issuer or instrument level.
- Record the horizon the rating is stated over.
- Record the instrument's seniority and any recovery assumptions where an instrument rating differs.
- Record that the rating excludes valuation and liquidity.
- Record any distinction between a published rating and a private assessment.
- Where several agencies rate the same issuer, record each separately rather than averaging.

## Procedure

1. Record the agency and the exact scale used.
2. Record issuer versus instrument level and the seniority.
3. Record the stated horizon.
4. Record the exclusions relevant to the position.
5. Record other agencies' ratings separately.
6. Write the rating summary with its scope.

## Anti-patterns

- Treating a rating as a probability of default.
- Averaging ratings across agencies into a composite.
- Assuming an issuer rating applies to every instrument.
- Treating the investment-grade boundary as a risk threshold.
- Reading a rating as a valuation opinion.

## Done checklist

- [ ] Agency and scale recorded.
- [ ] Issuer or instrument level recorded.
- [ ] Horizon recorded.
- [ ] Exclusions recorded.
- [ ] Other agencies recorded separately.
- [ ] Scope written.

The distinction that most affects a holder in practice is between the issuer rating and the instrument rating: a secured issue can be rated above the issuer because recovery is higher, which means a downgrade of the issuer does not automatically downgrade every instrument, and a portfolio aggregated at issuer level understates the dispersion it actually holds.

## Sources

- Credit rating agency regulation and disclosure: <https://www.sec.gov/investor>
- Capital framework references to ratings: <https://www.bis.org/>
- Investor education on credit risk: <https://www.investor.gov/introduction-investing>
