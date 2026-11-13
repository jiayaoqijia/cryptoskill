---
name: fully-diluted-count
domain: investing/fully-diluted-count
trigger: "Computing a fully diluted share count and the method behind it."
anti_trigger: "Not for predicting the share price, and not for the investment case."
scope: "Basic versus diluted shares, and the treasury stock method's mechanics."
status: seedling
---

# Fully diluted count

## Standard

The basic count is the shares outstanding. The diluted count adds the shares that would exist if every claim converted, but not all of them convert at full value: the treasury stock method assumes that option proceeds are used to buy shares at the average price, so only the excess of the option count over the shares those proceeds would buy is added.

That method makes dilution price-dependent. When the share price is above the strike, options are in the money and their dilutive effect rises with the price; when it is below, they add nothing. A diluted count computed at one price is therefore not the count at another, and the count used in a per-share calculation should be the one consistent with the price in the numerator.

Primary sources: <https://www.sec.gov/investor> and <https://www.fasb.org/>.

## Decision rules

- Record the basic count and the diluted count from the filing.
- Record the method used for options and its assumed proceeds.
- Record the average price used in the treasury stock method.
- Record the anti-dilutive securities excluded, since a loss-making period excludes them all.
- Recompute the count at a stated share price and record the sensitivity.
- Record convertible securities separately, since the if-converted method differs.

## Procedure

1. Record the basic count from the balance sheet or the equity statement.
2. Record the diluted count and the reconciliation between them.
3. Record the option count and strike distribution.
4. Record the average price used and the method.
5. Recompute at a higher and lower price.
6. Write the count with its method and price stated.

## Anti-patterns

- Using the basic count for a per-share calculation that reflects dilution.
- Computing dilution at a price different from the one in the numerator.
- Assuming a loss-making company's diluted count equals its basic count without checking.
- Treating convertible securities as if they used the treasury stock method.
- Using a stale count after a material issuance.

## Done checklist

- [ ] Basic and diluted counts recorded.
- [ ] Method recorded.
- [ ] Average price recorded.
- [ ] Excluded anti-dilutive securities recorded.
- [ ] Sensitivity to price computed.
- [ ] Convertible treatment recorded.

The count should also be reconciled across periods, because an increase that comes from a new grant programme looks the same in the total as one from acquired companies, and only the reconciliation distinguishes a recurring transfer from a one-off event.


## Sources

- Share count disclosure in filings: <https://www.sec.gov/investor>
- Earnings per share accounting standards: <https://www.fasb.org/>
- Investor education on per-share metrics: <https://www.investor.gov/introduction-investing>
