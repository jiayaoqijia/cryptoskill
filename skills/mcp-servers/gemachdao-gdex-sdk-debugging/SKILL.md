---
name: gdex-sdk-debugging
description: Troubleshoot GDEX SDK errors — error codes, encryption debugging, chain-specific quirks, HL gotchas, and copy trade pitfalls
---

# GDEX: SDK Debugging & Troubleshooting

Comprehensive troubleshooting guide for GDEX SDK errors, covering API error codes, encryption debugging, chain-specific quirks, HyperLiquid gotchas, and copy trade pitfalls. All issues documented from live E2E testing.

## When to Use

- Getting unexpected API errors (103, 102, TIMEOUT)
- Trades failing silently or returning wrong data
- Debugging encryption / `computedData` payload issues
- Chain-specific problems (wrong chainId, wrong managed wallet)
- HyperLiquid perp issues
- Copy trade configuration problems

## API Error Codes

| Code | Error | Common Cause | Fix |
|------|-------|-------------|-----|
| `103` | Unauthorized | Wrong `walletAddress` (using managed instead of control), wrong ABI type, signing with wrong key | Use **control wallet address** as `walletAddress` / `userId`. Verify session key matches sign-in. |
| `102` | Invalid chainId | Using wrong chainId for HL operations | HL operations require `chainId: 42161` (Arbitrum). Copy trades need specific chainIds (see below). |
| `102` | Invalid params | Reused nonce, unsupported token, or malformed ABI payload | Check nonce is fresh (`Date.now()`). Verify token is supported on chain. |
| `400` | Bad Request | Missing required fields or wrong field types | Check all required params are present and correctly typed. |
| `TIMEOUT` | Request timeout | Backend processing delay (common with `hlCloseAll`) | Retry once, or use alternative approach (reduce-only order to close). |
| `JSON parse error` | Invalid response | Backend returned non-JSON (HTML error page, Cloudflare block) | Check User-Agent header is set. Verify API key is valid. |

## Critical: Control Wallet vs Managed Wallet

This is the **#1 source of errors**:

```
Control wallet:  0x53D029a671bd1CF61a2fB1F4F6e4bD830BFBb2eD  ← used for API calls (userId, walletAddress)
Managed wallet:  0x9967179de55bd67e6b90fcc4f908556d93938c0f  ← server-side, executes trades on-chain
```

**Rule:** All API calls use the **control address** — the one you signed in with. The managed address is only used when querying on-chain state directly (e.g., `user_stats` on HL needs the managed address).

> The `/v1/user` endpoint returns a **different managed wallet per chainId**:
> - `chainId=1` → EVM managed: `0x9967...`
> - `chainId=622112261` → Solana managed: `CFSi4Y...` (base58)

## Chain ID Gotchas

| Issue | Wrong | Correct | Notes |
|-------|-------|---------|-------|
| Solana chain ID | `900` | `622112261` (`ChainId.SOLANA`) | `900` returns EVM managed address with `balance: null` |
| Copy trade sign-in | `chainId: 1` | `chainId: 622112261` | Solana copy trades need Solana chainId for sign-in |
| Perp copy trade sign-in | `chainId: 622112261` | `chainId: 1` | HL perp copy trades need EVM chainId for sign-in |
| HL operations | Any other | `42161` (Arbitrum) | HL deposit, create order, close — all use Arbitrum chainId |

## HyperLiquid-Specific Issues

### `hlCloseAll` is Unreliable

The `/v1/hl/close_all_positions` endpoint frequently returns `TIMEOUT` or JSON parse errors.

**Workaround:** Close each coin with `closePerpPosition` (MCP: `close_perp_position`). It reads the live
position and sends a reduce-only market order for the exact size on the opposite side:
```typescript
// Instead of skill.hlCloseAll() — use this:
const positions = await skill.getPerpPositions({ walletAddress: managedEvmAddress }); // positions live on the managed wallet
for (const pos of positions) {
  await skill.closePerpPosition({
    coin: pos.coin,
    positionAddress: managedEvmAddress,
    apiKey,
    walletAddress: controlAddress,  // control wallet signs
    sessionPrivateKey,
  });
}
```

### Leverage Is Set Per Order

The standalone `hlUpdateLeverage` / `/v1/hl/update_leverage` endpoint returns **404**. Set leverage on the
order instead: `hlCreateOrder({ ..., leverage: 5 })` (MCP: `open_perp_position` with `leverage`). The SDK
sends it as a top-level field next to `computedData`, which is where the backend reads it. Omitted, HL
uses its default (20x on most markets).

