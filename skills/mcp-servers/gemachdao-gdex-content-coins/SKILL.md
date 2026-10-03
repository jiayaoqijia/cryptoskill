---
name: gdex-content-coins
description: List Zora content coins and creator coins on Base — social posts and creator tokens tradable on GDEX — requires API key auth (Bearer token)
---

# GDEX: Content and Creator Coins

List Zora-protocol tokens. On GDEX these appear as two related markets on **Base**:

- **Content coins** — a token tied to an individual social post.
- **Creator coins** — a token tied to the creator rather than to any single post.

Both are ordinary ERC-20s once minted, so you discover them here and trade them with
`gdex-spot-trading`.

> **Auth required:** returns 403 "Access denied: Invalid client" without a Bearer token. Call
> `loginWithApiKey()` first.

## When to Use

- Listing coined posts or creator tokens available to trade
- Checking price and age on a content coin before buying
- Answering "what Zora coins can I trade on GDEX"

## Prerequisites

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY, ChainId } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);
```

## List Zora tokens

```typescript
const coins = await skill.getZoraTokens({
  chain: ChainId.BASE,  // optional; this is a Base market
  limit: 50,            // optional
  page: 1,              // optional
});
```

### Parameters

`getZoraTokens` takes `TokenListParams`:

```typescript
interface TokenListParams {
  chain?: SupportedChain;  // chain id or alias; omit for all chains
  limit?: number;          // page size
  page?: number;           // 1-based page number
}
```

There is **no parameter that separates content coins from creator coins**. The product UI splits
them into two tabs, but the SDK exposes one listing method. If you need only one of the two, filter
the response yourself once you have confirmed which field distinguishes them.

### Response

```typescript
Promise<Record<string, unknown>>
```

**The response is untyped.** There is no declared interface in the SDK, so inspect the payload:

```typescript
const coins = await skill.getZoraTokens({ chain: ChainId.BASE, limit: 5 });
console.log(JSON.stringify(coins, null, 2));
```

The product surface at `gdex.pro/base/creator-coin` renders each card with the coined post itself —
author handle, post text, and any image — plus token age and current price. Expect fields covering
at least those. Confirm the exact keys against a live call before depending on them.

## Trading a content coin

```typescript
await skill.buyToken({
  tokenAddress: '<address from getZoraTokens>',
  chain: ChainId.BASE,
  amount: '0.5',   // denominated in ETH on Base
});
```

See `gdex-spot-trading` for the full surface.

## Endpoint

| Method | Endpoint |
|---|---|
| `getZoraTokens` | `GET /v1/zora` |

## Notes

- This is a **Base** market. Quick-buy amounts in the product are denominated in ETH.
- Content coins are tied to social posts, so supply and liquidity can be extremely small and the
  underlying "asset" is a post that may be deleted. Check liquidity before quoting a fill.
- This method ships with no tests and no typed response in the SDK. Treat the shape as
  provisional.
