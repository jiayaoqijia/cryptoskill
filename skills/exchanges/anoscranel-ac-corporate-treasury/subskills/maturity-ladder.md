---
name: maturity-ladder
domain: investing/maturity-ladder
trigger: "Reading a company's debt maturity profile and its refinancing wall."
anti_trigger: "Not for predicting rates, and not for recommending a security."
scope: "The debt profile, refinancing walls, and the cost of extending."
status: seedling
---

# Maturity ladder

## Standard

A maturity ladder lists debt by the year it falls due, and its shape is a statement about refinancing risk. A ladder that is evenly spread refinances a small amount each year and can absorb a bad market; one with a large concentration in a single year faces a wall, and the company's bargaining position at that wall depends on the market's appetite at the time rather than on the company's intentions.

Two features make the wall decisive. The first is whether the maturing debt is secured, because a secured refinancing needs the existing lender's cooperation and can consume the unencumbered assets a new lender would want. The second is the covenant structure: a company approaching a wall with tight maintenance covenants may be forced to refinance on worse terms, and the refinancing cost can appear before the maturity as a higher spread on new issuance.

Primary sources: <https://www.sec.gov/investor> and <https://www.federalreserve.gov/>.

## Decision rules

- Record each instrument with its amount, coupon, maturity, and security.
- Record the annual maturity total and express it against annual operating cash flow.
- Record the secured versus unsecured split within each year.
- Record the undrawn committed facilities that could refinance a maturity.
- Record the covenant package attached to the nearest maturities.
- Record the weighted average maturity and how it has changed.

## Procedure

1. Read the debt note and build the schedule by year.
2. Record amount, coupon, maturity, and security for each instrument.
3. Compute the annual totals against cash flow.
4. Record undrawn facilities and their availability.
5. Record covenants on the nearest maturities.
6. Write the profile with the wall identified.

## Anti-patterns

- Reading the weighted average maturity and ignoring the distribution.
- Treating convertible debt as equity before conversion.
- Counting an undrawn facility that requires covenant compliance as certain.
- Overlooking secured debt, which reduces future borrowing capacity.
- Ignoring lease and pension obligations that compete for the same cash.

## Done checklist

- [ ] Schedule built by year.
- [ ] Amounts, coupons, security recorded.
- [ ] Annual totals against cash flow computed.
- [ ] Undrawn facilities recorded.
- [ ] Covenants on near maturities recorded.
- [ ] Refinancing wall identified.

The ladder should also be read alongside the covenant package: a maturity that falls in a year when a leverage covenant is close to its threshold is harder to refinance than the same maturity in a year with headroom, because the new lender inherits the constraint. The two disclosures together describe refinancing risk; either one alone describes only its schedule.


## Sources

- Debt and maturity disclosure: <https://www.sec.gov/investor>
- Interest rate and credit data: <https://www.federalreserve.gov/>
- Investor education on corporate debt: <https://www.investor.gov/introduction-investing>
