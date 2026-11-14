---
name: staking
description: Stake, unstake, claim, and compound rewards for STRK, WBTC, tBTC, SolvBTC, and LBTC on Starknet. View validators, pools, and staking positions. Use this skill when the user mentions staking, delegating, validators, staking pools, rewards, compounding, unstaking, earning yield, passive income on crypto, or wants to earn on their STRK or BTC tokens — even if they don't say "stake" explicitly.
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest validators)
    - Bash(npx starkfi@latest validators *)
    - Bash(npx starkfi@latest pools *)
    - Bash(npx starkfi@latest stake-status)
    - Bash(npx starkfi@latest stake-status *)
    - Bash(npx starkfi@latest stake *)
    - Bash(npx starkfi@latest unstake *)
    - Bash(npx starkfi@latest rewards *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Staking

Manage Starknet staking operations: delegate tokens to validators, claim or compound rewards, and unstake positions. Supports multiple token types across various validators and pools.

## Prerequisites

- Active session required.
- Sufficient token balance for staking + gas fees.

## Supported Tokens

| Token   | Type    |
| ------- | ------- |
| STRK    | Native  |
| WBTC    | Bitcoin |
| tBTC    | Bitcoin |
| SolvBTC | Bitcoin |
| LBTC    | Bitcoin |

## Rules

1. BEFORE staking, you MUST run `npx starkfi@latest validators` to list available validators, then `npx starkfi@latest pools <validator>` to see available pools.
2. BEFORE staking, check `balance` to confirm the user has enough tokens.
3. Unstaking is a **two-step process**: first `unstake intent` starts a cooldown, then `unstake exit` finalizes after the cooldown period. The user must wait between these steps.
4. `rewards --compound` atomically claims and restakes in one transaction.
5. AFTER any transactional operation (stake, unstake, rewards), verify with `tx-status`.
6. Use `stake-status` to view the user's current staking positions across all validators. When exit intents are active, unpooling amounts and cooldown dates are shown automatically.
7. Token defaults to `STRK` if `--token` is not specified.
8. **LST Disambiguation:** If the user mentions "liquid staking", "xSTRK", or "Endur", redirect to the `lst` skill instead. This skill handles **delegation staking** only. Do NOT use `rewards --claim` or `rewards --compound` for xSTRK positions.

## Commands

```bash
# Discovery
npx starkfi@latest validators [--json]
npx starkfi@latest pools <validator> [--json]
npx starkfi@latest stake-status [validator] [--json]

# Stake tokens
npx starkfi@latest stake <amount> --validator <name> [--token <symbol>] [--simulate] [--json]

# Unstake (two-step)
npx starkfi@latest unstake intent --validator <name> --amount <amount> [--token <symbol>]
npx starkfi@latest unstake exit --validator <name> [--token <symbol>]

# Rewards
npx starkfi@latest rewards --claim --validator <name> [--token <symbol>]
npx starkfi@latest rewards --compound --validator <name> [--token <symbol>]
```

## Parameters

### stake

| Parameter     | Type   | Description                                      | Required |
| ------------- | ------ | ------------------------------------------------ | -------- |
| `amount`      | number | Amount to stake (positional)                     | Yes      |
| `--validator` | string | Validator name (from `validators` list)          | Yes\*    |
| `--pool`      | string | Pool contract address (alternative to validator) | Yes\*    |
| `--token`     | string | Token symbol (default: `STRK`)                   | No       |
| `--simulate`  | flag   | Estimate fees without broadcasting               | No       |
| `--json`      | flag   | Output raw JSON                                  | No       |

\*Provide either `--validator` or `--pool`.

### unstake

| Parameter     | Type   | Description                               | Required   |
| ------------- | ------ | ----------------------------------------- | ---------- |
| action        | string | `intent` or `exit` (positional)           | Yes        |
| `--validator` | string | Validator name                            | Yes\*      |
| `--pool`      | string | Pool contract address                     | Yes\*      |
| `--amount`    | number | Amount to unstake (required for `intent`) | For intent |
| `--token`     | string | Token symbol (default: `STRK`)            | No         |

### rewards

| Parameter     | Type   | Description                    | Required |
| ------------- | ------ | ------------------------------ | -------- |
| `--claim`     | flag   | Claim pending rewards          | Yes\*    |
| `--compound`  | flag   | Claim and immediately restake  | Yes\*    |
| `--validator` | string | Validator name                 | Yes\*\*  |
| `--pool`      | string | Pool contract address          | Yes\*\*  |
| `--token`     | string | Token symbol (default: `STRK`) | No       |

\*Provide either `--claim` or `--compound`. \*\*Provide either `--validator` or `--pool`.

## Examples

**User:** "Which validators can I stake with?"

```bash
npx starkfi@latest validators
```

**User:** "Show me pools for Karnot"

```bash
npx starkfi@latest pools Karnot
```

**User:** "Stake 1000 STRK with Karnot"

```bash
npx starkfi@latest status
npx starkfi@latest balance --token STRK
npx starkfi@latest stake 1000 --validator Karnot
npx starkfi@latest tx-status <hash>
```

**User:** "Stake 0.5 WBTC with Karnot"

```bash
npx starkfi@latest balance --token WBTC
npx starkfi@latest stake 0.5 --validator Karnot --token WBTC
npx starkfi@latest tx-status <hash>
```

**User:** "Compound my STRK rewards from Karnot"

```bash
npx starkfi@latest rewards --compound --validator Karnot
npx starkfi@latest tx-status <hash>
```

**User:** "Claim my rewards from Karnot"

```bash
npx starkfi@latest rewards --claim --validator Karnot
npx starkfi@latest tx-status <hash>
```

**User:** "I want to unstake my STRK from Karnot"

```bash
# Step 1: Start unstake cooldown
npx starkfi@latest unstake intent --validator Karnot --amount 1000
npx starkfi@latest tx-status <hash>
# Inform user about cooldown period
# Step 2: After cooldown, finalize
npx starkfi@latest unstake exit --validator Karnot
npx starkfi@latest tx-status <hash>
```

**User:** "Show me all my staking positions"

```bash
npx starkfi@latest stake-status
```

## Error Handling

| Error                   | Action                                           |
| ----------------------- | ------------------------------------------------ |
| `Validator not found`   | Run `validators` to list valid names.            |
| `Pool not found`        | Run `pools <validator>` to list available pools. |
| `Insufficient balance`  | Check `balance` and suggest a smaller amount.    |
| `Cooldown not complete` | User must wait before running `unstake exit`.    |
| `No rewards to claim`   | Position has no pending rewards.                 |
| `Not authenticated`     | Run `authenticate-wallet` skill first.           |

## Related Skills

- Use `balance` to check available tokens before staking.
- Use `portfolio` for a full overview including staking positions with USD values.
- Use `batch` to combine staking with other operations in one transaction.
- Use `lst` for liquid staking via Endur (xSTRK — automatic yield, instant redemption).
