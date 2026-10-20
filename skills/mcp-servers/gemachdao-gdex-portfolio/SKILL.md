---
name: gdex-portfolio
description: Managed-account holdings, balances, native trading funds and cursor-paginated trade history per chain
---

# GDEX: Portfolio & Balances

Query cross-chain portfolio summaries, chain-specific balances, and trade history.

> **USDC across chains:** `getUsdcBalances` returns the user's USDC and gas balance on every USDC chain plus the total. See **gdex-usdc-wallet**.

## When to Use

- Reading a managed account's token holdings on a chain
- Checking token balances or native trading funds on a specific chain
- Retrieving trade history with cursor pagination

## Prerequisites

- `@gemachdao/gdex-skill` installed
- A managed session (control wallet + session key + API key, or `accountRef` in MCP) — see **gdex-authentication**

## Managed Holdings (`getPortfolio`)

`/v1/portfolio` is per chain and authenticated: `userId` (the **control**
wallet, not the managed wallet) + encrypted session `data` + `chainId`. The SDK
builds the query from your session; there is no public address-only holdings read.

```typescript
import { GdexSkill, ChainId } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
const session = { walletAddress: controlAddress, sessionPrivateKey, apiKey };

const p = await skill.getPortfolio({ ...session, chain: ChainId.SOLANA });
// { status: 'ok', mode: 'managed', userId, chainId, holdings: Balance[], balances: (same) }
for (const h of p.holdings) console.log(h.symbol, h.balance, h.rawBalance);
```

Pass `data` (from `buildGdexReadSessionData(sessionPrivateKey, apiKey)`) instead
of `sessionPrivateKey` + `apiKey` if you already have it. In MCP, pass `accountRef`.

```typescript
interface Balance {
  tokenAddress: string;
  symbol: string;
  name: string;
  decimals: number;
  rawBalance: string;      // exact integer base units
  balance: string;         // exact decimal of rawBalance
  priceUsd?: string;
  usdValue?: string;
  priceNative?: string;
  valueNative?: string;    // backend `holding` (current worth, native)
  investedNative?: string; // backend `invested`
  pnlPercentage?: number;
  chain: number;
  chainId?: number;
}
```

**Failures are errors, not zeros.** A refused session (400 code 102/104) or a
response without `holding[]` throws; `[]` only ever means the backend answered
with no holdings.

## Balances and Trading Funds

```typescript
// Token balances on one chain (optionally one token)
const usdc = await skill.getBalances({ ...session, chain: 8453, tokenAddress: '0x8335...' });

// Native balance available to trade (GET /v1/user)
const funds = await skill.getTradingFunds({ ...session, chain: 8453 });
// { address (managed wallet), nativeBalance, nativeSymbol, walletsByChain, precision: 'approximate' }
```

`nativeBalance` is a backend float, and the backend reports 0 when its RPC read
fails, so treat a zero as unconfirmed. Cross-chain USDC: `getUsdcBalances`
(**gdex-usdc-wallet**).

## Trade History

`/v1/user_history` is keyed by the control wallet (`user`) and `chainId`; it
needs no session. Cursor pagination, at most 50 per page:

```typescript
let page = await skill.getTradeHistory({ walletAddress: controlAddress, chain: 8453, limit: 50 });
while (page.nextCursor) {
  page = await skill.getTradeHistory({ walletAddress: controlAddress, chain: 8453, cursor: page.nextCursor });
}
// page.trades: TradeRecord[] — { type: 'buy'|'sell', tokenAddress, tokenAmount, nativeAmount (raw), txHash, timestamp, ... }
```

`page`, `startTime` and `endTime` are not supported by the backend and are rejected.
The backend returns an empty page on its own database errors, so an empty page is
not proof of no trades.

## Autonomous Agent Notes

1. Use `getPortfolio` / `getBalances` / `getTradingFunds` / `getTradeHistory`; no raw-client workaround is needed.
2. `walletAddress` is always the **control** wallet (GDEX `userId`).
3. Reads are per chain: pass `chain` every time (Solana `622112261`).
4. For percentage sells, `sellToken({ amount: '50%' })` reads the holding itself (**gdex-spot-trading**).

## Related Skills

- **gdex-authentication** — Auth setup required for portfolio queries
- **gdex-spot-trading** — Execute trades based on portfolio analysis
- **gdex-perp-trading** — View perp positions in portfolio
- **gdex-token-discovery** — Research tokens found in portfolio
