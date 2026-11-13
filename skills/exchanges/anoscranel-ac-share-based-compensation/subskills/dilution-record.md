---
name: dilution-record
domain: investing/dilution-record
trigger: "Writing the record of a company's dilution and compensation programme."
anti_trigger: "Not for recommending a security, and not for tax advice."
scope: "The written record: count, grants outstanding, dilution rate, and offset."
status: seedling
---

# Dilution record

## Standard

The dilution record states the starting count, the grants outstanding by type and strike, the annual dilution rate, the buyback offset, and the cumulative effect over a horizon. It is written so that a later comparison can answer a specific question: how much of the business has been transferred to employees since the record was made, and how much cash was spent to offset it.

Its second function is to preserve the method. The fully diluted count depends on a price and a method, and the dilution rate depends on which issuances are excluded, so a record that states the numbers without the method cannot be compared with anything. The record names the method, the price, and the exclusions, which is what makes the trend meaningful.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- The record states the diluted count with the method and price used.
- Grants outstanding are recorded by type, with the option strike distribution.
- The annual dilution rate is recorded with its exclusions named.
- The buyback offset is recorded as a percentage of the count and as cash spent.
- The cumulative effect at the current rate is stated over a stated horizon.
- Review triggers are dated: annual filing, new grant programme, change of control provision.

## Procedure

1. Record the diluted count and the method behind it.
2. Record grants outstanding by type and strike.
3. Compute and record the dilution rate.
4. Record the buyback offset in shares and cash.
5. State the cumulative effect over the horizon.
6. Review at each trigger and record the change.

## Anti-patterns

- Recording the count without the method that produced it.
- Omitting the strike distribution, which drives the dilution per option.
- Stating a rate without its exclusions.
- Recording the buyback as cash without its share equivalent.
- No trigger, so the record is never updated.

## Done checklist

- [ ] Diluted count and method recorded.
- [ ] Grants recorded by type and strike.
- [ ] Dilution rate recorded with exclusions.
- [ ] Buyback offset recorded in shares and cash.
- [ ] Cumulative effect stated.
- [ ] Triggers dated.

The record's most useful line is the cumulative effect at the current rate, stated as a percentage of the starting count over five years: it converts an annual number that feels small into the share of the business that would be transferred if nothing changed, which is the comparison that makes the programme legible.


## Sources

- Share count and compensation filings: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on dilution: <https://www.investor.gov/introduction-investing>
