---
name: credit-spreads
domain: investing/credit-spreads
trigger: "Reading a credit spread as the market's price of default risk."
anti_trigger: "Not for credit ratings as a substitute for analysis, and not for predicting defaults."
scope: "Spread as the price of default risk, ratings and their limits, and how spreads behave in stress."
status: seedling
---

# Credit spreads

## Standard

A credit spread is the extra yield a bond offers over a risk-free bond of the same maturity. It compensates for expected loss given default, for the risk that default arrives when the investor can least afford it, and for illiquidity. The spread is therefore a price, and like any price it can be rich or cheap relative to the risk it covers — but the risk itself must be assessed, not inferred from the spread.

Ratings are a summary of someone else's assessment, published with a lag and revised after the market has usually moved. They are useful as a screen and dangerous as a substitute for reading the issuer's financials. The historical record of ratings through crises is one of stability followed by sudden, large revisions.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Spread is recorded with its reference rate, maturity, and date.
- Expected loss is estimated from the issuer's financials, not from the rating alone.
- Ratings are recorded with their date and agency; a stale rating is noted as stale.
- Spread widening is separated into rate-driven and credit-driven components.
- In stress, spreads are assumed to gap rather than drift; liquidity is recorded separately.
- A spread that looks wide is a question, not an answer; record what would explain it.

## Procedure

1. Record the spread with reference rate, maturity, and date.
2. Pull the issuer's financials and estimate default risk independently.
3. Compare the implied default probability with the estimate.
4. Note the rating, its date, and the agency.
5. Check how the spread behaved in the last stress episode.
6. Record the finding with the basis for any disagreement.

## Anti-patterns

- Treating the rating as the risk assessment.
- Comparing spreads across different maturities without adjustment.
- Ignoring liquidity as a component of the spread.
- Assuming a wide spread is a bargain without an explanation.
- Reading spread moves in stress as gradual.

## Done checklist

- [ ] Spread recorded with reference, maturity, date.
- [ ] Independent default-risk estimate made from financials.
- [ ] Implied versus estimated probability compared.
- [ ] Rating recorded with date and agency.
- [ ] Stress behaviour checked.
- [ ] Finding recorded with its basis.

## Sources

- Credit-spread series and rate data: <https://fred.stlouisfed.org/>
- Regulatory context for issuer disclosure: <https://www.sec.gov/investor>
- Investor education on bond risk: <https://www.investor.gov/introduction-investing>
