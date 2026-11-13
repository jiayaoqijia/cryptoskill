---
name: gain-deferral
domain: investing/gain-deferral
trigger: "Weighing the value of deferring a realised gain."
anti_trigger: "Not for tax advice, and not for investment selection."
scope: "Holding period effects, deferral value, and the step-up question."
status: seedling
---

# Gain deferral

## Standard

Deferring a gain is worth the time value of the tax, which for a long holding period can be a substantial fraction of the liability. The arithmetic is straightforward: the benefit equals the tax multiplied by the return earned on it during the deferral, so a higher expected return and a longer horizon both increase the value of waiting.

The decision is not free. Holding a position to defer a gain keeps capital in an asset that may no longer be the best one, and the cost of that misallocation can exceed the deferral benefit. The comparison should be made explicitly: what the deferral is worth against what the capital would earn elsewhere, with the eventual tax still payable in both cases unless a step-up or a charitable route applies.

Primary sources: <https://www.irs.gov/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the unrealised gain, the applicable rate, and the resulting liability.
- Record the expected holding period and the return assumed on the deferred tax.
- Compute the deferral benefit as tax times return times time.
- Record the alternative use of the capital and its expected return.
- Record whether a step-up at death or another relief is expected to apply.
- Record the concentration risk of holding for the tax alone.

## Procedure

1. Record the gain and the liability.
2. Record the expected deferral period.
3. Compute the benefit at the assumed return.
4. Compare with the alternative investment's expected return.
5. Record any expected relief.
6. Write the comparison and the decision.

## Anti-patterns

- Treating a deferred gain as an avoided one.
- Holding a concentrated position for the tax alone.
- Ignoring the alternative use of the capital.
- Assuming a relief will apply without checking.
- Computing the benefit without a return assumption.

## Done checklist

- [ ] Gain and liability recorded.
- [ ] Deferral period recorded.
- [ ] Benefit computed.
- [ ] Alternative compared.
- [ ] Relief recorded.
- [ ] Concentration recorded.

The concentration point deserves its own line because it is where deferral becomes expensive: a position held only for the tax is a position whose risk is not being managed, and the deferral benefit computed from a modest return assumption can vanish against a drawdown the holder would not have accepted in any other context.


## Sources

- Tax administration guidance on capital gains: <https://www.irs.gov/>
- Investor education on holding periods: <https://www.investor.gov/introduction-investing>
- Market return data: <https://fred.stlouisfed.org/>
