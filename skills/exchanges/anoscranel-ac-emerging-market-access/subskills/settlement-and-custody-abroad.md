---
name: settlement-and-custody-abroad
domain: investing/settlement-and-custody-abroad
trigger: "Reading the settlement and custody chain for a foreign holding."
anti_trigger: "Not for choosing a custodian, and not for legal advice."
scope: "Settlement cycles, custody chains, and local-agent risk."
status: seedling
---

# Settlement and custody abroad

## Standard

A foreign holding passes through a chain: the global custodian, a local sub-custodian, and the local central securities depository. Each link adds a settlement convention, a legal regime, and a counterparty. A failure at any link is a failure to hold the asset, which is why the chain is worth recording rather than assuming.

Settlement differs too. Cycles vary by market, some require pre-funding, some operate on a delivery-versus-payment basis and some do not, and a market with a longer cycle ties up capital and currency for longer. The operational cost of these differences is real and shows up as funding requirements rather than as fees.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the custody chain: global custodian, sub-custodian, and local depository.
- Record the settlement cycle and whether delivery is against payment.
- Record any pre-funding or collateral requirement.
- Record the local regime's treatment of client assets and segregation.
- Record the sub-custodian's credit standing and its role.
- Record the process for corporate actions and how instructions are passed.

## Procedure

1. Record the custody chain with each entity named.
2. Record the settlement cycle and its funding implications.
3. Record pre-funding requirements.
4. Record segregation and client-asset rules.
5. Record sub-custodian standing.
6. Write the chain summary with the risks named.

## Anti-patterns

- Assuming the global custodian holds the asset directly.
- Ignoring the settlement cycle's funding cost.
- Assuming client-asset segregation applies identically in every market.
- Overlooking the sub-custodian's own credit.
- Treating corporate action processing as automatic.

## Done checklist

- [ ] Custody chain recorded.
- [ ] Settlement cycle recorded.
- [ ] Pre-funding recorded.
- [ ] Segregation rules recorded.
- [ ] Sub-custodian standing recorded.
- [ ] Corporate action process recorded.

The pre-funding requirement is the operational cost that most often surprises an allocator: a market requiring cash on the settlement date, in a currency that must itself be obtained beforehand, turns a small position into a funding commitment that has to be arranged in advance, and the arrangement has its own cost that belongs in the total.


The local depository's rules on client-asset segregation are worth recording as a separate fact from the custodian's: in some markets the depository holds assets in a pooled account at the local level even where the custodian's relationship with its client is segregated, so the protection the client believes it has exists at one link and not at another.


## Sources

- Settlement and custody standards: <https://www.bis.org/>
- Market infrastructure disclosure: <https://www.sec.gov/investor>
- Investment operations standards: <https://www.cfainstitute.org/>
