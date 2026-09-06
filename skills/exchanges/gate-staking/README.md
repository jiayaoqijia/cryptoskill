# Gate Exchange Staking Skill

## Overview

A comprehensive skill for querying and executing staking operations on Gate's on-chain earn platform. It supports five modules: positions, rewards, products, order history, and stake/redeem (swap).

### Core Capabilities

| Capability | Description | MCP Tools |
|------------|-------------|-----------|
| Query staking positions | View positions, available vs locked amounts, redeemable amounts | `cex_earn_asset_list`, `cex_earn_find_coin` |
| Check staking rewards | Daily/cumulative rewards, earnings history | `cex_earn_award_list` |
| Browse staking products | Discover products, compare APY, filter by coin | `cex_earn_find_coin` |
| View transaction history | Staking/redemption history, filters, order status | `cex_earn_order_list` |
| Stake / Redeem / Mint | Execute stake or redeem via swap (pid required); mint treated as immediate stake | `cex_earn_swap_staking_coin` |

## Architecture

```
gate-exchange-staking/
├── SKILL.md                        # AI Agent runtime instructions
├── README.md                       # Human-readable documentation
├── CHANGELOG.md                    # Version changelog
└── references/
    ├── staking-assets.md           # Positions query workflow
    ├── staking-coins.md            # Products query workflow
    ├── staking-list.md             # Order history and reward list workflows
    ├── staking-swap.md             # Stake/redeem swap workflow
    └── scenarios.md                # Usage scenarios and prompt examples
```

## Usage Examples

### Query Operations
```
"Show my staking positions"
"What are my staking rewards?"
"Find BTC staking products"
"Show staking history"
"What coins can I stake?"
```

### Execution Operations
```
"Stake 100 USDT"
"Redeem my ETH"
"Mint GT"
"Stake 1 BTC"
```

## Product Types Supported

| productType | Label | Description |
|-------------|-------|-------------|
| 0 | Certificate | Flexible staking with instant redemption (redeemPeriod = 0) |
| 1 | Lock-up | Fixed-term staking with a defined lock period (redeemPeriod > 0) |
| 2 | US Treasury Bond | Products backed by US Treasury bonds (e.g. GUSD) |

## MCP Tools

| Tool | Purpose | Auth Required |
|------|---------|---------------|
| `cex_earn_asset_list` | Query current staking positions | Yes |
| `cex_earn_award_list` | Retrieve reward history | Yes |
| `cex_earn_find_coin` | Discover available products and exchange rates | No |
| `cex_earn_order_list` | View transaction history | Yes |
| `cex_earn_swap_staking_coin` | Execute stake or redeem (requires pid, side) | Yes |

## Safety & Compliance

- **User confirmation required**: All stake/redeem/mint operations require explicit user confirmation before execution. An Action Draft is shown first summarizing the operation details.
- **Query operations**: No confirmation needed for read-only queries.
- **Cancel redeem**: Not supported — users are directed to the Gate website or app.
- No investment advice; APY and rates are for reference only.
- Sensitive user data (API keys, balances) is never logged or exposed in responses.
- Amounts and rates are displayed as-is from the API without modification.

## Number Formatting

| Category | Precision | Trailing zeros | Examples |
|----------|-----------|----------------|----------|
| General amounts | 8 decimals | Removed | `1.23` not `1.23000000` |
| Rate fields (APY, APR) | 2 decimals | Retained | `5.20%` not `5.2%` |

## Error Handling

The skill gracefully handles various error scenarios:
- Empty positions: Suggests available products
- No rewards: Explains reward accrual timing (T+1)
- Product not found / no capacity: Suggests alternatives by APY
- API failures: Provides retry guidance
- Auth failures (401): Prompts API key configuration

## Authentication

This skill does **not** handle credentials directly. Authentication is managed by the Gate MCP platform layer — the MCP server holds the user's API key and injects it into API calls automatically. No environment variables or secrets are required by the skill itself. Users should configure their Gate API key in the MCP server settings (see [Gate MCP](https://github.com/gateio/gate-mcp) for setup instructions).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
