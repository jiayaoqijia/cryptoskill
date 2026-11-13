---
name: valuation-record
domain: investing/valuation-record
trigger: "Writing the valuation record with its assumptions, range, and falsifiers."
anti_trigger: "Not for making the buy or sell decision, and not for the research record itself."
scope: "The written valuation: assumptions, outputs, ranges, and the facts that would falsify it."
status: seedling
---

# Valuation record

## Standard

A valuation that cannot be re-run by someone else is an opinion. The record exists so the analysis can be checked: method chosen, assumptions with their sources, the outputs, the range, the dominant driver, and the facts that would show the valuation wrong. It is written before the market price is compared, so the comparison is a finding rather than an input.

The record also carries the falsifiers. If the valuation rests on margin expansion, the record states which reported margin would falsify it. That converts the model from a spreadsheet into a testable claim.

Primary sources: <https://osf.io/prereg/> and <https://pages.stern.nyu.edu/~adamodar/>.

## Decision rules

- The record states the method, the assumptions, the outputs, and the range in that order.
- Every assumption carries a source or a stated judgement, and a confidence level.
- The range is reported, never a single point presented as precision.
- The dominant driver is named, and its falsifier is written.
- The record is append-only; amendments are dated.
- The comparison with the market price is recorded as a separate section, after the valuation is complete.

## Procedure

1. State the method and the reason it fits.
2. List assumptions in a table with value, source, and confidence.
3. Report outputs: base value, range, terminal share of value.
4. Name the dominant driver and write its falsifier.
5. Add the dated amendments rule.
6. Append the market-price comparison with its date.

## Anti-patterns

- Presenting a single number with no range.
- Omitting the assumptions table because the model exists.
- Writing the valuation after seeing the price.
- Leaving falsifiers implicit.
- Editing the record silently when a driver changes.

## Done checklist

- [ ] Method and fit stated.
- [ ] Assumption table with sources and confidence.
- [ ] Outputs, range, and terminal share reported.
- [ ] Dominant driver and falsifier written.
- [ ] Append-only rule recorded.
- [ ] Market comparison appended with date.

## Sources

- Pre-registration practice for assumptions before results: <https://osf.io/prereg/>
- Valuation reference material: <https://pages.stern.nyu.edu/~adamodar/>
- Full-text filing search for source data: <https://www.sec.gov/edgar/search/>

A valuation record is written for the person who will re-run it after the outcome is known, when the reasoning has to stand without the analyst present. That reader needs the assumptions, not the conclusion: the conclusion they can see in the price, but the assumptions they cannot recover from anywhere else.

