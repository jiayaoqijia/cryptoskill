---
name: config
description: View and modify StarkFi CLI configuration — set custom RPC URLs, switch networks, manage gas settings, and check transaction status. Use this skill when the user mentions RPC, rate limits, network settings, gas mode, gas token, configuration, settings, preferences, or wants to check a transaction hash. Also trigger when the user wants to customize their setup, troubleshoot connection issues, fix errors, switch between mainnet and testnet, change how gas is paid, enable free gas, "gas fees too high", "not working", verify whether a transaction succeeded, or check tx status — even if they don't say "config".
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: utility
allowed-tools:
    - Bash(npx starkfi@latest config *)
    - Bash(npx starkfi@latest tx-status *)
---

# Configuration & Utilities

Manage local configuration for the StarkFi CLI and check transaction status on-chain. Configuration includes RPC endpoints, network selection, and gas payment settings.

## Prerequisites

- None for configuration commands (`config list`, `config set-*`, `config get-rpc`).
- Active session required for `tx-status` and for `config list` to show the effective network source.

## Configuration Commands

```bash
# List all current settings
npx starkfi@latest config list

# Reset all settings to defaults
npx starkfi@latest config reset

# Set custom RPC URL
npx starkfi@latest config set-rpc <url>

# Get current RPC URL
npx starkfi@latest config get-rpc

# Switch network (takes effect immediately, no re-login needed)
npx starkfi@latest config set-network <network>

# Toggle developer-sponsored gas (Gasfree mode)
npx starkfi@latest config set-gasfree <on|off>

# Set gas payment token (for Gasless mode)
npx starkfi@latest config set-gas-token <token>
```

## Transaction Status

```bash
npx starkfi@latest tx-status <hash>
```

## Gas Modes

StarkFi supports two gas abstraction modes:

| Mode        | Who Pays      | Command                     | Description                                     |
| ----------- | ------------- | --------------------------- | ----------------------------------------------- |
| **Gasfree** | Developer     | `config set-gasfree on`     | Gas fees sponsored by StarkFi via Paymaster     |
| **Gasless** | User (ERC-20) | `config set-gas-token STRK` | User pays gas in an ERC-20 token (default mode) |

Supported gas tokens: **ETH**, **STRK**, **USDC**, **USDT**, **DAI**

Gasfree and Gasless are mutually exclusive — enabling one disables the other.

> **Default:** Gasless mode with STRK as gas token. Gas is paid through the Paymaster, so the user does not need native ETH for gas — any supported ERC-20 works.

## Parameters

| Parameter | Type   | Description                                   | Required |
| --------- | ------ | --------------------------------------------- | -------- |
| `url`     | string | Full HTTP(S) RPC endpoint URL                 | Yes      |
| `network` | string | `mainnet` or `sepolia`                        | Yes      |
| `on/off`  | string | Enable or disable Gasfree mode                | Yes      |
| `token`   | string | Gas token symbol or `reset` (reverts to STRK) | Yes      |
| `hash`    | string | Transaction hash (`0x...`)                    | Yes      |

## Rules

1. **Rate Limits**: If any skill fails with "rate limit" or "429" errors, use `config set-rpc` to set a custom RPC endpoint.
2. **Persistence**: Settings are stored locally and persist across sessions.
3. **Network switching**: `set-network` takes effect instantly for all commands — no re-login required. The config setting overrides the session's login network. `config list` shows the effective network with its source (e.g. `sepolia (config override, session: mainnet)`).
4. Use `tx-status` AFTER every `send`, `trade`, `multi-swap`, `batch`, `dca-create`, `dca-cancel`, `conf-fund`, `conf-transfer`, `conf-withdraw`, and staking/lending transaction to verify success.
5. Use `config get-rpc` to check the current RPC URL before changing it.

## Examples

**User:** "I'm getting rate limit errors"

```bash
npx starkfi@latest config get-rpc
npx starkfi@latest config set-rpc https://starknet-mainnet.g.alchemy.com/v2/<key>
```

**User:** "Show my current configuration"

```bash
npx starkfi@latest config list
```

**User:** "Switch to testnet"

```bash
npx starkfi@latest config set-network sepolia
npx starkfi@latest config list    # Verify: shows "sepolia (config override, session: mainnet)"
```

**User:** "Enable free gas mode"

```bash
npx starkfi@latest config set-gasfree on
```

**User:** "I want to pay gas in USDC"

```bash
npx starkfi@latest config set-gasfree off
npx starkfi@latest config set-gas-token USDC
```

**User:** "Reset gas token to default"

```bash
npx starkfi@latest config set-gas-token reset
```

**User:** "Reset all my settings"

```bash
npx starkfi@latest config reset
```

**User:** "Did my transaction go through? Hash is 0xabc..."

```bash
npx starkfi@latest tx-status 0xabc...
```

## Error Handling

| Error                   | Action                                              |
| ----------------------- | --------------------------------------------------- |
| `Invalid RPC URL`       | Ensure URL starts with `http://` or `https://`.     |
| `Invalid network`       | Use `mainnet` or `sepolia`.                         |
| `Unsupported gas token` | Must be one of: ETH, STRK, USDC, USDT, DAI.         |
| `Transaction not found` | Verify the hash is correct and the network matches. |
| `Pending`               | Transaction is still in mempool — wait and retry.   |

## Related Skills

- This skill is referenced by all other skills for rate limit recovery.
- Use `config set-gasfree on` for developer-sponsored gas.
- Use `tx-status` to verify transactions from any transactional skill.
