---
name: property-debt-and-covenants
domain: investing/property-debt-and-covenants
trigger: "Reading property-level debt and the covenants that govern it."
anti_trigger: "Not for predicting rates, and not for legal advice."
scope: "Property-level financing, DSCR and LTV covenants, and refinancing risk."
status: seedling
---

# Property debt and covenants

## Standard

Property-level debt is sized against the income it secures, through two tests: a debt service coverage ratio, which requires income to exceed payments by a margin, and a loan-to-value ratio, which caps the advance against appraised value. Both are tested at origination and often retested during the loan, and a breach can restrict distributions or trigger a cash sweep before any payment is missed.

Refinancing risk is the exposure that matters most in a property with a fixed-term loan, because the property's ability to refinance depends on rates and on appraised value at that date rather than on its performance. A loan maturing into a higher-rate environment with a lower appraisal can require an equity injection to refinance, which is a capital call on the owner arising from conditions outside the property's control.

Primary sources: <https://www.federalreserve.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the loan amount, rate, term, amortisation, and maturity.
- Record the DSCR and LTV at origination and the covenant levels.
- Record the testing frequency and the consequence of a breach.
- Record any cash management or sweep trigger.
- Record the refinancing assumptions at maturity and the sensitivity to rates and value.
- Record the recourse status and any guarantee provided.

## Procedure

1. Record the loan terms and amortisation.
2. Record DSCR and LTV at origination and the covenants.
3. Record testing frequency and breach consequences.
4. Record cash management triggers.
5. Model the refinancing at a higher rate and a lower value.
6. Write the debt summary with the refinancing gap.

## Anti-patterns

- Computing DSCR on the reported NOI without normalising it.
- Ignoring a cash sweep that activates before a payment default.
- Assuming the loan will refinance at its current terms.
- Overlooking a recourse guarantee in a non-recourse structure.
- Treating an interest-only period as permanent.

## Done checklist

- [ ] Loan terms recorded.
- [ ] Ratios and covenants recorded.
- [ ] Testing and consequences recorded.
- [ ] Cash management recorded.
- [ ] Refinancing modelled.
- [ ] Recourse recorded.

The number to compute before anything else is the equity required at refinancing under a plausible rate and value: an owner who has not done that calculation discovers the gap at the moment the loan matures, which is the moment when the alternatives are fewest and the cost of filling the gap is highest.

## Sources

- Interest-rate and credit data: <https://www.federalreserve.gov/>
- Property and loan disclosure: <https://www.sec.gov/investor>
- Rate series for refinancing scenarios: <https://fred.stlouisfed.org/>
