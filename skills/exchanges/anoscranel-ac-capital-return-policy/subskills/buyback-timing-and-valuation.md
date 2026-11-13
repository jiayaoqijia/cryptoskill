---
name: buyback-timing-and-valuation
domain: investing/buyback-timing-and-valuation
trigger: "Testing whether a company bought its own shares at sensible prices."
anti_trigger: "Not for predicting the share price, and not for the investment case."
scope: "Whether repurchases happen at sensible prices, and how to test it."
status: seedling
---

# Buyback timing and valuation

## Standard

A repurchase creates value for continuing holders when the shares are bought below intrinsic value and destroys it when they are bought above. That test is unfashionable because it requires a valuation, but it is the only test that distinguishes a buyback from a transfer of cash from the company to the sellers at a price the company chose.

The testable version uses the company's own disclosures: the average price paid each period against the range of prices the market offered, and against a valuation metric the company itself reports. A programme that accelerates when the shares are expensive and slows when they are cheap has a negative timing record, and the record is visible in the quarterly disclosures even without a valuation model.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the average price paid each period and the period's price range.
- Record the proportion of the authorisation used in each period.
- Record the valuation metric at the time of purchase if one is available.
- Record whether purchases clustered after price rises or after falls.
- Record the comparison with the alternative of debt reduction or investment.
- Record the effect on earnings per share, which is mechanical and not value creation.

## Procedure

1. Collect per-period repurchases and average prices.
2. Record the price range and the valuation metric for each period.
3. Test whether purchase intensity correlates with price level.
4. Record the earnings-per-share effect separately from the value effect.
5. Compare with the alternative uses of the same cash.
6. Write the timing assessment.

## Anti-patterns

- Treating the earnings-per-share accretion as evidence of value creation.
- Assuming a buyback at any price benefits continuing holders.
- Testing timing from the announcement rather than the execution.
- Ignoring that the same cash could have reduced debt.
- Concluding on timing from a single programme.

## Done checklist

- [ ] Per-period purchases and prices recorded.
- [ ] Price range and valuation metric recorded.
- [ ] Intensity versus price tested.
- [ ] EPS effect separated from value effect.
- [ ] Alternatives compared.
- [ ] Assessment written.

A further test is whether the programme is counter-cyclical by design or by accident: a company that buys steadily through a cycle will show reasonable average timing without any skill, while one that accelerates into strength and stops into weakness has a timing record that the average conceals. Recording intensity per period, not only the average price, is what exposes the difference.

## Sources

- Repurchase execution disclosure: <https://www.sec.gov/investor>
- Valuation and analysis standards: <https://www.cfainstitute.org/>
- Market and rate data: <https://fred.stlouisfed.org/>
