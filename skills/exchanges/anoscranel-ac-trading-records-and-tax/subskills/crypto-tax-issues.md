---
name: crypto-tax-issues
domain: investing/crypto-tax-issues
trigger: "Listing the crypto-specific questions that a tax pack must answer."
anti_trigger: "Not for computing crypto tax, and not for advising on treatment."
scope: "The crypto-specific questions: asset classification, perp versus spot, staking, and deduction at source."
status: seedling
---

# Crypto tax issues

## Standard

Crypto assets raise questions that older frameworks do not answer cleanly: is the asset a security, a commodity, or a new category the statute does not name; does a perpetual futures position transfer an asset at all; how are staking rewards and airdrops valued and when; and does a jurisdiction's deduction-at-source regime apply to the trade or only to transfers.

The record's job is to preserve the facts each question depends on: the instrument, the venue's legal entity, the jurisdiction of the account, the date and value at receipt for rewards, and the distinction between spot settlement and derivative settlement. Those facts are cheap to record when they happen and expensive to reconstruct later.

Primary sources: <https://www.irs.gov/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Every crypto holding is recorded with its instrument type: spot asset, derivative, or reward.
- Derivative positions are recorded separately from spot, because their treatment often differs.
- Rewards and airdrops carry a valuation date and a method.
- The venue's legal entity and the account's jurisdiction are recorded per account.
- Deduction-at-source and withholding questions are recorded as questions, with the amount if known.
- Where the law is unsettled, the record says unsettled and flags it.

## Procedure

1. Classify each instrument as spot, derivative, or reward.
2. Record venue entity and account jurisdiction per account.
3. Record rewards with date and valuation method.
4. Record any withholding or deduction at source, with the document.
5. List the unsettled questions for the professional.
6. Write the crypto annex to the tax pack.

## Anti-patterns

- Treating a perpetual position as a spot transfer without checking.
- Valuing a reward at year end instead of at receipt.
- Ignoring the venue's legal entity.
- Assuming a withholding did or did not apply without the document.
- Presenting an unsettled area as settled.

## Done checklist

- [ ] Instruments classified.
- [ ] Venue entity and jurisdiction recorded per account.
- [ ] Rewards dated and valued.
- [ ] Withholdings documented.
- [ ] Unsettled questions listed.
- [ ] Crypto annex written.

## Sources

- Tax administration guidance: <https://www.irs.gov/>
- Investor education on digital-asset reporting: <https://www.investor.gov/introduction-investing>
- Disclosure context for exchange entities: <https://www.sec.gov/investor>

The value of recording these facts early is that most of them are cheap to capture at the time and impossible to reconstruct later: the venue's legal entity, the account's jurisdiction, the price at the moment a reward arrived. A year-end attempt to recover them produces estimates, and estimates in a tax pack invite questions.
