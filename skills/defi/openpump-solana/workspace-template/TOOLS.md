# TOOLS -- OpenPump MCP Server Tool Reference

This workspace connects to the OpenPump MCP server, which provides 57 tools for Solana token operations on pump.fun. All tools communicate with the OpenPump REST API using your `OPENPUMP_API_KEY`.

## MCP Server Connection

The server is configured in `openclaw.json` and connects automatically when OpenClaw starts. All tools below are available as MCP tool calls.

**Important conventions:**
- SOL amounts are always in **lamports** as decimal integer strings (1 SOL = `"1000000000"`)
- Token amounts use raw **base units** as decimal strings (use the exact string from `get-token-holdings`)
- Never pass floats or JavaScript numbers for on-chain amounts -- always use strings
- Wallet IDs are UUIDs returned by `list-wallets`, not public key addresses

---

## Token Creation Tools

### `create-token`

Launch a new token on pump.fun with a bonding curve.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | ID of the creator/dev wallet |
| name | string | Yes | Token name (max 32 chars) |
| symbol | string | Yes | Token ticker symbol (max 10 chars) |
| description | string | Yes | Token description (max 500 chars) |
| imageUrl | string | Yes | Publicly accessible image URL (fetched and uploaded to IPFS) |
| initialBuyAmountSol | number | No | SOL amount for dev initial buy at creation |
| twitter | string | No | Twitter handle |
| telegram | string | No | Telegram link |
| website | string | No | Website URL |

**When to use:** Only when explicitly instructed to create a token. Not part of the standard trading workflow.

**Returns:** Mint address and transaction signature. Typical confirmation: 2-5 seconds.

---

## Trading Tools

### `bundle-launch`

Create a new token AND execute coordinated multi-wallet buys in one atomic operation. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| devWalletId | string | Yes | ID of the dev/creator wallet |
| buyWalletIds | string[] | Yes | IDs of wallets for coordinated buy (max 20) |
| tokenParams | object | Yes | `{ name, symbol, description, imageUrl }` |
| devBuyAmountSol | string | Yes | Dev buy amount in lamports |
| walletBuyAmounts | string[] | Yes | Per-wallet SOL amounts in lamports |
| priorityLevel | string | No | Priority tier (default: `"normal"`) |
| confirm | boolean | Yes | Must be `true` to execute |

**When to use:** Full token launch with simultaneous multi-wallet buy. Combines `create-token` + `bundle-buy` into one step. Always run `estimate-bundle-cost` first.

**Returns:** Job ID for async tracking via `poll-job`.

### `buy-token`

Buy a pump.fun token with SOL from a single wallet.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | ID of the wallet to buy with |
| mint | string | Yes | Token mint address (base58) |
| amountSol | string | Yes | SOL to spend in lamports (e.g., `"100000000"` = 0.1 SOL) |
| slippageBps | number | No | Slippage tolerance in basis points (default: 500 = 5%) |
| priorityLevel | string | No | `"economy"`, `"normal"` (default), `"fast"`, or `"turbo"` |

**When to use:** Primary buy tool. Always call `get-token-quote` first to preview.

**Returns:** Transaction result with updated wallet balance.

### `sell-token`

Sell a token position back to SOL.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | ID of the wallet holding the token |
| mint | string | Yes | Token mint address (base58) |
| tokenAmount | string | Yes | Raw base units as string, or `"all"` to sell entire balance |
| slippageBps | number | No | Slippage tolerance in basis points (default: 500 = 5%) |
| priorityLevel | string | No | `"economy"`, `"normal"` (default), `"fast"`, or `"turbo"` |

**When to use:** For all exits -- stop-loss, take-profit, time decay, manual sell. Use `tokenAmount: "all"` for full exits.

**Returns:** Transaction result with updated wallet balance.

### `bundle-buy`

Coordinated multi-wallet buy at token creation via Jito MEV bundles. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| devWalletId | string | Yes | ID of the dev/creator wallet |
| buyWalletIds | string[] | Yes | IDs of wallets for bundle buy (max 20) |
| tokenParams | object | Yes | `{ name, symbol, description, imageUrl }` |
| devBuyAmountSol | string | Yes | Dev buy amount in lamports |
| walletBuyAmounts | string[] | Yes | Per-wallet SOL amounts in lamports |
| priorityLevel | string | No | Priority tier (default: `"normal"`) |
| confirm | boolean | Yes | Must be `true` to execute |

