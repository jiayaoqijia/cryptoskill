---
name: clearing-and-ccps
domain: investing/clearing-and-ccps
trigger: "Understanding what a central counterparty does and what it requires."
anti_trigger: "Not for predicting a clearing failure, and not for legal advice."
scope: "Novation, margin at the clearing house, and default funds."
status: seedling
---

# Clearing and central counterparties

## Standard

A central counterparty becomes the buyer to every seller and the seller to every buyer through novation. That substitution removes bilateral credit exposure between the original parties and replaces it with exposure to the clearing house, which is why clearing is treated as a risk reduction even though it concentrates risk in one entity.

The concentration is managed through margin and a default fund. Members post initial margin against potential future exposure and variation margin against current exposure, and they contribute to a mutualised fund that absorbs losses if a member defaults and its margin is exhausted. Those two layers are what a participant should understand before assuming that a cleared trade carries no credit risk.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record which clearing house the trade is novated to and its jurisdiction.
- Record the initial margin methodology and the variation margin frequency.
- Record the default fund contribution and how it can be called.
- Record the margin eligibility and haircuts for posted collateral.
- Record the member through whom access is obtained, if indirect.
- Record the portability arrangements if the member fails.

## Procedure

1. Identify the clearing house and the clearing member.
2. Record margin requirements and their methodology.
3. Record default fund obligations.
4. Record collateral eligibility and haircuts.
5. Record the portability and default management framework.
6. Write the summary with the exposures named.

## Anti-patterns

- Treating a cleared trade as free of credit risk.
- Ignoring default fund calls in the capital calculation.
- Assuming collateral posted retains its market value.
- Overlooking the clearing member's own credit standing.
- Reading the margin schedule without the methodology behind it.

## Done checklist

- [ ] Clearing house and member recorded.
- [ ] Margin methodology recorded.
- [ ] Default fund recorded.
- [ ] Collateral terms recorded.
- [ ] Portability recorded.
- [ ] Exposures named.

The practical consequence for a participant is that clearing moves the question rather than removing it: the exposure is no longer to the original counterparty but to a mutualised pool, and the pool's strength depends on the margin of every other member. A clearing house that is well capitalised against normal conditions can still call for additional contributions in a stress event, and that call is a funding obligation which arrives exactly when funding is scarce.


## Sources

- Clearing and settlement standards: <https://www.bis.org/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on clearing: <https://www.investor.gov/introduction-investing>
