# x402 Paywall Kit

Crypto payments for AI agents and websites. OpenClaw skill + Express middleware for USDC payments on Base.

Your AI agent hits a paywall — and pays for it automatically. Your website accepts crypto — in 5 lines of code.

## What's Inside

| Package | Description | Install |
|---------|-------------|---------|
| [`@x402-kit/agent`](packages/agent) | HTTP interceptor — auto-detect and pay x402 paywalls | `npm i @x402-kit/agent` |
| [`@x402-kit/express`](packages/express) | Express middleware — add USDC paywalls to any route | `npm i @x402-kit/express` |
| [`@x402-kit/shared`](packages/shared) | Policy engine, payment logger, shared types | `npm i @x402-kit/shared` |

## For AI Agents: Auto-Pay Paywalls

```typescript
import { createAgentFetch } from "@x402-kit/agent";

const agentFetch = createAgentFetch({
  walletPrivateKey: process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`,
  network: "eip155:8453", // Base mainnet
  policy: {
    maxPerRequest: "1.00",
    maxDailySpend: "10.00",
    allowedNetworks: ["eip155:8453"],
    allowedAssets: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
    requireHumanApproval: false,
  },
});

// Use like regular fetch — payments happen automatically
const response = await agentFetch("https://api.example.com/premium/data");
```

When the server returns HTTP 402, the interceptor:
1. Parses x402 payment requirements
2. Checks your spending policy (amount, network, domain)
3. Signs a gasless EIP-3009 USDC authorization
4. Retries with the `X-PAYMENT` header
5. Returns the response

## For Websites: Accept USDC Payments

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
        network: "eip155:8453",
      },
    },
  }),
);

app.get("/api/premium", (req, res) => {
  res.json({ data: "premium content" });
});
```

## Policy Engine

Control what your agent is allowed to spend:

- **Per-request limits** — max USDC per single payment
- **Daily spending caps** — cumulative daily maximum
- **Network restrictions** — only pay on approved chains
- **Asset restrictions** — only pay with approved tokens
- **Domain filtering** — allowlist or denylist specific domains
- **Human approval** — require manual approval above thresholds

## Demo

A runnable demo with a paywalled Express API and an agent that pays for it. See [`demo/README.md`](demo/README.md).

```bash
# Terminal 1: Start the paywalled server
export X402_PAYTO_ADDRESS="0xYourAddress"
npx tsx demo/server.ts

# Terminal 2: Run the agent
export X402_WALLET_PRIVATE_KEY="0xYourPrivateKey"
npx tsx demo/agent.ts
```

## Development

```bash
# Install dependencies
npm install

# Build all packages
npm run build

# Run tests (49 tests)
npm test

# Type check
npm run typecheck
```

## Architecture

```
@x402-kit (our value-add layer)
├── @x402-kit/agent      — Policy-aware fetch wrapper + auto-pay
├── @x402-kit/express    — Enhanced middleware with logging hooks
└── @x402-kit/shared     — Policy engine + payment logger + types
         │
    Wraps @x402/* v2.5.0 (Coinbase official packages)
         │
    Coinbase x402 Facilitator (verify + settle on Base)
```

We wrap Coinbase's official `@x402/*` packages. We don't rebuild protocol or facilitator logic — we add the agent intelligence layer: policy engine, spending controls, payment logging, and simplified middleware config.

## Stack

- **TypeScript** — strict mode, dual CJS/ESM builds via tsup
- **Base** (Ethereum L2) — low fees, fast settlement
- **USDC** — stablecoin payments
- **Coinbase x402** — payment protocol and facilitator
- **Vitest** — 49 unit tests
- **npm workspaces** — monorepo with 3 packages

## Links

- [OpenClaw Skill (free)](x402-agent-free/) — basic detect+pay on ClawHub
- [OpenClaw Skill (full)](x402-agent/) — with policy engine + logging
- [Demo](demo/) — paywalled API + agent on Base Sepolia
- [PRD](docs/PRD.md) — full product requirements

## License

MIT
