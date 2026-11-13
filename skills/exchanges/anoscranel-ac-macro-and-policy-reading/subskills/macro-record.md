---
name: macro-record
domain: investing/macro-record
trigger: "Writing a macro view as a falsifiable claim with an expiry."
anti_trigger: "Not for making the investment decision, and not for portfolio policy."
scope: "The written macro record: claim, evidence, confidence, falsifier, and review date."
status: seedling
---

# Macro record

## Standard

A macro view is a hypothesis about the economy with a short half-life. Written down properly it has a claim, the evidence behind it, a confidence level, a falsifier, and an expiry — because the relationship between an indicator and an asset is unstable enough that a view held past its expiry is no longer the same view.

The record's purpose is to prevent the quiet conversion of a stale view into a permanent assumption. A portfolio positioned for a recession that never arrived needs the record to show whether the call was wrong or merely early, and only a dated claim with a falsifier can answer that.

Primary sources: <https://fred.stlouisfed.org/> and <https://osf.io/prereg/>.

## Decision rules

- The claim is stated as a falsifiable proposition, not as a direction for prices.
- Evidence is listed with dates and sources.
- Confidence is stated as a level, with the weakest link named.
- A falsifier is written: which observation would retire the claim.
- An expiry date is set; the claim is not extended without a new record.
- The record is append-only; reviews are dated amendments.

## Procedure

1. State the claim in one sentence.
2. List the evidence with dates and sources.
3. State confidence and the weakest link.
4. Write the falsifier and the observation that would trigger it.
5. Set the expiry date.
6. Append reviews and amendments with dates.

## Anti-patterns

- Stating a view as a price direction.
- Leaving the expiry open.
- Extending a claim because a position depends on it.
- Omitting the weakest link.
- Rewriting the record when the view changes.

## Done checklist

- [ ] Claim stated and falsifiable.
- [ ] Evidence dated and sourced.
- [ ] Confidence and weakest link stated.
- [ ] Falsifier written.
- [ ] Expiry date set.
- [ ] Reviews appended with dates.

## Sources

- Macro data for evidence: <https://fred.stlouisfed.org/>
- Pre-registration practice for claims before outcomes: <https://osf.io/prereg/>
- Investor education on economic analysis: <https://www.investor.gov/introduction-investing>

The record's greatest value appears in the review: a claim with a falsifier can be scored, and a scored claim becomes a calibration exercise. A claim without one can only be remembered as right or wrong, which teaches nothing about how much confidence to place in the next one.

Keep the record where the portfolio's decisions are reviewed, and reference it from the positions it justified. A macro claim that lives apart from the position it produced is a commentary; one that sits beside it is an audit trail.
