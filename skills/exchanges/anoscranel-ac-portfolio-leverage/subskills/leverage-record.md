---
name: leverage-record
domain: investing/leverage-record
trigger: "Writing the record of a leveraged position and its review triggers."
anti_trigger: "Not for recommending leverage, and not for tax computation."
scope: "The written record: ratio, cost, maintenance buffer, triggers, and the forced-sale scenario."
status: seedling
---

# Leverage record

## Standard

The leverage record states the loan, the ratio, the cost, the maintenance buffer, and the forced-sale scenario, and it is written before the borrowing begins. It exists so that every later decision — adding, reducing, or holding — starts from the same arithmetic rather than from a refreshed optimism, and so that a call is met with a plan rather than with improvisation.

The forced-sale scenario is the record's core. It names which holdings the broker would sell, the price assumption, the tax consequence, and the portfolio that would remain. A record that contains that scenario has already had the worst conversation; one that does not will have it during the fall, when attention is worst and the options are fewest.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://osf.io/prereg/>.

## Decision rules

- The record states the loan amount, the rate, the collateral, and the current ratio.
- The maintenance buffer is expressed as a percentage fall the portfolio can absorb.
- The cost is stated in currency per year at the current loan size.
- The forced-sale scenario is written in currency, including the tax consequence.
- De-risking and exit triggers are dated and specific.
- The record is append-only; changes to the loan are amendments with dates.

## Procedure

1. Record the loan, rate, collateral, and ratio.
2. Compute and record the buffer as a percentage fall.
3. Record the annual cost at the current size.
4. Write the forced-sale scenario in currency.
5. Record the de-risking and exit triggers.
6. File the record with the investment policy and review it at each trigger.

## Anti-patterns

- Recording the ratio without the buffer.
- Omitting the tax consequence from the forced-sale scenario.
- Writing triggers without levels.
- Updating the record only after a call.
- Keeping the record apart from the portfolio documents it constrains.

## Done checklist

- [ ] Loan, rate, collateral, ratio recorded.
- [ ] Buffer stated as a percentage fall.
- [ ] Annual cost recorded.
- [ ] Forced-sale scenario written in currency.
- [ ] Triggers dated and specific.
- [ ] Filed with the investment policy.

Reading the record before any change to the loan is the discipline that keeps it honest: the ratio, the buffer, and the scenario are all stated in the same terms, so an increase in borrowing is immediately visible as a reduction in the fall the portfolio can absorb.

## Sources

- Investor education on leveraged risk: <https://www.investor.gov/introduction-investing>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Tax treatment of forced realisations: <https://www.irs.gov/>
