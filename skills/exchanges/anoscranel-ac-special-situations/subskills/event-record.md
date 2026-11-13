---
name: event-record
domain: investing/event-record
trigger: "Writing the record of a special-situation position and its break case."
anti_trigger: "Not for predicting the outcome, and not for the investment case."
scope: "The written record: spread, timeline, break case, and review dates."
status: seedling
---

# Event record

## Standard

The event record states the position, the spread and its annualisation, the conditions the event must satisfy and when, and the loss if it fails. It is written before the position is opened and it is the document that makes the position reviewable at the moment the event resolves, when attention is entirely on the outcome.

Its second function is to make the break case concrete. A deal that fails does not return the security to its price before the announcement in a straight line; the return depends on what the market expected, on whether a competing bid emerged, and on what the target's standalone prospects became. Recording the break case as a range rather than a single number keeps the down-side honest.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the event, the position, and the consideration.
- The spread is recorded gross, annualised, and with its computation.
- The conditions and dates are listed individually.
- The break case is recorded as a range with its basis.
- Review dates are set at each condition date and at the outside date.
- The record is amended only by dated entries when terms change.

## Procedure

1. Record the event and position.
2. Record the spread and its annualisation.
3. List the conditions and dates.
4. Write the break case as a range.
5. Set review dates.
6. Amend on any change of terms.

## Anti-patterns

- Recording the spread without the break case.
- A break case stated as one number.
- No review dates, so the position is reviewed only when it resolves.
- Amending without a date when terms change.
- Recording the position without its consideration form.

## Done checklist

- [ ] Event and position recorded.
- [ ] Spread and annualisation recorded.
- [ ] Conditions and dates listed.
- [ ] Break case recorded as a range.
- [ ] Review dates set.
- [ ] Amendments dated.

The record also benefits from naming the observation that would change the assessment before the outcome is known: a second request from a regulator, a financing amendment, or a shareholder vote deferred are all visible in filings, and a position whose record names them can respond to the signal rather than to the eventual result.


## Sources

- Event filings and terms: <https://www.sec.gov/edgar/search/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Disclosure framework: <https://www.sec.gov/investor>
