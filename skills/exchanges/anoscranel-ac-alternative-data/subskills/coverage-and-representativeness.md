---
name: coverage-and-representativeness
domain: investing/coverage-and-representativeness
trigger: "Checking whether a panel represents the population being modelled."
anti_trigger: "Not for predicting returns, and not for pipeline design."
scope: "Who is in the panel, who is missing, and what that does to inference."
status: seedling
---

# Coverage and representativeness

## Standard

A dataset built from card transactions, app installs, or web traffic covers a subset of the population, and the subset is rarely random. It over-represents some geographies, some income levels, and some kinds of merchant, and the bias is stable enough to be invisible in a single period but decisive when the data is used to forecast an aggregate.

The test is to compare the panel with a known aggregate on a measure both share. If the panel's share of a category differs from the aggregate and the difference is stable, the panel can still be used with an adjustment; if the difference moves, the relationship being modelled may be changing for reasons unconnected to the business. Either way the comparison belongs in the record rather than being assumed away.

Primary sources: <https://www.nber.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record who is in the panel and how they were selected.
- Record who is systematically absent.
- Compare the panel with a known aggregate on a shared measure.
- Record whether the discrepancy is stable or moving.
- Record any adjustment applied to reconcile the panel with the aggregate.
- Record the period and the aggregate source used for the comparison.

## Procedure

1. Describe the panel's selection.
2. Identify likely absences.
3. Find an aggregate with a comparable measure.
4. Compute the discrepancy and its stability.
5. Record any adjustment.
6. Write the coverage assessment.

## Anti-patterns

- Assuming a large panel is representative.
- Comparing the panel with an aggregate on a measure defined differently.
- Applying an adjustment without recording its derivation.
- Ignoring a discrepancy that grows over time.
- Treating coverage as a fixed property rather than a moving one.

## Done checklist

- [ ] Selection described.
- [ ] Absences identified.
- [ ] Aggregate comparison made.
- [ ] Stability assessed.
- [ ] Adjustment recorded.
- [ ] Assessment written.

The direction of the bias matters as much as its size: a panel that over-represents large merchants will overstate aggregate growth when large merchants are growing faster, and the error is systematic rather than random, which means more data does not correct it. Recording the direction lets a user adjust or discount the signal rather than treating the whole dataset as unusable.


## Sources

- Research methods on sampling and coverage: <https://www.nber.org/>
- Statistical aggregates for comparison: <https://fred.stlouisfed.org/>
- Disclosure context: <https://www.sec.gov/investor>
