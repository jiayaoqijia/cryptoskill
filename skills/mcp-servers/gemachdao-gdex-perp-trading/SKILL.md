---
name: gdex-perp-trading
description: HyperLiquid perpetual futures — open/close positions, set leverage, place market and limit orders with TP/SL, edit or add TP/SL on open positions, and manage open orders
---

# GDEX: Perpetual Futures Trading (HyperLiquid)

Trade perpetual futures on HyperLiquid through GDEX managed-custody. Supports long/short positions, configurable leverage, take-profit/stop-loss, and market/limit orders.

## When to Use

- Opening or closing perp positions
- Setting leverage for an order
- Placing HL orders (market/limit) with TP/SL
- Moving, adding or removing a TP/SL on an open position; re-pricing a resting limit
- Querying positions, mark prices, or account state
- Canceling orders

## Prerequisites

- `@gemachdao/gdex-skill` installed
- Authenticated via `loginWithApiKey()` — see **gdex-authentication**
- USDC deposited to HyperLiquid — see **gdex-perp-funding**

## Open a Position (managed custody)

Perp orders go through `hlCreateOrder` after a managed sign-in. There is **no**
`openPerpPosition`/`setPerpLeverage` — those don't exist (closing has
`closePerpPosition`, below). The real flow:

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gemachdao/gdex-skill';
// ... do the managed sign-in (see gdex-authentication) to get sessionPrivateKey ...
const creds = { apiKey, walletAddress: controlAddress, sessionPrivateKey };

const res = await skill.hlCreateOrder({
  coin: 'ETH',           // 'BTC'|'ETH'|'SOL'… or a builder market 'xyz:NVDA' (lowercase dex prefix)
  isLong: true,
  price: String(mark),   // market: the mark price ('0' fetches it); the back-end adds its own 5% bound
  size: '0.05',          // size in CONTRACTS (coin units), not USD; min order value $11
  isMarket: true,
  tpPrice: String(tp),   // '' to skip — set both or neither
  slPrice: String(sl),   // '' to skip
  leverage: 3,           // ALWAYS pass it; see below
  ...creds,
});
// res: { isSuccess: true } — no order id; read open orders to get one
```

**Leverage** is sent as a top-level `leverage` field with the order, and that is
the only way to set it: the back-end updates the market's leverage just before
placing the order. The range is 1 up to **that market's own maximum** (a higher
value is clamped to the maximum). **Omitted, the back-end applies the market's
maximum** — on reduce-only orders too — so pass it on every `hlCreateOrder`.
`hlUpdateLeverage` always throws: there is no `/hl/update_leverage` route.

**Cross vs isolated** is decided by the back-end, not the caller: builder-dex
markets (`dex:ASSET`) and isolated-only assets are isolated, everything else is
cross. `marginMode` is not sent.

**TP/SL on the order** attach only as a pair and become market triggers.

### Limit entry and the mark rule

```typescript
await skill.hlCreateOrder({ coin: 'ETH', isLong: true, price: '3100', size: '0.05',
  isMarket: false, leverage: 3, ...creds });
```

A limit that would fill at once is refused: a long limit at or above the mark,
or a short limit at or below it ("would execute immediately at the current mark
price"). Use a market order for that. `getHlMarkPrice(coin)` returns the mark
(HyperLiquid `markPx`, read from the market's own dex), not the order-book mid.

### Percent TP/SL (how gdex.pro maps % to price)

gdex.pro's percentages are return on margin (ROE), so they scale with leverage:
`price = base × (1 ± pct / leverage / 100)` — `+` for a long's TP and a short's
SL, `−` for a long's SL and a short's TP. A 30% TP on a 10× long from 100 is
`100 × (1 + 30/10/100) = 103`.

## Close a Position

Prefer `closePerpPosition`: it reads the live position (dex-scoped
clearinghouse state, signed `szi`) and picks the side for you — a long closes
with a sell, a short with a buy. Omit `size` for a full close; a larger `size`,
a flat position, or a bare coin open on several builder dexes is rejected.
`positionAddress` is the address whose HL account holds the position (the
managed wallet; defaults to `walletAddress`).

```typescript
const r = await skill.closePerpPosition({ ...creds, coin: 'xyz:TSLA', positionAddress: managedAddress });
// r: { closeSide: 'buy' | 'sell', size, positionSize, remainingSize, order, ... }
```

It closes **at market**, the way the gdex.pro Close button does (`/hl/place_order`):
the back-end reads the live position, sends a reduce-only IOC at its own mark
±5%, and leaves leverage and margin mode alone. `hlClosePosition({ coin, size })`
is the same call without the position check. A **partial close must leave at
least $11** of position, otherwise close it all.

**Limit close** (rest a reduce-only limit, e.g. a manual take-profit): use
`hlCreateOrder` with `reduceOnly: true, isMarket: false`, the opposite side, and
the position's current leverage:

```typescript
await skill.hlCreateOrder({ coin: 'ETH', isLong: false, price: '3600', size: String(positionSize),
  reduceOnly: true, isMarket: false, leverage: positionLeverage, ...creds });