**When to use:** Advanced token launch with coordinated multi-wallet buying. Always run `estimate-bundle-cost` first.

**Returns:** Job ID for async tracking via `poll-job`.

### `bundle-sell`

Multi-wallet sell packed into Jito MEV bundles. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| mint | string | Yes | Token mint address (base58) |
| walletSells | object[] | Yes | Array of `{ walletId, tokenAmount }` (1-20 wallets) |
| tipWalletId | string | No | Wallet ID that pays the Jito tip |
| slippageBps | number | No | Slippage tolerance (default: 500 = 5%) |
| priorityLevel | string | No | Priority tier (default: `"normal"`) |
| confirm | boolean | Yes | Must be `true` to execute |

**When to use:** Selling from multiple wallets simultaneously. Only works on bonding curve tokens (not yet graduated).

### `estimate-bundle-cost`

Preview the total SOL required for a bundle launch without submitting.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| buyWalletCount | number | Yes | Number of buy wallets (max 20) |
| devBuyAmountSol | string | Yes | Dev buy amount in lamports |
| walletBuyAmounts | string[] | Yes | Per-wallet amounts in lamports |
| tipLamports | number | No | Custom Jito tip in lamports |
| priorityLevel | string | No | Priority tier (default: `"normal"`) |

**When to use:** Always call before `bundle-buy` to verify sufficient balances.

### `claim-creator-fees`

Claim all accumulated creator fees for a wallet address.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| creatorAddress | string | Yes | Creator wallet address (base58) |

**When to use:** After `get-creator-fees` shows a claimable balance. Call periodically to collect fees.

---

## Transfer Tools

### `transfer-sol`

Send SOL to any Solana address. Hard cap: 10 SOL per call. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| fromWalletId | string | Yes | Source wallet ID |
| toAddress | string | Yes | Destination Solana address (base58) |
| amountSol | string | Yes | Amount in lamports (max `"10000000000"` = 10 SOL) |
| memo | string | No | On-chain memo (max 256 chars) |
| priorityFeeMicroLamports | number | No | Priority fee in micro-lamports |
| dryRun | boolean | No | Validate without submitting (default: false) |
| confirm | boolean | Yes | Must be `true` to execute |

**When to use:** Moving SOL between wallets or to external addresses. Always use `dryRun: true` first to preview.

### `transfer-token`

Send SPL tokens to any Solana address. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| fromWalletId | string | Yes | Source wallet ID |
| toAddress | string | Yes | Destination Solana address (base58) |
| mint | string | Yes | SPL token mint address (base58) |
| tokenAmount | string | Yes | Raw base units as string, or `"all"` |
| memo | string | No | On-chain memo (max 256 chars) |
| priorityFeeMicroLamports | number | No | Priority fee in micro-lamports |
| dryRun | boolean | No | Validate without submitting (default: false) |
| confirm | boolean | Yes | Must be `true` to execute |

**When to use:** Moving tokens between wallets or to external addresses. Always use `dryRun: true` first.

---

## Wallet Management Tools

### `create-wallet`

Create a new HD-derived custodial wallet.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| label | string | No | Human-readable label (e.g., `"trading-main"`) |

**When to use:** Setting up a new trading wallet. Use labels to organize by purpose.

### `batch-create-wallets`

Create 2-50 HD-derived wallets in a single action with auto-numbered labels.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| count | number | Yes | Number of wallets to create (2-50) |
| labelPrefix | string | No | Label prefix — wallets named `"{prefix}-1"`, `"{prefix}-2"`, etc. Defaults to `"wallet"` |

**Credit cost:** 2,000 credits per wallet.

**When to use:** Setting up multiple wallets at once for sniping, distribution, or volume operations.

### `get-aggregate-balance`

Sum SOL across all user wallets. No parameters.

**When to use:** Quick check of total available capital before large operations.

### `get-wallet-deposit-address`

