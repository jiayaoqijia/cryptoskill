# Stacks L2 DeFi

Stacks is a Bitcoin L2 with smart contracts. This reference covers STX transfers, DEX swaps, lending protocols, and x402 paid endpoints.

## STX Transfers

Transfer STX tokens to any Stacks address:

```
"Send 2 STX to ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
```

Uses `transfer_stx` - amounts in micro-STX (1 STX = 1,000,000 micro-STX).

For gasless transfers (wallet has 0 STX), use `sponsored: true`:

```
"Send 2 STX to ST1... with sponsored=true"
```

Relay at x402-relay.aibtc.com covers the STX fee. Requires `SPONSOR_API_KEY` env var.

Check STX balance:

```
"What's my STX balance?"
```

Uses `get_stx_balance`.

## sBTC Bridge

sBTC is Bitcoin wrapped on Stacks L2. You can deposit BTC to receive sBTC, or withdraw sBTC back to BTC.

### Deposit BTC to Get sBTC

Deposit Bitcoin L1 to receive sBTC on Stacks L2:

```
"Deposit 0.001 BTC to get sBTC"
"Deposit 100000 sats with fast fees"
```

Uses `sbtc_deposit` - builds a Bitcoin Taproot deposit transaction:
- Amount in satoshis (1 BTC = 100,000,000 satoshis)
- Fee rate: "fast", "medium", "slow", or custom sat/vB
- Max signer fee: Maximum fee sBTC signers can charge (default: 80,000 sats)
- Reclaim lock time: Bitcoin blocks until reclaim available (default: 950 blocks ≈ 6.6 days)

### Check Deposit Status

Track your deposit progress:

```
"Check my deposit status for txid abc123"
```

Uses `sbtc_deposit_status` - queries Emily API for deposit processing status.

### Get Deposit Address

Get instructions for manual deposits (advanced):

```
"How do I deposit BTC for sBTC?"
"Show me my sBTC deposit address"
```

Uses `sbtc_get_deposit_info` - returns deposit address when wallet is unlocked.

### Transfer sBTC

Send sBTC to any Stacks address:

```
"Send 0.001 sBTC to ST1..."
"Transfer 100000 sats of sBTC with high fee"
```

Uses `sbtc_transfer` - 8 decimals, amount in satoshis.

### Check Balance

View sBTC holdings:

```
"What's my sBTC balance?"
```

Uses `sbtc_get_balance`.

### sBTC Tool Reference

| Tool | Description |
|------|-------------|
| `sbtc_deposit` | Deposit BTC to receive sBTC |
| `sbtc_deposit_status` | Check deposit status |
| `sbtc_get_deposit_info` | Get deposit address/instructions |
| `sbtc_get_balance` | Check sBTC balance |
| `sbtc_transfer` | Send sBTC to address |
| `sbtc_get_peg_info` | Get peg ratio and supply |

## Units & Decimals (Bitflow / DeFi)

All Bitflow tools accept an `amountUnit` parameter that controls how `amountIn` is interpreted.

### Quick Reference

| Token | Decimals | 1 human unit | Base units |
|-------|----------|-------------|------------|
| STX   | 6        | `1`         | `1000000`  |
| sBTC  | 8        | `1`         | `100000000`|

**Default is `"human"` (frontend-style).** Pass `amountUnit: "base"` only when you already have a raw integer from on-chain data.

### Human vs Base Examples

| What you want to swap | amountUnit | amountIn     |
|----------------------|------------|--------------|
| 2 STX                | `"human"`  | `"2"`        |
| 2 STX (base)         | `"base"`   | `"2000000"`  |
| 0.00000794 sBTC      | `"human"`  | `"0.00000794"` |
| 794 sats of sBTC     | `"base"`   | `"794"`      |

### bitflow_get_quote Example

Get a quote for swapping 2 STX to sBTC:

```
# Human units (default) — "2 STX"
bitflow_get_quote(tokenX="token-stx", tokenY="token-sbtc", amountIn="2")

# Equivalent in base units — "2000000 micro-STX"
bitflow_get_quote(tokenX="token-stx", tokenY="token-sbtc", amountIn="2000000", amountUnit="base")
```

Both calls produce the same quote. The server converts base to human internally.

### bitflow_swap Example

Swap 2 STX for sBTC:

```
# Human units (default)
bitflow_swap(tokenX="token-stx", tokenY="token-sbtc", amountIn="2")

# Equivalent in base units
bitflow_swap(tokenX="token-stx", tokenY="token-sbtc", amountIn="2000000", amountUnit="base")
```

### WARNING: Double-Scaling Error

The most common mistake is passing a value that has already been scaled to base units while leaving `amountUnit` at the default `"human"`.

**Wrong — double-scaled:**
```
# WRONG: "2000000" interpreted as 2,000,000 STX (human), which becomes
# 2,000,000,000,000 micro-STX internally — 1 million times too large!
bitflow_swap(tokenX="token-stx", tokenY="token-sbtc", amountIn="2000000")
```

