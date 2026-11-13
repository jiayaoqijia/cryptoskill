---
name: corporate-actions-and-options
domain: investing/corporate-actions-and-options
trigger: "Working out how a corporate action adjusts an option contract."
anti_trigger: "Not for predicting deal outcomes, and not for tax treatment."
scope: "Splits, mergers, and special dividends, and the contract adjustment they trigger."
status: seedling
---

# Corporate actions and options

## Standard

Option contracts are adjusted when the underlying changes. A split multiplies the deliverable and divides the strike; a special dividend may trigger an adjustment to preserve the contract's economics; a merger can convert the deliverable into cash, into another company's shares, or into a combination. The adjustment is made by the exchange under its rules and announced, and the adjusted contract often trades under a modified symbol.

The risk is that the adjusted contract is not the contract the trader thought they held. An option that delivers a mixed basket, or that settles in cash at a value determined by the deal terms, has different liquidity and different hedging behaviour from the original, and its price may no longer be comparable with the standard contract. Reading the adjustment notice is the only way to know what the position became.

Primary sources: <https://www.cboe.com/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the corporate action, its ex-date, and its payment or completion date.
- Record the exchange's adjustment notice and the adjusted deliverable.
- Record the adjusted strike and multiplier.
- Record the new symbol and the liquidity of the adjusted contract.
- Record whether the deliverable is shares, cash, or a combination.
- Record the position's exposure if the adjustment changes settlement.

## Procedure

1. Identify corporate actions affecting the underlying inside the option's life.
2. Obtain the exchange adjustment notice.
3. Record the adjusted terms and symbol.
4. Record the liquidity of the adjusted contract.
5. Reassess the hedge with the new deliverable.
6. Write the adjustment summary with its reference.

## Anti-patterns

- Assuming a split leaves the option unchanged.
- Trading an adjusted contract without knowing its deliverable.
- Comparing an adjusted price with a standard one.
- Ignoring the liquidity change after an adjustment.
- Assuming a merger converts everything into cash.

## Done checklist

- [ ] Action and dates recorded.
- [ ] Adjustment notice recorded.
- [ ] Adjusted strike, multiplier, symbol recorded.
- [ ] Deliverable recorded.
- [ ] Liquidity assessed.
- [ ] Hedge reassessed.

The adjustment also changes the option's hedging behaviour: an adjusted contract whose deliverable is a basket carries the volatility of that basket, which is not the volatility the original contract was priced on, so a hedge ratio computed before the adjustment is no longer the right one and the position should be re-measured rather than carried forward.


## Sources

- Exchange adjustment notices and rules: <https://www.cboe.com/>
- Corporate action disclosure: <https://www.sec.gov/investor>
- Investor education on corporate actions: <https://www.investor.gov/introduction-investing>