### HL Signature Format

```
message = "{action}-{userId.toLowerCase()}-{dataHex}"
digest  = keccak256(utf8Bytes(message))
output  = r(64hex) + s(64hex) + v(2hex)  // 130 chars total, v=00/01, no 0x prefix
```

Common signature errors:
- Wrong `userId` (must be control wallet, lowercase)
- Wrong `action` string (e.g., `"hl_deposit"` not `"deposit"`)
- Leading `0x` on signature output (must be stripped)
- Wrong `v` value (must be `00` or `01`, not `27`/`28`)

## Encryption Debugging

All managed-custody trades use AES-256-CBC encrypted `computedData`:

```
1. ABI-encode trade parameters → hex string (no 0x prefix)
2. Sign: keccak256(action + userId + dataHex) → r+s+v (130 chars)
3. Encrypt: AES-256-CBC(dataHex + signature, derivedKey, iv)
4. POST to backend with { computedData, userId, chainId }
```

### Common Encryption Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `103 Unauthorized` | ABI using `uint256` when backend expects `uint64`, or vice versa | Check the exact ABI types for each endpoint — HL deposit uses `uint64`, not `uint256` |
| `Invalid signature` | Signing with wrong key or wrong message format | Ensure session key (not control wallet key) signs the message. Check action string exactly matches. |
| Empty response | `computedData` encrypted with wrong key | Verify AES key derivation: `SHA256(SHA256(SHA256(apiKey)))` |
| `Reused nonce` | Same nonce value in consecutive trades | Always use fresh `Date.now()` or incrementing nonce |

### AES Key Derivation

```typescript
const key = SHA256(SHA256(SHA256(apiKey)));  // 3× SHA256 hash chain
const iv = randomBytes(16);                  // fresh IV per request
const encrypted = AES_CBC_encrypt(payload, key, iv);
// computedData = iv.hex + encrypted.hex (concatenated)
```

## Solana-Specific Issues

### Meteora Swaps Are Broken

Tokens routed through Meteora DLMM (e.g., BONK) fail with `Program error: 1` because the backend doesn't wrap SOL into WSOL.

**Workaround:** Use Raydium-routed tokens. Check `token.dexId`:
- `"raydium"` / `"raydium_v2"` → works
- `"meteora"` → **will fail**
- `"orca"` → works

### ATA Creation Costs

First trade on a new Solana token incurs ~0.007 SOL overhead:
- ATA creation: ~0.002 SOL
- Priority fee: ~0.0005 SOL (default)
- Keep at least 0.01 SOL in the managed wallet for safety

### Solana Managed Wallet

After sign-in with `chainId: 622112261`, the Solana managed wallet is a **base58 address** (not hex):
```
CFSi4YimeCbfSNqH2WmHwJKwj1YYG1cWBtQyVPB4sCe1
```

## Copy Trade Pitfalls

### `isDelete` Deletes, `isChangeStatus` Toggles

On both Solana and HyperLiquid the backend deletes only on `isDelete`; `isChangeStatus`
flips `isActive` (`isActive = !existing.isActive`). Neither closes positions or cancels
their TP/SL orders. Use `pauseCopyTrade`/`resumeCopyTrade`/`deleteCopyTrade` (and the
`Hl` variants), which read the current state before toggling.

SDK versions up to 4.12 ABI-encoded every copy-trade field as a string. The backend
decodes `uint64`/`bool` slots, so those versions sent `isDelete=true` on every update
(the old "both flags delete" behaviour) and stored `copyMode=416/480`,
`oppositeCopy=true`. The SDK now encodes the typed ABI the backend and gdex.pro use.

### Legacy Values in Responses

`copyMode` 416/480 and `oppositeCopy: true` in a response come from configs written by
SDK <= 4.12. Repair them with `updateHlCopyTradeSettings` and explicit values.

### Max 3 HL Copy Trades

The HyperLiquid perp copy trading system allows a maximum of 3 active copy trades per user. Creating a 4th will fail.

## Network Issues

### Cloudflare Blocking

The GDEX backend sits behind Cloudflare. Requests without a browser-like `User-Agent` may be blocked.

