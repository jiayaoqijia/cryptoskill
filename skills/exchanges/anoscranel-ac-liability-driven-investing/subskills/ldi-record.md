---
name: ldi-record
domain: investing/ldi-record
trigger: "Writing the record of a liability-driven mandate."
anti_trigger: "Not for recommending an allocation, and not for the actuarial valuation itself."
scope: "The written record: funding basis, surplus risk, hedge ratio, and triggers."
status: seedling
---

# LDI record

## Standard

The liability-driven record states the funding ratio and its basis, the surplus risk being managed, the hedge ratio achieved, the key-rate residuals after matching, and the de-risking triggers. It also records the liability assumptions, because the entire hedge is calibrated against them and a change in the discount basis moves both sides.

The record's distinguishing feature is that it holds two sides. An asset-only record can be read in isolation; this one cannot, because a fall in assets accompanied by a larger fall in liabilities is an improvement. Any review that reads only the asset side will draw the opposite conclusion from the same numbers, which is why the paired presentation is not a formatting choice but the substance.

Primary sources: <https://www.cfainstitute.org/> and <https://osf.io/prereg/>.

## Decision rules

- Record assets, liabilities, and the ratio on a common basis and date.
- Record the discount basis and the assumptions behind the liability.
- Record surplus risk with the window over which it was measured.
- Record the hedge ratio and the key-rate residuals.
- Record the de-risking triggers and the current distance to each.
- Record any change in benefit policy or contribution schedule in the period.

## Procedure

1. Record the paired valuation.
2. Record the basis and assumptions.
3. Record surplus risk and its measurement window.
4. Record the hedge ratio and residuals.
5. Record triggers and distances.
6. Review at each trigger and at any basis change.

## Anti-patterns

- Recording only the asset side.
- Mixing valuation dates between the two sides.
- Recording a hedge ratio without the residual exposures.
- Leaving the liability assumptions out of the record.
- Reviewing the ratio without the contributions in the period.

## Done checklist

- [ ] Paired valuation recorded.
- [ ] Basis and assumptions recorded.
- [ ] Surplus risk recorded with window.
- [ ] Hedge ratio and residuals recorded.
- [ ] Triggers and distances recorded.
- [ ] Policy changes recorded.

The record should also carry the contribution paid in the period, because a funding ratio that improved because of a contribution is a different fact from one that improved because assets rose, and a review that cannot separate the two will credit the investment strategy with a decision taken by the sponsor.

Storing the assumptions that produced the liability, rather than only the resulting figure, is what makes a later change auditable: when a discount basis or a longevity assumption is revised, the record is the only place that can say how much of a funding move came from the revision and how much from the market.

## Sources

- Investment management standards: <https://www.cfainstitute.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Interest-rate and policy data: <https://www.federalreserve.gov/>
