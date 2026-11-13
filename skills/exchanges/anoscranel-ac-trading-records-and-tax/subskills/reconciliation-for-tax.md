---
name: reconciliation-for-tax
domain: investing/reconciliation-for-tax
trigger: "Matching venue statements to the desk's own records before a tax pack is built."
anti_trigger: "Not for filing, and not for interpreting a jurisdiction's rules."
scope: "Matching venue statements to records, and how transfers, airdrops, and forks enter the picture."
status: seedling
---

# Reconciliation for tax

## Standard

Venue statements and the desk's records disagree, and the disagreement is normal: a fee reported differently, a transfer missing from one side, a staking reward valued at a different moment. Reconciliation is the process of explaining every difference, not eliminating it, because the explanation is what a professional needs.

Three categories cause most of the trouble. Transfers between the desk's own accounts look like a disposal on one statement and an acquisition on another. Airdrops and forks arrive without a purchase, so their basis comes from a valuation at receipt that somebody must record. And rewards accrue continuously, which makes the valuation date a choice that must be stated.

Primary sources: <https://www.irs.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Every difference between statement and record is explained, with the explanation kept.
- Internal transfers are matched on both sides and excluded from disposals.
- Airdrops, forks, and rewards are recorded with a valuation date and method.
- Fee differences between venue and record are resolved in favour of the venue statement, with a note.
- Unmatched items are listed explicitly; they are not averaged away.
- The reconciled file is dated and versioned; the prior version is retained.

## Procedure

1. Export venue statements for the full period.
2. Match every line against the desk record.
3. Categorise unmatched items: transfer, reward, fee, or unknown.
4. Resolve each category with its rule; list the unknowns.
5. Record the valuation method for rewards and airdrops.
6. Date the reconciled file and retain the prior version.

## Anti-patterns

- Treating a transfer as a sale.
- Valuing an airdrop at a later date to change the gain.
- Averaging unmatched items.
- Overwriting a reconciled file with a new version.
- Leaving fees unmatched because the amount is small.

## Done checklist

- [ ] Statements exported for the full period.
- [ ] Every line matched or categorised.
- [ ] Internal transfers excluded from disposals.
- [ ] Reward and airdrop valuation method recorded.
- [ ] Unknowns listed.
- [ ] Reconciled file dated and versioned.

## Sources

- Tax administration guidance on records and basis: <https://www.irs.gov/>
- Transaction reporting context: <https://www.sec.gov/investor>
- Investor education on record keeping: <https://www.investor.gov/introduction-investing>

Keep the reconciliation file alongside the raw exports rather than inside them, so that a re-run produces the same result from the same inputs. A reconciliation that cannot be reproduced is a narrative, and narratives do not survive review.
