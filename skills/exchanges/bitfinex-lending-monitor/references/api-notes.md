# Bitfinex API Notes (Funding Monitor)

This skill is built on Bitfinex API v2 authenticated endpoints.

## Confirmed endpoints

- `POST /v2/auth/r/wallets`
  - Returns wallets including funding wallet with:
    - `TYPE` (`funding`)
    - `BALANCE`
    - `UNSETTLED_INTEREST`
    - `AVAILABLE_BALANCE`

- `POST /v2/auth/r/funding/credits/{Symbol}`
  - Example symbol: `fUSD`
  - Returns active funding credits with amount, status, rate, payout timestamp.

- `POST /v2/auth/r/ledgers/{Currency}/hist`
  - Example currency: `USD`
  - Supports filters: `start`, `end`, `limit`, `wallet`
  - Use `wallet=funding` to focus on funding ledger entries.
  - Ledger descriptions include interest/funding clues for收益统计.

## API auth

Headers:

- `bfx-apikey`
- `bfx-nonce`
- `bfx-signature`

Signature format in this script:

- payload: `"/api" + path + nonce + rawBody`
- HMAC-SHA384 with API secret

## Permissions suggestion

Create a dedicated read-only API key for reporting:

- Wallet read
- Funding read
- Ledger/history read

Avoid trading/withdraw permissions for this monitor.
