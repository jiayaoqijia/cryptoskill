---
name: alternatives-record
domain: investing/alternatives-record
trigger: "Writing the record of an alternative-asset exposure."
anti_trigger: "Not for the purchase decision, and not for portfolio policy."
scope: "The written record: exposure, valuation basis, liquidity terms, and falsifiers."
status: seedling
---

# Alternatives record

## Standard

The record for an alternative asset has to do something a public-market record does not: it must state how the value was arrived at, because there is no observable price to appeal to. That means recording the valuation method, the mark's date and producer, the liquidity terms, and the evidence that would show the valuation wrong.

A record that says "worth X" without the method is not a record; it is an assertion. The useful version says "marked at X by method M on date D, with a sale estimate of X minus a haircut H, and a lockup until date L" — from which a reader can see both the number and its fragility.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Every value carries its method, date, and producer.
- The sale estimate is recorded alongside the mark, with the haircut stated.
- Liquidity terms are recorded as dates and conditions, not adjectives.
- A falsifier is written: which transaction or event would show the mark wrong.
- The record is append-only, and re-marks are appended with their dates.
- The record states the role the holding plays in the portfolio, in one sentence.

## Procedure

1. State the holding and its role in one sentence.
2. Record the mark, the method, the date, and the producer.
3. Record the sale estimate and the haircut.
4. Record the lockup, exit queue, and gates.
5. Write the falsifier.
6. Append re-marks with dates as they occur.

## Anti-patterns

- Recording a value with no method.
- Omitting the sale estimate and haircut.
- Describing liquidity as "long-term" without dates.
- Updating the mark without a date.
- Leaving the portfolio role unstated.

## Done checklist

- [ ] Holding and role stated.
- [ ] Mark with method, date, producer.
- [ ] Sale estimate and haircut recorded.
- [ ] Liquidity terms recorded with dates.
- [ ] Falsifier written.
- [ ] Re-marks appended with dates.

## Sources

- Regulatory context for private-asset valuation and disclosure: <https://www.sec.gov/investor>
- Investor education on alternative investments: <https://www.investor.gov/introduction-investing>
- Rate context for discounting marks: <https://fred.stlouisfed.org/>

The record's second reader is the one who has to price the position years later, when the mark has drifted and the original reasoning is gone. For that reader, the method matters more than the number: a cost-based mark and an appraisal-based mark diverge in what they can support, and only the record can say which was used.

Where an alternative has no observable transaction, record the mark as a range rather than a point, and state the two conditions under which the range's ends would be realised. That converts an unverifiable number into a checkable claim, and it is the closest an illiquid asset can come to a price.

