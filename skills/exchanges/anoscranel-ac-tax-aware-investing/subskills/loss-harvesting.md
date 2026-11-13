---
name: loss-harvesting
domain: investing/loss-harvesting
trigger: "Realising a loss and managing the wash-sale constraint."
anti_trigger: "Not for tax advice, and not for market timing."
scope: "Realising losses, the wash-sale trap, and the basis reset."
status: seedling
---

# Loss harvesting

## Standard

Realising a loss converts an unrealised decline into a usable offset against gains or income, subject to the jurisdiction's rules on how much can be used and carried forward. The benefit is the tax saved, not the loss recovered: the position's value has already fallen, and harvesting changes the timing of the tax consequence rather than the loss itself.

The wash-sale rule is the constraint that shapes the practice. Repurchasing a substantially identical security within a defined window disallows the loss and adjusts the basis instead, which means a harvesting trade needs a replacement that is not substantially identical. That requirement is where the design work happens: a substitute that is close enough to preserve the exposure and different enough to satisfy the rule.

Primary sources: <https://www.irs.gov/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the unrealised loss, its character, and the gains available to offset.
- Record the wash-sale window and what counts as substantially identical in the jurisdiction.
- Record the replacement security and how it differs.
- Record the basis reset and its effect on a future sale.
- Record the transaction cost of the pair, which reduces the benefit.
- Record the benefit as a tax saving at the applicable rate, not as recovered value.

## Procedure

1. Identify the loss and the gains or income it could offset.
2. Record the window the rule imposes.
3. Select a replacement that is not substantially identical.
4. Compute the tax saving at the applicable rate.
5. Record the basis reset and the future consequence.
6. Execute the pair and record the details.

## Anti-patterns

- Treating the harvested loss as recovered value.
- Repurchasing the same security inside the window.
- Ignoring the basis reset, which defers rather than eliminates the gain.
- Ignoring transaction costs that consume the benefit.
- Harvesting in a sheltered account where the loss has no tax effect.

## Done checklist

- [ ] Loss and offsets recorded.
- [ ] Window and rule recorded.
- [ ] Replacement selected and justified.
- [ ] Tax saving computed.
- [ ] Basis reset recorded.
- [ ] Costs recorded.

The planning horizon also matters: a loss harvested this year against gains realised next year is worth less than the same loss harvested against gains already realised, because the offset's value depends on a liability that exists, and the record should state which liability the loss is being applied to rather than assuming one will appear.


## Sources

- Tax administration guidance on losses: <https://www.irs.gov/>
- Investor education on capital losses: <https://www.investor.gov/introduction-investing>
- Tax records context: <https://www.sec.gov/investor>