```

> `hlPlaceOrder` is **not** a limit order. `/hl/place_order` only closes: it
> rejects non-reduce-only orders, ignores `price` and `isLong`, and closes
> `size` at market. The SDK method is a deprecated alias that requires
> `reduceOnly: true`.

## Edit, Add or Remove TP/SL on an Open Position

Order ids come from open orders: `getHlOpenOrdersForCopy({ userAddress: managedAddress, dex })`
(TP/SL show as trigger orders, possibly under a parent's `children`).

```typescript
// Move a stop or target: send the new trigger. HL replaces the order — keep retData.orderId.
const m = await skill.hlModifyOrder({ coin: 'ETH', orderId: slOrderId, triggerPrice: '3150', ...creds });
// m.retData: { previousOrderId, orderId, status, price, size, triggerPrice, triggerType: 'tp' | 'sl' }

// Re-price a resting limit (entry or limit close): send price. Size changes with `size`.
await skill.hlModifyOrder({ coin: 'ETH', orderId: limitOrderId, price: '3080', ...creds });

// Add a missing TP and/or SL to an open position (market triggers, whole position).
const a = await skill.hlAddPositionTpsl({ coin: 'ETH', tpTriggerPrice: '3600', slTriggerPrice: '3150', ...creds });
// a.retData.createdOrders: [{ triggerType, orderId, triggerPrice, ... }]

// Remove a TP or SL: cancel its order.
await skill.hlCancelOrder({ coin: 'ETH', orderId: tpOrderId, ...creds });
```

- `hlModifyOrder`: fields left out keep their value; give at least one of
  `price`, `size`, `triggerPrice`. `triggerPrice` is for TP/SL orders only. A
  non-reduce-only limit cannot be moved to or through the mark.
- `hlAddPositionTpsl` only adds. A side that already has a trigger is refused
  (code 409, "use modify_order"); no open position is code 102. The TP must be
  on the profit side of the mark and the SL on the loss side.
- Refusals arrive as `GdexApiError` (HTTP 400); the back-end's body is on
  `err.responseBody`. After an unclear result, read open orders before retrying.

## Builder / HIP-3 markets (stocks, commodities)

Builder-dex assets are named `dex:ASSET` with a **lowercase** dex prefix
(`xyz:NVDA`, `xyz:SPCX`, `flx:OIL`). Pass the coin in that exact form (the SDK
normalizes casing). They trade through the same `hlCreateOrder` flow as default
markets, are always **isolated**, and open at the `leverage` you pass, clamped to
the asset's maximum (omitted: the asset's maximum).

**Collateral depends on the dex.** The `xyz` stock/commodity perps are
**USDC-collateralized and 24-hour** — no collateral swap needed; trade them with
your existing HL USDC. Only dexes that settle in a different token (e.g. HYNA →
USDE) need `hlSwapCollateral` first. The account must be a **unified account**
(`hlEnableTrading`) to share margin across dexes.

**Reading builder positions is dex-scoped.** A `xyz:NVDA` position lives under the
`xyz` dex's isolated account, **not** the default clearinghouse — query
`getHlClearinghouseState({ userAddress, dex: 'xyz' })`. The default query (and
`getHlClearinghouseStateAll`, which omits `xyz`) returns it empty, which looks
like "the order never filled" when it actually did.

## Query Positions & Account State

Positions live on the **managed** EVM wallet (from sign-in / `getManagedUser`), so
reads take that address; writes take the control wallet.

```typescript
// Get open positions
const positions = await skill.getPerpPositions({
  walletAddress: managedEvmAddress,
  coin: 'BTC',   // optional filter
});
// Each: { coin, side, size, entryPrice, markPrice, leverage, unrealizedPnl, liquidationPrice }

// Full account state
const state = await skill.getHlAccountState(managedEvmAddress);
// { accountValue, totalNtlPos, totalRawUsd, totalMarginUsed, withdrawable, positions[] }

