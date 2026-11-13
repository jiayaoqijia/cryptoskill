---
name: refinancing-and-equity-return
domain: investing/refinancing-and-equity-return
trigger: "Understanding how refinancing produces a project's equity return."
anti_trigger: "Not for predicting rates, and not for recommending a position."
scope: "How refinancing produces the equity return, and the gain-share."
status: seedling
---

# Refinancing and equity return

## Standard

A project's base-case equity return is often modest, and the realised return comes from refinancing: once construction is complete and the asset is operating, the risk premium the lenders charged falls, and the project can borrow more cheaply or in greater size. The equity can then take cash out earlier than the base case assumed, which raises the internal rate of return without any change in the underlying cash flow.

That mechanism is contractual as well as financial. Many concessions include a refinancing gain-share that returns part of the benefit to the grantor, and the presence and size of that share determine how much of the gain reaches the equity. A base case that assumes refinancing without modelling the share, or that assumes a refinancing the contract permits only with consent, is a base case with an unstated assumption.

Primary sources: <https://www.worldbank.org/> and <https://www.eib.org/>.

## Decision rules

- Record the base-case equity return and the assumptions behind it.
- Record the assumed refinancing: timing, size, and rate.
- Record the gain-share provision and the proportion retained by the grantor.
- Record any consent required for a refinancing.
- Record the effect on the return of a refinancing that does not occur.
- Record the sensitivity of the return to the refinancing assumptions.

## Procedure

1. Read the financial model's base case and its refinancing assumptions.
2. Record the timing, size, and rate assumed.
3. Record the gain-share provision and any consent requirement.
4. Compute the return with and without the refinancing.
5. Record the delta, which is the reliance on the assumption.
6. Write the analysis with the reliance stated.

## Anti-patterns

- Reading the headline equity return without its refinancing assumption.
- Ignoring the gain-share, which reduces the benefit to the equity.
- Assuming a consent will be granted.
- Treating a refinancing as certain when it depends on market conditions.
- Comparing returns across projects with different refinancing assumptions.

## Done checklist

- [ ] Base-case return and assumptions recorded.
- [ ] Refinancing timing, size, rate recorded.
- [ ] Gain-share recorded.
- [ ] Consent requirement recorded.
- [ ] Return computed with and without refinancing.
- [ ] Reliance stated.

A further point is that the gain-share is often calculated on the increase in value rather than on the cash released, which means the equity can return capital without triggering a share if the calculation is based on a different measure. Reading the definition, not only the percentage, decides what the grantor actually receives.


## Sources

- Project finance and concession guidance: <https://www.worldbank.org/>
- Infrastructure financing standards: <https://www.eib.org/>
- Interest rate data: <https://fred.stlouisfed.org/>