Get deposit address and funding instructions for a wallet.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | Wallet ID to get deposit address for |

**When to use:** When a wallet needs to be funded from an external source.

### `get-wallet-transactions`

Paginated transfer history for a wallet.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | Wallet ID |
| type | string | No | Filter: `"buy"`, `"sell"`, or `"transfer"` |
| limit | number | No | Results per page (default: 50, max: 100) |
| offset | number | No | Pagination offset (default: 0) |

**When to use:** Reviewing trade history, calculating P&L, auditing transactions.

---

## Information & Analytics Tools

### `get-token-info`

Bonding curve state for a pump.fun token: price, market cap, graduation status.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| mint | string | Yes | Token mint address (base58) |

**When to use:** First check when evaluating a token. Confirms the token exists and is active.

### `get-token-market-info`

Rich analytics: volume, buy/sell counts, price changes, risk metrics (snipers, bundlers, insiders). Mainnet only.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| mint | string | Yes | Token mint address (base58) |

**When to use:** Second check in the safety checklist. Critical for risk assessment. Always check before buying.

### `list-my-tokens`

All tokens launched by the authenticated user. No parameters.

**When to use:** Reviewing tokens you have created (for creator fee claims).

### `get-token-holdings`

Check which wallets hold a specific token, or get all token holdings across all wallets.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| mint | string | No | Token mint address. Omit for ALL holdings across all wallets |

**When to use:** Before selling (to get exact token amounts), during heartbeat checks (to scan all positions), after buying (to verify purchase).

### `get-wallet-balance`

SOL and token balances for a single wallet. Real-time on-chain data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | Wallet ID |

**When to use:** Before buying (to confirm sufficient SOL), after trades (to verify balance changes).

### `list-wallets`

All wallets with public keys, labels, and derivation index. No parameters.

**When to use:** At startup to identify available wallets. After creating a new wallet.

### `get-creator-fees`

Check accumulated PumpFun creator fees across wallets.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| address | string | No | Specific creator address. Omit to check all wallets |

**When to use:** Periodically to check if creator fees are claimable.

### `get-token-quote`

Price quote for buy or sell without executing a transaction.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| mint | string | Yes | Token mint address |
| action | string | Yes | `"buy"` or `"sell"` |
| solAmount | string | Conditional | SOL in lamports (required for buy) |
| tokenAmount | string | Conditional | Raw base units (required for sell) |

**When to use:** Always before `buy-token` or `sell-token` to preview expected output and price impact.

### `get-jito-tip-levels`

Current Jito MEV tip amounts per priority level. No parameters.

**When to use:** Before trades to understand current MEV costs. Useful for selecting appropriate priority level.

---

## Job Management

### `poll-job`

Check status of async operations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| jobId | string | Yes | Job ID from a previous async tool call |

**When to use:** After `bundle-buy`, `spam-launch`, or any operation that returns a `jobId`. Poll every 2 seconds until status is `"completed"` or `"failed"`. Jobs expire after 10 minutes.

### `cancel-job`

Cancel a running orchestration job (e.g. spam-launch).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| jobId | string | Yes | Job ID of the running job to cancel |

**When to use:** To stop a long-running job mid-execution. Returns a progress summary showing completed/failed/remaining items.

---

## Vanity Address Tools

### `estimate-vanity-cost`

Get the credit cost and estimated generation time for a vanity Solana address.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pattern | string | Yes | Desired vanity pattern (1-8 characters, base58 charset) |
| patternType | string | No | Match location: `"prefix"` (default), `"suffix"`, or `"contains"` |
| caseSensitive | boolean | No | Whether matching is case-sensitive (default: `true`) |

**When to use:** Always call before `order-vanity-address` to preview cost.

### `order-vanity-address`

Order generation of a vanity Solana address.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pattern | string | Yes | Desired vanity pattern (1-8 characters, base58 charset) |
| patternType | string | No | Match location: `"prefix"`, `"suffix"`, or `"contains"` |
| caseSensitive | boolean | No | Case-sensitive matching (default: `true`) |
| addressType | string | No | `"wallet"` (default) or `"mint"` |

