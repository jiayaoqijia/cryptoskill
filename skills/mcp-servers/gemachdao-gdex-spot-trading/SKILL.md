---
name: gdex-spot-trading
description: Managed-custody buy and sell with native on Solana and EVM chains (session-signed purchase_v2/sell_v2), exact amounts, percentage sells from the held balance, and trade-status follow-up
---

# GDEX: Spot Trading

Buy and sell tokens for the chain's native token from the managed GDEX wallet. Every spot trade is session-signed (`purchase_v2` / `sell_v2` require `computedData`); the backend picks the route.

> **Paying with USDC?** To buy with USDC from any chain (GDEX bridges it in automatically) or sell straight into USDC, see **gdex-usdc-wallet**.
## When to Use

- Buying a token with native currency (SOL, ETH, etc.)
- Selling a token (absolute amount or percentage of holdings)
- Executing managed-custody spot trades with encrypted payloads

## Prerequisites

- `@gemachdao/gdex-skill` installed
- A managed session: control wallet (`walletAddress`), `sessionPrivateKey`, `apiKey` (MCP: `accountRef`). See **gdex-authentication**

## Buy a Token

```typescript
import { GdexSkill, ChainId } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
const session = { walletAddress: controlAddress, sessionPrivateKey, apiKey };

const { requestId, amountRaw } = await skill.buyToken({
  chain: 'solana',
  tokenAddress: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
  amount: '0.1',        // 0.1 SOL, converted exactly to lamports ('100000000')
  slippage: 10,         // optional, Solana/Sui only, sent as bps (max 50%)
  priorityFee: 500000,  // optional, Solana only, lamports (max 0.05 SOL)
  ...session,
});
const done = await skill.waitForTrade({ requestId });
// { outcome: 'filled' | 'failed' | 'not_found' | 'pending', hash, tokenAmount, ethAmount, error }
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | `string \| ChainId` | Yes | Buys: 1, 10, 56, 146, 252, 4663, 8453, 42161, Solana `622112261` (`'solana'`). Sui, Nibiru and Berachain are sell-only (retired for trading). |
| `tokenAddress` | `string` | Yes | Token to buy |
| `amount` | `string` | Yes | Decimal native amount; never rounded (more decimals than the chain has is an error) |
| `walletAddress`, `sessionPrivateKey`, `apiKey` | `string` | Yes | Managed session (or `accountRef` in MCP) |
| `slippage` | `number` | No | Percent. **Solana/Sui only**: on EVM the backend uses the account's stored slippage, so passing it is rejected. Omit to use the stored setting. |
| `priorityFee` | `number` | No | Solana tip in lamports (integer, max 50,000,000) |
| `inputToken` | `string` | No | Only the native token. For USDC use `buyWithUsdc` (**gdex-usdc-wallet**) |
| `dex`, `referrer` | — | — | Not supported by `purchase_v2`; rejected |

> **Critical:** The Solana numeric chainId is `622112261` (`ChainId.SOLANA`), NOT `900`.

## Sell a Token

```typescript
// Absolute amount: converted with the token's decimals from the managed holding
await skill.sellToken({ chain: 8453, tokenAddress: '0x8335...', amount: '100', ...session });