**Correct — either of these:**
```
# Option A: pass the human amount directly
bitflow_swap(tokenX="token-stx", tokenY="token-sbtc", amountIn="2")

# Option B: pass base units with the flag
bitflow_swap(tokenX="token-stx", tokenY="token-sbtc", amountIn="2000000", amountUnit="base")
```

**Rule of thumb:** If your number looks like a raw integer from a balance query or on-chain read, set `amountUnit: "base"`. If it looks like what a human would type (e.g. "2", "0.5"), use the default.

---

## ALEX DEX (Mainnet Only)

Decentralized exchange for token swaps on Stacks.

### Discover Pools

Find available trading pairs:

```
"What pools are available on ALEX?"
```

Uses `alex_list_pools` - shows all tradable token pairs.

### Get Quote

Check expected output before swapping:

```
"How much ALEX for 10 STX?"
```

Uses `alex_get_swap_quote` with token symbols (STX, ALEX, etc).

### Execute Swap

Swap tokens:

```
"Swap 0.1 STX for ALEX"
```

Uses `alex_swap` - handles routing, wrapping, and post-conditions automatically.

### ALEX Tool Reference

| Tool | Description |
|------|-------------|
| `alex_list_pools` | List all trading pools |
| `alex_get_swap_quote` | Get expected output |
| `alex_swap` | Execute token swap |
| `alex_get_pool_info` | Get pool reserves |

## Bitflow DEX (Mainnet Only)

DEX aggregator that routes trades across multiple liquidity sources on Stacks.

