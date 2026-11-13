---
name: cds-options-mechanics
domain: investing/cds-options-mechanics
trigger: "Reading an option on a single-name CDS and its two dates."
anti_trigger: "Not for CDS mechanics themselves, and not for credit analysis."
scope: "Payer and receiver options, expiry against the swap, and the upfront."
status: seedling
---

# CDS options mechanics

## Standard

An option on a credit default swap gives the holder the right to buy or sell protection at a stated spread on a stated date. The payer option gives the right to buy protection at that spread, so it gains value when spreads widen; the receiver gives the right to sell protection, and gains when spreads tighten. The instrument is identified by the reference entity, the option expiry, and the underlying swap's maturity.

The two dates are the common source of error. The option expires on one date, and the swap it delivers into has its own maturity and its own start date, which is the option expiry plus the swap tenor. A quote that names only the option expiry leaves the underlying undefined, and two trades with the same expiry but different underlying tenors are different instruments with different prices.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the reference entity, seniority, and documentation version.
- Record the option expiry and the underlying swap maturity separately.
- Record the strike spread and the standard coupon of the underlying.
- Record the premium, its convention, and its payment date.
- Record whether exercise is cash or physical into the swap.
- Record the settlement date conventions for the delivered swap.

## Procedure

1. Identify the reference, seniority, and documentation.
2. Record the option expiry and the underlying swap terms.
3. Record the strike spread and coupon.
4. Record premium and payment conventions.
5. Record the exercise mechanism.
6. Write the terms summary with both dates explicit.

## Anti-patterns

- Naming only the option expiry.
- Confusing the option expiry with the swap start date.
- Ignoring the underlying's standard coupon.
- Assuming physical exercise when the terms specify cash.
- Comparing prices across different underlying tenors.

## Done checklist

- [ ] Reference, seniority, documentation recorded.
- [ ] Option expiry and swap maturity recorded.
- [ ] Strike and coupon recorded.
- [ ] Premium recorded.
- [ ] Exercise mechanism recorded.
- [ ] Summary written with both dates.

The premium convention also deserves attention: it is usually quoted as a percentage of notional or in spread terms, and the payment is made upfront rather than accrued, so the option's cost is a cash outflow at inception and its value is carried as a mark. A trade framed as cheap because the premium is small relative to the notional can still be expensive once the probability of exercise is priced in, and the record should carry both numbers so the comparison is made on the option rather than on the headline.

## Sources

- Credit derivatives documentation: <https://www.isda.org/>
- Regulatory context: <https://www.federalreserve.gov/>
- Investor education on credit instruments: <https://www.investor.gov/introduction-investing>
