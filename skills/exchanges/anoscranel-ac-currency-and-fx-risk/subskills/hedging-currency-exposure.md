---
name: hedging-currency-exposure
domain: investing/hedging-currency-exposure
trigger: "Setting a hedge ratio and understanding what the hedge costs and leaves open."
anti_trigger: "Not for predicting exchange rates, and not for choosing instruments by brand."
scope: "Hedge ratios, instruments, the cost of hedging, and what hedging does not remove."
status: seedling
---

# Hedging currency exposure

## Standard

Hedging currency exposure is a decision about which risk you want to own. A fully hedged foreign holding gives you the asset's return in your own currency; an unhedged one gives you the asset plus the currency. Neither is right in general: the choice depends on the holding period, the correlation between the asset and the currency, and the cost of the hedge.

The cost is visible in the forward points, and it can be large when the interest differential is wide. Hedging also has basis risk — the hedge is a series of forwards with roll dates, not a permanent lock — and it can create cash-flow obligations if the currency moves against the hedge before the asset is sold.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the hedge ratio and the reason for it, before choosing instruments.
- Record the hedge's cost as forward points, annualised, with the differential's source.
- Record roll dates and the operational obligation each roll creates.
- A partial hedge is recorded as a ratio, not described as hedged.
- Record what the hedge does not cover: the asset's own currency risk within its revenues, for instance.
- Revisit the ratio on a schedule, not on a currency move.

## Procedure

1. Record the exposure and the intended hedge ratio with the reason.
2. Compute the annualised cost from forward points.
3. Record the roll schedule and obligations.
4. Identify the residual exposures the hedge leaves.
5. Record the instruments used and their counterparties.
6. Set the review date and the trigger that reopens the decision.

## Anti-patterns

- Treating a hedge as free.
- Setting the ratio after seeing the currency move.
- Ignoring roll obligations.
- Calling a partial hedge fully hedged.
- Assuming the hedge covers the asset's operating currency exposure.

## Done checklist

- [ ] Hedge ratio and reason recorded.
- [ ] Annualised cost computed.
- [ ] Roll schedule and obligations recorded.
- [ ] Residual exposures identified.
- [ ] Instruments and counterparties recorded.
- [ ] Review date and trigger set.

## Sources

- Rate and forward-point data: <https://fred.stlouisfed.org/>
- Investor education on currency hedging: <https://www.investor.gov/introduction-investing>
- Regulatory context for derivative disclosure: <https://www.sec.gov/investor>

The hedge ratio also interacts with the holding period: a hedge that must be rolled monthly is a series of decisions, each with its own cost and timing, while an unhedged position is a single decision not to act. Recording the roll obligation is what makes the difference in effort visible before it is undertaken.
