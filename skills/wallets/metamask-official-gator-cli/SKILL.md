---
name: gator-cli
description: Use when you need to operate the @metamask/gator-cli to initialize profiles, upgrade EOA to EIP-7702, grant, redeem, and revoke ERC-7710 delegations, or inspect balances and delegations. Covers commands, required flags, grant scopes, redeem action types, configuration locations, and common usage flows.
metadata:
  openclaw:
    emoji: "🐊"
    homepage: "https://docs.metamask.io/smart-accounts-kit"
    requires:
      bins: ["gator"]
    install:
      - id: "node"
        kind: "node"
        package: "@metamask/gator-cli"
        bins: ["gator"]
        label: "Install gator CLI"
---

## Quick Reference

Use this skill to run the gator CLI from the repo and to choose the correct command/flags for delegation workflows.

## Installation

```sh
npm install -g @metamask/gator-cli
```

## CLI Overview

- Binary name: `gator`
- Default profile: `default`
- Config path: `~/.gator-cli/permissions.json` (or `~/.gator-cli/profiles/<profile-name>.json`)
- Delegations local cache: `~/.gator-cli/delegations/<profile-name>.json` when storage not configured

## Configuration Requirements

Edit the profile config after `gator init`:

```json
{
  "delegationStorage": {
    "apiKey": "your-api-key",
    "apiKeyId": "your-api-key-id"
  },
  "rpcUrl": "https://your-rpc-url.com"
}
```

- `delegationStorage` is optional; when missing, delegations are stored locally.
- `rpcUrl` is required for on-chain actions.

## Commands

### init

Generate a private key and save config. Errors if the profile already exists.

- `gator init [--chain <chain>] [--profile <profile-name>]`
- `--chain` values: `base` (default), `baseSepolia`, `sepolia`
- `--profile` default: `default`
- Prints: address, chain, and config file path.

### create

Upgrade an EOA to an EIP-7702 smart account. Uses the chain in your profile config.

- `gator create [--profile <profile-name>]`
- Requires the account to be funded with native token first.
- Prints: address, chain, and the upgrade transaction hash.

### show

Display the EOA address for a profile.

- `gator show [--profile <profile-name>]`

### status

Check config and on-chain account status.

- `gator status [--profile <profile-name>]`
- Prints: address, chain, config upgrade status, on-chain code presence, storage and RPC URL config.

### balance

Show native balance and optional ERC-20 balance.

- `gator balance [--tokenAddress <address>] [--profile <profile-name>]`
- If `--tokenAddress` is provided, prints ERC-20 balance and decimals-derived units.

### grant

Create, sign, and store a delegation with a predefined scope.

- `gator grant --to <to-address> --scope <type> [scope flags] [--profile <profile-name>]`

Scope flags:

- Token scopes: `--tokenAddress <token-address>`, `--maxAmount <amount>`, `--tokenId <id>`
- Periodic scopes: `--periodAmount <amount>`, `--periodDuration <seconds>`, `--startDate <timestamp>`
- Streaming scopes: `--amountPerSecond <amount>`, `--initialAmount <amount>`, `--startTime <timestamp>`
- Function call scope: `--targets <addresses>`, `--selectors <sigs>`, `--valueLte <ether>`
- Ownership transfer: `--contractAddress <contract-address>`

Supported scopes:

- `erc20TransferAmount`
- `erc20PeriodTransfer`
- `erc20Streaming`
- `erc721Transfer`
- `nativeTokenTransferAmount`
- `nativeTokenPeriodTransfer`
- `nativeTokenStreaming`
- `functionCall`
- `ownershipTransfer`

Grant flags per scope:

| Scope                       | Required Flags                                                          | Optional Flags   |
| --------------------------- | ----------------------------------------------------------------------- | ---------------- |
| `erc20TransferAmount`       | `--tokenAddress`, `--maxAmount`                                         |                  |
| `erc20PeriodTransfer`       | `--tokenAddress`, `--periodAmount`, `--periodDuration`                  | `--startDate`    |
| `erc20Streaming`            | `--tokenAddress`, `--amountPerSecond`, `--initialAmount`, `--maxAmount` | `--startTime`    |
| `erc721Transfer`            | `--tokenAddress`, `--tokenId`                                           |                  |
| `nativeTokenTransferAmount` | `--maxAmount`                                                           |                  |
| `nativeTokenPeriodTransfer` | `--periodAmount`, `--periodDuration`                                    | `--startDate`    |
| `nativeTokenStreaming`      | `--amountPerSecond`, `--initialAmount`, `--maxAmount`                   | `--startTime`    |
| `functionCall`              | `--targets`, `--selectors`                                              | `--valueLte`     |
| `ownershipTransfer`         | `--contractAddress`                                                     |                  |

