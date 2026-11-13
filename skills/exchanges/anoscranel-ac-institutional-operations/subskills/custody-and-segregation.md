---
name: custody-and-segregation
domain: investing/custody-and-segregation
trigger: "Establishing how institutional assets are held and protected."
anti_trigger: "Not for legal advice, and not for assessing a custodian's solvency."
scope: "Nominee, sub-custody, segregation, and rehypothecation."
status: seedling
---

# Custody and segregation

## Standard

Institutional assets are typically held through a chain: the client's account at a custodian, the custodian's omnibus account at a sub-custodian or central securities depository, and the depository's records. Each link determines what happens if an entity in the chain fails, and the protections differ by jurisdiction and by the terms of the account.

Segregation is the central concept. Client assets held in segregated accounts are not available to the firm's creditors; assets that may be rehypothecated are, in economic substance, lent to the firm. The record should state which of the two applies to each holding, because the answer decides the exposure in a failure and it is usually buried in a schedule rather than stated in the summary.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the custody chain: client, custodian, sub-custodian, depository.
- Record whether assets are segregated or held in an omnibus account.
- Record the rehypothecation permissions and their limits.
- Record the jurisdiction whose insolvency rules apply to each link.
- Record the reconciliation frequency and the reporting the client receives.
- Record the exceptions: assets held outside the standard chain and why.

## Procedure

1. Map the custody chain for each asset class.
2. Record segregation status at each link.
3. Record rehypothecation permissions.
4. Record the applicable insolvency regimes.
5. Record reconciliation and reporting.
6. Write the custody summary with exceptions named.

## Anti-patterns

- Assuming segregation applies throughout the chain.
- Ignoring rehypothecation because it is standard.
- Treating an omnibus account as equivalent to a segregated one.
- Overlooking assets held outside the main custodian.
- Reading the summary rather than the schedule.

## Done checklist

- [ ] Custody chain mapped.
- [ ] Segregation recorded per link.
- [ ] Rehypothecation recorded.
- [ ] Insolvency regimes recorded.
- [ ] Reconciliation recorded.
- [ ] Exceptions named.

A further record field is the reconciliation exception process: assets that do not match the custodian's records on the daily reconciliation are the earliest signal that something has gone wrong in the chain, and the record should state who investigates, within what period, and what escalation follows if the difference persists across two cycles.


The reconciliation report is therefore the document to ask for when assessing any custody arrangement: it shows whether the chain agrees with itself on a normal day, which is the only evidence available before a day when it does not.


## Sources

- Client asset protection standards: <https://www.bis.org/>
- Custody and broker-dealer regulation: <https://www.sec.gov/investor>
- Investor education on custody: <https://www.investor.gov/introduction-investing>
