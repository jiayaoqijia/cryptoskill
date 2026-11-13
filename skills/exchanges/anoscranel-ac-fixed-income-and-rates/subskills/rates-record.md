---
name: rates-record
domain: investing/rates-record
trigger: "Writing the record of a portfolio's rate and credit exposure."
anti_trigger: "Not for the trade decision, and not for performance reporting."
scope: "The written rates record: exposure, sensitivity, assumptions, and review triggers."
status: seedling
---

# Rates record

## Standard

The rates record states what the portfolio is exposed to and how much it would lose if the relevant rate moved. It separates three risks that are often bundled — interest-rate, credit, and liquidity — because the response to each differs. It is written so that a reader can answer one question in under a minute: if yields rise one percentage point across the curve, what happens to this portfolio.

The record also carries the assumptions that make the arithmetic work: a parallel shift, unchanged credit spreads, and stable liquidity. Each assumption is a simplification, and each fails in a different stress scenario, which is why the record states them rather than hiding them in a model.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- The record shows exposure by maturity bucket, modified duration, and credit quality.
- Rate sensitivity is stated for a one-point parallel shift, with convexity noted.
- Credit sensitivity is stated separately: the effect of a spread widening with rates unchanged.
- Liquidity risk is recorded as vehicle mismatch and issuer concentration.
- The assumptions are listed, with the stress that would break each.
- Review triggers are dated: rate moves, spread moves, maturities approaching.

## Procedure

1. List holdings by maturity bucket and credit quality.
2. Record modified duration and the portfolio total.
3. Compute the one-point rate sensitivity.
4. Compute the spread-widening sensitivity separately.
5. Record liquidity and concentration exposures.
6. List assumptions and the stress that breaks each.
7. Set review triggers with dates.

## Anti-patterns

- Reporting a single duration number as the whole risk picture.
- Bundling credit and rate risk in one figure.
- Omitting the assumptions behind the arithmetic.
- Ignoring vehicle liquidity when recording exposure.
- Setting no review triggers.

## Done checklist

- [ ] Holdings listed by maturity and credit quality.
- [ ] Modified duration recorded per holding and in total.
- [ ] Rate sensitivity computed for a one-point shift.
- [ ] Credit sensitivity computed separately.
- [ ] Liquidity and concentration exposures recorded.
- [ ] Assumptions listed with breaking stresses.
- [ ] Review triggers dated.

## Sources

- Rate and spread series: <https://fred.stlouisfed.org/>
- Investor education on bond portfolio risk: <https://www.investor.gov/introduction-investing>
- Regulatory context for portfolio disclosure: <https://www.sec.gov/investor>

The record earns its keep in the moment someone asks whether to shorten duration, because the answer is already there: the sensitivity figure, the credit exposure, and the liquidity mismatch are all stated before the question arrives. A record assembled after the question is a rationalisation, not a record.
