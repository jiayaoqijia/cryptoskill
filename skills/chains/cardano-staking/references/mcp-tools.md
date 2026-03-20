# Staking MCP Tools Reference

## get_stake_delegation

Retrieve the staked pool ID and available ADA rewards for the connected wallet.

**Input:** None

**Output:**

| Field | Type | Description |
|-------|------|-------------|
| `poolId` | `string` | Unique pool ID the wallet is staked to |
| `availableAdaRewards` | `number` | Available and claimable ADA staking rewards (in ADA, not lovelace) |