// Mark price (HyperLiquid markPx, not the mid); builder markets as 'xyz:NVDA'
const price = await skill.getHlMarkPrice('BTC');
```

## Place Orders (HL Managed-Custody)

### Market Order with TP/SL

```typescript
await skill.hlCreateOrder({
  coin: 'ETH',
  isLong: true,
  price: '0',       // '0' on a market order = the SDK fetches the mark price
  size: '0.5',      // position size
  reduceOnly: false,
  isMarket: true,
  tpPrice: '4000',  // take-profit (optional, with slPrice)
  slPrice: '3200',  // stop-loss (optional, with tpPrice)
  leverage: 5,
  apiKey,
  walletAddress,
  sessionPrivateKey,
});
```

### Limit Order (no TP/SL)

```typescript
await skill.hlCreateOrder({
  coin: 'SOL',
  isLong: false,     // short
  price: '180',      // limit price — must be above the mark for a short entry
  size: '10',
  isMarket: false,
  leverage: 5,
  apiKey,
  walletAddress,
  sessionPrivateKey,
});
```

## Cancel Orders

```typescript
// Cancel specific order
await skill.hlCancelOrder({
  coin: 'BTC',
  orderId: '12345',
  apiKey,
  walletAddress,
  sessionPrivateKey,
});

// Cancel all orders
await skill.hlCancelAllOrders({
  apiKey,
  walletAddress,
  sessionPrivateKey,
});
```

## Close All Positions

> **WARNING:** The `hlCloseAll` / `/v1/hl/close_all_positions` endpoint is unreliable — it frequently returns `TIMEOUT` or JSON parse errors from the backend. **Close per coin with `closePerpPosition`** (see below).

```typescript
// ❌ Unreliable — may timeout
await skill.hlCloseAll({
  apiKey,
  walletAddress,   // MUST be control address, not managed address
  sessionPrivateKey,
});

// ✅ Reliable — close one coin; side and size come from the live position
await skill.closePerpPosition({ coin: 'BTC', positionAddress: managedEvmAddress, apiKey, walletAddress, sessionPrivateKey });
```

## HL ABI Schemas (Critical)

HL operations use a **different crypto pipeline** than spot trades. Getting any detail wrong produces `400 Unauthorized (code 103)`.

| Action | ABI Types | Fields |
|--------|-----------|--------|
| `hl_deposit` | `['uint64', 'address', 'uint256', 'string']` | `[chainId, tokenAddress, amount, nonce]` |
| `hl_withdraw` | `['string', 'string']` | `[amount, nonce]` |
| `hl_create_order` | `['string', 'bool', 'string', 'string', 'bool', 'string', 'string', 'string', 'bool']` | `[coin, isLong, price, size, reduceOnly, nonce, tpPrice, slPrice, isMarket]` |
| `hl_place_order` (close at market) | `['string', 'bool', 'string', 'string', 'bool', 'string']` | `[coin, isLong, price, size, reduceOnly, nonce]` |
| `hl_modify_order` | `['string', 'string', 'string', 'string', 'string', 'string']` | `[nonce, coin, orderId, price, size, triggerPrice]` |
| `hl_add_position_tpsl` | `['string', 'string', 'string', 'string', 'string', 'bool', 'string', 'string', 'bool']` | `[nonce, coin, size, tpTriggerPrice, tpPrice, tpIsMarket, slTriggerPrice, slPrice, slIsMarket]` |
| `hl_close_all` | `['string']` | `[nonce]` |
| `hl_cancel_order` | `['string', 'string', 'string']` | `[nonce, coin, orderId]` |
| `hl_cancel_all_orders` | `['string']` | `[nonce]` |

`leverage` is not part of any signed payload: it is a top-level field of the `create_order` request body.

**CRITICAL:** `hl_deposit` chainId is `uint64`, NOT `uint256`. This is the #1 cause of Unauthorized errors. The backend re-encodes with `uint64` for signature verification — if you encode with `uint256`, the hex differs and you get code 103.

## HL Managed-Custody Credentials

All HL write operations require `HlManagedCredentials`:

```typescript
interface HlManagedCredentials {
  apiKey: string;            // GDEX API key for AES encryption
  walletAddress: string;     // CONTROL wallet address (from sign-in), NOT managed address
  sessionPrivateKey: string; // Session key from sign-in flow
}
```

## Default HL Assets

BTC, ETH, SOL, DOGE, AVAX, APE, APT, ARB, ATOM, BCH, BLUR, BNB, COMP, CRV, DOT, EOS, FIL, FTM, HBAR, ICP, IMX, INJ, JUP, KPEPE, LDO, LINK, LTC, MATIC, MKR, NEAR, OP, ORDI, PEPE, PYTH, RNDR, RUNE, SEI, SHIB, SNX, STX, SUI, TIA, TON, TRX, UNI, WIF, WLD, XRP

## Critical: walletAddress Must Be Control Address

**The #1 cause of `400 Unauthorized (code 103)` on HL operations is passing the wrong `walletAddress`.**

- During sign-in, the session key is registered against your **control wallet address** (e.g., `0x53D0...2eD`).
- The backend returns a **managed address** (e.g., `0x9967...0f`) that holds the actual funds.
- All HL write operations sign the message as `{action}-{walletAddress}-{data}`, and the backend verifies the signature against the session key registered for that address.
- If you pass the managed address, the signature verification fails → code 103.

```typescript
// ❌ WRONG — causes 400 Unauthorized (code 103)
const creds = { apiKey, walletAddress: managedAddress, sessionPrivateKey };