```typescript
// The SDK handles this automatically, but for manual requests:
headers: {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${apiKey}`,
}
```

### Bridge Endpoint Paths

Bridge endpoints use non-obvious paths:
- `GET /v1/bridge/estimate_bridge` (not `/bridge/estimate`)
- `POST /v1/bridge/request_bridge` (not `/bridge/execute`)
- `GET /v1/bridge/bridge_orders` (not `/bridge/orders`)

## Debugging Checklist

When a trade fails, check in order:

1. **Auth:** Is `loginWithApiKey()` called? Is the API key valid?
2. **Wallet:** Are you using the **control** wallet address (not managed)?
3. **Chain ID:** Is chain ID correct for the operation? (See table above)
4. **Nonce:** Is the nonce fresh (`Date.now()`)?
5. **ABI types:** Do the ABI types exactly match what the backend expects?
6. **Signature:** Is the session key signing (not control key)? Is the message format correct?
7. **Balance:** Does the managed wallet have enough funds + gas?

## Portfolio / Balances / Trade History (Fixed in SDK)

The high-level methods now send what the backend reads; no raw-client workaround is needed.

| Method | Backend call |
|--------|--------------|
| `getPortfolio({ walletAddress, sessionPrivateKey, apiKey, chain })` | `GET /v1/portfolio?userId&data&chainId` → `{ holding: [] }` |
| `getBalances({ ..., chain, tokenAddress? })` | same read, filtered |
| `getTradingFunds({ ..., chain })` | `GET /v1/user?userId&data&chainId` → native `balance` |
| `getTradeHistory({ walletAddress, chain, limit?, cursor? })` | `GET /v1/user_history?user&chainId&limit&cursor` (no session) |

- `walletAddress` / `userId` is the **control** wallet; `data` is derived from the session key.
- A refused or malformed response throws (`GdexApiError`); `[]` only means the backend reported no holdings.
- History pages with `cursor` (= `nextCursor`), at most 50 per page; `page`/`startTime`/`endTime` are rejected.
- Solana history uses the same chain id as every other Solana read (`622112261`); older notes said `900`. If a live Solana history call comes back empty, compare both.

## Limit Order ABI Bug (Fixed in SDK)

The `limit_buy` and `update_order` ABI schemas encode `profitPercent` and `lossPercent` as `uint256`, NOT `string`. Using `string` type causes the backend to receive ABI byte-offsets (e.g. 192) instead of the actual percentage values, which always fails the 0-100 range validation.

**Symptom:** `"lossPercent must be between 0 and 100"` even with valid values like `lossPercent: '25'`
**Cause:** ABI `string` type → encoded offset (192) → fails range check
**Fix:** SDK encodes as `uint256` (correct). Only matters if encoding manually.
8. **Token support:** Is the token supported on this chain? Is the DEX working? (Meteora is broken)

## Backend-Limited Behavior (Not SDK Bugs)

These are server-side behaviors, verified live. They are **not fixable in the SDK** — don't
waste a debugging loop on them. Treat the listed responses as expected.

### Deposit returns HTTP 400 even when the transfer succeeds

`perpDeposit` (USDC → HyperLiquid) frequently returns HTTP 400 while the on-chain transfer
**still completes**. The error is a backend response-handling bug, not a failed deposit.

**Symptom:** `perpDeposit` throws a 400, but the USDC arrives in the HL account moments later.
**Do:** Don't retry blindly on the 400 (you'll double-deposit). Poll the HL perp balance /
`getHlAccount` to confirm before retrying. Verify state, not the HTTP status.

### Outcome-market listings are controlled by the backend, not the SDK

The SDK can place/cancel/close orders on **any** outcome market (coin format
`#<outcomeId><sideIndex>`, e.g. `#1010` = outcome 101, Yes side), but *which* markets exist —
and that they may currently be limited (e.g. only a BTC over/under) — is decided by the
backend / HIP-3 deployer, not the SDK.

**Symptom:** `listOutcomeMarkets` returns few/limited markets, or a `#…` coin you expect is absent.
**Do:** Only trade markets returned by `listOutcomeMarkets` / the outcome account query. An empty
or short list is a market-config state on the backend, not a discovery bug. HIP-3/HIP-4 markets
may also quote in non-USDC collateral (USDH/USDE/USDT0) — use `swap_collateral` first.

## Related Skills

- **gdex-authentication** — Full auth flow and encryption details
- **gdex-spot-trading** — Spot trade parameters and chain support
- **gdex-perp-trading** — HL perp specifics
- **gdex-copy-trading** — Solana copy trade ABI format
- **gdex-perp-copy-trading** — HL perp copy trade ABI format