**When to use:** After reviewing cost with `estimate-vanity-cost`. Returns a job ID to track with `get-vanity-job`.

### `list-vanity-jobs`

List vanity address generation jobs.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | number | No | Results per page (1-100, default: 20) |
| offset | number | No | Pagination offset (default: 0) |

**When to use:** To check status of all vanity generation jobs.

### `get-vanity-job`

Get details of a specific vanity address job.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| jobId | string | Yes | Vanity job UUID |

**When to use:** To check status and retrieve the generated address when complete.

---

## Market Making Tools

### Pool Management

### `mm-create-pool`

Create a new wallet pool for market making. Generates fresh HD-derived wallets.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| label | string | Yes | Pool label (1-64 characters) |
| walletCount | number | Yes | Number of wallets to create (2-50) |

**When to use:** Before starting a market making session that uses a pool. Pools organize wallets for coordinated trading.

### `mm-fund-pool`

Distribute SOL from a source wallet to all wallets in a pool. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| poolId | string | Yes | Pool ID (from `mm-create-pool` or `mm-list-pools`) |
| totalAmountSol | number | Yes | Total SOL to distribute (positive number, in SOL not lamports) |
| sourceWalletId | string | Yes | Wallet ID to fund from (from `list-wallets`) |
| hops | number | No | Intermediate transfer hops for obfuscation (0-3, default: 0) |
| confirm | boolean | Yes | Must be `true` to execute |

**When to use:** After creating a pool, before starting a session. Use `mm-pool-status` to verify balances after funding.

### `mm-pool-status`

Get detailed balance information for all wallets in a pool.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| poolId | string | Yes | Pool ID to inspect |

**When to use:** After funding to verify distribution, during sessions to monitor balances, before consolidation to review.

**Returns:** Per-wallet SOL + token balances, aggregate totals.

### `mm-consolidate-pool`

Sweep all funds from every wallet in a pool to a single target wallet. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| poolId | string | Yes | Pool ID to consolidate |
| targetWalletId | string | Yes | Wallet ID to receive all consolidated funds |
| mint | string | No | Optional SPL token mint to also consolidate. If omitted, only SOL is swept |
| confirm | boolean | Yes | Must be `true` to execute |

**When to use:** After ending a market making session to recover funds. Use `mm-pool-status` first to review balances.

### `mm-list-pools`

List all wallet pools for the authenticated user. No parameters.

**When to use:** To find pool IDs for use with other MM tools.

**Returns:** Pool ID, label, wallet count, and creation date for each pool.

### Session Lifecycle

### `mm-start-session`

Start a new market making session on a PumpFun token. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| mint | string | Yes | Token mint address (base58) to market-make |
| walletPoolId | string | Conditional | Wallet pool ID. Mutually exclusive with `walletIds` |
| walletIds | string[] | Conditional | Explicit wallet IDs. Mutually exclusive with `walletPoolId` |
| config | object | Yes | Session configuration (see Config Object below) |
| confirm | boolean | Yes | Must be `true` to start |

**Config Object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| netBias | number | No | Buy/sell bias 0-1 (0=all sell, 0.5=neutral, 1=all buy). Default: 0.5 |
| amountRange | [string, string] | Yes | Min/max SOL per trade in lamports (e.g. `["10000000", "50000000"]`) |
| intervalRange | [number, number] | No | Min/max seconds between trades. Default: `[10, 45]` |
| supportLevels | string[] | No | Market cap SOL levels to defend (lamport strings) |
| takeProfitLevels | object[] | No | Array of `{ price: string, sellPercent: number }` |
| maxPositionSol | string | Yes | Maximum position size in lamports |
| maxDrawdownPercent | number | No | Stop-loss drawdown threshold (5-50). Default: 15 |
| volumeMode | boolean | No | If true, buys and immediately sells for volume. Default: false |
| maxDurationMinutes | number | No | Auto-stop after N minutes (0=infinite, max 10080). Default: 1440 |
| slippageBps | number | No | Slippage tolerance (100-5000 bps). Default: 500 |
| priorityLevel | string | No | Jito priority: `"economy"`, `"normal"` (default), `"fast"`, `"turbo"` |

