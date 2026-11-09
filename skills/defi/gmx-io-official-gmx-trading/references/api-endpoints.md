# GMX API endpoints

Prefer `GmxApiSdk` from `@gmx-io/sdk/v2` for typed requests and bigint parsing. This mapping was checked against package 2.2.1 on 2026-10-13. See the [API integration guide](https://docs.gmx.io/docs/api/integration-guide/) and [SDK v2](https://docs.gmx.io/docs/sdk/v2/) for current behavior.

## Hosts and transport

| Chain | SDK default host | Peer host |
|-------|------------------|-----------|
| Arbitrum (42161) | `https://arbitrum.gmxapi.io` | `https://arbitrum.gmxapi.ai` |
| Avalanche (43114) | `https://avalanche.gmxapi.io` | `https://avalanche.gmxapi.ai` |
| MegaETH (4326) | `https://megaeth.gmxapi.io` | `https://megaeth.gmxapi.ai` |

`apiUrl` takes an **unversioned host**. SDK methods append `/v1/...` (or `/v2/...` for JIT); supplying `/v1` in `apiUrl` duplicates the path. The two peer deployments are independent. Through 2.2.1 the packaged fallback arrays are empty; explicit configuration is required to enable peer failover:

```typescript
import { GmxApiSdk, HttpClientWithFallback } from "@gmx-io/sdk/v2";

const sdk = new GmxApiSdk({
  chainId: 42161,
  api: new HttpClientWithFallback([
    "https://arbitrum.gmxapi.io",
    "https://arbitrum.gmxapi.ai",
  ]),
});
```

Use `isApiSupported(chainId)` / `getApiUrl(chainId)` from `@gmx-io/sdk/configs/api` for support checks. Arbitrum Sepolia (421614) resolves to `https://arbitrum-sepolia-test.gmxapi.ai`; Avalanche Fuji has no configured API. Do not derive testnet hosts from mainnet naming rules.

## Read routes

Paths below include their version prefix. GET parameters are query parameters; `searchTrades` sends a POST body.

| SDK method | HTTP route | Parameters / result |
|------------|------------|---------------------|
| `fetchMarkets()` | GET `/v1/markets` | Exact symbols, addresses, leverage tiers, minimums |
| `fetchMarketsInfo()` | GET `/v1/markets/info` | `RawMarketInfo[]`: configuration and changing values |
| `fetchMarketsConfig()` | GET `/v1/markets/config` | `RawMarketConfig[]`: slower-changing configuration |
| `fetchMarketsValues()` | GET `/v1/markets/values` | `RawMarketValues[]`, including `updatedAt` |
| `fetchMarketsTickers(params?)` | GET `/v1/markets/tickers` | `symbols?: string[]`, `addresses?: string[]` |
| `getTradingCapacity(params)` | GET `/v1/markets/trading-capacity` | Full `symbol`, `direction: "long" \| "short"` |
| `fetchTokens()` / `fetchTokensData()` | GET `/v1/tokens` / `/v1/tokens/info` | Token catalog / prices and metadata |
| `fetchPositionsInfo(params)` | GET `/v1/positions` | `address`, optional `includeRelatedOrders` |
| `fetchOrders(params)` | GET `/v1/orders` | `address`; active orders with `key` |
| `fetchTrades(params)` | GET `/v1/trades` | `address`, filters, `limit`, `cursor` |
| `searchTrades(params)` | POST `/v1/trades/search` | Advanced filters; follow the returned cursor |
| `fetchOhlcv(params)` | GET `/v1/prices/ohlcv` | `symbol`, `timeframe`, optional `limit`, `since` |
| `fetchPairs()` | GET `/v1/pairs` | Pair summaries |
| `fetchRates(params?)` | GET `/v1/rates` | Historical snapshots; `period`, `averageBy`, `address` |
| `fetchApy(params?)` | GET `/v1/apy` | `period`; market/GLV APY records |
| `fetchPerformanceAnnualized(params?)` | GET `/v1/performance/annualized` | `period`, optional `address` |
| `fetchPerformanceSnapshots(params?)` | GET `/v1/performance/snapshots` | `period`, optional `address` |
| `fetchGmPoolYieldPnl(params?)` | GET `/v1/yield/gm-pools` | `pools`, `period`, `includeComponents` |
| `fetchGmUserEarnings(params)` | GET `/v1/yield/gm-user-earnings` | `account` (not `address`) |
| `fetchWalletBalances(params)` | GET `/v1/balances/wallet` | `address` |
| `fetchAllowances(params)` | GET `/v1/allowances` | `address`, `spender: "router"` |
| `fetchBuybackWeeklyStats()` | GET `/v1/buyback/weekly-stats` | Buyback summaries |
| `fetchStakingPower(params)` | GET `/v1/staking/power` | `address` |
| `fetchJitLiquidityInfo({ apiVersion: "v2" })` | GET `/v2/jit/liquidity_info` | JIT map; explicitly pass `v2` |

Through 2.2.1 the JIT method defaults to `apiVersion: "v1"`, which returns HTTP 500 on every host, so `fetchJitLiquidityInfo()` throws unless you pass `{ apiVersion: "v2" }`. For trade sizing prefer `getTradingCapacity()`.

`period` is typed as `"1d" | "7d" | "30d" | "90d" | "180d" | "1y" | "total"`, but accepted values differ by route. Prefer `7d` or `30d`:

- The performance routes reject `1d` (HTTP 400 "Invalid period"; their default is `90d`).
- `total` currently returns HTTP 500 for `/v1/apy`, `/v1/yield/gm-pools` and `/v1/performance/annualized` on Arbitrum; longer windows can also fail or time out.
- All-market `/v1/rates` returns HTTP 500 for 30d and longer; pass `address` for one market.

Treat such errors as unknown data, not zero yield. `fetchApy()` values are fractions (`0.0117` = 1.17%), and its `glvs` map can come back empty although GLVs exist on-chain, so a missing entry means unknown yield. Respect each method's actual response types: market/position amounts are parsed to bigint, while APY/performance analytics may be numbers, decimal strings, or null.

## Write and status routes

All these routes use POST. Builders such as `buildApproveTransaction()` encode calldata locally and do not broadcast it.

| SDK method | Route |
|------------|-------|
| `prepareOrder()` | `/v1/orders/txns/prepare` |
| `prepareEditOrder()` | `/v1/orders/txns/edit/prepare` |
| `prepareCancelOrder()` | `/v1/orders/txns/cancel/prepare` |
| `prepareCollateral()` | `/v1/orders/txns/collateral/prepare` |
| `submitOrder()` | `/v1/orders/txns/submit` |
| `fetchOrderStatus()` | `/v1/orders/txns/status` |
| `fetchSubaccountStatus()` | `/v1/subaccounts/status` |
| `prepareSubaccountApproval()` | `/v1/subaccounts/approval/prepare` |

`signOrder()` and `signSubaccountApproval()` sign locally through the supplied signer, but neither checks amounts, actions or grant limits against the user's intent. Follow [SDK reference](sdk-reference.md) for the complete request, signed payload and submission fields.

For direct HTTP, encode bigint values as decimal strings, never floating point JSON numbers. Use the [GMX API reference](https://docs.gmx.io/docs/category/gmx-api-openapi-reference/) for endpoints not wrapped by the SDK; do not guess routes by appending a method name. The generic relay API and GMX Account funding API are separate from GM/GLV liquidity requests.

## Freshness and retry behavior

- Check `updatedAt` on market values (Unix milliseconds, nullable). A successful HTTP response can contain retained stale values. Inspect JIT/market freshness flags and preparation warnings before sizing a trade.
- `/rates` is historical; use market info/tickers for current rates. APY and yield windows update more slowly than prices; preserve the returned window and missing values.
- Back off transient read failures and rate limits. Do not turn network errors into zero balances, no positions, or unlimited liquidity.
- The default single-host client has no pinning or failover. With `HttpClientWithFallback`, the SDK pins prepare/submit/status to the serving host only within that `api` object (an LRU of 256 request IDs, dropped on a 404). It starts on a random host and fails over only on 5xx or network errors, not on a 404. The SDK does not expose which host served a request; to recover after a restart, use one single-host instance per `apiUrl` and persist which one you used.
- On an uncertain submission, query status with the original request ID and reconcile on-chain/account state. The API has no idempotency key; submit/status bodies with extra fields get HTTP 400. Do not re-prepare and re-sign as a blind retry: that creates a new intent. A 404 on a different peer is not proof that the original write failed.

## Oracle and indexed data

Oracle hosts such as `https://arbitrum-api.gmxinfra.io` expose a separate read API with `/prices/tickers`, `/tokens`, `/markets`, and `/markets/info`. They are not `GmxApiSdk` base URLs and do not accept `/orders/txns/*` writes. Use the [Oracle API docs](https://docs.gmx.io/docs/category/oracle-api/) for specialized signed-price reads.

Use [GraphQL](https://docs.gmx.io/docs/api/graphql/) for indexed historical analysis beyond `fetchTrades()` / `searchTrades()`. Use its published chain endpoints and schema. Indexer history is not a substitute for transaction receipts or keeper execution events.
