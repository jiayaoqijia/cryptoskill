# @x402-kit/shared

Shared types, policy engine, and payment logger for [x402-kit](https://github.com/tara-quinn-ai/x402-kit) — crypto payments for AI agents and Express middleware.

## Installation

```bash
npm install @x402-kit/shared
```

## Policy Engine

Evaluate payment requests against configurable spending rules.

```typescript
import { evaluate, createPolicyEngine } from "@x402-kit/shared";
import type { X402Policy } from "@x402-kit/shared";

const policy: X402Policy = {
  maxPerRequest: "1.00",
  maxDailySpend: "10.00",
  allowedNetworks: ["eip155:8453"],
  allowedAssets: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"], // USDC on Base
  requireHumanApproval: false,
};

// Pure function — pass current daily spend explicitly
const result = evaluate("0.50", "eip155:8453", "0x833589f...", "api.example.com", policy, 2.0);
// { decision: "approved" }

// Stateful engine — tracks daily spend automatically
const engine = createPolicyEngine(policy, { spendFilePath: "./spend.json" });
const decision = engine.evaluate("0.50", "eip155:8453", "0x833589f...", "api.example.com");
engine.recordSpend("0.50");
```

### Policy Options

| Field | Type | Description |
|-------|------|-------------|
| `maxPerRequest` | `string` | Max amount per single payment (e.g., `"1.00"`) |
| `maxDailySpend` | `string` | Max cumulative amount per day (e.g., `"10.00"`) |
| `allowedNetworks` | `string[]` | Allowed CAIP-2 network IDs (e.g., `["eip155:8453"]`) |
| `allowedAssets` | `string[]` | Allowed token contract addresses |
| `domainAllowlist?` | `string[]` | If set, only pay these domains |
| `domainDenylist?` | `string[]` | If set, never pay these domains |
| `requireHumanApproval` | `boolean` | Return `"needs-human-approval"` instead of `"denied"` for limit violations |

## Payment Logger

Append-only JSONL logger for payment events.

```typescript
import { createPaymentLogger } from "@x402-kit/shared";

const logger = createPaymentLogger("./payments.jsonl");

logger.log({
  timestamp: new Date().toISOString(),
  url: "https://api.example.com/data",
  amount: "0.50",
  asset: "USDC",
  network: "eip155:8453",
  facilitator: "https://x402.org/facilitator",
  txHash: "0xabc...",
  success: true,
  policyDecision: "approved",
});

const entries = logger.getEntries(); // Read all logged payments
```

## Types

Re-exports upstream `@x402/core` types plus kit-specific interfaces.

```typescript
import type {
  X402Policy,
  PolicyDecision,
  EvaluateResult,
  X402PaymentLog,
  X402KitConfig,
  PaymentRequirements,
  Network,
} from "@x402-kit/shared";
```

## Sub-path Exports

```typescript
import { evaluate } from "@x402-kit/shared/policy";
import { createPaymentLogger } from "@x402-kit/shared/logger";
import type { X402Policy } from "@x402-kit/shared/types";
```

## License

MIT
