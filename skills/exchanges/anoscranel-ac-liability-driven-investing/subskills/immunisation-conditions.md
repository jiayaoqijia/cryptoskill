---
name: immunisation-conditions
domain: investing/immunisation-conditions
trigger: "Testing whether an immunised portfolio is actually immunised."
anti_trigger: "Not for guaranteeing a return, and not for actuarial advice."
scope: "What immunisation requires, and the conditions that break it."
status: seedling
---

# Immunisation conditions

## Standard

Immunisation is the construction of a bond portfolio whose value at a target horizon is protected against rate changes, within a range. It requires three things: matching duration between assets and liabilities, matching the present value of the two, and rebalancing as duration drifts with time and rate moves. Without the third, the position becomes unmatched within months of being established.

The conditions that break it are worth naming. Convexity differences mean the protection holds only for small rate moves and fails for large ones, in a direction that is usually favourable for the asset holder but not always. Cash flows must be reinvested at the assumed rate, which is unavailable if the curve has shifted. And a default in the portfolio removes both the cash flow and the immunisation simultaneously.

Primary sources: <https://www.federalreserve.gov/> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the target horizon and the liability stream being immunised.
- Record duration, present value, and the rebalancing rule.
- Record the convexity of each side and the direction of the mismatch.
- Record the assumed reinvestment rate and its sensitivity.
- Record the credit quality of the immunising assets and the default assumption.
- Record the rebalancing frequency and the cost of rebalancing.

## Procedure

1. Record the horizon and the liability present value.
2. Match duration and value at inception.
3. Record the convexity difference.
4. Set the rebalancing rule and frequency.
5. Record the reinvestment assumption.
6. Write the immunisation summary with its conditions.

## Anti-patterns

- Calling a portfolio immunised without a rebalancing rule.
- Assuming protection holds for large rate moves.
- Ignoring the credit risk in the immunising assets.
- Assuming cash flows can be reinvested at the entry rate.
- Setting the horizon and then never revisiting it.

## Done checklist

- [ ] Horizon and liability value recorded.
- [ ] Duration and value matched.
- [ ] Convexity difference recorded.
- [ ] Rebalancing rule set.
- [ ] Reinvestment assumption recorded.
- [ ] Credit assumption recorded.

The rebalancing requirement is also a cost: each adjustment trades against a spread, and a portfolio rebalanced monthly to maintain a duration match can spend more on transaction costs than the mismatch it is correcting would have cost, so the frequency should be set against the size of the drift it controls.

A stronger form of the test is to run the portfolio through the rate moves of the last two decades and ask at each horizon whether the terminal value stayed above the liability: a construction that survives the average move but fails the two or three largest is an immunisation that works in the conditions it was calibrated for and not in the ones that matter.

## Sources

- Interest-rate and policy data: <https://www.federalreserve.gov/>
- Investment management standards: <https://www.cfainstitute.org/>
- Yield series: <https://fred.stlouisfed.org/>
