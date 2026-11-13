---
name: lockup-expiry-flows
domain: investing/lockup-expiry-flows
trigger: "Working out what a lock-up expiry releases and when."
anti_trigger: "Not for predicting selling, and not for the investment case."
scope: "What a lock-up releases, when, and how the supply is absorbed."
status: seedling
---

# Lock-up expiry flows

## Standard

A lock-up is a contractual bar on insiders and pre-issue holders selling for a stated period after an offering. When it expires, a large quantity of shares becomes legally sellable in one moment, and the market knows the date in advance. The supply itself is scheduled, the selling is not: holders may sell, hold, or sell gradually, and the disclosure rarely says which.

The mechanics that decide the impact are the size of the released block relative to the free float and to average daily volume, whether the expiry is staggered across several dates, and whether the holders have a plan in place. A release equal to a few days of volume is absorbed quietly; one equal to months of volume changes the supply-demand balance for as long as it takes to clear, and the market typically begins to price that before the date arrives.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the expiry date and the number of shares released.
- Express the released block as a percentage of free float and in days of average volume.
- Record any staggered tranches and their dates.
- Record whether holders have disclosed a selling plan or intent.
- Record the price relative to the offer and to any vesting or tax thresholds.
- Record the historical behaviour around the issuer's prior expiries where available.

## Procedure

1. Read the lock-up terms from the prospectus.
2. Record the date and share count.
3. Compute the block relative to float and to average volume.
4. Record any staggering and any disclosed plans.
5. Record the price context.
6. Write the analysis with the absorption estimate.

## Anti-patterns

- Treating the expiry date as the selling date.
- Measuring the block against total shares rather than free float.
- Ignoring staggered releases, which spread the supply.
- Assuming holders sell because they can.
- Forgetting that a price above the offer changes the incentive to hold.

## Done checklist

- [ ] Expiry date and share count recorded.
- [ ] Block measured against float and volume.
- [ ] Staggering recorded.
- [ ] Disclosed plans recorded.
- [ ] Price context recorded.
- [ ] Absorption estimate written.

The absorption estimate is worth stating as a range rather than a number, because the variable that matters most — how much of the released block is actually sold — is not observable in advance. A range of ten to forty percent of the block, expressed in days of volume, is a more honest input to a decision than a single assumption.


## Sources

- Offering disclosure and lock-up terms: <https://www.sec.gov/investor>
- Trading practice guidance: <https://www.finra.org/>
- Investor education on new issues: <https://www.investor.gov/introduction-investing>
