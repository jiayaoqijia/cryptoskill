---
name: unitranche-and-splits
domain: investing/unitranche-and-splits
trigger: "Reading a unitranche or a first-out and last-out split."
anti_trigger: "Not for pricing the loan, and not for fund selection."
scope: "Unitranche, first-out and last-out, and the agreement among lenders."
status: seedling
---

# Unitranche and splits

## Standard

A unitranche collapses the senior and subordinated layers into one facility with a single set of terms, which lets a borrower deal with one lender group and lets a lender offer a larger commitment. Behind the single facility, lenders often agree among themselves to split the economics and the recovery: a first-out tranche takes a lower rate and is repaid first, a last-out tranche takes a higher rate and absorbs the first loss.

That intercreditor agreement is the important document for a holder of either tranche. It defines the payment waterfall, the voting rights, the ability of each tranche to act in a default, and what happens if the parties disagree. A last-out holder who has not read the voting provisions may find that the first-out group controls every decision that matters.

Primary sources: <https://www.federalreserve.gov/> and <https://www.cfainstitute.org/>.

## Decision rules

- Record which tranche is held and its place in the waterfall.
- Record the rates, the fees, and the allocation of any recovery.
- Record the voting provisions and the thresholds for action.
- Record who controls the agent role and the enforcement decision.
- Record the circumstances in which the tranches can turn against each other.
- Record the transfer rights of each tranche.

## Procedure

1. Identify the tranche and its waterfall position.
2. Record the economics of the held tranche.
3. Record voting thresholds and the agent's powers.
4. Record enforcement control.
5. Record the conflict scenarios.
6. Write the split summary.

## Anti-patterns

- Treating a unitranche as a single undifferentiated loan.
- Ignoring the intercreditor voting provisions.
- Assuming the holder's tranche controls enforcement.
- Comparing tranche yields without the loss position.
- Missing transfer rights that differ between tranches.

## Done checklist

- [ ] Tranche and waterfall recorded.
- [ ] Economics recorded.
- [ ] Voting thresholds recorded.
- [ ] Enforcement control recorded.
- [ ] Conflict scenarios recorded.
- [ ] Transfer rights recorded.

The waterfall also governs what happens outside a default: a first-out tranche is usually repaid first from any prepayment or asset sale, so a last-out holder's exposure can grow as the facility amortises unevenly. Recording the amortisation priority alongside the default waterfall is what shows how the tranche mix changes over the loan's life without any new lending taking place.

The intercreditor agreement should be read for what it says about a sale of the business: enforcement often requires a threshold of both tranches or of the agent alone, and a structure in which the first-out group can sell the collateral without the last-out's consent gives the junior tranche a very different recovery profile from the one its yield implies.


## Sources

- Credit market structure: <https://www.federalreserve.gov/>
- Credit analysis standards: <https://www.cfainstitute.org/>
- Fund disclosure: <https://www.sec.gov/investor>
