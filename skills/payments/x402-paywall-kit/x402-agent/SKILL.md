---
name: x402-agent
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

# x402 Agent Skill

Automatically detect and pay x402 crypto paywalls when your AI agent encounters HTTP 402 Payment Required responses.

## When to Activate

Activate this skill when an HTTP response returns **status 402 Payment Required** and the response body contains an `x402Version` field with an `accepts` array describing payment options.

Detection pattern:
- HTTP status code: `402`
- Response body: JSON with `x402Version` (number) and `accepts` (array of payment requirements)
- Response header: `PAYMENT-REQUIRED` (base64-encoded payment requirements)

## How to Use

### Step 1: Install

```bash
npm install @x402-kit/agent @x402-kit/shared
```

### Step 2: Set Up the Agent Fetch Wrapper

```typescript
import { createAgentFetch } from "@x402-kit/agent";

const agentFetch = createAgentFetch({
  walletPrivateKey: process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`,
  network: "eip155:8453",        // Base mainnet
  policy: {
    maxPerRequest: "1.00",       // Max 1 USDC per request
    maxDailySpend: "10.00",      // Max 10 USDC per day
    allowedNetworks: ["eip155:8453"],
    allowedAssets: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"], // USDC on Base
    requireHumanApproval: false,
  },
  logFilePath: "./x402-payments.jsonl",
});
```

### Step 3: Use as a Drop-in Fetch Replacement

```typescript
// Use agentFetch exactly like regular fetch
const response = await agentFetch("https://api.example.com/premium/data");
const data = await response.json();
```

### What Happens Internally

1. The initial request is made normally
2. If the server returns HTTP 402 with x402 payment requirements, the skill:
   - Parses the payment requirements from the response headers and body
   - Finds a matching payment option for the configured network
   - Converts the raw token amount to human-readable format
   - Checks the spending policy (per-request limit, daily limit, network/asset/domain rules)
   - If approved: signs an EIP-3009 payment authorization and retries with the `X-PAYMENT` header
   - Records the spend and logs the payment event
3. If the policy denies the payment, the original 402 response is returned without spending

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `X402_WALLET_PRIVATE_KEY` | Yes | Hex private key (with `0x` prefix) of a wallet funded with USDC on Base |

### Policy Configuration

The policy object controls what the agent is allowed to spend:

```typescript
interface X402Policy {
  maxPerRequest: string;        // Max USDC per single request (e.g., "1.00")
  maxDailySpend: string;        // Max USDC per day (e.g., "10.00")
  allowedNetworks: string[];    // CAIP-2 networks (e.g., ["eip155:8453"])
  allowedAssets: string[];      // Token contract addresses
  domainAllowlist?: string[];   // Only pay these domains (optional)
  domainDenylist?: string[];    // Never pay these domains (optional)
  requireHumanApproval: boolean;
}
```

### Supported Networks

| Network | CAIP-2 ID | USDC Address |
|---------|-----------|--------------|
| Base (mainnet) | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Base Sepolia (testnet) | `eip155:84532` | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

### Full Config Reference

```typescript
interface AgentFetchConfig {
  walletPrivateKey: Hex;        // From env: X402_WALLET_PRIVATE_KEY
  policy: X402Policy;           // Spending rules
  network: Network;             // CAIP-2 format (e.g., "eip155:8453")
  spendFilePath?: string;       // Daily spend persistence (default: ".x402/daily-spend.json")
  logFilePath?: string;         // Payment log file path
  rpcUrl?: string;              // Custom JSON-RPC URL
  tokenDecimals?: number;       // Token decimals (default: 6 for USDC)
}
```

## Examples

### Basic: Pay for Premium API Data

Agent calls `api.example.com/premium`, gets 402, pays 0.10 USDC, gets data:

```typescript
const agentFetch = createAgentFetch({
  walletPrivateKey: process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`,
  network: "eip155:8453",
  policy: {
    maxPerRequest: "0.50",
    maxDailySpend: "5.00",
    allowedNetworks: ["eip155:8453"],
    allowedAssets: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
    requireHumanApproval: false,
  },
});

const response = await agentFetch("https://api.example.com/premium/weather");
// First request returns 402 -> agent auto-pays 0.10 USDC -> retries -> gets 200 with data
```

### Domain-Restricted: Only Pay Trusted APIs

```typescript
const agentFetch = createAgentFetch({
  walletPrivateKey: process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`,
  network: "eip155:8453",
  policy: {
    maxPerRequest: "1.00",
    maxDailySpend: "20.00",
    allowedNetworks: ["eip155:8453"],
    allowedAssets: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
    domainAllowlist: ["api.trusted-service.com", "data.partner.io"],
    requireHumanApproval: false,
  },
});
```

### Testnet Development

```typescript
const agentFetch = createAgentFetch({
  walletPrivateKey: process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`,
  network: "eip155:84532",  // Base Sepolia testnet
  policy: {
    maxPerRequest: "10.00",
    maxDailySpend: "100.00",
    allowedNetworks: ["eip155:84532"],
    allowedAssets: ["0x036CbD53842c5426634e7929541eC2318f3dCF7e"], // USDC on Base Sepolia
    requireHumanApproval: false,
  },
});
```

## Safety Rules

1. **Never expose the private key.** Always load `X402_WALLET_PRIVATE_KEY` from environment variables. Never hardcode it in source files or logs.
2. **Respect spending limits.** The policy engine enforces per-request and daily limits. Configure conservative limits for production.
3. **Log all payments.** Set `logFilePath` to maintain an audit trail. The log file records every payment attempt (approved, denied, or failed) in JSONL format.
4. **Use domain filtering.** Set `domainAllowlist` or `domainDenylist` to restrict which services the agent can pay.
5. **Start with testnet.** Use Base Sepolia (`eip155:84532`) during development. Only switch to mainnet (`eip155:8453`) for production.
6. **Daily spend resets at UTC midnight.** The spend tracker persists to disk and resets automatically each day.

## Payment Log Format

Each payment event is logged as a JSON line in the log file:

```json
{
  "timestamp": "2026-02-27T12:00:00.000Z",
  "url": "https://api.example.com/premium/data",
  "amount": "0.1",
  "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "network": "eip155:8453",
  "facilitator": "",
  "success": true,
  "policyDecision": "approved"
}
```
