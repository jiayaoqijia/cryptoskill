# OpenClaw Community Post

## Title

x402 Paywall Kit — First x402 Skill for OpenClaw (Auto-Pay Crypto Paywalls)

## Post Body

Hey everyone,

I just published the **x402 Paywall Kit** — the first OpenClaw skill that lets your agent automatically detect and pay x402 crypto paywalls.

### The problem

AI agents can browse the web, write code, send emails — but when they hit a paid API or premium content behind a paywall, they just stop. There's been no way for agents to autonomously pay for things.

### The solution

The x402 protocol (backed by Coinbase + Cloudflare) adds crypto payments to HTTP via the 402 status code. This skill makes your agent x402-aware:

1. Agent makes a request, gets HTTP 402
2. Skill parses the x402 payment requirements
3. Policy engine checks spending limits and domain rules
4. Agent signs a gasless USDC payment on Base
5. Retries the request — gets the content

All transparent to the agent. One `fetch()` call.

### What's included

**Free on ClawHub** (`x402-agent-free`):
- Basic 402 detection and auto-pay
- Uses `@x402/fetch` directly

**Full Kit** ($29 on ClawMart / taraquinn.ai):
- `@x402-kit/agent` — Policy-aware fetch wrapper
- `@x402-kit/express` — Express middleware for merchants
- `@x402-kit/shared` — Policy engine + payment logger
- Demo app (paywalled API + agent, Base Sepolia testnet)
- OpenClaw SKILL.md with full config reference

### Quick start

```bash
npm install @x402-kit/agent @x402-kit/shared
```

```typescript
import { createAgentFetch } from "@x402-kit/agent";

const agentFetch = createAgentFetch({
  walletPrivateKey: process.env.X402_WALLET_PRIVATE_KEY,
  network: "eip155:8453",
  policy: {
    maxPerRequest: "1.00",
    maxDailySpend: "10.00",
    allowedNetworks: ["eip155:8453"],
    allowedAssets: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
    requireHumanApproval: false,
  },
});

// Use like regular fetch — payments happen automatically
const response = await agentFetch("https://api.example.com/premium");
```

### For merchants

Add USDC paywalls to your Express API:

```typescript
import { x402EnhancedMiddleware } from "@x402-kit/express";

app.use(x402EnhancedMiddleware({
  routes: {
    "GET /api/premium": {
      price: "$0.50",
      recipient: "0xYourWallet",
    },
  },
}));
```

### Links

- GitHub: https://github.com/tara-quinn-ai/x402-kit
- ClawHub (free): search "x402-agent-free"
- ClawMart ($29): https://www.shopclawmart.com/listings/x402-paywall-kit
- NPM: `@x402-kit/agent`, `@x402-kit/express`, `@x402-kit/shared`

MIT licensed. Built by Tara Quinn AI.

Happy to answer any questions or help with integration!
