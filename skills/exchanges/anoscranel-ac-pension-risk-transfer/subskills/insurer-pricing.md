---
name: insurer-pricing
domain: investing/insurer-pricing
trigger: "Decomposing a bulk annuity quote into its drivers."
anti_trigger: "Not for predicting a quote, and not for recommending an insurer."
scope: "What drives a bulk annuity quote, and which inputs the plan controls."
status: seedling
---

# Insurer pricing

## Standard

A bulk annuity quote is a price for a set of liabilities, and it is built from the same components an actuary would use: the discount rate the insurer can earn on the assets backing the liabilities, the longevity assumption, the expenses of administering the benefits, and a capital charge for the risk the insurer retains. Each component is visible in the quote's sensitivity even when the quote itself is a single number.

The inputs the plan controls are the ones that make preparation worthwhile. Clean data reduces the insurer's uncertainty and therefore its price; a scheme with accurate member records and resolved benefit queries is cheaper to insure than one with gaps, because the insurer prices the gaps. Early engagement with the market, and a scheme that is ready to transact, is itself a pricing input.

Primary sources: <https://www.fca.org.uk/> and <https://www.bis.org/>.

## Decision rules

- Record the quoted price as a percentage of the liabilities on the scheme's basis.
- Record the discount rate implied by the quote and compare it with market yields.
- Record the longevity assumption used and its source.
- Record the data quality findings, since they price into the quote.
- Record the insurer's capital charge evidence, where disclosed.
- Record the quote's date and its validity period.

## Procedure

1. Record the quote and the basis on which it was provided.
2. Back out the implied discount rate and compare it with the market.
3. Record the longevity assumption.
4. Record the data quality work completed and outstanding.
5. Record the quote's validity and the conditions attached.
6. Write the analysis with the controllable inputs named.

## Anti-patterns

- Comparing quotes without comparing the bases they were struck on.
- Treating the quote as a single number rather than a set of assumptions.
- Ignoring data quality, which is the input most within the plan's control.
- Assuming a quote remains valid after a market move.
- Comparing a buy-in quote with a buy-out quote as if they were the same product.

## Done checklist

- [ ] Quote and basis recorded.
- [ ] Implied discount rate computed.
- [ ] Longevity assumption recorded.
- [ ] Data quality recorded.
- [ ] Validity and conditions recorded.
- [ ] Controllable inputs named.

The competitive dynamic also matters: insurers quote into a finite appetite for longevity risk, and a scheme that approaches the market when several insurers have capacity will see keener pricing than one that approaches at the end of a busy year. That is not a forecast, it is a fact about supply, and it is why preparing the data and then choosing the moment is worth more than negotiating a single quote.


## Sources

- Pensions and insurance regulation: <https://www.fca.org.uk/>
- Longevity and insurance risk standards: <https://www.bis.org/>
- Market yield data: <https://fred.stlouisfed.org/>
