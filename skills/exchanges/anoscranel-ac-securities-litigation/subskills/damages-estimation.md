---
name: damages-estimation
domain: investing/damages-estimation
trigger: "Reading a damages estimate and the method behind the number."
anti_trigger: "Not for legal advice, and not for predicting a judgment."
scope: "Inflation per share, event studies, and the methods behind a number."
status: seedling
---

# Damages estimation

## Standard

Securities damages are usually computed from price inflation: the amount by which the share price was inflated by the misstatement, isolated by comparing the actual price path with a counterfactual estimated from the market's reaction to corrective disclosures. The method is an event study, and its output depends on the model of expected returns, the size of the event window, and the assumption that the corrective disclosure removed all of the inflation at once.

Those assumptions are where the argument happens. A wider event window attributes less of a price move to the disclosure; a model with different risk factors attributes a different amount; and a corrective disclosure that arrives in stages produces a series of smaller inflation estimates rather than one. A damages figure in a complaint and one in a settlement are therefore different objects computed for different purposes.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the inflation estimate per share and the period it applies to.
- Record the event study method: model, window, and estimation period.
- Record the corrective disclosure dates and whether they were staged.
- Record the holding's transaction history against the inflation periods.
- Record the difference between the claimed figure and the settlement figure.
- Record the assumptions the estimate depends on, and how it changes if they move.

## Procedure

1. Record the inflation estimates and their periods.
2. Record the event study method and its parameters.
3. Map the holding's transactions onto the periods.
4. Compute the recognised loss under the plan.
5. Compare claimed and settled figures.
6. Write the estimate with its assumptions.

## Anti-patterns

- Treating a complaint's damages figure as a valuation.
- Ignoring the event window's effect on the estimate.
- Assuming a single corrective disclosure.
- Applying inflation to shares bought after the corrective disclosure.
- Comparing estimates computed under different methods.

## Done checklist

- [ ] Inflation estimates recorded.
- [ ] Method and parameters recorded.
- [ ] Transactions mapped.
- [ ] Recognised loss computed.
- [ ] Claimed versus settled compared.
- [ ] Assumptions stated.

The estimation period matters as much as the event window: a counterfactual built from a stable market period produces a different inflation figure from one built through a volatility spike, and a case whose class period spans a crisis will have its estimate contested on exactly that ground. Recording the period used, and testing the estimate with an alternative, is what makes the number defensible.


## Sources

- Litigation disclosure and filings: <https://www.sec.gov/investor>
- Financial analysis standards: <https://www.cfainstitute.org/>
- Market data for event studies: <https://fred.stlouisfed.org/>
