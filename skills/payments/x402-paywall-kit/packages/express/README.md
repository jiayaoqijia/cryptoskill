# @x402-kit/express

Enhanced Express middleware for [x402](https://x402.org) crypto paywalls with simplified config and payment logging. Part of [x402-kit](https://github.com/tara-quinn-ai/x402-kit).

Add USDC paywalls to your Express API routes in a few lines. Wraps the upstream `@x402/express` middleware with a friendlier config format and automatic payment logging.

## Installation

```bash
npm install @x402-kit/express express
```

## Quick Start

```typescript
import express from "express";
import { x402EnhancedMiddleware } from "@x402-kit/express";

const app = express();

app.use(
  x402EnhancedMiddleware({
    routes: {
      "GET /api/premium": {
        price: "$0.50",
        recipient: "0xYourWalletAddress",
        network: "eip155:8453", // Base mainnet
        description: "Premium API access",
      },
    },
    logFilePath: "./payments.jsonl",
  }),
);

app.get("/api/premium", (req, res) => {
  // Only reached after successful payment
  res.json({ data: "premium content" });
});

app.listen(3000);
```

## How It Works

1. Unauthenticated requests to protected routes get HTTP 402 with x402 payment requirements
2. Client signs a USDC payment and retries with `X-PAYMENT` header
3. Middleware verifies the payment via the Coinbase facilitator
4. On success: settles the payment on-chain and passes the request through
5. Payment events are logged to a JSONL file

## Configuration

### Route Config

```typescript
x402EnhancedMiddleware({
  routes: {
    "GET /api/data": {
      price: "$0.10",              // Price with $ prefix
      recipient: "0xWallet...",     // Wallet that receives payment
      network: "eip155:8453",      // CAIP-2 network ID (optional, defaults to Base)
      description: "API data",     // Human-readable description
      mimeType: "application/json", // Response MIME type
      maxTimeoutSeconds: 60,       // Payment timeout
    },
    "POST /api/generate": {
      price: "$1.00",
      recipient: "0xWallet...",
    },
  },
});
```

### Single Route Shorthand

```typescript
// Apply the same pricing to all routes handled by this middleware
x402EnhancedMiddleware({
  routes: {
    price: "$0.50",
    recipient: "0xWallet...",
  },
});
```

### Full Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `routes` | `Record<string, RoutePaymentConfig>` or `RoutePaymentConfig` | Yes | Route-level or global payment config |
| `logFilePath?` | `string` | No | Path for payment log JSONL file |
| `facilitatorUrl?` | `string` | No | Custom facilitator URL (defaults to Coinbase) |
| `paywallConfig?` | `object` | No | Paywall page customization |
| `paywallConfig.appName?` | `string` | No | App name shown on paywall page |
| `paywallConfig.appLogo?` | `string` | No | App logo URL |
| `paywallConfig.testnet?` | `boolean` | No | Enable testnet mode |

## Testnet Usage

```typescript
app.use(
  x402EnhancedMiddleware({
    routes: {
      "GET /api/joke": {
        price: "$0.01",
        recipient: "0xYourAddress",
        network: "eip155:84532", // Base Sepolia
      },
    },
    paywallConfig: { testnet: true },
  }),
);
```

## Re-exports

For users who need lower-level control:

```typescript
import { paymentMiddleware } from "@x402-kit/express";
```

## License

MIT
