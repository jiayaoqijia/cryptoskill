---
name: confidential
description: Manage confidential (private) transfers via Tongo Cash on Starknet — setup, fund, transfer, withdraw, ragequit, rollover using ZK proofs. Use this skill when the user wants to send tokens privately, hide transfer amounts, use zero-knowledge proofs, set up Tongo, fund or withdraw from a confidential account, perform an emergency exit (ragequit), or activate pending balance (rollover). Also trigger when the user says "send privately", "confidential transfer", "hide my transaction", "Tongo Cash", "ZK transfer", or any variation about privacy-preserving transfers — even if they don't use the word "confidential".
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest conf-setup *)
    - Bash(npx starkfi@latest conf-balance)
    - Bash(npx starkfi@latest conf-balance *)
    - Bash(npx starkfi@latest conf-fund *)
    - Bash(npx starkfi@latest conf-transfer *)
    - Bash(npx starkfi@latest conf-withdraw *)
    - Bash(npx starkfi@latest conf-ragequit)
    - Bash(npx starkfi@latest conf-ragequit *)
    - Bash(npx starkfi@latest conf-rollover)
    - Bash(npx starkfi@latest conf-rollover *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Confidential Transfers (Tongo Cash)

Privacy-preserving token transfers using ZK proofs on Starknet. Amounts are hidden on-chain; recipients are identified by elliptic curve public keys, not Starknet addresses.

## Prerequisites

- Active session required. If not authenticated, run `authenticate-wallet` skill first.
- Tongo credentials configured (`conf-setup`). Must be done once before any other confidential command.
- Sufficient public token balance for `conf-fund` operations.

## Rules

1. BEFORE any confidential operation, run `npx starkfi@latest status` to verify authentication.
2. `conf-setup` MUST be called before any other confidential command. It only needs to run once.
3. BEFORE `conf-fund`, check `balance` to verify sufficient public token balance.
4. BEFORE `conf-transfer` or `conf-withdraw`, check `conf-balance` to verify sufficient active balance.
5. After the recipient receives a transfer, remind them to run `conf-rollover` to activate pending balance.
6. `conf-ragequit` is a DESTRUCTIVE operation — it empties the entire confidential balance. Always warn the user and get explicit confirmation.
7. AFTER any transactional operation (`conf-fund`, `conf-transfer`, `conf-withdraw`, `conf-ragequit`, `conf-rollover`), verify with `tx-status`.
8. The Tongo private key is stored locally at `~/.local/share/starkfi/confidential.json` with strict `0o600` permissions and is **never sent to the network**.

## Setup (One-Time)

The user first needs a Tongo Private Key. They can generate or export this key through the [Tongo Cash](https://tongo.cash/) or refer to the [Tongo Documentation](https://docs.tongo.cash/protocol/contracts.html).

```bash
npx starkfi@latest conf-setup --key <TONGO_PRIVATE_KEY> --contract 0x1234…
```

## Commands

### Check Balance

```bash
npx starkfi@latest conf-balance [--json]
```

Returns: active balance, pending balance, nonce, Tongo address.

### Fund Confidential Account

Move public ERC-20 tokens into a private confidential balance.

```bash
npx starkfi@latest conf-fund <amount> [--token <symbol>] [--simulate] [--json]
```

### Transfer Confidentially

Send tokens privately to another Tongo account. Recipient is identified by their public key coordinates (x, y).

```bash
npx starkfi@latest conf-transfer <amount> --recipient-x <x> --recipient-y <y> [--token <symbol>] [--simulate] [--json]
```

### Withdraw to Public

Convert private balance back to public ERC-20 tokens.

```bash
npx starkfi@latest conf-withdraw <amount> [--to <address>] [--token <symbol>] [--simulate] [--json]
```

### Ragequit (Emergency Exit)

Withdraw the entire confidential balance to a public address immediately.

```bash
npx starkfi@latest conf-ragequit [--to <address>] [--json]
```

### Rollover (Activate Pending)

Received transfers start as "pending" and must be rolled over to become spendable.

```bash
npx starkfi@latest conf-rollover [--json]
```

## Parameters

| Parameter       | Type   | Description                        | Required       |
| --------------- | ------ | ---------------------------------- | -------------- |
| `amount`        | number | Amount for fund/transfer/withdraw  | Yes            |
| `--key`         | string | Tongo private key (setup only)     | Yes (setup)    |
| `--contract`    | string | Tongo contract address             | Yes (setup)    |
| `--recipient-x` | string | Recipient public key X coordinate  | Yes (transfer) |
| `--recipient-y` | string | Recipient public key Y coordinate  | Yes (transfer) |
| `--token`       | string | Token symbol (default: `USDC`)     | No             |
| `--to`          | string | Recipient Starknet address         | No             |
| `--simulate`    | flag   | Estimate fees without broadcasting | No             |
| `--json`        | flag   | Output as JSON                     | No             |

## Examples

**User:** "Set up my Tongo account"

```bash
npx starkfi@latest conf-setup --key <KEY> --contract 0x1234…
```

**User:** "Fund 100 USDC into my confidential account"

```bash
npx starkfi@latest status
npx starkfi@latest balance --token USDC
npx starkfi@latest conf-fund 100 --token USDC --simulate
npx starkfi@latest conf-fund 100 --token USDC
npx starkfi@latest tx-status <hash>
```

**User:** "Send 50 privately to this public key"

```bash
npx starkfi@latest conf-balance
npx starkfi@latest conf-transfer 50 --recipient-x 0xABC --recipient-y 0xDEF --simulate
npx starkfi@latest conf-transfer 50 --recipient-x 0xABC --recipient-y 0xDEF
npx starkfi@latest tx-status <hash>
```

**User:** "Withdraw 100 from my confidential account"

```bash
npx starkfi@latest conf-balance
npx starkfi@latest conf-withdraw 100 --simulate
npx starkfi@latest conf-withdraw 100
npx starkfi@latest tx-status <hash>
```

**User:** "Emergency withdraw everything"

```bash
# WARN: This empties the entire confidential balance
npx starkfi@latest conf-ragequit
npx starkfi@latest tx-status <hash>
```

**User:** "Activate my pending balance"

```bash
npx starkfi@latest conf-rollover
npx starkfi@latest tx-status <hash>
```

## Error Handling

| Error                         | Action                                                      |
| ----------------------------- | ----------------------------------------------------------- |
| `CONFIDENTIAL_NOT_CONFIGURED` | Run `conf-setup` with valid Tongo key and contract address. |
| `CONFIDENTIAL_FAILED`         | Check balance, credentials, and retry.                      |
| `Insufficient balance`        | Check `conf-balance` for active balance before operations.  |
| `Not authenticated`           | Run `authenticate-wallet` skill first.                      |

## Related Skills

- Use `authenticate-wallet` to ensure an active session before confidential operations.
- Use `balance` to verify public token balance before funding.
- Use `send` for standard (non-private) token transfers.
- Use `config` to set a custom RPC if experiencing rate limits.
