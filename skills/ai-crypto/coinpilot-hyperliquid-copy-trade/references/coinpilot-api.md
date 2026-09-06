## Coinpilot API reference (copy trade)

Base URL: `https://api.coinpilot.bot`

If `coinpilot.json.apiBaseUrl` is set, it must still resolve to an allowlisted
HTTPS origin.

### Authentication

- All Coinpilot endpoints require these headers:
  - `x-api-key`: `coinpilot.json.apiKey`
  - `x-wallet-private-key`: the primary wallet `privateKey` from `coinpilot.json`
  - `x-user-id`: `coinpilot.json.userId`
- For experimental write routes, continue sending the wallet keys required in the
  request body (`primaryWalletPrivateKey`, `followerWalletPrivateKey`) in
  addition to the auth headers.
- Suggested readonly authentication validation flow:
  - `GET /experimental/:wallet/me`
  - `GET /users/:userId/subscriptions`
  - one lead-discovery GET
  - Hyperliquid `clearinghouseState` (`hl-account`) for the primary wallet

Rate limit: 1 request per second.

### Experimental copy trading

- `GET /experimental/:wallet/me`
  - Returns `{ userId }` for the primary wallet.
- `GET /experimental/:wallet/subscriptions/prepare-wallet`
  - Returns `{ address, hdWalletIndex }`
- `POST /experimental/:wallet/subscriptions/start`
  - Body (required):
    - `primaryWalletPrivateKey`
    - `followerWalletPrivateKey`
    - `subscription: { leadWallet, followerWallet, config }`
  - `config` options:
    - `allocation` (required, min $5 USDC)
    - `stopLossPercent` (decimal 0-1, `0` disables; e.g. 50% = `0.5`)
    - `takeProfitPercent` (decimal >= 0, `0` disables; e.g. 50% = `0.5`, 150% = `1.5`)
    - `inverseCopy`, `forceCopyExisting`
    - `maxLeverage`, `maxMarginPercentage`
- `POST /experimental/:wallet/subscriptions/stop`
  - Body (required):
    - `followerWalletPrivateKey`
    - `subscriptionId`
  - Continue sending `x-wallet-private-key`; `primaryWalletPrivateKey` may also
    be accepted in the body for legacy flows.
- `POST /experimental/:wallet/subscriptions/:subscriptionId/renew-api-wallet`
  - Body (required):
    - `followerWalletPrivateKey`
  - Renews the API wallet when `apiWalletExpiry` is within 5 days.
  - Returns `{ apiWallet: { address, encryptedApiWalletKey, apiWalletExpiry } }`.

### Lead wallet discovery

- `GET /lead-wallets/metrics/wallets/:wallet`
  - Returns a single lead wallet metrics object (or `null` if not found).
- `GET /lead-wallets/metrics/wallets/:wallet/periods`
  - Returns an array of period metrics for the wallet.
- `GET /lead-wallets/metrics/categories`
  - Query params:
    - `limit` (default `10`, max `100`)
  - Returns an object keyed by category with `{ data, totalCount }`.
- `GET /lead-wallets/metrics/categories/:category`
  - Query params:
    - `period`: `perpDay | perpWeek | perpMonth | perpAllTime` (default `perpMonth`)
    - `sortBy`: `sharpe | sortino | gpr | winRate | avgPnlPerVlm | pnl | roi | vlm | maxDrawdown | default`
      - `default` uses the category's default sort (fallback: `roi`)
    - `sortOrder`: `asc | desc` (default `desc`)
    - `search` (default empty)
    - `page` (default `1`)
    - `limit` (default `20`, max `100`)
  - Available categories (from code):
    - `all`: all available wallets on the platform
    - `top`: top picks curated by coinpilot
    - `totalPnl`: highest total PnL
    - `winRate`: highest win rate
    - `avgPnlPerVlm`: best PnL per volume
    - `subscriptionCount`: most subscribers
    - `mostPopular`: highest total allocation
    - `longBias`: long-leaning traders
    - `shortBias`: short-leaning traders
    - `scalpers`: short average trade duration
    - `swing`: mid-term average trade duration
    - `holders`: long average trade duration
    - `smart`: smart money traders
    - `whales`: whale-size traders
    - `kol`: key opinion leaders
    - `institution`: institutional traders
    - `coinpilot`: community-sourced wallets
  - Do not use: `bot`, `nof1-s1.5`, `watchlist`.

### Subscription management (non-experimental)

These routes require the standard auth headers listed above, and the `:userId`
path param must match the wallet owner.

- LeadSubscription schema:
  - `userId`: string
  - `leadWallet`: string
  - `leadWalletName?`: string
  - `followerWallet`: string
  - `primaryWallet`: string
  - `apiWallet`: string
  - `encryptedApiWalletKey`: string
  - `config`: `LeadSubscriptionConfig`
  - `priority`: number
  - `leverages`: `LeadSubscriptionLeverage[]`
  - `apiWalletExpiry?`: number
  - `dex?`: string
  - `balance?`: number (follower account value)
  - `balanceUpdatedAt?`: number (timestamp)
  - `_id`: `${leadWallet}:${userId}`
- LeadSubscriptionConfig:
  - `allocation`: number (USDC)
  - `stopLossPercent`: number (decimal 0-1, `0` disables; e.g. 50% = `0.5`)
  - `takeProfitPercent`: number (decimal >= 0, `0` disables; e.g. 50% = `0.5`, 150% = `1.5`)
  - `inverseCopy`: boolean
  - `forceCopyExisting`: boolean
  - `positionTPSL?`: record keyed by coin
    - `stopLossPrice?`: number (>= 0)
    - `takeProfitPrice?`: number (>= 0)
  - `maxLeverage?`: number (0 disables)
  - `maxMarginPercentage?`: number (0-1, 0 disables)
- LeadSubscriptionLeverage:
  - `coin`: string
  - `assetId`: number
  - `type`: `cross | isolated`
  - `value`: number
- LeadSubscriptionHistory extends LeadSubscriptionParams:
  - `closedAt`: number
  - `pnl`: number (USD)

- `GET /users/:userId/subscriptions`
  - Returns an array of LeadSubscription objects.
- `PATCH /users/:userId/subscriptions/:subscriptionId`
  - Body: `{ config, leverages, positionTPSL? }`
  - Note: `config.inverseCopy` is ignored and removed server-side.
  - `positionTPSL` is merged into `config` if provided.
- `POST /users/:userId/subscriptions/:subscriptionId/close-all`
  - Returns `{ orders, activities, errors }`.
- `POST /users/:userId/subscriptions/:subscriptionId/close`
  - Body: `{ coin, percentage }`
  - `percentage` must be between `0` and `1` (default `1`)
  - Returns `{ orders, activities }`.
  - Note: partial closes may fail if trade value is below minimum.
- `GET /users/:userId/subscriptions/:subscriptionId/activities`
  - Query params:
    - `cursor` (default `0`)
    - `size` (default `10`)
  - Returns `{ activities, nextCursor, hasMore }`.
- `GET /users/:userId/subscriptions/history`
  - Returns an array of LeadSubscriptionHistory, sorted by `closedAt` desc.