**When to use:** To start automated market making. Only one active session per token per user. Use `mm-session-status` to monitor.

### `mm-stop-session`

Stop a running or paused market making session.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sessionId | string | Yes | Session ID (from `mm-list-sessions`) |

**When to use:** To permanently halt trading. Positions are NOT automatically liquidated — use `sell-token` or `bundle-sell` to exit.

### `mm-pause-session`

Pause a running market making session.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sessionId | string | Yes | Session ID (from `mm-list-sessions`) |

**When to use:** To temporarily halt trading while retaining position and config. Resume with `mm-resume-session`.

### `mm-resume-session`

Resume a paused market making session.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sessionId | string | Yes | Session ID (from `mm-list-sessions`) |

**When to use:** After pausing, to restart trading from where it left off.

### `mm-session-status`

Get detailed status of a market making session including config, live stats, and recent trades.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sessionId | string | Yes | Session ID (from `mm-list-sessions`) |

**When to use:** To monitor a running session. Returns trades executed, volume, position size, P&L, and drawdown.

### `mm-list-sessions`

List all market making sessions for the authenticated user.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter: `"active"`, `"paused"`, `"stopped"`, or `"error"`. Omit for all |

**When to use:** To find session IDs and get an overview of all sessions.

### `mm-update-strategy`

Hot-update strategy parameters on a running or paused session. Changes take effect on the next tick.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sessionId | string | Yes | Session ID (from `mm-list-sessions`) |
| config | object | Yes | Partial config — only include fields to change (same fields as Config Object above) |

**When to use:** To adjust strategy without stopping the session. Only provided fields are updated.

### `mm-get-pnl`

Get a detailed P&L report for a market making session.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sessionId | string | Yes | Session ID (from `mm-list-sessions`) |

**When to use:** To review session profitability.

**Returns:** WAC cost basis, realized P&L, unrealized P&L (mark-to-market AND slippage-adjusted sell simulation), fees, ROI%, and position summary.

---

## Sniping & Stop-Loss Tools

### Sniping

### `snipe-start`

Start monitoring for new token launches matching criteria, with automatic buy on match. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | Wallet ID to buy with |
| tickerPattern | string | Yes | Regex pattern to match token symbols (e.g. `"^PEPE"`, `".*AI.*"`) |
| buyAmountSol | string | Yes | SOL to spend per snipe in lamports |
| minMarketCapSol | string | No | Minimum market cap in lamports to trigger |
| maxMarketCapSol | string | No | Maximum market cap in lamports to trigger |
| maxDevPercent | number | No | Max developer token holding percentage |
| maxTop10Percent | number | No | Max top-10 holder concentration percentage |
| maxSniperCount | number | No | Max number of snipers detected on the token |
| maxAgeSeconds | number | No | Max token age in seconds since creation |
| requireSocial | boolean | No | Require at least one social link (Twitter/Telegram/website) |
| slippageBps | number | No | Slippage tolerance (default: 500 = 5%) |
| priorityLevel | string | No | Jito priority level (default: `"fast"`) |
| maxBuys | number | No | Max number of buys before auto-stopping |
| confirm | boolean | Yes | Must be `true` to start |

**When to use:** To automatically buy tokens matching specific criteria as they launch. Monitor with `snipe-status`.

### `snipe-stop`

Permanently stop a snipe monitor. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| monitorId | string | Yes | Monitor ID (from `snipe-list`) |
| confirm | boolean | Yes | Must be `true` to stop |

### `snipe-pause`

Pause a running snipe monitor.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| monitorId | string | Yes | Monitor ID (from `snipe-list`) |

### `snipe-resume`

Resume a paused snipe monitor.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| monitorId | string | Yes | Monitor ID (from `snipe-list`) |

### `snipe-update`

