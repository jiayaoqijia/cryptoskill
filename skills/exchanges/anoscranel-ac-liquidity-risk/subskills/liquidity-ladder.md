---
name: liquidity-ladder
domain: investing/liquidity-ladder
trigger: "Building a time-bucketed view of what can be turned into cash."
anti_trigger: "Not for predicting needs, and not for portfolio allocation."
scope: "Buckets by time to cash, with haircuts applied to each."
status: seedling
---

# Liquidity ladder

## Standard

A liquidity ladder sorts holdings by how quickly they become cash: overnight, a week, a month, a quarter, a year, and beyond. Each bucket carries a haircut reflecting the price concession assumed to exit within that window, so the ladder reports not the market value of each bucket but the cash it would plausibly produce under the stated assumption.

The value of the structure is that it forces the assumptions to be explicit and comparable. A portfolio that looks liquid on total value can be shown to have most of its value in the beyond-a-year bucket once haircuts are applied, and a requirement that falls in the one-month bucket can be compared directly with the cash the ladder says that bucket holds. The ladder is a budget, not a valuation.

Primary sources: <https://www.bis.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Define the buckets before assigning assets, and keep them fixed for comparability.
- Assign each holding to the bucket matching its realistic exit time.
- Apply a haircut per bucket, stated as a percentage of market value.
- Record the cash equivalent per bucket, not the market value.
- Record the requirements that fall in each bucket.
- Compare cash equivalent with requirements bucket by bucket, not in total.

## Procedure

1. Define the buckets and their time windows.
2. Assign holdings by realistic exit time.
3. Apply haircuts and compute cash equivalents.
4. Record the requirements per bucket.
5. Compare per bucket and identify the shortfall.
6. Write the ladder with its assumptions dated.

## Anti-patterns

- Assigning an asset to the bucket matching its stated liquidity rather than its observed behaviour.
- Applying one haircut across all buckets.
- Comparing total cash equivalent with total requirements, which hides a bucket shortfall.
- Leaving the bucket definitions to change each review.
- Ignoring redemption terms on funds held.

## Done checklist

- [ ] Buckets defined and fixed.
- [ ] Holdings assigned with reasoning.
- [ ] Haircuts applied per bucket.
- [ ] Cash equivalents computed.
- [ ] Requirements mapped to buckets.
- [ ] Per-bucket comparison made.

The ladder is most useful when compared between two dates rather than read once: a portfolio whose cash equivalent in the short buckets has fallen while the market value has risen is one that has become more dependent on prices staying where they are, and that shift is invisible in a single ladder.


## Sources

- Liquidity and collateral standards: <https://www.bis.org/>
- Investor education on liquidity: <https://www.investor.gov/introduction-investing>
- Market data for haircut assumptions: <https://fred.stlouisfed.org/>
