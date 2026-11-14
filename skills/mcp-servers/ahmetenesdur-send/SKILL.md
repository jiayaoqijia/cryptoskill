---
name: send
description: Send STRK, ETH, or any ERC-20 token to a Starknet address. Supports simulation (dry-run) before execution. Use this skill when the user wants to send, transfer, pay, tip, or move tokens to another wallet address on Starknet. Also trigger when the user mentions sending funds to someone, making a payment, transferring assets, or moving crypto to a specific address — even if they just say "pay 10 STRK to 0x...".
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest send *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Send Transaction

Transfer STRK, ETH, or ERC-20 tokens to a destination Starknet address. The CLI automatically checks balance before sending and validates the recipient address. Supports simulation (dry-run) mode to estimate fees without broadcasting.

## Prerequisites

- Active session required.
- Sufficient balance for the transfer amount + gas fees.

## Rules

1. BEFORE any send, you MUST run `npx starkfi@latest status` and `npx starkfi@latest balance` to verify connectivity and funds.
2. If the recipient address was NOT previously mentioned in the conversation, you MUST ask for explicit confirmation: _"Sending [amount] [token] to [address]. Confirm?"_
3. Suggest using `--simulate` first for large amounts so the user can review the estimated fee before committing.
4. AFTER a successful send, you MUST verify the transaction using `npx starkfi@latest tx-status <hash>`.
5. Starknet addresses start with `0x` and can be up to 66 characters long (including the `0x` prefix).

## Commands

```bash
npx starkfi@latest send <amount> <token> <recipient> [--simulate] [--json]
```

## Parameters

| Parameter    | Type   | Description                               | Required |
| ------------ | ------ | ----------------------------------------- | -------- |
| `amount`     | number | Amount to send (e.g. `10`, `0.5`)         | Yes      |
| `token`      | string | Token symbol (e.g. `STRK`, `ETH`, `USDC`) | Yes      |
| `recipient`  | string | Destination Starknet address (`0x...`)    | Yes      |
| `--simulate` | flag   | Estimate fees without broadcasting        | No       |
| `--json`     | flag   | Output as JSON                            | No       |

## Examples

**User:** "Send 10 STRK to 0x04a3..."

```bash
npx starkfi@latest status
npx starkfi@latest balance --token STRK
# Confirm recipient with user if needed
npx starkfi@latest send 10 STRK 0x04a3...
npx starkfi@latest tx-status <hash>
```

**User:** "Simulate sending 100 USDC to 0x07b2..."

```bash
npx starkfi@latest send 100 USDC 0x07b2... --simulate
```

## Error Handling

| Error                  | Action                                                   |
| ---------------------- | -------------------------------------------------------- |
| `Insufficient balance` | Inform user of current balance via `balance`.            |
| `Invalid address`      | Validate recipient is a valid `0x` Starknet address.     |
| `Simulation failed`    | Transaction would revert — check amount, token, and gas. |
| `Not authenticated`    | Run `authenticate-wallet` skill first.                   |

## Related Skills

- Use `balance` to verify funds before sending.
- Use `config` to set a custom RPC if experiencing rate limits.
- Use `trade` if the user needs to swap tokens before sending.
- Use `confidential` for privacy-preserving transfers (hidden amounts, ZK proofs).
