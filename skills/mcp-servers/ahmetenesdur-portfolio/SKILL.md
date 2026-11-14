---
name: portfolio
description: View a comprehensive DeFi portfolio dashboard and optimize portfolio allocation via automated rebalancing. Use this skill when the user wants an overview, summary, dashboard, total value, net worth, portfolio rebalancing, target allocation, or wants to see all their DeFi positions across Starknet at once. Also trigger when the user asks "what do I have", "show me everything", "how much am I worth", "my positions", "my investments", "rebalance my portfolio", "I want 50% ETH", "optimize my holdings", or any request for a holistic view of their Starknet holdings — even if they don't explicitly say "portfolio".
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.3.0
    author: ahmetenesdur
    category: wallet-data
allowed-tools:
    - Bash(npx starkfi@latest portfolio)
    - Bash(npx starkfi@latest portfolio *)
    - Bash(npx starkfi@latest portfolio-rebalance *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Portfolio Overview & Optimization

Display a comprehensive DeFi portfolio dashboard aggregating token balances, staking positions, Troves vault positions, Endur liquid staking (LST), lending positions, DCA orders, and confidential Tongo balances — all with USD valuations. Rebalance the portfolio to a target allocation via automated batch swaps.

## Prerequisites

- Active session required.
- For rebalancing: sufficient token balances + gas for batch swap transactions.

## Rules

1. Use `portfolio` as the FIRST command when the user asks "what do I have?" or wants an overall assessment.
2. The `portfolio` command is read-only — it never modifies any on-chain state.
3. USD prices are sourced from the StarkZap SDK and may have slight variations.
4. For `portfolio-rebalance`, ALWAYS use `--simulate` first to preview the plan before executing.
5. Target allocations must sum to **100%**. If they don't, inform the user and ask them to adjust.
6. After rebalancing, run `portfolio` again to confirm the new allocation.

## Commands

### Portfolio Dashboard

```bash
npx starkfi@latest portfolio [--json]
```

### Portfolio Rebalance

```bash
# Rebalance to target allocation
npx starkfi@latest portfolio-rebalance --target "<allocation>" [--slippage <n>] [--simulate] [--json]
```

## Parameters

### portfolio

| Parameter | Type | Description    | Required |
| --------- | ---- | -------------- | -------- |
| `--json`  | flag | Output as JSON | No       |

### portfolio-rebalance

| Parameter      | Type   | Description                                          | Required |
| -------------- | ------ | ---------------------------------------------------- | -------- |
| `--target`     | string | Target allocation (e.g. `"50 ETH, 30 USDC, 20 STRK"`) | Yes    |
| `--slippage`   | number | Slippage tolerance % (default: 1)                    | No       |
| `--simulate`   | flag   | Preview plan without executing                       | No       |
| `--json`       | flag   | Output as JSON                                       | No       |

**Target allocation format:** Comma-separated `<percentage> <token>` pairs that sum to 100.

## Dashboard Sections

The portfolio displays seven sections:

1. **Token Balances** — STRK, ETH, and all ERC-20 tokens with non-zero balances and their USD values.
2. **Staking Positions** — Active stakes across all validators/pools with pending rewards. Shows unpooling amounts and cooldown dates when exit intents are active.
3. **Lending Positions** — Active Vesu V2 positions: supplied and borrowed amounts with pool details.
4. **DCA Orders** — Active Dollar-Cost Averaging recurring swap orders.
5. **Confidential Tongo Balance** — Private active and pending balances under Tongo Cash.
6. **Troves Vault Positions** — Active deposits in Troves DeFi yield strategies with current value and APY.
7. **LST Positions** — xSTRK holdings from Endur liquid staking with current STRK value and yield accrued.

## Examples

**User:** "Show me my portfolio"

```bash
npx starkfi@latest portfolio
```

**User:** "What's my total value on Starknet?"

```bash
npx starkfi@latest portfolio
```

**User:** "Get my portfolio as JSON for analysis"

```bash
npx starkfi@latest portfolio --json
```

**User:** "Rebalance to 50% ETH, 30% USDC, 20% STRK"

```bash
# 1. View current allocation
npx starkfi@latest portfolio

# 2. Preview the rebalance plan
npx starkfi@latest portfolio-rebalance --target "50 ETH, 30 USDC, 20 STRK" --simulate

# 3. Execute after user confirms
npx starkfi@latest portfolio-rebalance --target "50 ETH, 30 USDC, 20 STRK"
npx starkfi@latest tx-status <hash>

# 4. Verify new allocation
npx starkfi@latest portfolio
```

**User:** "I want 60% ETH and 40% STRK"

```bash
npx starkfi@latest portfolio-rebalance --target "60 ETH, 40 STRK" --simulate
```

**User:** "Optimize my portfolio with 2% slippage"

```bash
npx starkfi@latest portfolio-rebalance --target "50 ETH, 30 USDC, 20 STRK" --slippage 2
```

## Error Handling

| Error                  | Action                                                                                             |
| ---------------------- | -------------------------------------------------------------------------------------------------- |
| `Not authenticated`    | Run `authenticate-wallet` skill first.                                                             |
| `Partial failure`      | Some sections may show errors while others succeed. The portfolio uses fault-tolerant aggregation. |
| `Network error`        | Retry once. Use `config` to set custom RPC.                                                        |
| `Invalid allocation`   | Ensure target percentages sum to 100 and token symbols are valid.                                  |
| `Rebalance failed`     | Check balances, ensure tokens have sufficient liquidity on supported providers. |
| `Insufficient balance` | Not enough tokens to execute swaps — check `balance` first.                                        |

## Related Skills

- Use `balance` for a focused view of token balances only.
- Use `staking` `stake-status` for detailed staking positions.
- Use `lending` `lend-status` for detailed lending positions.
- Use `lending` `lend-monitor` to monitor health factors across lending positions.
- Use `dca` `dca-list` to view active DCA orders.
- Use `troves` `troves-position` for detailed vault positions.
- Use `lst` `lst-position` for detailed liquid staking positions.
- Use `trade` if you need to swap a single token pair (not full rebalance).

