---
name: gdex-hl-outcomes
description: HyperLiquid HIP-3 outcome / event markets — list markets, place outcome orders, and manage outcome positions
---

# GDEX: HyperLiquid Outcomes (HIP-3 Event Markets)

Trade discrete-outcome event markets running on HyperLiquid HIP-3 permissioned
perp DEXes. These are prediction-market-style instruments where each market
resolves to a discrete outcome rather than a continuous price.

## When to Use

- Listing the currently open / resolved outcome markets
- Getting an account state on an outcomes perp dex
- Opening, cancelling, or closing positions on an outcome market

## Prerequisites

- `@gemachdao/gdex-skill` installed
- Authenticated via managed custody — see **gdex-authentication**
- Trading enabled on HL (one-time `/v1/hl/enable_trading`) — see
  **gdex-perp-trading** for the HIP-3 setup flow
- For write operations: a pre-built `computedData` payload built by the
  caller using the standard managed-custody encrypted-payload contract
  (ABI schemas for outcome actions live in
  `src/api/services/ServiceHyperLiquid.ts` of the backend)

## Backend Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/v1/hl/outcomes` | List outcome markets |
| `GET`  | `/v1/hl/outcome_account` | Account state on outcomes dex |
| `POST` | `/v1/hl/outcome/create_order` | Open an outcome order |
| `POST` | `/v1/hl/outcome/cancel_order` | Cancel an outcome order |
| `POST` | `/v1/hl/outcome/close_order` | Close an outcome position |

All read endpoints accept an optional `dex` query parameter to target a
specific HIP-3 perp dex registered via `/v1/hl/perp_dexes`.

## SDK Usage

The SDK builds the encrypted payload for you — pass structured params plus
managed-custody credentials (`apiKey`, `walletAddress` = your **control**
address from sign-in, `sessionPrivateKey`). A pre-built `computedData` is
still accepted for advanced callers.

```typescript
import { GdexSkill } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(process.env.GDEX_API_KEY!);

// 1. List markets. Each `mids` key is a coin id: "#<outcomeId><sideIndex>",
//    e.g. "#1010" = outcome 101 / side 0 (Yes), "#1011" = side 1 (No).
const markets = await skill.getHlOutcomes({ status: 'open' });

// 2. Enable trading once before the first outcome order (see Prerequisites).
await skill.hlEnableTrading({ apiKey, walletAddress, sessionPrivateKey });

// 3. Account state for one market (outcomeId is REQUIRED).
const state = await skill.getHlOutcomeAccount({
  userAddress: managedAddress,   // the managed wallet holds outcome balances
  outcomeId: 101,
});

// 4. Place an order. price is a probability in [0,1]; size is in contracts.
const order = await skill.createHlOutcomeOrder({
  apiKey, walletAddress, sessionPrivateKey,
  outcomeId: 101,
  coin: '#1010',        // Yes side of outcome 101
  isBuy: true,
  price: '0.55',        // limit; pass isMarket:true to take the book
  size: '20',
  isMarket: false,
});

// 5. Cancel / close
await skill.cancelHlOutcomeOrder({ apiKey, walletAddress, sessionPrivateKey, outcomeId: 101, coin: '#1010', orderId });
await skill.closeHlOutcomeOrder({ apiKey, walletAddress, sessionPrivateKey, outcomeId: 101, coin: '#1010', price: '0', size: '20', isMarket: true });
```

## Collateral currency (HIP-3 / HIP-4) — swap before trading

Each outcome market is quoted in a specific stablecoin (its `quoteToken` —
`USDC`, `USDH`, `USDE`, or `USDT0`). HIP-3 and HIP-4 deployments use different
quote currencies, so **before placing an order you must hold that market's
currency in your HL spot balance.** If you only hold USDC, swap into the
market's currency first with `hlSwapCollateral` (a HL spot swap), then swap
back when done.

```typescript
// Check the market's currency
const m = (await skill.getHlOutcomes({ status: 'open' })).data.meta.outcomes
  .find((o) => o.outcome === 101);
console.log(m.quoteToken);   // e.g. 'USDH'

// If it's not USDC, swap USDC -> that currency (amount = NON-USDC token amount).
// HyperLiquid enforces a $10 minimum per swap order.
await skill.hlSwapCollateral({
  apiKey, walletAddress, sessionPrivateKey,
  fromToken: 'USDC', toToken: 'USDH', amount: '15',   // buy 15 USDH
});

// ...place / manage outcome orders in that currency...

// Swap leftover back to USDC when finished
await skill.hlSwapCollateral({
  apiKey, walletAddress, sessionPrivateKey,
  fromToken: 'USDH', toToken: 'USDC', amount: '15',
});
```

Supported swap currencies: `USDC` ⇄ `USDH` / `USDE` / `USDT0`. MCP exposes this
as the `hl_swap_collateral` tool with the same structured params.

## Notes

- **Coin format:** orders take `coin` as `"#<outcomeId><sideIndex>"` — side 0
  is the first `sideSpecs` entry (usually "Yes"), side 1 the second ("No").
  Current prices are in the `mids` map returned by `getHlOutcomes`.
- **Price is a probability** in `(0,1)`; **size is contracts**. HyperLiquid
  enforces its own minimum order value (~$10–11 notional).
- **`walletAddress` is the control address** used at sign-in (the same rule as
  perp trading); outcome balances/positions live under the **managed** address,
  so pass the managed address to `getHlOutcomeAccount`.
- Outcome markets settle through HyperLiquid **spot** collateral, separate from
  the perp engine. Funding an HL account (via **gdex-perp-funding**) and placing
  an outcome order can move USDC from the perp to the spot/outcomes balance;
  check both `getHlAccountState` (perp) and `getHlSpotState` (spot).
- MCP: the same flow is available via the `hl_enable_trading`,
  `hl_create_outcome_order`, `hl_cancel_outcome_order`, and
  `hl_close_outcome_order` tools with these structured params.
