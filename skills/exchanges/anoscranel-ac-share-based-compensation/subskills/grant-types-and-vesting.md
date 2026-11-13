---
name: grant-types-and-vesting
domain: investing/grant-types-and-vesting
trigger: "Reading the grant types a company uses and when they become shares."
anti_trigger: "Not for tax treatment, and not for recommending a security."
scope: "Options, restricted stock, and units, and when each becomes shares."
status: seedling
---

# Grant types and vesting

## Standard

The grant type determines when shares actually appear in the count. A stock option gives the holder the right to buy at a strike, so it dilutes only when exercised and only by the spread; restricted stock is issued immediately and is in the count from the start, with vesting affecting forfeiture rather than issuance; a restricted stock unit is a promise to deliver shares later, so it sits outside the count until settlement.

Vesting schedules determine the timing of the supply. Time-based vesting releases shares on a calendar, which makes the future dilution predictable; performance-based vesting releases them only if conditions are met, which makes it conditional; and a grant with a cliff releases nothing until a date and then releases everything at once. Recording the schedule and the form together is what makes the forward share count estimable rather than guessed.

Primary sources: <https://www.sec.gov/investor> and <https://www.fasb.org/>.

## Decision rules

- Record each grant type: options, restricted stock, restricted stock units, or another form.
- Record the number outstanding and the weighted average strike for options.
- Record the vesting schedule, including any cliff and any acceleration provision.
- Record whether vesting is time-based, performance-based, or market-based.
- Record the forfeiture rate assumed and the unvested balance.
- Record any repricing or exchange that occurred, since it changes the strike and the count.

## Procedure

1. Read the compensation note for the grant types outstanding.
2. Record the units and, for options, the strike distribution.
3. Record the vesting schedules and cliffs.
4. Record the performance and market conditions attaching.
5. Record forfeiture assumptions and the unvested balance.
6. Write the summary with the forward supply stated.

## Anti-patterns

- Treating restricted stock and restricted stock units as the same instrument.
- Ignoring the strike distribution, which determines the dilution per option.
- Assuming a vesting schedule runs on the disclosed calendar after a modification.
- Overlooking acceleration provisions on a change of control.
- Using a forfeiture rate from a different company's experience.

## Done checklist

- [ ] Grant types recorded with outstanding counts.
- [ ] Strike distribution recorded.
- [ ] Vesting schedules and cliffs recorded.
- [ ] Vesting conditions recorded.
- [ ] Forfeiture assumptions recorded.
- [ ] Forward supply stated.

## Sources

- Compensation disclosure in filings: <https://www.sec.gov/investor>
- Accounting standards for share-based payment: <https://www.fasb.org/>
- Investor education on dilution: <https://www.investor.gov/introduction-investing>
