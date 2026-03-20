---
name: openpump-solana-mcp
description: >
  Solana token launch and trading tools via the OpenPump MCP server.
  Creates tokens on pump.fun, buys and sells tokens, runs market-making bots,
  snipes new token launches, sets stop-loss orders, generates vanity addresses,
  manages custodial wallets, transfers SOL and SPL tokens, checks balances,
  gets price quotes, monitors portfolio positions and creator fees.
  Use when the user asks to launch a token, trade a memecoin, buy or sell on pump.fun,
  check wallet balance, transfer SOL, set up a sniper, run a market maker,
  create wallets, get a price quote, claim creator fees, or do anything with pump.fun tokens.
  Also use for bundle launches, Jito bundles, bonding curve queries, and spam launches.
  Do not use for general Solana RPC queries, non-pump.fun DeFi (Raydium, Jupiter, Orca),
  NFT operations, or importing external private keys.
version: "2.0.0"
author: openpump
license: MIT
homepage: https://openpump.io
user-invocable: true

metadata:
  openclaw:
    emoji: "\U0001F680"
    requires:
      bins: ["node", "npx"]
      env: ["OPENPUMP_API_KEY"]
    primaryEnv: "OPENPUMP_API_KEY"
    install:
      - id: openpump-mcp
        kind: node
        package: "@openpump/mcp"
        bins: ["openpump-mcp"]
        label: "Install OpenPump MCP Server (npm)"
    os: ["linux", "darwin", "win32"]
    network: ["api.openpump.io", "mcp.openpump.io"]
    homepage: "https://openpump.io"

tags:
  - solana
  - crypto
  - trading
  - pump-fun
  - defi
  - mcp
  - token-launch
  - memecoin
  - jito
  - bonding-curve
  - market-making
  - sniper
  - stop-loss
---

# OpenPump MCP Server

Trade pump.fun tokens, manage Solana wallets, run market making bots, snipe new tokens, and monitor positions via MCP.

## Setup

### 1. Get Your API Key

