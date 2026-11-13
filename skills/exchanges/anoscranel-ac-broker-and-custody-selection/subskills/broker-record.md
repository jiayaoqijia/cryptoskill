---
name: broker-record
domain: investing/broker-record
trigger: "Writing the provider record that justifies where assets are held."
anti_trigger: "Not for recommending a firm, and not for the investment policy itself."
scope: "The written provider record: structure, cost, controls, and review triggers."
status: seedling
---

# Broker record

## Standard

The provider record states which institution holds what, under which structure, at what total cost, with which controls, and on what evidence the choice was made. It is short, dated, and written before the account is funded, so that a later review can see whether the reasons still hold rather than reconstructing them from memory and marketing material.

It also carries the alternative providers that were rejected and why. That section is what makes the record a decision rather than a preference, and it is what allows a review to notice that the rejected provider has since become cheaper or that the chosen one has changed its custody terms. Providers change; a record that cannot detect change is a record that quietly expires.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://osf.io/prereg/>.

## Decision rules

- The record names the legal custodian, the structure, and the applicable jurisdiction.
- The total cost is stated in basis points per year at a stated activity level.
- The controls in place are listed with their state.
- The rejected alternatives and the reasons are recorded with dates.
- Review triggers are dated: fee change, ownership change, terms change, balance above a threshold.
- The record is append-only, and corrections are dated amendments.

## Procedure

1. State the accounts, the custodian, and the structure.
2. Record the fee stack total and its assumptions.
3. List the controls and their state.
4. Record the alternatives considered and the reasons for rejection.
5. Set the review triggers with dates.
6. File the record with the investment policy and reference it.

## Anti-patterns

- A record that lists the chosen provider without the alternatives.
- Recording fees without an activity assumption.
- Omitting the custody structure because the account "just works".
- No review triggers, so a changed fee schedule goes unnoticed.
- Editing the record instead of amending it.

## Done checklist

- [ ] Custodian, structure, and jurisdiction recorded.
- [ ] Total cost in basis points with assumptions.
- [ ] Controls listed with state.
- [ ] Alternatives and reasons recorded.
- [ ] Review triggers dated.
- [ ] Filed and cross-referenced.

Reviewing the record against the current fee schedule and terms takes minutes and catches the change that matters: providers rarely announce a custody change loudly, and the record's dated assumptions are what make the change visible.

## Sources

- Investor education on brokerage accounts: <https://www.investor.gov/introduction-investing>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Regulatory context for account terms: <https://www.sec.gov/investor>
