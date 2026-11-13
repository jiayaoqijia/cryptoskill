---
name: rights-issues
domain: investing/rights-issues
trigger: "Working through a rights issue and the value of the right."
anti_trigger: "Not for predicting the outcome, and not for legal advice."
scope: "Subscription rights, rump placement, and the arbitrage."
status: seedling
---

# Rights issues

## Standard

A rights issue offers existing holders the right to buy new shares at a discount, in proportion to their holding. The right has a value: it is the difference between the subscription price and the theoretical ex-rights price, multiplied by the number of new shares each existing share entitles the holder to buy. That value can be sold rather than exercised, which is what makes the event tradeable.

The mechanics around the right decide its value. The subscription period is finite, and a holder who does nothing receives nothing unless the lapsed rights are sold in a rump placement, whose proceeds are returned to the holder. The ex-rights date changes the price of the existing shares, and a holder who buys on the wrong side of it does not receive the right.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the subscription price, the ratio, and the record date.
- Record the theoretical ex-rights price and the value of the right.
- Record the subscription period and the deadline for action.
- Record the rump placement arrangement and how lapsed rights are handled.
- Record the ex-rights date and the last date to buy with the right.
- Record whether the right is listed and tradeable.

## Procedure

1. Record the terms and the record date.
2. Compute the theoretical ex-rights price.
3. Compute the value of one right.
4. Record the subscription window and deadline.
5. Record the rump arrangement.
6. Write the summary with the action required.

## Anti-patterns

- Ignoring lapsed rights and assuming the value is lost quietly.
- Buying shares on the ex-rights date expecting the right.
- Treating the right's value as the discount to the subscription price.
- Missing the subscription deadline.
- Assuming the rump placement returns full value.

## Done checklist

- [ ] Terms and record date recorded.
- [ ] Theoretical ex-rights price computed.
- [ ] Right value computed.
- [ ] Subscription window recorded.
- [ ] Rump arrangement recorded.
- [ ] Action required stated.

The subscription decision also depends on the holder's view of the company rather than on the right's value in isolation: exercising at a discount is only advantageous if the shares are worth more than the subscription price, and a right that trades below its theoretical value is telling the holder that the market disagrees with the arithmetic.


## Sources

- Rights issue filings: <https://www.sec.gov/edgar/search/>
- Disclosure and rights framework: <https://www.sec.gov/investor>
- Investor education on rights issues: <https://www.investor.gov/introduction-investing>
