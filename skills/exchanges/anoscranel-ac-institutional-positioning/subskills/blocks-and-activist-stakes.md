---
name: blocks-and-activist-stakes
domain: investing/blocks-and-activist-stakes
trigger: "Reading a block trade print or an activist stake filing."
anti_trigger: "Not for predicting a campaign's outcome, and not for deal advice."
scope: "Block prints, 13D and 13G thresholds, and what an activist filing announces."
status: seedling
---

# Blocks and activist stakes

## Standard

A block trade is a large position crossed away from the continuous book, usually negotiated between a seller and a buyer at a discount or premium to the market. The print is visible, and it is informative: the size, the price relative to the last trade, and the time of day all say something about who needed to transact and how urgently. What it does not say is who was on each side.

An activist filing announces a position taken with intent. Crossing five percent of a class of beneficial ownership triggers a disclosure within a short window, and the choice between the short-form and the intent-form filing is itself the signal: one states that the holder is passive, the other that they may seek to influence the company. The filing names the holder, the size, and often the purpose, which makes it one of the few disclosures that states intent rather than only position.

Primary sources: <https://www.sec.gov/investor> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Record the block's size, price, spread to the last trade, and time.
- Record whether the block was reported on a venue with delayed publication.
- Record the filing type for a stake and the threshold it crossed.
- Record the stated purpose and any intent language in the filing.
- Record the holder's prior position, since an addition differs from a new stake.
- Record the amendment history, because the position and the intent can change.

## Procedure

1. Record the block print and its terms.
2. Compare the price with the prevailing market.
3. Identify the filing type and threshold for any stake disclosure.
4. Record the stated purpose and intent.
5. Record prior and subsequent filings.
6. Write the summary with the filing references.

## Anti-patterns

- Assuming the buyer of a block is an institution accumulating.
- Treating a passive filing as an activist stake.
- Ignoring amendments that change the stated intent.
- Reading a block discount as bearish without the context.
- Assuming a block print is the whole position.

## Done checklist

- [ ] Block terms recorded.
- [ ] Price relative to market recorded.
- [ ] Filing type and threshold recorded.
- [ ] Stated purpose recorded.
- [ ] Prior position and amendments recorded.
- [ ] Summary references the filings.

## Sources

- SEC filing search for ownership disclosures: <https://www.sec.gov/edgar/search/>
- Disclosure rules and thresholds: <https://www.sec.gov/investor>
- Investor education on ownership filings: <https://www.investor.gov/introduction-investing>
