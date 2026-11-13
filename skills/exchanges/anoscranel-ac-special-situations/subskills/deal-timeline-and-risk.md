---
name: deal-timeline-and-risk
domain: investing/deal-timeline-and-risk
trigger: "Mapping what must happen for a deal to close and when."
anti_trigger: "Not for predicting a regulatory decision, and not for legal advice."
scope: "Approvals, financing, and the events that break a deal."
status: seedling
---

# Deal timeline and risk

## Standard

A deal closes when a sequence of conditions is satisfied: shareholder votes, regulatory clearances in each jurisdiction, financing, and the absence of a material adverse change. Each condition has a date and an authority, and the timeline is the schedule of those dates. The spread is earned only if every one of them is satisfied, which is why the record lists them individually rather than as a single probability.

The risks that break deals cluster. Regulatory review is the most common and the most uncertain, because the outcome depends on an authority's judgement and the timeline can extend through a second request. Financing is a risk when the consideration is cash and the acquirer is leveraged. A material adverse change clause is rarely invoked and, when it is, it becomes a legal dispute rather than a commercial one.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.sec.gov/investor>.

## Decision rules

- Record each condition: shareholder vote, regulatory clearances, financing, and other consents.
- Record the expected date of each and the authority that decides it.
- Record the outside date and the termination fee.
- Record the regulatory jurisdictions and any history of second requests.
- Record the financing terms and whether they are committed.
- Record the material adverse change clause and its scope.

## Procedure

1. Extract the conditions from the merger agreement.
2. List each with its authority and expected date.
3. Record the outside date and the break fee.
4. Record the regulatory path and any precedent.
5. Record financing commitments.
6. Write the timeline with the conditions that matter most.

## Anti-patterns

- Treating a deal as a single probability rather than a sequence.
- Ignoring the outside date and the termination fee.
- Assuming a regulatory clearance will arrive on the announced timeline.
- Overlooking a financing condition in a leveraged cash deal.
- Treating a material adverse change clause as a routine formality.

## Done checklist

- [ ] Conditions listed with authorities.
- [ ] Expected dates recorded.
- [ ] Outside date and break fee recorded.
- [ ] Regulatory path recorded.
- [ ] Financing recorded.
- [ ] Timeline written.

The outside date is also the calendar anchor for the spread's annualisation: a deal whose expected close slips from one quarter to the next loses a third of its annualised return for every quarter of delay, which is why a timeline change is a repricing event even when every condition remains satisfiable.


## Sources

- Merger agreements and proxy filings: <https://www.sec.gov/edgar/search/>
- Disclosure framework: <https://www.sec.gov/investor>
- Investor education on deal risk: <https://www.investor.gov/introduction-investing>
