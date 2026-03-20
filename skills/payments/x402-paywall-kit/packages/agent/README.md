# @x402-kit/agent

HTTP interceptor for AI agents to auto-pay [x402](https://x402.org) crypto paywalls. Part of [x402-kit](https://github.com/tara-quinn-ai/x402-kit).

Your agent makes HTTP requests as usual. When a server returns HTTP 402 with x402 payment requirements, this interceptor automatically checks your spending policy, signs a USDC payment, and retries the request.

## Installation

```bash
npm install @x402-kit/agent
```

## Quick Start

```typescript
import { createAgentFetch } from "@x402-kit/agent";

const agentFetch = createAgentFetch({
  walletPrivateKey: process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`,
  network: "eip155:8453", // Base mainnet
  policy: {
    maxPerRequest: "1.00",       // Max 1 USDC per request
    maxDailySpend: "10.00",      // Max 10 USDC per day
    allowedNetworks: ["eip155:8453"],
    allowedAssets: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"], // USDC on Base
    requireHumanApproval: false,
  },
  logFilePath: "./payments.jsonl",
});

// Use exactly like fetch — payments happen automatically
const response = await agentFetch("https://api.example.com/premium-data");
const data = await response.json();
```

## How It Works

1. Agent sends a request to a paywalled endpoint
2. Server returns HTTP 402 with x402 payment requirements
3. `createAgentFetch` parses the requirements (amount, network, asset)
4. Policy engine checks: amount within limits? Network allowed? Domain allowed?
5. If approved: signs an EIP-3009 USDC transfer authorization
6. Retries the request with the signed payment in `X-PAYMENT` header
7. Logs the payment event to a JSONL file

## Configuration

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `walletPrivateKey` | `Hex` | Yes | Wallet private key (`0x...`) with USDC balance |
| `network` | `Network` | Yes | CAIP-2 network ID (e.g., `"eip155:8453"` for Base) |
| `policy` | `X402Policy` | Yes | Spending rules (see [@x402-kit/shared](../shared/README.md)) |
| `logFilePath?` | `string` | No | Path for payment log JSONL file |
| `spendFilePath?` | `string` | No | Path for daily spend persistence |
| `rpcUrl?` | `string` | No | Custom RPC URL (defaults to public RPC) |
| `tokenDecimals?` | `number` | No | Token decimals (default: 6 for USDC) |

## Testnet Usage

```typescript
const agentFetch = createAgentFetch({
  walletPrivateKey: process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`,
  network: "eip155:84532", // Base Sepolia testnet
  policy: {
    maxPerRequest: "0.05",
    maxDailySpend: "1.00",
    allowedNetworks: ["eip155:84532"],
    allowedAssets: ["0x036CbD53842c5426634e7929541eC2318f3dCF7e"], // USDC on Base Sepolia
    requireHumanApproval: false,
  },
});
```

Get testnet USDC from [Circle Faucet](https://faucet.circle.com) (select Base Sepolia, USDC).

## Re-exports

For users who want the bare x402 client without the policy layer:

```typescript
import { wrapFetchWithPayment } from "@x402-kit/agent";
```

## License

MIT