See [Units & Decimals](#units--decimals-bitflow--defi) above for amount handling.

### Get Quote

Check expected output before swapping:

```
"Get a Bitflow quote for 2 STX to sBTC"
```

Uses `bitflow_get_quote` with token IDs (`token-stx`, `token-sbtc`, etc).

### Execute Swap

Swap tokens:

```
"Swap 2 STX for sBTC on Bitflow"
```

Uses `bitflow_swap` — finds the best route automatically. Requires an unlocked wallet.

### Bitflow Tool Reference

| Tool | Description |
|------|-------------|
| `bitflow_get_ticker` | Get market data (no API key needed) |
| `bitflow_get_tokens` | List available swap tokens |
| `bitflow_get_swap_targets` | Get possible output tokens for a given input |
| `bitflow_get_routes` | Get all routes between two tokens |
| `bitflow_get_quote` | Get swap quote with price impact |
| `bitflow_swap` | Execute token swap |

## Zest Protocol (Mainnet Only)

Lending and borrowing protocol for earning yield on assets.

### Supported Assets

| Symbol | Description |
|--------|-------------|
| sBTC | Wrapped Bitcoin |
| aeUSDC | Bridged USDC |
| stSTX | Staked STX |
| wSTX | Wrapped STX |
| USDH | Stablecoin |
| sUSDT | Bridged USDT |
| USDA | Arkadiko stablecoin |
| DIKO | Arkadiko governance token |
| ALEX | ALEX token |
| stSTX-BTC | Staked STX/BTC LP |

### Check Position

View your lending position:

```
"What's my Zest position for stSTX?"
```

Uses `zest_get_position` with asset symbol.

### Supply Assets

Deposit to earn interest:

```
"Supply 1000 stSTX to Zest"
```

Uses `zest_supply` - amounts in smallest units (check decimals per asset).

### Borrow Assets

Borrow against collateral:

```
"Borrow 100 aeUSDC from Zest"
```

Uses `zest_borrow` - ensure sufficient collateral first.

### Repay Loan

Repay borrowed assets:

```
"Repay 50 aeUSDC on Zest"
```

Uses `zest_repay`.

### Withdraw Assets

Withdraw supplied assets:

```
"Withdraw 500 stSTX from Zest"
```

Uses `zest_withdraw`.

### Zest Tool Reference

| Tool | Description |
|------|-------------|
| `zest_list_assets` | List supported assets |
| `zest_get_position` | Check supply/borrow |
| `zest_supply` | Deposit assets |
| `zest_withdraw` | Withdraw assets |
| `zest_borrow` | Borrow assets |
| `zest_repay` | Repay loan |

## x402 Protocol

Pay-per-use APIs with automatic micropayments. The agent handles HTTP 402 payment challenges automatically.

### API Services

Three complementary x402 API services are available:

#### STX402 Directory (stx402.com)

Meta layer for the x402 ecosystem:

| Category | Endpoints |
|----------|-----------|
| **Registry** | `/registry/list`, `/registry/probe`, `/registry/register` |
| **Agent Identity** | `/agent/info`, `/agent/lookup`, `/agent/metadata` |
| **Reputation** | `/agent/reputation/summary`, `/agent/reputation/feedback` |
| **Links** | `/links/create`, `/links/stats`, `/links/expand/{slug}` |

[API Docs](https://stx402.com/docs) · [Guide](https://stx402.com/guide) · [Toolbox](https://stx402.com/toolbox)

#### x402 AIBTC API (x402.aibtc.com)

Utility services for agents:

| Category | Endpoints |
|----------|-----------|
| **Inference** | `/inference/openrouter/chat`, `/inference/cloudflare/chat` |
| **Stacks** | `/stacks/address`, `/stacks/decode`, `/stacks/profile` |
| **Hashing** | `/hashing/sha256`, `/hashing/keccak256`, `/hashing/hash160` |
| **Storage** | `/storage/kv/*`, `/storage/paste/*`, `/storage/db/*`, `/storage/memory/*` |

[API Docs](https://x402.aibtc.com/docs) · [Staging](https://x402.aibtc.dev)

#### x402 Biwas API (x402.biwas.xyz)

DeFi analytics and market data:

| Category | Endpoints |
|----------|-----------|
| **Pools** | `/api/pools/trending`, `/api/pools/all` |
| **Market Data** | `/api/tokens/prices`, `/api/tokens/trending` |
| **Wallet Analysis** | `/api/wallet/holdings`, `/api/wallet/history` |
| **Security** | `/api/security/audit`, `/api/security/score` |

[API Docs](https://x402.biwas.xyz/docs)

### Usage

Discover endpoints:

```
"List x402 endpoints for inference"
"What storage APIs are available?"
```

Execute endpoint:

```
"Chat with Claude via x402"
"Store this data in x402 KV"
```

Uses `list_x402_endpoints` to discover, `probe_x402_endpoint` to check cost, `execute_x402_endpoint` to call.

### Payment

- **Tokens**: STX, sBTC, USDCx
- **Pricing**: Standard tier (~0.001 STX) or dynamic (LLM pass-through + 20%)
- **Safe by default**: `execute_x402_endpoint` now probes first (returns cost), requires `autoApprove: true` to pay. Free endpoints work transparently.

### Two-Phase Workflow

For paid endpoints, use a probe-before-pay pattern to prevent sBTC loss:

1. **Probe**: Call `probe_x402_endpoint` with endpoint details → returns cost (amount, asset, recipient)
2. **Present**: Show cost to user for approval
3. **Execute**: Call `execute_x402_endpoint` with `autoApprove: true` to pay and get response

Alternatively, call `execute_x402_endpoint` without `autoApprove` (default `false`) — it probes first and returns cost, then re-call with `autoApprove: true` to pay.

### x402 Tool Reference

| Tool | Description |
|------|-------------|
| `list_x402_endpoints` | Discover APIs by source/category |
| `probe_x402_endpoint` | Check cost without paying (never executes payment) |
| `execute_x402_endpoint` | Call endpoint (safe mode by default, use autoApprove: true to pay) |
| `scaffold_x402_endpoint` | Generate x402 API project |
| `scaffold_x402_ai_endpoint` | Generate x402 AI API project |

## Smart Contract Calls

Call any Stacks smart contract:

```
"Call get-balance on token contract"
```

Uses `call_contract` for write operations, `call_read_only_function` for read-only.

For gasless contract calls or deployments (wallet has 0 STX), use `sponsored: true`:

```
"Call transfer on my contract with sponsored=true"
"Deploy my contract with sponsored=true"
```

Relay at x402-relay.aibtc.com covers the STX fee. Requires `SPONSOR_API_KEY` env var.

### Contract Tool Reference

| Tool | Description | Parameters |
|------|-------------|------------|
| `call_contract` | Call contract function (signs tx) | `contractAddress`, `contractName`, `functionName`, `functionArgs`, `postConditionMode`, `postConditions` (optional), `fee` (optional), `sponsored` (optional, default false) |
| `call_read_only_function` | Read-only call (no signing) | `contractId`, `functionName`, `functionArgs`, `senderAddress` (optional) |
| `deploy_contract` | Deploy Clarity contract | `contractName`, `codeBody`, `fee` (optional), `sponsored` (optional, default false) |
| `get_contract_info` | Get contract ABI | `contractId` |
| `get_transaction_status` | Check tx status | `txid` |

## Gasless Transactions (Sponsored)

Agents with 0 STX can execute transactions via the sponsor relay at x402-relay.aibtc.com. The relay signs as fee sponsor and pays the STX gas fee on behalf of the sender.

**Supported tools**: `transfer_stx`, `call_contract`, `deploy_contract`

**Setup**: Set `SPONSOR_API_KEY` environment variable (or wallet-level `sponsorApiKey`) before using sponsored mode.

**Usage pattern**:
1. Add `sponsored: true` to any supported tool call
2. The tool builds a sponsored transaction (fee=0) and submits it to the relay
3. Relay broadcasts the fee-sponsored transaction and returns the txid

**Note**: The `fee` parameter is ignored when `sponsored: true` — the relay determines and pays the fee.

## More Information

- [Stacks Docs](https://docs.stacks.co)
- [ALEX DEX](https://alexgo.io)
- [Zest Protocol](https://zestprotocol.com)
- [x402 Protocol](https://www.x402.org)
- [STX402 Docs](https://stx402.com/docs)
- [x402 AIBTC Docs](https://x402.aibtc.com/docs)
- [CLAUDE.md DeFi Sections](../../CLAUDE.md#defi---alex-dex-mainnet-only)

---

*Back to: [SKILL.md](../SKILL.md)*
