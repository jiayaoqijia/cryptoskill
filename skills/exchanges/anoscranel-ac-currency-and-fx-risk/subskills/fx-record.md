---
name: fx-record
domain: investing/fx-record
trigger: "Writing the record of currency exposure and hedging decisions."
anti_trigger: "Not for the investment decision, and not for tax reporting."
scope: "The written record: exposure, hedge, cost, and falsifiers."
status: seedling
---

# FX record

## Standard

The FX record states, in one place, what currency exposure the portfolio carries, whether it is intended, how it is hedged, what the hedge costs, and what would show the decision wrong. Without it the exposure drifts: positions change, hedges roll, and the original ratio survives only as a memory.

The record is written at the level of the portfolio rather than the trade, because currency exposure is a portfolio property. Individual conversions are logged in the operational record; the rationale and the ratio belong here.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://fred.stlouisfed.org/>.

## Decision rules

- Record exposure by currency as a share of the portfolio, with the date.
- Record the intended hedge ratio and the reason for it.
- Record the hedge instruments, roll schedule, and annualised cost.
- Record the residual exposures the hedge leaves.
- Write the falsifier: what evidence would show the ratio wrong.
- Review on schedule and on the named triggers; amend, never rewrite.

## Procedure

1. Record exposure shares by currency with the date.
2. Record the hedge ratio and the reason.
3. Record instruments, rolls, and cost.
4. Record residual exposures.
5. Write the falsifier and the review triggers.
6. Amend on changes with dates.

## Anti-patterns

- Recording exposure only after a currency move.
- Omitting the hedge cost.
- Leaving the falsifier unwritten.
- Rewriting the record when the ratio changes.
- Keeping the rationale in the trade log instead of the portfolio record.

## Done checklist

- [ ] Exposure by currency recorded with date.
- [ ] Hedge ratio and reason recorded.
- [ ] Instruments, rolls, and cost recorded.
- [ ] Residual exposures recorded.
- [ ] Falsifier and review triggers written.
- [ ] Amendments dated.

## Sources

- Exchange-rate and rate data: <https://fred.stlouisfed.org/>
- Investor education on currency exposure: <https://www.investor.gov/introduction-investing>
- Regulatory context for portfolio disclosure: <https://www.sec.gov/investor>

The record's most useful line is the reason for the ratio, because it is the only thing that tells a later reader whether the hedge was a policy or a reaction. Ratios without reasons get revised after every currency move; reasons survive the move and are the basis for a calm review.

Keep the record short enough to be read before a decision and complete enough to answer a question a year later. The two constraints meet at roughly one page: exposure, ratio, reason, cost, residuals, falsifier, and the date of the next review.
