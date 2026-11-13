---
name: wrapper-record
domain: investing/wrapper-record
trigger: "Writing the record of a fund wrapper and what it permits."
anti_trigger: "Not for recommending a fund, and not for legal or tax advice."
scope: "The written record: wrapper, eligibility, limits, and exit mechanics."
status: seedling
---

# Wrapper record

## Standard

The wrapper record states the legal form, the rule set it operates under, the eligibility it requires, the limits it enforces, and the mechanics by which an investor exits. Those five items are what distinguish one vehicle from another holding the same assets, and each of them can change the outcome in a stress that the assets themselves would survive.

Its second function is to make comparison possible across jurisdictions. Two funds with the same strategy can carry different investor protections, different suspension powers, and different redemption rights, and a record that names those differences allows a choice to be made on them rather than on the strategy description alone. The record is written at the point of purchase and amended when the wrapper changes.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- The record states the legal form, domicile, and authorising regulator.
- The rule set is named: UCITS, registered fund, private vehicle, or another framework.
- The eligibility criteria and whether the holder meets them are recorded.
- The limits the wrapper enforces are recorded: diversification, leverage, concentration.
- Exit mechanics are recorded: redemption frequency, notice periods, gates, and suspension powers.
- Review triggers are dated: prospectus change, regulator change, domicile change, fee change.

## Procedure

1. Record the form, domicile, and regulator.
2. Record the rule set and its limits.
3. Record the eligibility criteria and the holder's status.
4. Record the exit mechanics and any suspension power.
5. Record the tax reporting the wrapper creates.
6. Set the review triggers and amend at each.

## Anti-patterns

- Recording the strategy and not the wrapper.
- Omitting the rule set, which is what the form is governed by.
- Assuming eligibility without checking the investor category.
- Leaving the exit mechanics out, which is the part that matters in stress.
- No trigger for a prospectus change.

## Done checklist

- [ ] Form, domicile, and regulator recorded.
- [ ] Rule set and limits recorded.
- [ ] Eligibility recorded and tested.
- [ ] Exit mechanics recorded.
- [ ] Tax reporting recorded.
- [ ] Triggers dated.

The record should also note the wrapper's failure mode in one sentence: what happens to a holder if redemptions exceed the vehicle's capacity to meet them. For an open-end fund it is a gate or a suspension, for a closed-end fund it is a widening discount, and for a private vehicle it is simply waiting, and naming which of the three applies is the fastest way to compare two wrappers that look alike.


## Sources

- Fund regulation and disclosure framework: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- European fund regulation: <https://www.esma.europa.eu/>
