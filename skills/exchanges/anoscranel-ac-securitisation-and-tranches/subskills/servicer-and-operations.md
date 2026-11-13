---
name: servicer-and-operations
domain: investing/servicer-and-operations
trigger: "Assessing the servicing arrangement and the operational risk in a pool."
anti_trigger: "Not for predicting servicing failures, and not for legal advice."
scope: "Servicing standards, commingling, replacement, and the operational risk in the pool."
status: seedling
---

# Servicer and operations

## Standard

The servicer collects payments, manages delinquencies, and decides when to modify or foreclose. Those decisions determine the pool's realised cash flow, which means the servicer is a risk the structure cannot fully price: a servicer that advances aggressively preserves cash flow, one that does not delays it, and a transfer to a backup servicer can disrupt collections for months.

Commingling is the sharper risk. If collections pass through the servicer's own accounts before reaching the trust, an insolvency of the servicer can trap cash that belongs to noteholders. The documents address this with a trigger that requires collections to be deposited directly into a trust account once the servicer's rating falls, and the adequacy of that trigger is worth reading.

Primary sources: <https://www.sec.gov/investor> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the servicer's identity, its rating, and its experience with the asset class.
- Record the servicing standard: the obligation owed to noteholders.
- Record the advance obligations and the conditions under which they cease.
- Record the commingling trigger and the deposit arrangements before and after it.
- Record the backup servicer and the transfer mechanics.
- Record any fee that ranks ahead of noteholders in the waterfall.

## Procedure

1. Identify the servicer and its role in the structure.
2. Record the servicing standard and advance obligations.
3. Record the commingling provisions and trigger.
4. Record the backup servicer arrangement.
5. Record servicing fees and their ranking.
6. Write the operational summary with its concentration.

## Anti-patterns

- Treating servicing as a back-office detail.
- Ignoring the point at which advances stop.
- Assuming commingling protections activate before the rating trigger.
- Overlooking the servicer's own credit.
- Ignoring a sole servicer with no backup.

## Done checklist

- [ ] Servicer identified with rating.
- [ ] Servicing standard recorded.
- [ ] Advance obligations recorded.
- [ ] Commingling provisions recorded.
- [ ] Backup arrangement recorded.
- [ ] Fee ranking recorded.

The servicing fee also deserves attention for its ranking: it typically sits ahead of the noteholders in the waterfall, which means it is paid through the stress that stops everything else, and a servicer with a large portfolio of its own distressed loans has an incentive to prioritise its own book over the trust's.

A single servicer with no backup and a large book is a concentration the structure discloses rather than solves, and the record should name it as one: the loss would arrive through the cash flow rather than through the collateral, which is the kind of risk that ratings modelled least well.

## Sources

- Servicing and transaction disclosure: <https://www.sec.gov/investor>
- Regulatory framework for servicing: <https://www.federalreserve.gov/>
- Securitisation operational standards: <https://www.bis.org/>
