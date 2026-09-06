# Agent Operations Guide

Complete reference for non-interactive CLI operations. Every command here is safe for agents — no prompts, no hangs.

## Interactive vs Non-Interactive Commands

### NEVER use these (interactive, will hang):
```
perp setup                       # interactive wizard — asks questions via stdin
perp init                        # alias for setup
perp wallet setup                # interactive wallet wizard
```

### ALWAYS use these (non-interactive, agent-safe):
```bash
perp --json wallet set <exchange> <key>     # set private key (or Aster API key)
perp --json wallet generate evm             # generate EVM wallet
perp --json wallet generate solana          # generate Solana wallet
perp --json wallet show                     # check configured wallets
perp --json wallet list                     # list named wallets
perp --json wallet balance                  # on-chain USDC balances
perp --json -e <EX> account balance         # exchange account balance
perp --json -e <EX> account positions       # open positions
perp --json -e <EX> market list             # available markets
perp --json -e <EX> trade market ...        # execute trade
perp --json -e <EX> trade buy ...           # alias for market buy
perp --json -e <EX> trade sell ...          # alias for market sell
perp --json risk status                     # risk assessment
perp --json risk liquidation-distance       # % from liquidation for all positions
perp --json risk limits                     # view/set risk limits
perp --json risk check --notional <$> --leverage <L>  # pre-trade risk check
```

**Rule: every command MUST include `--json`.** Without it, output is human-formatted and harder to parse.

## Zero to Trading: Complete Setup Flow

### Single Exchange Setup
```bash
# 1. Install
npm install -g perp-cli@latest
# or use npx -y perp-cli@latest as the prefix

# 2. Register wallet (user provides key)
perp --json wallet set hl 0xUSER_PRIVATE_KEY

# 3. Verify
perp --json wallet show
# → check "ok": true and address appears

# 4. Check balance
perp --json -e hl account balance
# → if balance is 0, tell user to deposit USDC

# 5. Ready to trade
perp --json -e hl market list
```

### Multi-Exchange Setup (for Funding Rate Arb)
To run arb, you need wallets on AT LEAST 2 exchanges. Each exchange needs:
- A configured wallet with a private key (or API key for Aster)
- USDC balance deposited on-exchange

```bash
# 1. Register wallets (any 2+ of: hl, pac, lt, aster)
perp --json wallet set hl 0xEVM_KEY
perp --json wallet set pac SOLANA_BASE58_KEY
perp --json wallet set lt 0xEVM_KEY          # may be the same EVM key as HL
perp --json wallet set aster <ASTER_API_KEY>

# 2. Verify
perp --json wallet show

# 3. Check balances (each exchange holds its own balance)
perp --json -e hl account balance
perp --json -e pac account balance
perp --json -e lt account balance
perp --json -e aster account balance

# 4. If one side needs funding, bridge USDC via funds bridge
perp --json funds bridge quote --from solana --to arbitrum --amount 500
# → show quote to user, get confirmation
perp --json funds bridge send --from solana --to arbitrum --amount 500
perp --json funds bridge status <orderId>     # wait for completion

# 5. Verify both sides have balance, then start arb
perp --json arb scan --min 5
```

### Lighter API Key Setup
Lighter uses a separate API key for trading. Two paths:

