---
name: issuance-record
domain: investing/issuance-record
trigger: "Writing the record of a primary issuance and its supply calendar."
anti_trigger: "Not for recommending participation, and not for the investment case."
scope: "The written record: issue terms, supply calendar, and dilution."
status: seedling
---

# Issuance record

## Standard

The issuance record states the terms of the issue, the supply it creates, and the dates on which that supply becomes sellable. It is written before the position, and its function is to convert a set of contractual dates into a calendar: the pricing date, the settlement date, the stabilisation window's end, and every lock-up expiry across the register.

The dilution section is what distinguishes it from a trade note. An issue changes the share count, and the change is not only the new shares sold: options, warrants, convertibles, and the greenshoe all add to the fully diluted count, and the difference between basic and diluted is the number that matters for per-share arithmetic afterwards. Recording it at the issue means the later comparison has a starting point.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- The record states the issue type, size, price, and gross proceeds.
- Primary and secondary components are separated.
- The supply calendar lists every date on which sellable shares increase.
- Dilution is recorded as a percentage of the fully diluted count, including options and warrants.
- The greenshoe and any stabilisation window are recorded with dates.
- The record is append-only; amendments carry dates as terms change.

## Procedure

1. Record the issue terms and proceeds.
2. Separate primary from secondary.
3. Build the supply calendar from the lock-up and stabilisation terms.
4. Compute dilution on a fully diluted basis.
5. Record the syndicate and the stabilising manager.
6. Review at each calendar date and record what occurred.

## Anti-patterns

- Recording the deal size without the dilution.
- Omitting the supply calendar, which is the actionable part.
- Measuring dilution on basic shares only.
- Ignoring the stabilisation window's end.
- Amending the entry record after the fact.

## Done checklist

- [ ] Issue terms and proceeds recorded.
- [ ] Primary and secondary separated.
- [ ] Supply calendar built with dates.
- [ ] Dilution computed on a fully diluted basis.
- [ ] Greenshoe and window recorded.
- [ ] Reviews dated at each calendar point.

The record should also note what the issue does to the existing holders' position in percentage terms, not only to the share count: a shareholder who does not participate in a primary offering is diluted by the ratio of new shares to the old, and stating that percentage at the issue makes the cost of inaction explicit rather than leaving it to be discovered at the next report.


## Sources

- Issuance disclosure requirements: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market practice guidance: <https://www.finra.org/>
