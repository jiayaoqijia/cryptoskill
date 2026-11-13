---
name: longevity-swaps
domain: investing/longevity-swaps
trigger: "Reading a longevity swap and the risks it leaves with the scheme."
anti_trigger: "Not for actuarial advice, and not for recommending a counterparty."
scope: "Hedging longevity while keeping the assets, and the residual risks."
status: seedling
---

# Longevity swaps

## Standard

A longevity swap transfers the risk that members live longer than assumed to a counterparty, in exchange for a series of payments. The scheme keeps its assets and its investment risk; what it gives up is the longevity exposure, and what it receives is a hedge that pays more if mortality is lighter than the agreed basis.

The residual risks are the point of the analysis. The swap references a set of mortality assumptions and an experience population, and if the scheme's actual membership diverges from that reference — through transfers out, option exercises, or a different mix — the hedge can be imperfect. There is also counterparty risk, since the swap is a long-dated contract with a single entity, and collateral terms that determine what must be posted when the exposure moves.

Primary sources: <https://www.bis.org/> and <https://www.fca.org.uk/>.

## Decision rules

- Record the notional and the reference population the swap covers.
- Record the mortality basis and how it can be revised.
- Record the counterparty and its credit standing, with a date.
- Record the collateral terms and the threshold at which posting begins.
- Record the residual risks: basis, population drift, and counterparty.
- Record the termination terms and the cost of unwinding early.

## Procedure

1. Read the swap documentation for the reference population and basis.
2. Record the notional and the covered liabilities.
3. Record the counterparty and its credit.
4. Record collateral terms and thresholds.
5. Record the residual risks and their measurement.
6. Write the analysis with the hedge's limits stated.

## Anti-patterns

- Treating a longevity swap as removing all longevity risk.
- Ignoring population drift as members transfer out or exercise options.
- Overlooking counterparty risk in a decades-long contract.
- Assuming collateral terms are symmetric.
- Comparing a swap's cost with an insurance premium without the risk difference.

## Done checklist

- [ ] Notional and reference population recorded.
- [ ] Mortality basis recorded.
- [ ] Counterparty and credit recorded.
- [ ] Collateral terms recorded.
- [ ] Residual risks recorded.
- [ ] Termination terms recorded.

A further consideration is the collateral's own cost: a swap that requires posting collateral as mortality improves consumes liquidity precisely when the liability is lengthening, and the scheme's liquidity policy has to accommodate that call. A hedge that creates a funding obligation in the state it protects against is a hedge with a second-order risk.


## Sources

- Insurance and longevity risk standards: <https://www.bis.org/>
- Pensions regulation: <https://www.fca.org.uk/>
- Market and rate data: <https://fred.stlouisfed.org/>
