---
name: gdex-usdc-wallet
description: Unified USDC wallet — one USDC balance across chains, buy with USDC or native, sell to USDC, auto-bridge funding, native-to-USDC convert, USDC bridge
---

# GDEX: Unified USDC Wallet

A GDEX user's USDC on Ethereum, Optimism, BSC, Sonic, Base, Arbitrum and Solana works as **one balance**.
Buy any token with USDC (or the chain's native token) on any of those chains; if the target chain is short,
GDEX bridges USDC in from the user's other chains automatically (`autoBridge`), never spending more than
the source budget the user signed. Sells settle back to USDC.

## When to Use

- "What's my USDC balance?" across all chains → `getUsdcBalances`
- Buying a token with USDC without first bridging by hand → `buyWithUsdc`
- Selling a token into USDC → `sellToUsdc`
- Paying with ETH/BNB/SOL but letting GDEX top up from other chains → `buyWithNative`
- Turning leftover gas tokens into USDC → `convertNativeToUsdc`
- Moving USDC between chains yourself → `estimateUsdcBridge` + `executeUsdcBridge`

## Prerequisites

- `@gemachdao/gdex-skill` installed
- Managed-custody sign-in done — see **gdex-authentication**. Every call takes
  `{ apiKey, walletAddress, sessionPrivateKey }`, where `walletAddress` is the **control wallet**
  used at sign-in (not the managed address).

## Automatic Funding and Gas (On by Default)

Like gdex.pro's **"Automatic funding — bridge USDC & top up gas"** checkbox, which is ticked by default,
the SDK turns it on for every **buy** (`autoBridge: true`, paying with USDC or native; gdex.pro's Native tab
has the same "Auto-bridge from other chains" option). **Sells** settle on their own chain and never auto-fund,
exactly as gdex.pro does. If a buy's chain is
short of USDC or of native gas, GDEX bridges USDC and tops up gas from the user's other chains. It
never spends more than the signed `maxSourceSpendRaw`. Bridges to EVM chains also add a **$1 destination
gas top-up** by default (`gasTopUp`, off for Solana destinations, where Relay can't top up gas). Its cost
is already in the estimate. Pass `autoBridge: false` or `gasTopUp: false` only when the user asks to opt out.

## Supported Chains

| Chain | chainId | USDC decimals | Native decimals |
|-------|---------|---------------|-----------------|
| Ethereum | 1 | 6 | 18 |
| Optimism | 10 | 6 | 18 |
| BSC | 56 | **18** | 18 |
| Sonic | 146 | 6 | 18 |
| Base | 8453 | 6 | 18 |
| Arbitrum | 42161 | 6 | 18 |
| Solana | 622112261 | 6 | 9 |

Robinhood Chain (4663, uses USDG) and Fraxtal (252) have **no USDC**. All amounts are **raw integer
strings** (`'5000000'` = 5 USDC on a 6-decimal chain); decimals are rejected, not rounded.

## Balances

```typescript
import { GdexSkill, describeUsdcFundingStep } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
const creds = { apiKey, walletAddress, sessionPrivateKey };

const b = await skill.getUsdcBalances(creds);
// { asOf, totalUsdc: '42.10', totalUsd: '57.33',
//   chains: [{ chainId: 8453, usdc: '30.1', usdcRaw: '30100000', native: '0.004', nativeSymbol: 'ETH', ... }] }
```

## Buy With USDC

Quote first, apply slippage, then buy:

```typescript
const quote = await skill.getUsdcTradeQuote({
  ...creds, chainId: 8453, tokenAddress, payAsset: 'usdc', amountInRaw: '5000000', side: 'buy',
});
// { amountOutRaw: '123456789', source: 'kyberswap' }

const minTokenOutRaw = (BigInt(quote.amountOutRaw as string) * 99n / 100n).toString(); // 1% slippage

const res = await skill.buyWithUsdc({
  ...creds,
  chainId: 8453,
  tokenAddress,
  usdcAmountRaw: '5000000',   // 5 USDC
  minTokenOutRaw,
  // autoBridge defaults to true: USDC and gas are pulled from other chains if Base is short
  // maxSourceSpendRaw: '6000000', // optional; default ceil(amount × 1.2)
});
```

A direct fill returns `status` and `hash`. When funding or confirmation is still running the response is
`{ status: 'pending', requestId }`. Follow it the way gdex.pro's live progress note does:

```typescript
const r = await skill.watchUsdcTrade({
  ...creds, requestId: res.requestId as string,
  onUpdate: (funding, steps) => console.log(funding.status, steps.map(describeUsdcFundingStep)),
});
// planning [] -> bridging ['bridge USDC Arbitrum -> Base: active'] -> done ['bridge USDC Arbitrum -> Base: done', 'swap: done']
// r.outcome: 'success' | 'failed' (r.errorCode) | 'needs_retry' (dropped sell, see below) | 'pending' (still settling: never resubmit)
```

It polls `/v1/usdc/funding/status` every 3 s and, once funding succeeds, reads the trade result from
`/v1/trade-status/:requestId`. Step keys: `balance_check`, `bridge`, `native_topup` (gas), `approve`, `swap`.

### The Signed Source Budget

With `autoBridge`, the user signs `maxSourceSpendRaw`: the most the backend may spend across all funding
legs, in the target chain's units. The SDK defaults it to gdex.pro's rule: `ceil((amount + gas headroom) × 1.2)`, where the gas headroom is
3 USDC on EVM chains and 2 USDC on Solana (for a buy with ~0 native gas) and the 20% covers bridge fees. If funding would cost more, the trade fails with `EXCEEDS_SIGNED_MAX` instead of
overspending. With `autoBridge: false` the budget is `0` and only the target chain's USDC is used.

## Sell to USDC

```typescript
const q = await skill.getUsdcTradeQuote({
  ...creds, chainId: 42161, tokenAddress, payAsset: 'usdc', amountInRaw: tokenAmountRaw, side: 'sell',
});
await skill.sellToUsdc({
  ...creds, chainId: 42161, tokenAddress, tokenAmountRaw,
  minUsdcOutRaw: (BigInt(q.amountOutRaw as string) * 99n / 100n).toString(),
});
```

If a sell's broadcast is dropped, `watchUsdcTrade` returns `outcome: 'needs_retry'` with the backend's
`retry` capability (`SAME_NONCE_RETRY_AVAILABLE`). Retry it in place: the SDK reads chain, token, amount and
nonce from that capability and generates the retry id (a UUID, as gdex.pro does). It reuses the same
transaction nonce, so the sell cannot execute twice. The backend allows two retries.

```typescript
const q2 = await skill.getUsdcTradeQuote({ ...creds, chainId, tokenAddress, payAsset: 'usdc', amountInRaw: tokenAmountRaw, side: 'sell' });
await skill.retryUsdcSell({ ...creds, requestId, minUsdcOutRaw: (BigInt(q2.amountOutRaw as string) * 97n / 100n).toString() });
```

## Buy With Native

```typescript
await skill.buyWithNative({
  ...creds, chainId: 622112261, tokenAddress: mint,
  nativeAmountRaw: '100000000',   // 0.1 SOL
  minTokenOutRaw, autoBridge: true,
});
```

## Convert Gas Tokens to USDC

```typescript
const cq = await skill.getUsdcConvertQuote({ ...creds, chainId: 8453, amount: 'max' });
// { nativeSpent, nativeRetained (gas reserve kept), estimatedUsdcOut, minUsdcOut }
await skill.convertNativeToUsdc({
  ...creds, chainId: 8453, nativeAmountRaw: cq.nativeSpent as string, minUsdcOutRaw: cq.minUsdcOut as string,
});
```

## Bridge USDC Between Chains

`amountRaw` is what **arrives** on the destination, in destination decimals. Sign the estimate's source
spend (plus a little headroom) as the cap:

```typescript
const est = await skill.estimateUsdcBridge({
  ...creds, fromChainId: 8453, toChainId: 42161, amountRaw: '10000000',
  // gas top-up defaults to $1 for EVM destinations; gasTopUpAmountUsd sets up to $50
});
const maxFromAmountRaw = (BigInt(est.fromAmountRaw as string) * 101n / 100n).toString();
const br = await skill.executeUsdcBridge({
  ...creds, fromChainId: 8453, toChainId: 42161, amountRaw: '10000000', maxFromAmountRaw,
});
await skill.getUsdcBridgeStatus({ ...creds, bridgeId: br.bridgeId as string, refresh: true });
await skill.getUsdcBridgeOrders(creds);
```

## Never Double-Submit

If a trade's outcome is unknown (timeout, `503 USDC_STATUS_UNCONFIRMED`, `indeterminate: true`), do **not**
submit it again. Check `getUsdcPendingTrades({ ...creds, chainId })` and `getUsdcFundingStatus` first.

## MCP Tools

`usdc_get_balances`, `usdc_get_trade_quote`, `usdc_buy`, `usdc_sell`, `usdc_buy_with_native`,
`usdc_retry_sell`, `usdc_get_funding_status`, `usdc_wait_for_trade`, `usdc_get_deferred_trade`, `usdc_get_pending_trades`,
`usdc_get_convert_quote`, `usdc_convert_native`, `usdc_estimate_bridge`, `usdc_execute_bridge`,
`usdc_get_bridge_status`, `usdc_get_bridge_orders`.

## Common Errors

| Code | Meaning |
|------|---------|
| `V2_REQUIRED` | Called a retired v1 route; the SDK always uses v2 |
| `CHAIN_MISMATCH` | Body `chainId` differs from the signed one |
| `MISSING_SIGNED_MAX` | Auto-funding needed but the signed budget was `0` |
| `EXCEEDS_SIGNED_MAX` | Funding or bridge would cost more than the signed cap; re-quote |
| `BELOW_MINIMUM` | Bridge amount under the minimum |
| `INVALID_GAS_TOPUP` | Gas top-up outside (0, 50] USD |
| `USDC_QUOTE_UNAVAILABLE` | No executable route right now |
| `USDC_STATUS_UNCONFIRMED` | Status still being confirmed; do not resubmit |

## Related Skills

- **gdex-spot-trading** — classic native-paid swaps
- **gdex-bridge** — the native-asset bridge (`/v1/bridge/*`)
- **gdex-portfolio** — balances and trade history
- **gdex-perp-funding** — moving USDC into Hyperliquid
