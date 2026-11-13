---
name: rights-issues
domain: investing/rights-issues
trigger: "Reading a rights issue and the discount and rump arithmetic it involves."
anti_trigger: "Not for predicting take-up, and not for the investment case."
scope: "Subscription price, discount, renounceability, and the rump placement."
status: seedling
---

# Rights issues

## Standard

A rights issue offers existing holders the right to buy new shares at a subscription price below the market, in proportion to what they already own. The discount is the incentive to participate, and it is arithmetic rather than generosity: the theoretical ex-rights price is a weighted average of the old shares and the new ones, and the discount determines how much value is transferred from non-participants to participants.

Renounceability is the feature that decides whether a holder who does not want to subscribe loses anything. If the rights are renounceable, they can be sold, and the holder captures some of the value; if they are not, the value is lost and the rump is placed with others, which is why non-renounceable issues transfer value away from passive holders. The rump placement price is the market's read on the demand that did not show up.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the ratio, the subscription price, and the market price before the announcement.
- Compute the theoretical ex-rights price and the discount to it.
- Record whether the rights are renounceable and how they trade.
- Record the subscription period and the last day to renounce.
- Record the rump placement terms and the underwriter's commitment.
- Record the use of proceeds and any conditions attaching to the issue.

## Procedure

1. Read the offering document for the ratio and price.
2. Compute the theoretical ex-rights price and the discount.
3. Record renounceability and the trading window.
4. Record the rump arrangements and underwriting.
5. Record the use of proceeds.
6. Write the analysis with the value transfer to non-participants stated.

## Anti-patterns

- Reading the discount as free value for shareholders.
- Ignoring the ex-rights price adjustment on the announcement.
- Treating a non-renounceable issue as equivalent to a renounceable one.
- Forgetting the value transfer from holders who do not act.
- Assuming the underwriter will absorb an unsold rump at the same price.

## Done checklist

- [ ] Ratio and subscription price recorded.
- [ ] Theoretical ex-rights price computed.
- [ ] Discount calculated.
- [ ] Renounceability recorded.
- [ ] Rump and underwriting recorded.
- [ ] Value transfer stated.

The ex-rights adjustment also affects any comparison with historical prices: the price series before and after the ex-date are not comparable without adjustment, and a chart that ignores the adjustment will show a fall that did not occur. The theoretical ex-rights price is the correct reference for anything measured across the announcement.


## Sources

- Rights issue disclosure: <https://www.sec.gov/investor>
- Market practice guidance: <https://www.finra.org/>
- Investor education on corporate actions: <https://www.investor.gov/introduction-investing>
