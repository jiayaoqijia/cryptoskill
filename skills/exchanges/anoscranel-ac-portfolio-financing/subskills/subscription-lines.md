---
name: subscription-lines
domain: investing/subscription-lines
trigger: "Reading how a subscription line changes a fund's reported return."
anti_trigger: "Not for predicting returns, and not for the allocation decision."
scope: "Delayed capital calls and the IRR they flatter."
status: seedling
---

# Subscription lines

## Standard

A subscription line is a facility secured on investors' uncalled commitments that lets a fund pay for investments before calling capital. Instead of drawing from investors on the day of a purchase, the fund borrows and calls the capital later, sometimes much later, once the facility matures or reaches its limit.

The effect on reported performance is arithmetic. Internal rate of return is sensitive to the timing of cash outflows, and delaying the outflow shortens the period over which the return is measured, which raises the annualised figure without any change in the underlying investment. Two funds with identical gross outcomes can report materially different IRRs depending on how long their subscription lines run.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the facility size, its term, and how long the fund may defer calls.
- Record the interest cost and who bears it.
- Record whether the reported return is gross or net of the facility's cost.
- Recompute the return on the basis of investor cash flows, not the fund's.
- Compare the reported IRR with the multiple, which is unaffected by timing.
- Record whether the facility is disclosed in the fund's reporting.

## Procedure

1. Record the facility terms and deferral period.
2. Record the cost and its bearer.
3. Reconstruct investor cash flow dates from the call history.
4. Compute the IRR on those dates.
5. Compare with the reported figure and with the multiple.
6. Write the adjustment with both measures.

## Anti-patterns

- Comparing IRRs across funds with different line lengths.
- Accepting a reported IRR without the cash-flow dates.
- Ignoring the facility's cost as immaterial.
- Treating the multiple as affected by timing, when it is not.
- Assuming the line is disclosed when it is only described generally.

## Done checklist

- [ ] Facility terms recorded.
- [ ] Cost and bearer recorded.
- [ ] Investor cash flows reconstructed.
- [ ] IRR recomputed.
- [ ] Reported versus recomputed compared.
- [ ] Multiple recorded.

The cleanest comparison across funds is the multiple, which measures total value returned against total capital invested and is unaffected by when the calls were made. Reporting the multiple beside every IRR, and recomputing the IRR from investor cash flows where the call history is available, produces a comparison that does not depend on how each manager structured its financing.


## Sources

- Fund reporting and disclosure: <https://www.sec.gov/investor>
- Performance measurement standards: <https://www.cfainstitute.org/>
- Market financing conditions: <https://www.federalreserve.gov/>
