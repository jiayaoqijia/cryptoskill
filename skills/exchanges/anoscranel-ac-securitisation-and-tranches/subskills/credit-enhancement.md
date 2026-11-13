---
name: credit-enhancement
domain: investing/credit-enhancement
trigger: "Measuring how much loss the structure absorbs before a tranche is touched."
anti_trigger: "Not for predicting losses, and not for rating the deal."
scope: "Overcollateralisation, excess spread, reserve accounts, and how much loss they absorb."
status: seedling
---

# Credit enhancement

## Standard

Enhancement is the loss-absorbing capacity beneath a tranche, and it comes in three forms. Subordination is the junior tranches that take losses first. Overcollateralisation is the excess of pool balance over note balance, which absorbs losses without any cash movement. Excess spread is the difference between the interest earned on the pool and the interest paid on the notes, which can be trapped in a reserve rather than distributed.

The three behave differently under stress. Subordination is fixed unless the pool amortises unevenly; overcollateralisation shrinks as losses reduce the pool; and excess spread disappears first, because it is the most sensitive to rising defaults and falling recoveries. A tranche described as having eight percent enhancement may be relying mostly on spread that vanishes in the scenario it is meant to protect against.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record subordination as a percentage of the pool at closing.
- Record overcollateralisation and how it amortises.
- Record excess spread and whether it is trapped or distributed.
- Record reserve accounts, their target levels, and their release conditions.
- Record which enhancement absorbs losses first and which can disappear.
- Record the enhancement required to breach each rating level.

## Procedure

1. Record the capital structure and subordination percentages.
2. Record overcollateralisation at closing and its amortisation rule.
3. Record excess spread and the trapping mechanism.
4. Record reserve accounts and target balances.
5. Rank the enhancement by how quickly each erodes.
6. Write the enhancement summary with its weakest component.

## Anti-patterns

- Adding subordination and excess spread into one "enhancement" figure.
- Assuming trapped spread stays trapped when a trigger releases it.
- Ignoring overcollateralisation's shrinkage under losses.
- Treating enhancement at closing as the enhancement today.
- Comparing enhancement percentages across asset classes.

## Done checklist

- [ ] Subordination recorded.
- [ ] Overcollateralisation recorded.
- [ ] Excess spread and trapping recorded.
- [ ] Reserves recorded.
- [ ] Erosion ranking written.
- [ ] Weakest component named.

A further point is that enhancement measured at closing is a statement about the pool as it was originated, and pools change: a revolving structure can add receivables with different characteristics, a static pool can concentrate as it amortises, and a deal that was eight percent enhanced can be four percent enhanced without a single loss if the collateral mix has shifted.

## Sources

- Securitisation disclosure and standards: <https://www.sec.gov/investor>
- Capital and securitisation framework: <https://www.bis.org/>
- Regulatory market context: <https://www.federalreserve.gov/>