// Percentage of the held balance: floor(held * pct / 100) in integer math; 100% sells the exact raw balance
const r = await skill.sellToken({ chain: 'solana', tokenAddress: 'DezX...B263', amount: '50%', ...session });
// r.amountRaw, r.heldRaw
```

Both read `/v1/portfolio` first (as gdex.pro does before sizing a sell). A token
missing from the managed holdings cannot be sold by percentage; for an absolute
amount pass `tokenDecimals`. An amount above the held balance is rejected before
signing. `outputToken` must be native (use `sellToUsdc` for USDC).

## Trade Status

`buyToken` / `sellToken` return `{ requestId, status: 'pending', amountRaw, ... }`.
`/v1/trade-status/:requestId` reports `pending` → `processing` → `success` | `error`.

```typescript
const r = await skill.waitForTrade({ requestId, timeoutMs: 120000 });
if (r.outcome === 'pending') {
  // still settling: never resubmit; check again later
}
```

## Low-Level Managed Submission

`buildGdexManagedTradeComputedData()` + `submitManagedPurchase()` / `submitManagedSell()`
are still available. The signed data is ABI `['string','uint256','string']` =
`[tokenAddress, amountRaw, nonce]` (raw native units for a buy, raw token units
for a sell). Prefer `buyToken` / `sellToken`, which do the unit conversion and
option checks.

### Solana-Specific Notes (Live-Tested)

- **Raydium-routed tokens work; Meteora tokens fail.** The backend has a bug where Meteora DLMM swaps don't wrap SOL into WSOL before swapping. Check `token.dexId` — if `"meteora"`, the swap will fail with `Program error: 1`. Tokens with `dexId: "raydium"` work correctly.
- **Minimum ~0.01 SOL balance needed.** Each new token ATA costs ~0.002 SOL rent + priority fee (0.0005 default) + base tx fee. The first trade on a token needs significantly more SOL than just the swap amount.
- **Amount is in lamports** (1 SOL = 1,000,000,000 lamports). Pass as a string, e.g. `'5000000'` for 0.005 SOL.
- **Use `chainId: 622112261`**, not `900`. Using `900` will submit the trade to the wrong chain context.
## Supported Chains × DEXes

| Chain | Available DEXes |
|-------|-----------------|
| Solana | Raydium, Raydium v2, Orca |
| Sui | Cetus, Bluefin |
| Ethereum | Uniswap v2, Uniswap v3, Odos |
| Base | Uniswap v3, Odos, Arcadia |
| Robinhood Chain | Uniswap v2, KyberSwap aggregator |
| Arbitrum | Uniswap v3, Odos |
| BSC | PancakeSwap, Odos |
| Optimism | Uniswap v3, Odos |
| Fraxtal | Uniswap v3 |

## Error Handling

```typescript
import { GdexValidationError, GdexApiError, GdexRateLimitError } from '@gemachdao/gdex-skill';

try {
  await skill.buyToken({ chain: 'solana', tokenAddress: '...', amount: '0.1', ...session });
} catch (err) {
  if (err instanceof GdexRateLimitError) {
    await delay(err.retryAfter * 1000);  // wait and retry
  } else if (err instanceof GdexValidationError) {
    console.error('Invalid param:', err.message);
  } else if (err instanceof GdexApiError) {
    console.error('API error:', err.status, err.message);
  }
}
```

## Notes

- All amounts are strings to preserve precision (e.g., `'0.1'`, `'1000'`)
- Chain can be string (`'solana'`) or ChainId number (`622112261`)
- The SDK retries on transient errors (429, 503) with exponential backoff
- The backend selects the route; `dex` is not accepted

## Autonomous Agent Notes (Live-Tested)

### Managed-Custody Trades Require Raw Units

For `buildGdexManagedTradeComputedData()` + `submitManagedPurchase()` / `submitManagedSell()`, the `amount` must be in **raw units** (lamports for Solana, wei for EVM), NOT human-readable:

```typescript
// ❌ WRONG: amount: '0.01' (this is a float, not raw units)
// ✅ CORRECT: amount: '10000000' (0.01 SOL = 10,000,000 lamports)
// ✅ CORRECT: amount: '10000000000000000' (0.01 ETH = 10^16 wei)
```

### Raydium vs Meteora on Solana

- **Raydium-routed tokens work correctly** (WIF, most liquid tokens)
- **Meteora DLMM tokens fail** with `Program error: 1` (backend bug — doesn't wrap SOL into WSOL)
- **Check before buying:** `token.dexId === 'raydium'` ✅ / `token.dexId === 'meteora'` ❌
- If you get `Program error: 1`, the token is Meteora-routed — don't retry, pick a different token

### Minimum SOL Balance

Keep at least **0.01 SOL** in the managed Solana wallet. First trade on a new token costs ~0.007 SOL overhead (ATA creation + priority fee + base tx fee) on top of the trade amount.

### Trade Status Polling

Use `waitForTrade({ requestId })` (MCP: `wait_for_trade`). Terminal statuses are
`success` and `error`; `processing` means it is still running.

### Sell by Percentage

`amount: '50%'` is resolved by the SDK from the managed holding (exact integer
math) before signing; the backend only ever sees a raw amount.

## Related Skills

- **gdex-authentication** — Auth setup required before trading
- **gdex-portfolio** — Check balances and trade history after trading
- **gdex-token-discovery** — Research tokens before buying (no auth needed)
- **gdex-limit-orders** — Set limit orders instead of market buys/sells
