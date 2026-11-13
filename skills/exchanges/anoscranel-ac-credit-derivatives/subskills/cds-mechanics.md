---
name: cds-mechanics
domain: investing/cds-mechanics
trigger: "Reading a credit default swap and how its two legs settle."
anti_trigger: "Not for assessing a borrower, and not for predicting defaults."
scope: "Premium legs, protection legs, quoting conventions, and settlement."
status: seedling
---

# CDS mechanics

## Standard

A credit default swap has two legs. The protection buyer pays a periodic premium, usually quarterly, at a spread expressed in basis points of notional per year. The protection seller receives that premium and, on a credit event, pays the difference between par and the recovery value of the reference obligation. The premium continues until maturity or the event, which is why the contract's value moves with both the spread and the probability of an event arriving early.

Quoting conventions matter more than they appear. Spreads are quoted on a standard coupon, with an upfront payment adjusting for the difference between the quoted spread and the coupon, so a contract trading far from the standard coupon settles with a large upfront. Reading a quote as if it were a clean price leads to a materially wrong view of what the position costs to enter.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the reference entity, seniority, currency, and maturity.
- Record the quoted spread, the standard coupon, and the resulting upfront.
- Record the premium payment dates and the day-count convention.
- Record the settlement method: physical, cash, or auction-determined.
- Record the documentation version, since definitions change between them.
- Record which obligations are deliverable and any restructuring clause.

## Procedure

1. Identify the reference entity and the seniority of the obligation.
2. Record the maturity, currency, and documentation version.
3. Record the quoted spread and compute the upfront against the standard coupon.
4. Record the premium schedule and accrual convention.
5. Record the settlement method and deliverable obligations.
6. Write the mechanics summary with its date.

## Anti-patterns

- Reading the spread as if no upfront applies.
- Confusing the reference obligation with the deliverable basket.
- Ignoring the restructuring clause, which changes the event definition.
- Assuming cash settlement when the contract specifies auction settlement.
- Comparing spreads across different seniorities as if they were the same risk.

## Done checklist

- [ ] Reference entity and seniority recorded.
- [ ] Maturity, currency, documentation recorded.
- [ ] Spread and upfront recorded.
- [ ] Premium schedule recorded.
- [ ] Settlement method and deliverables recorded.
- [ ] Summary dated.

The premium leg also has an accrual that changes hands when a trade is closed before a payment date, and that accrued amount is easy to overlook when comparing an entry and an exit spread: the difference between the two spreads is not the whole profit or loss, because the accrual and the upfront both move independently of it.

## Sources

- Standard credit derivatives documentation: <https://www.isda.org/>
- Regulatory context for credit derivatives: <https://www.federalreserve.gov/>
- Investor education on complex instruments: <https://www.investor.gov/introduction-investing>