1. **Auto-setup (default)**: When `LIGHTER_PRIVATE_KEY` is set (env or `wallet set lt`), the CLI auto-generates and saves the API key on first use. Default index is 4 (indexes 0–3 are reserved by Lighter's frontend). Override with `LIGHTER_API_KEY_INDEX` env var. Valid range: 4–254.
2. **Managed agent (recommended for long-running agents)**: `perp wallet agent approve lighter --master <wallet> --api-key-index <slot>` registers a per-agent slot with explicit expiry tracking + 3-tier signer routing.

If auto-setup fails (e.g. transient network error), retry manually:
```bash
perp --json wallet agent approve lighter --master <wallet>
```

### Using the Same EVM Key for Multiple Exchanges
One EVM private key works for both Hyperliquid and Lighter:
```bash
perp --json wallet set hl 0xKEY
perp --json wallet set lt 0xKEY        # same key, different exchange binding
```

## Wallet Key Types

| Exchange | Chain | Key Format | Example |
|----------|-------|-----------|---------|
| Pacifica | Solana | Base58 string | `5KQwrPbwdL6PhXu...` |
| Hyperliquid | EVM (HyperEVM) | Hex with 0x prefix, 66 chars | `0x4c0883a69102937d...` |
| Lighter | EVM (Ethereum) | Hex with 0x prefix, 66 chars | `0x4c0883a69102937d...` |
| Aster | API key (BNB Chain) | Hex string | `3971f62b...` |

Aliases for exchange names:
- `pac` or `pacifica`
- `hl` or `hyperliquid`
- `lt` or `lighter`
- `aster`

## Deposit & Withdraw Flows

### Check On-Chain vs Exchange Balance
```bash
perp --json wallet balance               # on-chain USDC in your wallet
perp --json -e hl account balance        # USDC deposited on exchange
```

**On-chain balance ≠ exchange balance.** USDC in your wallet must be deposited to the exchange before trading.

### Deposit to Exchange (`funds deposit`)
```bash
# Hyperliquid (from Arbitrum wallet)
perp --json funds deposit hyperliquid 100

# Pacifica (from Solana wallet)
perp --json funds deposit pacifica 100

# Lighter (multiple routes)
perp --json funds deposit lighter info                # show all available routes
perp --json funds deposit lighter ethereum 100        # L1 direct (min 1 USDC)
perp --json funds deposit lighter cctp arbitrum 100   # via CCTP from Arbitrum (min 5 USDC)
```

### Withdraw from Exchange (`funds withdraw`)
```bash
perp --json funds withdraw hyperliquid 100
perp --json funds withdraw pacifica 100
perp --json funds withdraw lighter 100
```

### Internal Transfer (Hyperliquid)
```bash
perp --json funds transfer 100 <ADDRESS>     # instant HL→HL spot transfer
```

### Bridge Between Chains (`funds bridge`)
When you need to move USDC between chains (different networks):
```bash
# 1. Withdraw from source exchange to wallet
perp --json funds withdraw pacifica 500

# 2. Quote the bridge (auto-cheapest of cctp / relay / debridge)
perp --json funds bridge quote --from solana --to arbitrum --amount 500

# 3. Send (after user confirmation; pin --provider to override auto)
perp --json funds bridge send --from solana --to arbitrum --amount 500
perp --json funds bridge send --from solana --to arbitrum --amount 500 --provider cctp

# 4. Wait for completion
perp --json funds bridge status <orderId>

# 5. Deposit to destination exchange
perp --json funds deposit hyperliquid 500
```

### Inter-Exchange Rebalance (one command, end-to-end)
```bash
perp --json funds rebalance check                        # current distribution
perp --json funds rebalance plan                         # compute optimal moves
perp --json funds rebalance execute --auto-bridge        # withdraw → bridge → deposit
perp --json funds rebalance execute --withdraw-only      # only withdraw, manual rest
```

## Order Types & Execution

### Market Orders (immediate execution)
```bash
perp --json -e hl trade market BTC buy 0.01       # market buy
perp --json -e hl trade market BTC sell 0.01      # market sell
perp --json -e hl trade buy BTC 0.01              # shorthand
perp --json -e hl trade sell BTC 0.01             # shorthand
perp --json -e hl trade buy BTC 0.01 --smart      # IOC limit at best ask (less slippage)
```

### Split Orders (orderbook-aware, for large orders)
```bash
perp --json -e hl trade split BTC buy 5000        # split $5000 into depth-based slices
perp --json -e hl trade split BTC sell 10000 --max-slippage 0.5 --max-slices 5
perp --json -e hl trade market BTC buy 0.5 --split   # split via market command flag
```
Returns `{ slices[], filledUsd, avgPrice, totalSlippagePct, status }`.
Status: `complete` (all filled), `partial` (some filled), `failed` (none filled).

### Limit / Stop / TPSL
```bash
perp --json -e hl trade limit BTC buy 60000 0.01     # buy 0.01 BTC at $60k
perp --json -e hl trade stop BTC sell 0.01 58000     # stop sell at $58k
perp --json -e hl trade tpsl BTC long --tp 65000 --sl 58000
```

### Close / Reduce
```bash
perp --json -e hl trade close BTC                 # close entire position
perp --json -e hl trade close-all                 # close all positions on this exchange
perp --json -e hl trade flatten                   # cancel all orders + close all positions
perp --json -e hl trade reduce BTC 50             # reduce position by 50%
```

### Cancel Orders
```bash
perp --json -e hl account orders                  # list open orders
perp --json -e hl trade cancel BTC                # cancel by symbol
perp --json -e hl trade cancel <orderId>          # cancel specific order
perp --json -e hl trade cancel-all                # cancel all orders
perp --json -e hl trade cancel-stop BTC <stopId>  # cancel stop order
perp --json -e hl trade cancel-twap BTC <twapId>  # cancel TWAP order
```

### Pre-Flight Validation
ALWAYS run before executing a trade:
```bash
perp --json -e hl trade check BTC buy 0.01 --leverage 3
```
Returns estimated fees, slippage, and whether the trade is within risk limits.

> **Important:** `trade check` does NOT read the exchange-set leverage. Always pass `--leverage` explicitly so the cost estimate matches what the exchange will apply.

## Parsing JSON Output

Every command returns this envelope:
```json
{
  "ok": true,
  "data": { ... },
  "meta": { "timestamp": "2026-05-02T..." }
}
```

Error case:
```json
{
  "ok": false,
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "Not enough USDC",
    "retryable": false
  }
}
```

**Always check `ok` field first.** If `ok` is `false`, read `error.code` to decide next action. If `error.retryable` is `true`, wait 5 seconds and retry once.

## Idempotency & Safety

### Safe to retry (idempotent):
- `wallet show`, `wallet list`, `wallet balance` — read-only
- `account balance`, `account positions`, `account orders`, `account margin` — read-only
- `market list`, `market mid`, `market book`, `market info`, `market funding` — read-only
- `arb scan` (any mode), `arb status`, `arb history`, `arb config` — read-only
- `portfolio`, `risk status`, `risk liquidation-distance` — read-only
- `funds bridge quote`, `funds bridge status`, `funds rebalance check`, `funds rebalance plan` — read-only
- `funds info`, `funds deposit lighter info` — read-only

### NOT safe to retry blindly:
- `trade market`, `trade buy`, `trade sell`, `trade limit`, `trade tpsl` — will open duplicate positions
- `trade close`, `trade close-all`, `trade flatten` — usually safe (no-op when nothing to close), but verify
- `funds bridge send` — will send duplicate transfers
- `funds deposit *`, `funds withdraw *`, `funds transfer` — will move funds twice
- `arb exec`, `arb close`, `arb auto` — open/close real positions
- `funds rebalance execute` — orchestrated multi-leg movement

**For non-idempotent commands:** always verify the result before retrying. Check positions or balances to confirm whether the first attempt succeeded.

### Idempotency Key
Use `--client-id <unique>` on `trade market` to prevent duplicate orders. The CLI tracks recent client IDs and rejects duplicates.

## Symbol Naming Across Exchanges

Symbols are auto-resolved by the CLI. **Always use bare symbols** (e.g., `BTC`, `SOL`, `ICP`) — the CLI handles exchange-specific naming automatically:

| Input | Pacifica | Hyperliquid | Lighter | Aster |
|-------|----------|-------------|---------|-------|
| `ICP` | → `ICP` | → `ICP-PERP` | → `ICP` | → `ICP` |
| `BTC` | → `BTC` | → `BTC` | → `BTC` | → `BTC` |
| `SOL` | → `SOL` | → `SOL` | → `SOL` | → `SOL` |

- `arb scan` returns bare symbols — pass them directly to trade/leverage commands on any exchange.
- Do NOT manually add `-PERP` suffix — the CLI resolves this automatically.
- For HL spot+perp: BTC→`UBTC`, ETH→`UETH`, SOL→`USOL` are auto-resolved.

## Exchange-Specific Constraints

| Exchange | Min Order (notional) | Notes |
|----------|---------------------|-------|
| Pacifica | ~$1 (varies by symbol) | Lower minimums |
| Hyperliquid | **$10** | Rejects orders below $10 notional |
| Lighter | Varies by symbol | Check `market info` |
| Aster | Varies by symbol | BNB Chain, API key based |

**`trade check` is advisory only** — it returns `valid: true/false` but does NOT block execution. The exchange itself enforces minimums and will reject with an error if the order is too small.

## Common Agent Mistakes

1. **Using `perp setup` / `perp init` / `perp wallet setup`** — interactive, will hang forever. Use `wallet set` instead.
2. **Forgetting `--json`** — output becomes unparseable human text.
3. **Trading with zero balance** — check `account balance` first, tell user to deposit.
4. **Retrying a trade without checking** — leads to double positions. Always check `account positions` after a trade, even if it seemed to fail.
5. **Bridging without quoting** — always run `funds bridge quote` first to show the user fees and estimated time.
6. **Assuming deposit is instant** — after `funds bridge send`, wait for `funds bridge status` to confirm completion before depositing to the destination exchange.
7. **Manually adding `-PERP` suffix** — the CLI auto-resolves symbols. Just use bare names like `ICP`, `SOL`, `BTC`.
8. **Order below exchange minimum** — Hyperliquid requires $10+ notional. Compute `size × price` before submitting.
9. **Using legacy command names** — `arb rates`/`prices`/`dex`/`spot-exec`/`spot-close` are removed; use `arb scan --rates`/`--gaps`/`--hip3` and `arb exec spot:<exch>` / `arb close <SYM> --spot-exch <ex>` instead.
10. **Calling `trade check` without `--leverage`** — the CLI does not read exchange-set leverage, so cost estimates will be wrong.