1. Sign up at [openpump.io](https://openpump.io)
2. Go to Dashboard > API Keys
3. Create a new key (starts with `op_sk_live_`)

### 2. Set the Environment Variable

```bash
export OPENPUMP_API_KEY="op_sk_live_YOUR_KEY_HERE"
```

### 3. Add MCP Server

**Claude Code (HTTP transport -- no local process):**

```bash
claude mcp add --transport http openpump https://openpump.io/api/mcp \
  --header "Authorization: Bearer op_sk_live_YOUR_KEY_HERE"
```

**Claude Desktop / any MCP client (stdio via npx):**

```json
{
  "mcpServers": {
    "openpump": {
      "command": "npx",
      "args": ["-y", "@openpump/mcp@latest"],
      "env": {
        "OPENPUMP_API_KEY": "op_sk_live_YOUR_KEY_HERE"
      }
    }
  }
}
```

**HTTP transport (remote, no local process):**

```json
{
  "mcpServers": {
    "openpump": {
      "url": "https://mcp.openpump.io/mcp",
      "headers": {
        "Authorization": "Bearer ${OPENPUMP_API_KEY}"
      }
    }
  }
}
```

## Available Tools (57)

### Token Creation (2)

| Tool | Description |
|------|-------------|
| `create-token` | Launch a new token on pump.fun with name, symbol, description, and image |
| `bundle-launch` | Atomically create a token AND coordinate multi-wallet buys via Jito bundles |

### Trading (7)

| Tool | Description |
|------|-------------|
| `buy-token` | Buy a pump.fun token with SOL (single wallet). `amountSol` is a decimal SOL string (e.g. `"0.1"`) |
| `sell-token` | Sell a token position back to SOL. Use `tokenAmount: "all"` for entire balance |
| `bundle-buy` | Multi-wallet buy of an existing token via Jito bundles |
| `bundle-sell` | Multi-wallet sell packed into Jito bundles (bonding curve tokens only) |
| `get-token-quote` | Price quote for buy or sell without executing. `solAmount` in lamports string for buys |
| `estimate-bundle-cost` | Preview total SOL required for a bundle launch before executing |
| `claim-creator-fees` | Claim accumulated pump.fun creator fees for a wallet address |

### Transfers (2)

| Tool | Description |
|------|-------------|
| `transfer-sol` | Send SOL to any Solana address. `amountSol` is decimal SOL string. 10 SOL cap per call. Supports `dryRun` |
| `transfer-token` | Send SPL tokens to any Solana address. `tokenAmount` in raw base units or `"all"` |

### Wallet Management (5)

| Tool | Description |
|------|-------------|
| `create-wallet` | Create a new HD-derived custodial wallet with optional label |
| `batch-create-wallets` | Create 2-50 wallets in one action with auto-numbered labels |
| `get-aggregate-balance` | Sum SOL across all user wallets |
| `get-wallet-deposit-address` | Get deposit address and funding instructions for a wallet |
| `get-wallet-transactions` | Paginated transfer history (buy/sell/transfer) for a wallet |

### Market Making (13)

| Tool | Description |
|------|-------------|
| `mm-create-pool` | Create a wallet pool with N wallets grouped under a label (2-50 wallets) |
| `mm-list-pools` | List all wallet pools for the user |
| `mm-pool-status` | Aggregate status: per-wallet SOL and token balances, totals |
| `mm-fund-pool` | Distribute SOL from source wallet to all pool wallets. Supports multi-hop obfuscation (hops 0-3) |
| `mm-consolidate-pool` | Sweep all funds from pool wallets back to a single target wallet |
| `mm-start-session` | Start autonomous market making on a token with configurable strategy |
| `mm-stop-session` | Stop a running session. Positions are NOT auto-liquidated |
| `mm-pause-session` | Pause a session (retains position and config) |
| `mm-resume-session` | Resume a paused session from where it left off |
| `mm-session-status` | Detailed session stats: config, live data, recent trades |
| `mm-list-sessions` | List all sessions, optionally filter by status |
| `mm-update-strategy` | Hot-update strategy params on a running/paused session |
| `mm-get-pnl` | P&L report: WAC cost basis, realized/unrealized P&L, slippage-adjusted sell simulation, ROI% |

### Sniping (7)

| Tool | Description |
|------|-------------|
| `snipe-start` | Create a monitor that auto-buys new tokens matching criteria (ticker pattern, market cap, risk filters) |
| `snipe-stop` | Stop a snipe monitor permanently |
| `snipe-pause` | Pause a snipe monitor (resume later) |
| `snipe-resume` | Resume a paused snipe monitor |
| `snipe-update` | Update criteria on an active or paused monitor |
| `snipe-status` | Detailed status including criteria, buy count, state |
| `snipe-list` | List all snipe monitors, optionally filter by status |

### Stop Loss (4)

| Tool | Description |
|------|-------------|
| `stop-loss-set` | Create a stop-loss monitor. Auto-sells when market cap drops below trigger |
| `stop-loss-remove` | Remove a stop-loss monitor |
| `stop-loss-list` | List all stop-loss monitors |
| `stop-loss-status` | Detailed status of a specific stop-loss |

### Vanity Addresses (4)

| Tool | Description |
|------|-------------|
| `estimate-vanity-cost` | Estimate credits for a vanity pattern before ordering |
| `order-vanity-address` | Order a vanity wallet or mint address (prefix, suffix, or contains) |
| `list-vanity-jobs` | List vanity mining jobs (newest first) |
| `get-vanity-job` | Check status of a specific vanity job. Wallet auto-added on completion |

### Spam Launch (3)

| Tool | Description |
|------|-------------|
| `spam-launch` | Create multiple tokens in rapid succession from one wallet (1-100) |
| `estimate-spam-cost` | Estimate total SOL and credits for a spam launch |
| `cancel-spam-launch` | Cancel a running spam launch job |

### Information (9)

| Tool | Description |
|------|-------------|
| `get-token-info` | Bonding curve state: price, market cap, graduation status |
| `get-token-market-info` | Rich analytics: volume, buy/sell counts, risk metrics (snipers, bundlers, insiders) |
| `list-my-tokens` | All tokens launched by the authenticated user |
| `get-token-holdings` | Which wallets hold a specific token. Omit mint to see ALL holdings |
| `get-wallet-balance` | Live SOL + token balances for a single wallet |
| `list-wallets` | All wallets with public keys, labels, derivation index |
| `get-creator-fees` | Check accumulated pump.fun creator fees. Omit address to check all wallets |
| `get-jito-tip-levels` | Current Jito MEV tip amounts per priority level (refreshed every 20s) |

### Job Management (2)

| Tool | Description |
|------|-------------|
| `poll-job` | Check status of async operations. Poll every 2s until "completed" or "failed" |
| `cancel-job` | Cancel a running async job |

## Workflows

### 1. Launch a Token

```
1. create-wallet (label: "launch-wallet")
2. Fund the wallet with SOL (use get-wallet-deposit-address for the address)
3. create-token (name, symbol, description, imageUrl)
4. poll-job (wait for "completed")
5. get-token-info (verify token is live)
```

### 2. Bundle Launch (Create + Multi-Wallet Buy)

```
1. create-wallet (dev wallet)
2. batch-create-wallets (count: 5, labelPrefix: "buyer")
3. Fund all wallets with SOL
4. estimate-bundle-cost (buyWalletCount: 5, devBuyAmountSol: "0.1", walletBuyAmounts)
5. bundle-launch (devWalletId, buyWalletIds, tokenParams, amounts, confirm: true)
6. poll-job (wait for "completed")
7. get-token-holdings (mint) -- verify all wallets hold the token
```

### 3. Buy and Sell Flow

```
1. list-wallets (find walletId with SOL balance)
2. get-token-quote (action: "buy", solAmount: "100000000") -- 0.1 SOL in lamports
3. buy-token (mint, walletId, amountSol: "0.1") -- decimal SOL string
4. get-token-holdings (mint) -- verify purchase
5. get-token-quote (action: "sell", tokenAmount from holdings)
6. sell-token (mint, walletId, tokenAmount or "all")
```

### 4. Market Making

```
1. mm-create-pool (label: "mm-pool", walletCount: 10)
2. mm-fund-pool (poolId, sourceWalletId, totalAmountSol: 2.5, hops: 2)
3. mm-pool-status (poolId) -- verify funding
4. mm-start-session (mint, walletPoolId, config: {
     amountRange: ["5000000", "50000000"],  -- 0.005 to 0.05 SOL in lamports
     maxPositionSol: "1000000000",           -- 1 SOL max
     netBias: 0.5,                           -- balanced buys/sells
     intervalRange: [10, 45],                -- 10-45s between trades
     confirm: true
   })
5. mm-session-status (sessionId) -- monitor
6. mm-get-pnl (sessionId) -- check profitability
7. mm-stop-session (sessionId) -- when done
8. mm-consolidate-pool (poolId, targetWalletId) -- recover funds
```

### 5. Sniping New Tokens

```
1. list-wallets -- pick a funded wallet
2. snipe-start (walletId, tickerPattern: "PEPE*", buyAmountSol: 0.05, {
     maxDevPercent: 10,       -- filter rugs
     maxSniperCount: 5,       -- avoid crowded launches
     maxBuys: 3,              -- stop after 3 buys
     confirm: true
   })
3. snipe-status (monitorId) -- check matches
4. snipe-update (monitorId, ...) -- adjust criteria live
5. snipe-stop (monitorId) -- when done
```

### 6. Stop Loss Protection

```
1. get-token-holdings (mint) -- confirm position
2. get-token-market-info (mint) -- check current market cap
3. stop-loss-set (walletId, mint, triggerMarketCapSol: 5.0, confirm: true)
4. stop-loss-status (stopLossId) -- verify active
5. stop-loss-remove (stopLossId) -- cancel if no longer needed
```

### 7. Check Portfolio

```
1. list-wallets -- see all wallets
2. get-aggregate-balance -- total SOL across wallets
3. get-token-holdings -- all token positions (omit mint for everything)
4. get-token-market-info (per mint) -- current prices and risk metrics
```

### 8. Claim Creator Fees

```
1. get-creator-fees -- check all wallets for accumulated fees
2. claim-creator-fees (creatorAddress)
3. get-wallet-balance (walletId) -- verify SOL increased
```

### 9. Transfer SOL Out

```
1. get-wallet-balance (walletId) -- check available SOL
2. transfer-sol (walletId, toAddress, amountSol: "1.0", dryRun: true) -- preview
3. transfer-sol (walletId, toAddress, amountSol: "1.0", confirm: true) -- execute
```

### 10. Vanity Address

```
1. estimate-vanity-cost (pattern: "PUMP", patternType: "prefix")
2. order-vanity-address (pattern: "PUMP", patternType: "prefix")
3. get-vanity-job (jobId) -- poll until "completed"
4. list-wallets -- new vanity wallet appears automatically
```

## Safety Guardrails

**All trading actions require explicit user confirmation before execution.**

1. **Always check balances first.** Run `get-wallet-balance` or `get-aggregate-balance` before any trade or transfer.

2. **Use quotes before trading.** Call `get-token-quote` to preview expected output and price impact.

3. **Confirm large trades explicitly.** Bundle operations, MM sessions, and snipe monitors all require `confirm: true`. Review parameters first.

4. **Verify addresses on transfers.** Double-check destination addresses. Transfers are irreversible on Solana.

5. **Use dryRun for transfers.** Both `transfer-sol` and `transfer-token` support `dryRun: true`.

6. **Check risk metrics.** Use `get-token-market-info` to check sniper count, bundler activity, and insider percentage before buying.

7. **Set stop-losses.** Use `stop-loss-set` to protect positions from sudden drops.

8. **Bundle slippage.** `bundle-launch` packs multiple wallets per TX. Use 2500+ bps slippage (25%) for bundles, not the default 500 bps.

9. **MM drawdown.** Market making sessions have a `maxDrawdownPercent` circuit breaker (default 15%). Session auto-stops if losses exceed this.

10. **Transfer cap.** `transfer-sol` has a 10 SOL cap per call. Split larger amounts into multiple calls.

11. **Monitor async ops.** After `create-token`, `bundle-launch`, or `spam-launch`, poll every 2 seconds. Jobs expire after 10 minutes.

## Key Concepts

- **SOL amounts:** `amountSol` params accept decimal SOL strings (`"0.1"` = 0.1 SOL). NOT lamports.
- **Lamports:** Some params (`get-token-quote` solAmount, `mm-start-session` amountRange) use lamports as integer strings (1 SOL = 1,000,000,000).
- **Token base units:** Token amounts use raw base units. Use the exact `"amount"` string from `get-token-holdings`.
- **Custodial wallets:** HD-derived, managed by the platform. Cannot import external keys.
- **Bonding curve:** pump.fun tokens trade on a bonding curve until graduation to PumpSwap. `bundle-sell` only works on bonding curve tokens.
- **Jito bundles:** Atomic, same-block execution. First bundle is guaranteed atomic; overflow wallets go into subsequent bundles.
- **Wallet pools:** Groups of wallets for market making. Multi-hop funding breaks on-chain clustering.

## Links

- Website: [openpump.io](https://openpump.io)
- npm: [@openpump/mcp](https://www.npmjs.com/package/@openpump/mcp)