// ✅ CORRECT — use the control wallet address from sign-in
const creds = { apiKey, walletAddress: controlAddress, sessionPrivateKey };
```

## Related Skills

- **gdex-authentication** — Auth setup required for all HL operations
- **gdex-perp-funding** — Deposit/withdraw USDC to HyperLiquid
- **gdex-portfolio** — View positions and P&L

## Autonomous Agent Notes (Live-Tested)

### Endpoints That Don't Work

| Endpoint | Status | What to Do |
|----------|--------|------------|
| `hlCloseAll` / `/v1/hl/close_all_positions` | Returns TIMEOUT or 400 | Close per coin with `closePerpPosition` |
| `hlUpdateLeverage` / `/v1/hl/update_leverage` | No such route; the SDK method throws | Pass `leverage` on `hlCreateOrder` (sent top-level with the order) |
| `hlPlaceOrder` as a limit order | `/hl/place_order` only closes at market | `hlCreateOrder` with `isMarket: false` |
| `getGbotUsdcBalance` | Returns 404 | Use `getHlAccountState()` or clearinghouse state to check balance |

### Close Position Reliably (Live-Tested)

```typescript
// Positions are read from the MANAGED wallet; the close is signed with the CONTROL wallet.
const positions = await skill.getPerpPositions({ walletAddress: managedEvmAddress });

for (const pos of positions) {
  // Reads the live side/size and closes at market (the gdex.pro Close button)
  await skill.closePerpPosition({
    coin: pos.coin,
    positionAddress: managedEvmAddress,
    apiKey,
    walletAddress: controlAddress,   // MUST be control address
    sessionPrivateKey,
  });
}
```

### HL Deposit Minimum

- **Minimum deposit: 10 USDC** (10000000 in smallest unit)
- Managed wallet must hold `amount × 1.01` (1% fee buffer)
- Delivery takes ~10 minutes after Arbitrum tx confirms

### Leverage and Position Sizing

- Set leverage per order with `leverage` on `hlCreateOrder` (MCP: `open_perp_position`); it is sent as a
  top-level field with the order. Omitted, the back-end applies the market's maximum, so always pass it.
- `hlUpdateLeverage` (MCP: `set_leverage`) always errors — there is no `/hl/update_leverage` route.
- **Effective leverage** = position notional value / account equity, so size positions with that in mind.

### Critical Checks Before Opening a Position

1. Verify USDC is deposited on HL (use `getHlAccountState()`)
2. Use **control** wallet address (not managed) for all write operations
3. Generate a fresh nonce for every order
4. For market orders: set `isMarket: true` and pass the mark price (`'0'` is resolved to the mark price by the SDK)
5. Pass `''` for `tpPrice` / `slPrice` to skip TP/SL. Set both or neither: the backend drops a lone TP or SL (add one later with `hlAddPositionTpsl`)
6. Prices and sizes are plain positive decimals (no exponent). Pass `szDecimals` (HL meta) to also check Hyperliquid precision before signing: size up to `szDecimals` decimals; limit/TP/SL prices up to 5 significant figures and `6 - szDecimals` decimals. Without it the backend rounds instead of rejecting
7. Reuse the session. Sign-in is limited to 10 per 15 minutes per account (30 per IP): sign in once, keep `sessionPrivateKey`, and carry the session across processes with `getBrowserSession()` / `setBrowserSession()` + `setSessionSigningKey()` instead of signing in per call
