---
name: asset-location
domain: investing/asset-location
trigger: "Deciding which account type should hold which asset."
anti_trigger: "Not for tax advice, and not for asset allocation itself."
scope: "Which assets belong in taxable, deferred, and exempt accounts."
status: seedling
---

# Asset location

## Standard

Different account types tax the same asset differently. A taxable account taxes income and realised gains annually; a deferred account taxes withdrawals as ordinary income; an exempt account taxes nothing. That means the same asset produces different after-tax returns depending on where it sits, and the differences compound over a holding period.

The standard logic puts the most tax-inefficient assets — those generating ordinary income or high turnover — inside the sheltered accounts, and keeps the most tax-efficient — broad index holdings with low turnover and qualified distributions — in the taxable account. The logic has a second-order correction: expected return matters, because a high-return asset in a sheltered account grows the shelter's value, so the simple rule can invert when one asset is expected to compound much faster.

Primary sources: <https://www.irs.gov/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record each account type and how it taxes income, gains, and withdrawals.
- Record each asset's expected return, turnover, and distribution character.
- Place high-tax-drag assets in sheltered accounts and low-drag assets in taxable.
- Record the expected-return adjustment where one asset compounds materially faster.
- Record the liquidity constraint: sheltered accounts may be harder to access.
- Revisit when an account type changes or an asset's character changes.

## Procedure

1. List accounts and their tax treatment.
2. List assets with expected return and tax character.
3. Rank by tax drag per unit of expected return.
4. Place assets accordingly, respecting liquidity needs.
5. Record the placement and its reasoning.
6. Review on any change of account or asset.

## Anti-patterns

- Putting the highest-return asset in the taxable account without the return adjustment.
- Ignoring liquidity when sheltering an asset needed for spending.
- Treating all sheltered accounts as identical.
- Rebalancing across accounts without considering location.
- Assuming the placement is permanent.

## Done checklist

- [ ] Account types and treatment recorded.
- [ ] Assets ranked by tax drag.
- [ ] Placement decided with reasoning.
- [ ] Return adjustment applied where relevant.
- [ ] Liquidity constraint recorded.
- [ ] Review trigger set.

The exception that most often overrides the rule is access: an asset needed for near-term spending cannot be sheltered in an account with penalties or delays, and a location plan that ignores the spending schedule produces a portfolio that is tax-efficient and unusable at the same time.


## Sources

- Tax administration guidance on accounts: <https://www.irs.gov/>
- Investor education on account types: <https://www.investor.gov/introduction-investing>
- Regulatory context for retirement accounts: <https://www.sec.gov/investor>
