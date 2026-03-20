---
name: derivatives-trading-portfolio-margin-pro
description: Binance Derivatives-trading-portfolio-margin-pro request using the Binance API. Authentication requires API key and secret key. 
metadata:
  version: 1.0.0
  author: Binance
license: MIT
---

# Binance Derivatives-trading-portfolio-margin-pro Skill

Derivatives-trading-portfolio-margin-pro request on Binance using authenticated API endpoints. Requires API key and secret key for certain endpoints. Return the result in JSON format.

## Quick Reference

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/sapi/v1/portfolio/bnb-transfer` (POST) | BNB transfer(USER_DATA) | amount, transferSide | recvWindow | Yes |
| `/sapi/v1/portfolio/repay-futures-switch` (POST) | Change Auto-repay-futures Status(TRADE) | autoRepay | recvWindow | Yes |
| `/sapi/v1/portfolio/repay-futures-switch` (GET) | Get Auto-repay-futures Status(USER_DATA) | None | recvWindow | Yes |
| `/sapi/v1/portfolio/repay` (POST) | Portfolio Margin Pro Bankruptcy Loan Repay | None | from, recvWindow | Yes |
| `/sapi/v1/portfolio/auto-collection` (POST) | Fund Auto-collection(USER_DATA) | None | recvWindow | Yes |
| `/sapi/v1/portfolio/asset-collection` (POST) | Fund Collection by Asset(USER_DATA) | asset | recvWindow | Yes |
| `/sapi/v2/portfolio/account` (GET) | Get Portfolio Margin Pro SPAN Account Info(USER_DATA) | None | recvWindow | Yes |
| `/sapi/v1/portfolio/account` (GET) | Get Portfolio Margin Pro Account Info(USER_DATA) | None | recvWindow | Yes |
| `/sapi/v1/portfolio/balance` (GET) | Get Portfolio Margin Pro Account Balance(USER_DATA) | None | asset, recvWindow | Yes |
| `/sapi/v1/portfolio/delta-mode` (GET) | Get Delta Mode Status(USER_DATA) | None | recvWindow | Yes |
| `/sapi/v1/portfolio/delta-mode` (POST) | Switch Delta Mode(TRADE) | deltaEnabled | recvWindow | Yes |
| `/sapi/v1/portfolio/earn-asset-balance` (GET) | Get Transferable Earn Asset Balance for Portfolio Margin (USER_DATA) | asset, transferType | recvWindow | Yes |
| `/sapi/v1/portfolio/pmLoan` (GET) | Query Portfolio Margin Pro Bankruptcy Loan Amount(USER_DATA) | None | recvWindow | Yes |
| `/sapi/v1/portfolio/interest-history` (GET) | Query Portfolio Margin Pro Negative Balance Interest History(USER_DATA) | None | asset, startTime, endTime, size, recvWindow | Yes |
| `/sapi/v1/portfolio/pmloan-history` (GET) | Query Portfolio Margin Pro Bankruptcy Loan Repay History(USER_DATA) | None | startTime, endTime, current, size, recvWindow | Yes |
| `/sapi/v1/portfolio/repay-futures-negative-balance` (POST) | Repay futures Negative Balance(USER_DATA) | None | from, recvWindow | Yes |
| `/sapi/v1/portfolio/earn-asset-transfer` (POST) | Transfer LDUSDT/RWUSD for Portfolio Margin(TRADE) | asset, transferType, amount | recvWindow | Yes |
| `/sapi/v1/portfolio/collateralRate` (GET) | Portfolio Margin Collateral Rate(MARKET_DATA) | None | None | No |
| `/sapi/v1/portfolio/margin-asset-leverage` (GET) | Get Portfolio Margin Asset Leverage(USER_DATA) | None | None | Yes |
| `/sapi/v2/portfolio/collateralRate` (GET) | Portfolio Margin Pro Tiered Collateral Rate(USER_DATA) | None | recvWindow | Yes |
| `/sapi/v1/portfolio/asset-index-price` (GET) | Query Portfolio Margin Asset Index Price (MARKET_DATA) | None | asset | No |

---

## Parameters

### Common Parameters

* **amount**:  (e.g., 1.0)
* **transferSide**: "TO_UM","FROM_UM"
* **recvWindow**:  (e.g., 5000)
* **autoRepay**: Default: `true`; `false` for turn off the auto-repay futures negative balance function (e.g., true)
* **from**: SPOT or MARGIN，default SPOT (e.g., SPOT)
* **asset**: `LDUSDT` and `RWUSD`
* **asset**: 
* **transferType**: `EARN_TO_FUTURE` /`FUTURE_TO_EARN`
* **startTime**:  (e.g., 1623319461670)
* **endTime**:  (e.g., 1641782889000)
* **size**: Default:10 Max:100 (e.g., 10)
* **current**: Currently querying page. Start from 1. Default:1 (e.g., 1)
* **deltaEnabled**: `true` to enable Delta mode; `false` to disable Delta mode


## Authentication

For endpoints that require authentication, you will need to provide Binance API credentials.
Required credentials:

* apiKey: Your Binance API key (for header)
* secretKey: Your Binance API secret (for signing)

Base URLs:
* Mainnet: https://api.binance.com

## Security

### Share Credentials

Users can provide Binance API credentials by sending a file where the content is in the following format:

```bash
abc123...xyz
secret123...key
```

### Never Disclose API Key and Secret

Never disclose the location of the API key and secret file.

Never send the API key and secret to any website other than Mainnet and Testnet.

### Never Display Full Secrets

When showing credentials to users:
- **API Key:** Show first 5 + last 4 characters: `su1Qc...8akf`
- **Secret Key:** Always mask, show only last 5: `***...aws1`

Example response when asked for credentials:
Account: main
API Key: su1Qc...8akf
Secret: ***...aws1

### Listing Accounts

When listing accounts, show names and environment only — never keys:
Binance Accounts:
* main (Mainnet)
* futures-keys (Mainnet)

### Transactions in Mainnet

When performing transactions in mainnet, always confirm with the user before proceeding by asking them to write "CONFIRM" to proceed.

---

## Binance Accounts

### main
- API Key: your_mainnet_api_key
- Secret: your_mainnet_secret

### TOOLS.md Structure

```bash
## Binance Accounts

### main
- API Key: abc123...xyz
- Secret: secret123...key
- Description: Primary trading account


### futures-keys
- API Key: futures789...def
- Secret: futuressecret...uvw
- Description: Futures trading account
```

## Agent Behavior

1. Credentials requested: Mask secrets (show last 5 chars only)
2. Listing accounts: Show names and environment, never keys
3. Account selection: Ask if ambiguous, default to main
4. When doing a transaction in mainnet, confirm with user before by asking to write "CONFIRM" to proceed
5. New credentials: Prompt for name, environment, signing mode

## Adding New Accounts

When user provides new credentials:

* Ask for account name
* Store in `TOOLS.md` with masked display confirmation 

## Signing Requests

For trading endpoints that require a signature:

1. Build query string with all parameters, including the timestamp (Unix ms).
2. Percent-encode the parameters using UTF-8 according to RFC 3986.
3. Sign query string with secretKey using HMAC SHA256, RSA, or Ed25519 (depending on the account configuration).
4. Append signature to query string.
5. Include `X-MBX-APIKEY` header.

Otherwise, do not perform steps 3–5.

## User Agent Header

Include `User-Agent` header with the following string: `binance-derivatives-trading-portfolio-margin-pro/1.0.0 (Skill)`

See [`references/authentication.md`](./references/authentication.md) for implementation details.
