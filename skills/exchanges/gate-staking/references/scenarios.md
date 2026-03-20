# Gate Exchange Staking — Scenario Index

This document is a cross-reference index of all scenarios defined in the sub-module documents. Each sub-module owns its scenarios with full detail (Context, Prompt Examples, Expected Behavior, Response Template). Do **not** duplicate scenario content here.

## Scenario distribution

| Sub-module | Scenarios | Coverage |
|------------|-----------|----------|
| `staking-assets.md` | 6 | Positions: all positions, specific coin, redeemable check, empty, multi-product, portfolio value |
| `staking-coins.md` | 8 | Products: browse all, specific coin, high APY, flexible only, sold out, lock period comparison, min requirements, DeFi vs traditional |
| `staking-list.md` (Part 1) | 5 | Order history: all orders, specific coin, filter by type, recent activity, failed/pending |
| `staking-list.md` (Part 2) | 9 | Rewards: all rewards, specific coin, yesterday, sources, monthly, verify APY, empty, reward types, pagination |
| **Total** | **28** | |

## Quick lookup by user intent

### Positions

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query all staking positions | staking-assets.md | Scenario 1 |
| Query specific coin position | staking-assets.md | Scenario 2 |
| Check available for redemption | staking-assets.md | Scenario 3 |
| Empty positions | staking-assets.md | Scenario 4 |
| Position with multiple products | staking-assets.md | Scenario 5 |
| Calculate total portfolio value | staking-assets.md | Scenario 6 |

### Products

| Scenario | Sub-module | ID |
|----------|------------|----|
| Browse all staking products | staking-coins.md | Scenario 1 |
| Find products for specific coin | staking-coins.md | Scenario 2 |
| Search high APY products | staking-coins.md | Scenario 3 |
| Find flexible products only | staking-coins.md | Scenario 4 |
| Product sold out | staking-coins.md | Scenario 5 |
| Compare products by lock period | staking-coins.md | Scenario 6 |
| Check minimum requirements | staking-coins.md | Scenario 7 |
| DeFi vs Traditional comparison | staking-coins.md | Scenario 8 |

### Order history

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query all order history | staking-list.md (Part 1) | Scenario 1 |
| Query specific coin history | staking-list.md (Part 1) | Scenario 2 |
| Filter by order type | staking-list.md (Part 1) | Scenario 3 |
| Recent activity | staking-list.md (Part 1) | Scenario 4 |
| Failed or pending orders | staking-list.md (Part 1) | Scenario 5 |

### Rewards

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query all rewards | staking-list.md (Part 2) | Scenario 6 |
| Specific coin rewards | staking-list.md (Part 2) | Scenario 7 |
| Yesterday's rewards | staking-list.md (Part 2) | Scenario 8 |
| Reward sources | staking-list.md (Part 2) | Scenario 9 |
| Monthly rewards | staking-list.md (Part 2) | Scenario 10 |
| Verify APY | staking-list.md (Part 2) | Scenario 11 |
| Empty rewards | staking-list.md (Part 2) | Scenario 12 |
| Reward types | staking-list.md (Part 2) | Scenario 13 |
| Pagination handling | staking-list.md (Part 2) | Scenario 14 |

## Error scenarios (summary)

Error handling is embedded within the sub-module scenarios listed above. Key error paths:

| Error condition | Handled in |
|-----------------|------------|
| No staking positions | staking-assets.md Scenario 4 |
| No rewards yet | staking-list.md Scenario 12 |
| Product sold out / not found | staking-coins.md Scenario 5 |
| Failed / pending orders | staking-list.md Scenario 5 |
| API error / 401 | SKILL.md Safety rules → Errors table |

## Unsupported operations

These intents are handled by the routing rules in `SKILL.md` and never reach a sub-module:

| Intent | Response |
|--------|----------|
| Stake / Redeem | "Staking and redemption are not supported here; please use the Gate website or app." |
| Mint | "Mint is not supported here; please use the Gate website or app." |