- `--startDate` and `--startTime` default to the current time (unix seconds) when omitted.
- `--valueLte` sets the max native token value per call for `functionCall` scopes.

### redeem

Redeem a stored delegation using a specific action type.

- `gator redeem --from <from-address> --action <type> [action flags] [--profile <profile-name>]`

Supported action types: `erc20Transfer`, `erc721Transfer`, `nativeTransfer`, `functionCall`, `ownershipTransfer`, `raw`

Action-specific flags:

- `erc20Transfer`: `--tokenAddress`, `--to`, `--amount`
- `erc721Transfer`: `--tokenAddress`, `--to`, `--tokenId`
- `nativeTransfer`: `--to`, `--amount`
- `functionCall`: `--target`, `--function`, `--args`, `--value`
- `ownershipTransfer`: `--contractAddress`, `--to`
- `raw`: `--target`, `--callData`, `--value`

### revoke

Revoke a delegation on-chain. Revokes the first matching delegation.

- `gator revoke --to <to-address> [--profile <profile-name>]`

### inspect

Inspect delegations for your account.

- `gator inspect [--from <from-address>] [--to <to-address>] [--profile <profile-name>]`
- With no filters, prints both Given and Received.
- Printed fields: From, To, Authority, Caveats count, Signed flag.

## Redeem Flags per Action

| Action              | Required Flags                        |
| ------------------- | ------------------------------------- |
| `erc20Transfer`     | `--tokenAddress`, `--to`, `--amount`  |
| `erc721Transfer`    | `--tokenAddress`, `--to`, `--tokenId` |
| `nativeTransfer`    | `--to`, `--amount`                    |
| `functionCall`      | `--target`, `--function`, `--args`    |
| `ownershipTransfer` | `--contractAddress`, `--to`           |
| `raw`               | `--target`, `--callData`              |

## Example Flows

Initialize and upgrade:

```bash
gator init --profile <profile-name>
gator create --profile <profile-name>
```

Grant an ERC-20 transfer delegation:

```bash
gator grant --profile <profile-name> --to <to-address> --scope erc20TransferAmount \
  --tokenAddress <token-address> --maxAmount 50
```

Redeem an ERC-20 transfer:

```bash
gator redeem --profile <profile-name> --from <from-address> --action erc20Transfer \
  --tokenAddress <token-address> --to <to-address> --amount 10
```

Redeem a native transfer:

```bash
gator redeem --profile <profile-name> --from <from-address> --action nativeTransfer \
  --to <to-address> --amount 0.5
```

Redeem in raw mode:

```bash
gator redeem --profile <profile-name> --from <from-address> --action raw \
  --target <contract-address> --callData 0xa9059cbb...
```

Inspect delegations:

```bash
gator inspect --profile <profile-name>
gator inspect --profile <profile-name> --from <from-address>
gator inspect --profile <profile-name> --to <to-address>
```

Revoke a delegation:

```bash
gator revoke --profile <profile-name> --to <to-address>
```

## Operational Notes

- **Private key security**: This is alpha version. Private keys are stored in plaintext JSON. Never use accounts with significant funds.
- `--from` refers to the delegator address; `--to` refers to the delegate/recipient.
- `--targets` and `--selectors` are comma-separated lists.
- `--function` accepts a human-readable Solidity function signature like `"approve(address,uint256)"`. Do **not** pass a 4-byte selector (e.g. `0x095ea7b3`) — the CLI derives the selector from the signature automatically.
- `--startDate` and `--startTime` accept unix timestamps in seconds. When omitted, they default to the current time.
- `--action` is required for `redeem` and must be one of: `erc20Transfer`, `erc721Transfer`, `nativeTransfer`, `functionCall`, `ownershipTransfer`, `raw`.
- Supported chains for `--chain` in `gator init`: `base` (default), `baseSepolia`, `sepolia`.
