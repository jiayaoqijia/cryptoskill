---
name: gdex-xstocks
description: List tokenised equities (xStocks) — real-world stocks traded as tokens on GDEX — requires API key auth (Bearer token)
---

# GDEX: xStocks

List tokenised equities. xStocks are real-world stocks issued as on-chain tokens, so they trade
through the same spot rails as any other token on GDEX: you discover them here, then buy or sell
them with `gdex-spot-trading`.

> **Auth required:** returns 403 "Access denied: Invalid client" without a Bearer token. Call
> `loginWithApiKey()` first.

## When to Use

- Listing the tokenised stocks available to trade
- Checking price, market cap, liquidity, or 24h volume on an xStock before buying
- Answering "can I trade Nvidia / Circle / McDonald's on GDEX"

Use `gdex-spot-trading` to actually execute. This skill is discovery only.

## Prerequisites

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY, ChainId } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);
```

## List xStocks

```typescript
const xstocks = await skill.getXstocks({
  chain: ChainId.SOLANA,  // optional
  limit: 50,              // optional
  page: 1,                // optional
});
```

### Parameters

`getXstocks` takes `TokenListParams`, which is the same shape used by `getNewestTokens` and
`getTopTokens`:

```typescript
interface TokenListParams {
  chain?: SupportedChain;  // chain id or alias; omit for all chains
  limit?: number;          // page size
  page?: number;           // 1-based page number
}
```

There are no other filters. Sorting, market-cap floors, and age windows are not exposed.

### Response

```typescript
Promise<Record<string, unknown>>
```

**The response is untyped.** Unlike `getTokenDetails`, this endpoint has no declared interface in
the SDK, so inspect the payload rather than assuming a shape:

```typescript
const xstocks = await skill.getXstocks({ limit: 5 });
console.log(JSON.stringify(xstocks, null, 2));
```

The product surface at `gdex.pro/<network>/xstock` renders each row with token symbol and name,
age, price, 24h price change, market cap, liquidity, and 24h volume, so expect fields covering at
least those. Confirm the exact keys against a live call before you depend on them.

## Trading an xStock

xStocks are ordinary SPL/ERC-20 tokens, so once you have an address from this listing you buy and
sell them with the normal spot methods:

```typescript
await skill.buyToken({
  tokenAddress: '<address from getXstocks>',
  chain: ChainId.SOLANA,
  amount: '0.5',
});
```

See `gdex-spot-trading` for the full buy and sell surface, slippage handling, and trade-status
polling.

## Endpoint

| Method | Endpoint |
|---|---|
| `getXstocks` | `GET /v1/xstocks` |

## Notes

- Tokenised equities carry issuer and market-hours risk that ordinary tokens do not. Liquidity on
  individual names can be very thin — the live board shows several with under $10k — so size
  accordingly and check the liquidity figure before quoting a fill.
- This method ships with no tests and no typed response in the SDK. Treat the shape as
  provisional.