Update criteria on a running or paused snipe monitor.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| monitorId | string | Yes | Monitor ID (from `snipe-list`) |
| tickerPattern | string | No | Updated regex pattern |
| buyAmountSol | string | No | Updated buy amount in lamports |
| minMarketCapSol | string | No | Updated min market cap |
| maxMarketCapSol | string | No | Updated max market cap |
| maxDevPercent | number | No | Updated max dev percentage |
| maxTop10Percent | number | No | Updated max top-10 percentage |
| maxSniperCount | number | No | Updated max sniper count |
| maxAgeSeconds | number | No | Updated max age |
| requireSocial | boolean | No | Updated social requirement |
| slippageBps | number | No | Updated slippage tolerance |
| priorityLevel | string | No | Updated priority level |
| maxBuys | number | No | Updated max buys |

**When to use:** To adjust snipe criteria without stopping and restarting.

### `snipe-status`

Get detailed status of a snipe monitor.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| monitorId | string | Yes | Monitor ID |

### `snipe-list`

List all snipe monitors.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter: `"active"`, `"paused"`, or `"stopped"` |

### Stop-Loss

### `stop-loss-set`

Set a stop-loss order that auto-sells when market cap drops below threshold. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | Wallet ID holding the token |
| mint | string | Yes | Token mint address (base58) |
| triggerMarketCapSol | string | Yes | Market cap threshold in lamports — sells when price drops to this level |
| sellPercent | number | No | Percentage of position to sell (1-100, default: 100) |
| slippageBps | number | No | Slippage tolerance (default: 500 = 5%) |
| priorityLevel | string | No | Jito priority level (default: `"fast"`) |
| confirm | boolean | Yes | Must be `true` to set |

**When to use:** To protect a position with automatic downside protection.

### `stop-loss-remove`

Remove an active stop-loss order. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| stopLossId | string | Yes | Stop-loss ID (from `stop-loss-list`) |
| confirm | boolean | Yes | Must be `true` to remove |

### `stop-loss-list`

List all stop-loss orders.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter: `"active"`, `"triggered"`, or `"stopped"` |

### `stop-loss-status`

Get detailed status of a stop-loss order.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| stopLossId | string | Yes | Stop-loss ID |

---

## Spam Launch Tools

### `spam-launch`

Launch multiple tokens in rapid succession. Requires `confirm: true`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| walletId | string | Yes | Creator wallet ID |
| count | number | Yes | Number of tokens to launch (1-100) |
| delayMs | number | No | Delay between launches in ms (500-60000, default: 2000) |
| nameTemplate | string | No | Token name template, `{i}` = index (max 32 chars, default: `"Token #{i}"`) |
| symbolTemplate | string | No | Symbol template, `{i}` = index (max 10 chars, default: `"TKN{i}"`) |
| description | string | Yes | Token description (max 500 chars) |
| imageUrl | string | No | Image URL (fetched once and reused). Random generated if omitted |
| initialBuyAmountSol | string | No | Initial buy per token in lamports |
| failureMode | string | No | `"stop"`, `"skip"` (default), or `"retry"` — behavior on individual launch failure |
| priorityLevel | string | No | Jito priority (default: `"economy"`) |
| confirm | boolean | Yes | Must be `true` to execute |

**When to use:** For batch token creation campaigns. Returns a job ID — track with `poll-job`, cancel with `cancel-spam-launch`. Circuit breaker: auto-stops after 5 consecutive failures.

### `estimate-spam-cost`

Preview the total cost of a spam launch campaign.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| count | number | Yes | Number of tokens to launch (1-100) |
| initialBuyAmountSol | string | No | Initial buy per token in lamports (default: `"0"`) |
| priorityLevel | string | No | Jito priority (default: `"economy"`) |

**When to use:** Always call before `spam-launch` to verify sufficient balance.

### `cancel-spam-launch`

Cancel a running spam launch job.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| jobId | string | Yes | Job ID from `spam-launch` |

**When to use:** To stop a spam launch mid-execution. Returns progress summary.

---

## Priority Level Reference

| Level | Jito Tip Range | Use Case |
|-------|---------------|----------|
| `economy` | ~1,000 - 10,000 lamports | Low-urgency trades, saving fees |
| `normal` | ~2,000 - 100,000 lamports | Standard trading (default) |
| `fast` | ~10,000 - 500,000 lamports | Stop-loss exits, time-sensitive entries |
| `turbo` | ~100,000 - 1,000,000 lamports | Emergency exits, rug detection response |
