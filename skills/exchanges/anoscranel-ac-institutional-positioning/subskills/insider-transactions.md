---
name: insider-transactions
domain: investing/insider-transactions
trigger: "Reading an insider transaction filing and separating signal from routine."
anti_trigger: "Not for inferring a view on the business, and not for legal analysis."
scope: "Form 4 timing, codes, and distinguishing signal from compensation."
status: seedling
---

# Insider transactions

## Standard

Insiders must report their transactions within two business days, which makes these filings the timeliest disclosure in the equity market. That timeliness is why they attract attention, and it is also why most of them are noise: grants, option exercises, tax withholding, and planned sales under a pre-arranged schedule are all reported alongside discretionary open-market purchases.

The distinction that matters is between a transaction the insider chose and one that happened to them. A grant, an award vesting, or shares withheld for tax are compensation mechanics. An open-market purchase with the insider's own money, at the market price, is a choice, and a cluster of such purchases across several insiders is the strongest form of this signal the data offers.

Primary sources: <https://www.sec.gov/investor> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Record the transaction code, the number of shares, the price, and the date.
- Separate discretionary open-market transactions from grants, exercises, and withholding.
- Record whether the transaction was made under a pre-arranged plan, where disclosed.
- Record the insider's role and their existing holding, since a purchase by a large holder differs from a small one.
- Record clusters: several insiders buying in the same window is stronger than one.
- Where the filing is ambiguous, record the code and the ambiguity rather than inferring intent.

## Procedure

1. Pull the filing and record the transaction code and terms.
2. Classify the transaction as discretionary or mechanical.
3. Record the insider's role and resulting holding.
4. Check for a pre-arranged plan disclosure.
5. Look for other filings in the same window.
6. Write the summary with the classification stated.

## Anti-patterns

- Counting grants as insider buying.
- Treating a single small purchase as a signal.
- Ignoring pre-arranged sale plans.
- Reading an option exercise as a bullish view.
- Assuming insiders know more than the filing shows.

## Done checklist

- [ ] Code, size, price, date recorded.
- [ ] Transaction classified.
- [ ] Insider role and holding recorded.
- [ ] Plan disclosure checked.
- [ ] Cluster checked.
- [ ] Summary states the classification.

The size of a purchase relative to the insider's compensation also matters: a purchase that is small for the individual is a different statement from one that represents a meaningful share of their wealth, and the filing alone does not say which. Where the record can state the insider's role and the scale of the transaction, it should, rather than counting the trade as a unit of sentiment.


## Sources

- SEC insider filing search: <https://www.sec.gov/edgar/search/>
- Investor education on insider transactions: <https://www.investor.gov/introduction-investing>
- Disclosure requirements: <https://www.sec.gov/investor>
