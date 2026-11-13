---
name: credit-option-settlement
domain: investing/credit-option-settlement
trigger: "Working out what happens when a credit option is exercised."
anti_trigger: "Not for legal advice, and not for credit analysis."
scope: "Exercise into protection, cash settlement, and the documentation."
status: seedling
---

# Credit option settlement

## Standard

Exercising a credit option usually delivers a credit default swap: the holder becomes the protection buyer or seller at the strike spread, with the swap's own maturity and its own premium payments. The alternative is cash settlement against the value of that swap, which converts the position into a payment rather than an ongoing contract.

The documentation decides which applies and what the delivered swap's terms are. A physically settled option leaves the holder with an ongoing obligation whose mark-to-market and collateral requirements begin immediately, and a cash-settled one requires a valuation method that the confirmation specifies. Reading the settlement clause is the only way to know which position the exercise creates.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record whether settlement is physical into the swap or cash.
- Record the delivered swap's maturity, coupon, and premium schedule.
- Record the valuation method for a cash-settled option.
- Record the collateral and margin consequences of the delivered swap.
- Record the exercise notice period and the cut-off time.
- Record who calculates the settlement amount and how disputes are resolved.

## Procedure

1. Read the settlement clause.
2. Record the delivered instrument's terms.
3. Record the valuation method for cash settlement.
4. Record margin consequences.
5. Record notice requirements.
6. Write the settlement summary.

## Anti-patterns

- Assuming cash settlement because the option premium was cash.
- Ignoring the ongoing obligations of a delivered swap.
- Missing the exercise notice period.
- Assuming the counterparty's valuation is binding without checking the clause.
- Forgetting that a delivered swap needs collateral arrangements.

## Done checklist

- [ ] Settlement method recorded.
- [ ] Delivered swap terms recorded.
- [ ] Valuation method recorded.
- [ ] Margin consequences recorded.
- [ ] Notice period recorded.
- [ ] Calculation agent recorded.

The exercise decision also interacts with the underlying's own events: exercising into a swap shortly before a credit event transfers the protection but also the premium obligation, and exercising after a restructuring can be worth less than the option's mark because the delivered swap's terms are the standard ones rather than the terms the option was priced against. The timing of the notice, not only its existence, belongs in the plan.

Recording the calculation agent matters more here than in most markets, because a discretionary valuation on a thinly traded reference has no observable price to check it against, and the record's only defence is having named who decides.


## Sources

- Credit derivatives documentation standards: <https://www.isda.org/>
- Counterparty and margin context: <https://www.federalreserve.gov/>
- Investor education on derivatives: <https://www.investor.gov/introduction-investing>
