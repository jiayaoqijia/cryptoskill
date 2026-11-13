---
name: scenarios-and-sensitivity
domain: investing/scenarios-and-sensitivity
trigger: "Showing how the valuation moves with its drivers."
anti_trigger: "Not for choosing which scenario you prefer."
scope: "Bull, base, and bear cases as driver tables, and the sensitivity that shows what actually moves the value."
status: seedling
---

# Scenarios and sensitivity

## Standard

A single valuation number is a point chosen from a distribution the analyst has not described. Scenario and sensitivity work describes that distribution: which drivers move the value, by how much, and what the bull and bear cases actually assume. The output is not three numbers to average, but three named worlds and the driver values that define them.

Sensitivity analysis is the cheap version: hold the model, flex one assumption at a time, and record the range. Scenario analysis is the honest version: change a coherent set of drivers together, because growth and margins usually move in the same direction in the same world.

Primary sources: <https://pages.stern.nyu.edu/~adamodar/> and <https://osf.io/prereg/>.

## Decision rules

- Scenario drivers are chosen before the values are set, and the same driver set is used for all three cases.
- Bull and bear cases change at least three drivers coherently; changing one driver while holding the rest is sensitivity, not a scenario.
- Every scenario has a stated probability or is explicitly left unweighted; silent weighting by averaging is forbidden.
- Sensitivity tables flex one variable at a time and show the value range.
- The driver that moves value most is named; that is the assumption to monitor afterwards.
- Scenarios are recorded before the market price is compared, so the comparison cannot reshape them.

## Procedure

1. List the five or six drivers that materially affect the model.
2. Choose the ones used for scenarios and record why.
3. Write the bull, base, and bear worlds in one sentence each.
4. Set driver values per scenario and compute the three values.
5. Build a sensitivity table for the top two drivers.
6. Name the dominant driver and set it as a review trigger.
7. Record everything before comparing with the market price.

## Anti-patterns

- Choosing scenario values to bracket the current price.
- Averaging the three cases into a target without saying so.
- Changing a single driver and calling it a scenario.
- Setting scenarios after seeing which one flatters the thesis.
- Building a sensitivity table that varies the least important driver.

## Done checklist

- [ ] Drivers listed and scenario drivers chosen with reasons.
- [ ] Three worlds written in one sentence each.
- [ ] Driver values set per scenario and three values computed.
- [ ] Sensitivity table for the top two drivers built.
- [ ] Dominant driver named and set as a review trigger.
- [ ] Scenarios recorded before the market comparison.

## Sources

- Valuation reference material on scenarios and sensitivity: <https://pages.stern.nyu.edu/~adamodar/>
- Pre-registration practice for stating scenarios before results: <https://osf.io/prereg/>
- Full-text filing search for driver history: <https://www.sec.gov/edgar/search/>
