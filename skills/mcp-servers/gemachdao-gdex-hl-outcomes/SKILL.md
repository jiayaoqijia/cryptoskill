---
name: gdex-hl-outcomes
description: Hyperliquid HIP-4 outcome markets on GDEX — discover a market, pick a side, check spot collateral, place a limit order, track resting/fill state, cancel or exit (partial/full), and reconcile
---

# GDEX: Hyperliquid HIP-4 Outcome Markets

GDEX outcome markets are **Hyperliquid HIP-4 outcome markets**: each market has
two or more sides; each side is a token that trades at a probability price in
(0, 1), and the winning side settles on Hyperliquid. They are traded with spot
collateral (the market's `quoteToken`, USDC today) from the managed wallet's
**Hyperliquid spot balance**.

They are **not** HIP-3 builder perps, not perps, and not spot tokens. **GDEX has
no Polymarket or Kalshi integration.**

## When to Use

- "What prediction / outcome markets can I trade?" → discover
- Buy or sell one side of an outcome market
- Track a resting order, cancel it, or exit a position fully or partially
- Explain what happens when a market expires or resolves

## Prerequisites

- `@gemachdao/gdex-skill` installed and a managed-custody session — see
  **gdex-authentication**. You need `apiKey`, the **control** `walletAddress`
  used at sign-in, and `sessionPrivateKey`. The SDK and the MCP tools build
  and encrypt the payload for you; you don't need the backend ABI.
- The **managed** wallet address (outcome balances and orders live there).
- Quote collateral in the managed wallet's **HL spot** balance (step 3).

## Workflow

### 1. Discover

```typescript
const { markets } = await skill.getHlOutcomeMarkets({ state: 'active', query: 'BTC' });
```

MCP: `hl_outcomes` (`state`, `query`, `excludeFallback`, `limit` (default 20), `offset`, `sortBy: "volume" | "expiry"`, `detail`, `withVolume`). It returns compact pages; ask for `detail: true` only for the markets you will trade.
Each market is normalised:

| Field | Meaning | Source |
|---|---|---|
| `outcomeId` | Market id | `outcomeMeta.outcomes[].outcome` |
| `title` | Readable question built from the market parameters | `name` + `description` (`key:value\|…`), question parameters |
| `sides[]` | `{ sideIndex, label, rawName, coin, balanceCoin, assetId, exchangeAssetId, price }` | `sideSpecs[]`. `coin` = `#<token>` or `#<outcomeId*10+sideIndex>`. `balanceCoin` = `+<assetId>`. `price` = `allMids[coin]`. |
| `quoteToken` | Collateral currency | `outcomes[].quoteToken` |
| `state` | `active` · `pre_launch` (no mids yet) · `expired` (deadline passed, not yet settled) · `settled` | `questions[].settledNamedOutcomes`, the expiry parameter, `allMids` |
| `rules` | Price 0.00001–0.99999, tick 0.00001 (5 dp); whole-contract size; min notional 11 quote; full-position sell exempt; market orders ±5%; `reduceOnlyHonoured: false` | GDEX backend + gdex.pro (see Rules) |
| `settlement` | `claimViaGdex: false`, resolution source and deadline, and what to do | see "Expiry and settlement" |
| `volume24h` | Only with `withVolume`: `{ volume, asOf, source, coverage }`. `coverage` is `complete`, `partial` or `unavailable`. A zero that was actually read stays `0`; `null` means no reading. The wait is bounded (default 2.5 s), so a slow feed never blocks discovery. | Hyperliquid WS `activeAssetCtx.dayNtlVlm` |

`isFallback: true` marks the "none of the listed outcomes" leg of a
multi-outcome question.

### 2. Pick a side

Read `sides[].label`. **Don't assume side 0 is "Yes".**

- A match market's sides can be the two team names (`LOS` / `T1`).
- A question can have one market per candidate, each with its own Yes/No.

Select a side with exactly one of these:

- `coin` (e.g. `"#143151"`)
- `sideIndex`
- `sideLabel` (exact label)

The SDK rejects a coin that doesn't belong to `outcomeId`.

### 3. Check collateral

```typescript
const c = await skill.checkHlOutcomeCollateral({
  managedAddress, quoteToken: market.quoteToken, size: '120', price: '0.12',
});
// { available, required: 14.4, sufficient: true|false, ... }
```

MCP: `hl_outcome_check_collateral`.

- Buys draw on the managed wallet's HL **spot** balance of `quoteToken`
  (`total − hold`), not on the perp account.
- If it's short, move USDC from perp to spot or fund the account. See
  **gdex-perp-funding**.
- If a market is ever quoted in a token other than USDC, swap into it with
  `hl_swap_collateral` first.

### 4. Place a limit order

```typescript
const r = await skill.createHlOutcomeOrder({
  apiKey, walletAddress /* control */, sessionPrivateKey,
  outcomeId: 14315, sideLabel: 'Yes', isBuy: true,
  price: '0.12',   // probability, at most 5 decimals
  size: '120',     // whole contracts; 120 × 0.12 = 14.4 ≥ 11
});
// r.status: 'resting' (r.orderId) | 'filled' (r.filledSize, r.avgPrice) | 'rejected' (r.error)
```

MCP: `hl_create_outcome_order`.

- `isBuy: false` sells side tokens you hold. It can't short.
- `isMarket: true` takes the book at ±5% of the top level. Omit `price`
  (or pass `"0"`) for market orders.
- Pass `managedAddress` on sells. The SDK then checks the real position, and
  a sell of the whole position is allowed below the minimum.

### 5. Track resting and fill state

```typescript
const s = await skill.getHlOutcomeAccountState({ userAddress: managedAddress, outcomeId: 14315 });
```

MCP: `hl_outcome_account`. It returns:

- `positions[]`: `size`, `hold`, `available`, `avgEntryPrice`, `markPrice`,
  `value`, `unrealizedPnl`.
- `openOrders[]`: `orderId`, `price`, `size`, `originalSize`, `filledSize`,
  and `status` (`resting` or `partially_filled`).
- `fills[]`.
- `historicalOrders[]`, with Hyperliquid's status, e.g. `filled`, `canceled`,
  `minTradeNtlRejected`.

### 6. Cancel, or exit fully or partially

```typescript
await skill.cancelHlOutcomeOrder({ apiKey, walletAddress, sessionPrivateKey,
  outcomeId: 14315, coin: '#143150', orderId: String(r.orderId) });

// Full exit: omit size (the backend sells everything available).
await skill.closeHlOutcomeOrder({ apiKey, walletAddress, sessionPrivateKey,
  outcomeId: 14315, sideLabel: 'Yes', price: '0.15' });

// Partial exit: the sold part AND the remainder must each be worth ≥ 11.
await skill.closeHlOutcomeOrder({ apiKey, walletAddress, sessionPrivateKey,
  outcomeId: 14315, sideLabel: 'Yes', price: '0.15', size: '80', managedAddress });
```

MCP: `hl_cancel_outcome_order` and `hl_close_outcome_order`.

- `orderId` is the numeric Hyperliquid oid.
- A close is always a sell of held tokens.
- Any partial fill that happened before a cancel stays in the position.

### 7. Reconcile

Call `hl_outcome_account` again. Check that:

- a cancelled order has left `openOrders`;
- fills are in `fills`;
- `positions[].available` matches what you expect.

If a write's outcome is unknown, check here before you submit anything again.

## Rules (and where they come from)

- **Price** must be in (0, 1). The backend rounds to 5 decimals
  (`hyperLiquidOutcomes.ts:85-91`). The SDK rejects anything outside
  [0.00001, 0.99999] or with more than 5 decimals.
- **Size** is whole contracts (`OUTCOME_SIZE_DECIMALS = 0`,
  `hyperLiquidOutcomes.ts:69,185-188`).
- **Minimum order** is size × price ≥ **11** quote units. This is gdex.pro's
  rule (`HyperliquidOutcomeDetail.tsx:84`). Hyperliquid's own floor is 10. A
  sell of the full position is exempt. Partial closes must leave both legs at
  11 or more.
- **`reduceOnly`** is ignored: the backend always sends `r:false`.
- **Tick size and minimum order** aren't per-market fields in `outcomeMeta`.
  The rules above apply to every outcome market.

## Parameter modes

Every write accepts **either** the structured fields **or** a pre-built
`computedData` on its own. Never mix them.

- **Structured fields:** the SDK validates against the live market first.
- **Pre-built `computedData`:** posted as is, with no validation.

A mix of the two is rejected with `VALIDATION_ERROR` before anything is signed
or sent, as are missing structured fields. `dex` and `status` are not read by
the backend for outcomes.

## Expiry and settlement

- **`expired`:** the market's deadline has passed, but Hyperliquid hasn't
  marked it settled yet. The SDK refuses new orders. You can still try to
  exit with `hl_close_outcome_order`, but it may fail if the book has halted.
- **`settled`:** the outcome is listed in its question's
  `settledNamedOutcomes`. There is no book.
- **Settlement is done on Hyperliquid** by the market deployer (the
  `settleOutcome` and `settleQuestion` permissions in `outcomeMeta.deployers`).
- **GDEX has no claim, redeem or settle endpoint.** The backend's outcome
  routes are exactly: `outcomes`, `outcome_account`, `outcome/create_order`,
  `outcome/cancel_order`, `outcome/close_order`. After resolution there is
  nothing to claim through GDEX. Read the managed wallet's HL spot balances
  (`hl_outcome_account`) to see the result.

## Backend endpoints

| Method | Path | Notes |
|--------|------|-------|
| `GET`  | `/v1/hl/outcomes` | `{ meta: outcomeMeta, mids: allMids }`. Ignores query params. `outcomeMeta` is cached for 60 s. |
| `GET`  | `/v1/hl/outcome_account?address=<managed>&outcomeId=<id>` | positions (spot balances `+<assetId>`), openOrders, fills, historicalOrders |
| `POST` | `/v1/hl/outcome/create_order` | `{ computedData }` |
| `POST` | `/v1/hl/outcome/cancel_order` | `{ computedData }` |
| `POST` | `/v1/hl/outcome/close_order` | `{ computedData }` (always a sell) |
