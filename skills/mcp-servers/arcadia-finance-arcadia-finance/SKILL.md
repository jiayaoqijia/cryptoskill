---
name: arcadia-finance
version: 1.2.0
description: "DeFi liquidity management on Uniswap and Aerodrome, live on Base, Unichain, and Optimism. Deploy concentrated liquidity positions with automated rebalancing, compounding, yield optimization, and leverage, or provide single-sided liquidity to lending pools."
metadata:
  openclaw:
    homepage: https://arcadia.finance
    requires:
      bins: [curl, jq]
---

# Arcadia Finance

> **Agent note:** `{baseDir}` refers to the directory containing this SKILL.md file. Resolve all `{baseDir}` paths relative to it.

Arcadia helps users deploy concentrated liquidity positions on Uniswap, Aerodrome, and Velodrome with automated rebalancing, compounding, yield optimization, and optional leverage, or provide single-sided liquidity to lending pools to earn borrower interest. Supported chains: Base (8453), Unichain (130), Optimism (10), Robinhood (4663).

## CLI Usage

```bash
# Discover all available tools (run this first)
{baseDir}/arcadia.sh --list

# Call a specific tool
{baseDir}/arcadia.sh <tool_name> '<json_args>'
```

Requires: `curl`, `jq`. No other dependencies.

## Read Operations

```bash
# List all accounts for a wallet
{baseDir}/arcadia.sh read_wallet_accounts '{"wallet_address":"0x..."}'

# Account details (health factor, collateral, debt, positions)
{baseDir}/arcadia.sh read_account_info '{"account_address":"0x..."}'

# Featured LP strategies with APY
{baseDir}/arcadia.sh read_strategy_list '{"featured_only":true}'

# Lending pools (TVL, APY, utilization)
{baseDir}/arcadia.sh read_pool_list '{}'

# Workflow guides (automation setup, strategy selection)
{baseDir}/arcadia.sh read_guides '{"topic":"overview"}'

# Available automations (rebalancer, compounder, yield claimer)
{baseDir}/arcadia.sh read_asset_manager_intents '{}'
```

## Single-Sided Liquidity (Lending)

Provide single-sided liquidity by depositing the pool's underlying asset into an Arcadia lending tranche (ERC-4626), earning interest from borrowers. Use `read_pool_list` to find `tranches[0].address` for each pool. Approve the tranche first (`write_wallet_approve`).

```bash
# Lender deposit: lend 10 USDC into the USDC tranche, receive shares to your wallet
{baseDir}/arcadia.sh write_pool_deposit '{"tranche_address":"0x...","assets":"10000000","receiver":"0x...","chain_id":8453}'

# Lender exit: redeem shares back to the underlying asset
{baseDir}/arcadia.sh write_pool_redeem '{"tranche_address":"0x...","shares":"10000000","receiver":"0x...","owner":"0x...","chain_id":8453}'
```

`write_pool_deposit` is for lenders earning yield. For depositing collateral into an Arcadia account, use `write_account_deposit` instead.

## Write Operations

All write tools return unsigned transactions `{ to, data, value, chainId }`. Sign with your wallet before broadcasting. See `{baseDir}/wallet-signing.md` for wallet options.

```bash
# Open LP position (deposits + swaps + mints LP atomically)
{baseDir}/arcadia.sh write_account_add_liquidity '{"account_address":"0x...","wallet_address":"0x...","positions":[{"strategy_id":123}],"deposits":[{"asset":"0x...","amount":"1000000","decimals":6}]}'

# Close position (burn LP + swap + repay in one tx)
{baseDir}/arcadia.sh write_account_close '{"account_address":"0x...","assets":[...],"receive_assets":[...]}'

# Create a new account (salt must be unique per wallet)
{baseDir}/arcadia.sh write_account_create '{"wallet_address":"0x...","salt":1,"chain_id":8453}'

# Enable automation
{baseDir}/arcadia.sh read_asset_manager_intents '{"account_address":"0x...","chain_id":8453}'
{baseDir}/arcadia.sh write_account_automations '{"account_address":"0x...","position_id":12345,"intents":[{"kind":"compound_fees"},{"kind":"rebalance"}],"chain_id":8453}'
```

## Configuration

The CLI connects to `https://mcp.arcadia.finance/mcp` by default. Set `ARCADIA_MCP_URL` to override (e.g. for local development).

## Data and Safety

This skill connects to Arcadia's public API at `https://mcp.arcadia.finance/mcp` (override via `ARCADIA_MCP_URL`). Tool calls send public wallet addresses, account addresses, and transaction parameters to this server. This is the same data that is publicly visible on-chain. No private keys or signing capabilities are transmitted.

- Write tools return unsigned transactions only. Never auto-sign.
- Always confirm transaction details with the user before signing.
- Check account health factor with `read_account_info` before risky operations.
- Do not pass private keys or secrets as tool arguments. Only public addresses and amounts are needed.

## References

- Full tool documentation: https://mcp.arcadia.finance/llms-full.txt
- Contract addresses: see `{baseDir}/contracts.md`
- Signing guide: see `{baseDir}/wallet-signing.md`
- Website: https://arcadia.finance
- Docs: https://docs.arcadia.finance
