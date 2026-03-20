# GoldRush x402 Overview

## Quick Reference

| Item | Value |
|------|-------|
| **Base URL** | `https://x402.goldrush.dev/v1` |
| **Protocol** | x402 (HTTP 402 Payment Required) |
| **Authentication** | None — wallet-based micropayments replace API keys |
| **Payment Network** | Base Sepolia testnet (Base mainnet coming soon) |
| **Payment Method** | Stablecoins on Base |
| **Rate Limit** | 100 requests/minute per wallet |
| **Available Endpoints** | 60+ Foundational API endpoints |
| **Client Libraries** | `@x402/core`, `@x402/evm` |

## Pricing Model

- **Fixed-Price:** One price per call (e.g., token balances, NFT holdings)
- **Tiered Pricing:** For variable-length data — Small (1-50), Medium (51-200), Large (201-500), XL (501+)
- **Response Caching:** Cached responses cost less (TTLs: 30s for balances, 5m for pricing)

## Response Headers

```
X-Pricing-Model: fixed
X-Base-Price: 0.000001
X-Cache: MISS
X-RateLimit-Remaining: 97
```

---

GoldRush x402 lets you access the full GoldRush blockchain data API by paying per request using the [x402 protocol](https://x402.org). No account, no API key, no billing page - just pay for exactly what you use, directly from a wallet.

> **Note:** GoldRush x402 is live on **Base Sepolia testnet**. Mainnet support is coming soon.

## What is x402?

HTTP status code `402 Payment Required` has existed since 1997, reserved for "future use." The [x402 protocol](https://x402.org) makes it real - enabling native payments over HTTP using stablecoins.

When you call a GoldRush x402 endpoint without payment, the server responds with `402 Payment Required` along with payment instructions. Your client pays using stablecoins on Base, retries the request with proof of payment, and gets the data - all in a single request-response cycle.

## How it works

GoldRush x402 is a transparent reverse proxy in front of `api.covalenthq.com`. It exposes the same paths and returns the same responses - the only difference is how you authenticate. Instead of an API key, you attach a micropayment.

```
Your App -- x402 payment --> GoldRush x402 Proxy --> api.covalenthq.com
                                    |
                              validates request
                              verifies payment
                              caches response
                              returns data
```

The proxy validates your request **before** charging you. If the chain doesn't exist, the address is malformed, or the endpoint doesn't support that network - you get a clear error and pay nothing.

## What's supported

- **60+ endpoints** covering balances, NFTs, transactions, blocks, DEX data, pricing, security, and cross-chain operations
- **100+ blockchain networks** including Ethereum, Base, Arbitrum, Optimism, Polygon, Solana, Bitcoin, and more
- **Response caching** with intelligent TTLs (30s for balances, 5m for pricing data) - cached responses cost less
- **Per-wallet rate limiting** at 100 requests per minute
- **Request validation** before payment - you never pay for a request that would fail

## Pricing

Every endpoint has a credit rate. The price per call is:

```
Price = creditRate x $0.000001
```

### Fixed pricing

Most endpoints have a fixed cost per request. Token balances, NFT holdings, block details - one price, one call, one response.

### Dynamic pricing

Endpoints that return variable-length data (transaction histories, event logs) use tiered pricing. You select a tier upfront based on how much data you expect:

| Tier   | Items    | You pay for ... |
|--------|----------|----------------------|
| Small  | 1-50     | 50 items             |
| Medium | 51-200   | 200 items            |
| Large  | 201-500  | 500 items            |
| XL     | 501+     | 1000 items           |

If the response contains fewer items than your tier covers, you overpaid slightly but get the data immediately. If it contains more, you get a `402` telling you exactly which tier you need.

## x402 vs API key

**x402 (Pay-per-call):** - No signup or account needed
  - Pay per request with a wallet
  - Ideal for AI agents and autonomous workflows
  - Live on Base Sepolia testnet

**API Key (Subscription):** - Predictable monthly cost
  - API key for any project
  - Ideal for apps with steady usage
  - For Vibe Coders or Teams

Both paths give you the same data, the same endpoints, and the same response format. Pick the one that fits how you build.

---

## 1. Discover endpoints (free)

The discovery API requires no payment. Use it to explore available endpoints and pricing.

```bash
# List all endpoints with pricing
curl https://x402.goldrush.dev/v1/x402/endpoints | jq

# Search for specific functionality
curl https://x402.goldrush.dev/v1/x402/search?q=balance | jq

# Get details for a specific endpoint
curl https://x402.goldrush.dev/v1/x402/endpoints/get-token-balances-for-address | jq
```

Every endpoint returns its credit rate, pricing model, supported chains, and x402 payment instructions.

## 2. Set up a wallet

You need a wallet with testnet USDC on Base Sepolia. You'll use the wallet's private key to sign x402 payments.

Never commit your private key to source control. Use environment variables or a secrets manager.

```bash
export WALLET_PRIVATE_KEY="your-base-sepolia-private-key"
```

## 3. Install the x402 client

```bash npm
npm install @x402/core @x402/evm
```

```bash yarn
yarn add @x402/core @x402/evm
```

## 4. Make your first request

```typescript
import { HTTPClient } from "@x402/core";
import { ExactEvmScheme } from "@x402/evm";

const client = new HTTPClient({
  scheme: new ExactEvmScheme({
    network: "eip155:84532", // Base Sepolia (testnet)
    privateKey: process.env.WALLET_PRIVATE_KEY,
  }),
});

// Get token balances - payment is handled automatically
const balances = await client.get(
  "https://x402.goldrush.dev/v1/eth-mainnet/address/demo.eth/balances_v2/"
);

console.log(balances);
```

The x402 client handles the full payment flow: if a request gets a `402`, it reads the payment instructions, signs a transaction, and retries. From your code's perspective, it's just a GET request.

## 5. Use tiers for variable-length data

Endpoints with dynamic pricing (transactions, event logs) require a `tier` parameter:

```typescript
// Get transactions with tier selection
const txns = await client.get(
  "https://x402.goldrush.dev/v1/eth-mainnet/address/demo.eth/transactions_v3/?tier=medium"
);
```

| Tier   | Items    |
|--------|----------|
| Small  | up to 50     |
| Medium | up to 200    |
| Large  | up to 500    |
| XL     | up to 1000   |

If your selected tier is too small for the response, you'll get a `402` indicating the correct tier.

## Response headers

Every paid response includes pricing metadata:

```
X-Pricing-Model: fixed
X-Base-Price: 0.000001
X-Cache: MISS
X-RateLimit-Remaining: 97
```

For dynamic-priced endpoints, you also get:

```
X-Item-Count: 42
X-Actual-Price: 0.000042
X-Paid-Price: 0.000050
X-Selected-Tier: small
```