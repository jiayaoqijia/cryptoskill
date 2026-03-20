---
name: x402-agent-free
description: Detect and pay x402 crypto paywalls automatically. When your agent
  gets a 402 Payment Required response with x402 JSON, this skill handles payment
  via Coinbase facilitator on Base network with USDC. Use when agent hits paid
  APIs, premium content, or any x402-enabled endpoint.
version: 1.0.0
homepage: https://taraquinn.ai
metadata:
  openclaw:
    emoji: "\U0001F4B0"
    homepage: "https://taraquinn.ai"
    requires:
      env:
        - X402_WALLET_PRIVATE_KEY
      bins:
        - node
    primaryEnv: X402_WALLET_PRIVATE_KEY
---

# x402 Agent Skill (Free)

Automatically detect and pay x402 crypto paywalls when your AI agent encounters HTTP 402 Payment Required responses.

This is the **free community edition**. It covers basic x402 detect-and-pay using the upstream `@x402/fetch` package. For the full kit with policy engine, spending limits, domain filtering, payment logging, Express middleware, and a demo app, see [x402 Paywall Kit on ClawMart](https://www.shopclawmart.com/listings/x402-paywall-kit).

## When to Activate

Activate this skill when an HTTP response returns **status 402 Payment Required** and the response body contains an `x402Version` field with an `accepts` array describing payment options.

Detection pattern:
- HTTP status code: `402`
- Response body: JSON with `x402Version` (number) and `accepts` (array of payment requirements)
- Response header: `PAYMENT-REQUIRED` (base64-encoded payment requirements)

## How to Use

### Step 1: Install

```bash
npm install @x402/fetch @x402/evm viem
```

### Step 2: Set Up the x402 Fetch Wrapper

```typescript
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";
import { wrapFetchWithPayment } from "@x402/fetch";
import { toClientEvmSigner, ExactEvmScheme } from "@x402/evm";

// Load wallet from environment (never hardcode!)
const account = privateKeyToAccount(process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`);

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(),
});

const signer = toClientEvmSigner(
  {
    address: account.address,
    signTypedData: (message) => walletClient.signTypedData(message),
  },
  walletClient,
);

const x402Fetch = wrapFetchWithPayment(fetch, {
  schemes: [new ExactEvmScheme(signer)],
});
```

### Step 3: Use as a Drop-in Fetch Replacement

```typescript
// x402Fetch handles 402 responses automatically:
// detects paywall → signs payment → retries with X-PAYMENT header
const response = await x402Fetch("https://api.example.com/premium/data");
const data = await response.json();
```

### What Happens Internally

1. The initial request is made normally
2. If the server returns HTTP 402 with x402 payment requirements:
   - Parses the payment requirements from the response
   - Signs an EIP-3009 USDC transfer authorization
   - Retries the request with the signed `X-PAYMENT` header
3. Returns the successful response

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `X402_WALLET_PRIVATE_KEY` | Yes | Hex private key (with `0x` prefix) of a wallet funded with USDC on Base |

### Supported Networks

| Network | Chain | USDC Address |
|---------|-------|--------------|
| Base (mainnet) | `base` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Base Sepolia (testnet) | `baseSepolia` | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

## Example

```typescript
// Agent calls a paid API — payment happens automatically
const response = await x402Fetch("https://api.example.com/premium/weather");

if (response.ok) {
  const data = await response.json();
  console.log("Got premium data:", data);
} else if (response.status === 402) {
  console.log("Payment failed — check wallet balance");
} else {
  console.log("Request failed:", response.status);
}
```

## Safety Rules

1. **Never expose the private key.** Always load `X402_WALLET_PRIVATE_KEY` from environment variables.
2. **Start with testnet.** Use Base Sepolia during development. Switch to mainnet for production.
3. **Monitor spending.** This free edition does not include spending limits. Monitor your wallet balance manually.

## Want More Control?

The **[x402 Paywall Kit](https://www.shopclawmart.com/listings/x402-paywall-kit)** ($29) adds:

- **Policy engine** — per-request limits, daily spending caps, domain allow/deny lists
- **Payment logging** — JSONL audit trail for every transaction
- **Express middleware** — add USDC paywalls to your own APIs in minutes
- **Demo app** — working paywalled API + agent on testnet
- **Domain filtering** — restrict which services your agent can pay

NPM packages: `@x402-kit/agent`, `@x402-kit/express`, `@x402-kit/shared`

Available on [ClawMart](https://www.shopclawmart.com/listings/x402-paywall-kit) and [taraquinn.ai](https://taraquinn.ai).
