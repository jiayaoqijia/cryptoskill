---
name: lst
description: Liquid staking via Endur on Starknet — stake STRK to receive xSTRK, redeem xSTRK back to STRK, check positions, and view protocol stats. Yield is embedded in the xSTRK share price (no manual claim needed). Use this skill when the user mentions liquid staking, LST, xSTRK, Endur, liquid staking token, share price, instant staking, tradeable staking position, or wants a staking token they can trade or use in DeFi — even if they don't say "liquid staking" explicitly.
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.2.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest lst-position)
    - Bash(npx starkfi@latest lst-position *)
    - Bash(npx starkfi@latest lst-stats)
    - Bash(npx starkfi@latest lst-stats *)
    - Bash(npx starkfi@latest lst-stake *)
    - Bash(npx starkfi@latest lst-redeem *)
    - Bash(npx starkfi@latest lst-exit-all)
    - Bash(npx starkfi@latest lst-exit-all *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Liquid Staking (Endur LST)

Stake STRK tokens through the Endur liquid staking protocol to receive **xSTRK** — a liquid staking token whose value appreciates over time as staking yield accrues automatically.

## Prerequisites

- Active session required.
- Sufficient STRK balance for staking + gas fees.

## ⚠️ Critical: Yield Model

Endur LST yield is **NOT** a claimable reward. The xSTRK share price increases automatically to reflect accumulated staking yield. To realize your yield, redeem xSTRK back to STRK — you will receive more STRK than you originally staked.

**Do NOT use the `staking` skill's `rewards --claim` or `rewards --compound` for xSTRK positions.** Those commands are for delegation staking only.

## LST vs Delegation Staking

| Feature             | Delegation Staking (`staking` skill) | Endur LST (`lst` skill)          |
| ------------------- | ------------------------------------ | -------------------------------- |
| Token received      | None (position tracked on-chain)     | xSTRK (ERC-20, tradeable)        |
| Yield mechanism     | Manual claim via `rewards --claim`   | Automatic via share price        |
| Liquidity           | Locked until unstake cooldown        | Liquid — trade xSTRK anytime     |
| DeFi composability  | Limited                              | xSTRK usable in Troves, lending  |
| Unstaking           | 2-step process with cooldown         | Instant redemption               |

## Rules

1. BEFORE staking, check `balance --token STRK` to confirm sufficient STRK.
2. Use `lst-stats` to check the current exchange rate, total STRK staked, and APR before staking.
3. Use `lst-position` to check the user's current xSTRK balance and its STRK value.
4. **NEVER** suggest using `rewards --claim` or `rewards --compound` for LST positions. Yield is automatic.
5. When the user asks about "how much yield" from LST, show `lst-position` which displays the current STRK value vs original deposit.
6. AFTER any transactional operation (stake, redeem, exit-all), verify with `tx-status`.
7. `lst-exit-all` redeems the entire xSTRK balance — warn the user before executing.

## Commands

```bash
# Check LST position (xSTRK balance and STRK value)
npx starkfi@latest lst-position [-a <symbol>] [--json]

# View Endur protocol stats (exchange rate, APR, total staked)
npx starkfi@latest lst-stats [-a <symbol>] [--json]

# Stake STRK to receive xSTRK
npx starkfi@latest lst-stake <amount> [-a <symbol>] [--json]

# Redeem xSTRK back to STRK (partial)
npx starkfi@latest lst-redeem <amount> [-a <symbol>] [--json]

# Redeem all xSTRK back to STRK
npx starkfi@latest lst-exit-all [-a <symbol>] [--json]
```

## Parameters

### lst-position / lst-stats

| Parameter    | Type   | Description                                    | Required |
| ------------ | ------ | ---------------------------------------------- | -------- |
| `-a, --asset`| string | Underlying asset symbol (default: STRK)        | No       |
| `--json`     | flag   | Output as JSON                                 | No       |

### lst-stake

| Parameter    | Type   | Description                                    | Required |
| ------------ | ------ | ---------------------------------------------- | -------- |
| `amount`     | number | Amount of the asset to stake                   | Yes      |
| `-a, --asset`| string | Asset to stake (default: STRK)                 | No       |
| `--json`     | flag   | Output as JSON                                 | No       |

### lst-redeem

| Parameter    | Type   | Description                                    | Required |
| ------------ | ------ | ---------------------------------------------- | -------- |
| `amount`     | number | Amount of LST shares to redeem                 | Yes      |
| `-a, --asset`| string | Underlying asset (default: STRK)               | No       |
| `--json`     | flag   | Output as JSON                                 | No       |

### lst-exit-all

| Parameter    | Type   | Description                                    | Required |
| ------------ | ------ | ---------------------------------------------- | -------- |
| `-a, --asset`| string | Asset to exit completely (default: STRK)       | No       |
| `--json`     | flag   | Output as JSON                                 | No       |

## Examples

**User:** "What's the current LST exchange rate?"

```bash
npx starkfi@latest lst-stats
```

**User:** "Stake 1000 STRK via liquid staking"

```bash
npx starkfi@latest status
npx starkfi@latest balance --token STRK
npx starkfi@latest lst-stats   # Check current exchange rate
npx starkfi@latest lst-stake 1000
npx starkfi@latest tx-status <hash>
```

**User:** "How much is my xSTRK worth?"

```bash
npx starkfi@latest lst-position
```

**User:** "Redeem 500 xSTRK back to STRK"

```bash
npx starkfi@latest lst-position  # Check available xSTRK balance
npx starkfi@latest lst-redeem 500
npx starkfi@latest tx-status <hash>
```

**User:** "Exit all my liquid staking"

```bash
npx starkfi@latest lst-position  # Show what will be redeemed
# WARN: This redeems all xSTRK. Confirm with user.
npx starkfi@latest lst-exit-all
npx starkfi@latest tx-status <hash>
```

**User:** "Should I use regular staking or liquid staking?"

```bash
# Show both options for comparison
npx starkfi@latest lst-stats          # LST: exchange rate, APR
npx starkfi@latest validators         # Delegation: validator list
# Explain: LST = liquid + auto-yield; Delegation = locked + manual claim
```

## Error Handling

| Error                  | Action                                                   |
| ---------------------- | -------------------------------------------------------- |
| `Insufficient balance` | Check `balance --token STRK` for staking, or `lst-position` for redeem. |
| `Not authenticated`    | Run `authenticate-wallet` skill first.                   |

## Related Skills

- Use `balance` to check available STRK before staking.
- Use `staking` for delegation staking (validator-based, manual reward claims).
- Use `troves` to deposit xSTRK into yield vaults for additional yield.
- Use `portfolio` for a full overview including LST positions with USD values.
- Use `batch` to combine swaps with liquid staking in one transaction.
