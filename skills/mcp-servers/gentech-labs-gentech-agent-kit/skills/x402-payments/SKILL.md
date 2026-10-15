---
name: x402-payments
description: "How to build x402 payment-gated APIs for AI agents. Covers facilitators (GoPlausible, Naven, CDP), settlement flows, session management, and multi-chain payment rails."
---

# x402 Payments for AI Agents

x402 is the HTTP-native payment standard. When an agent hits an endpoint without payment, the server returns `402 Payment Required` with a challenge. The agent signs the payment and retries. The server verifies and serves the resource.

## Payment Flow

```
Agent                    Server                   Facilitator
  │                        │                          │
  ├── GET /api/data ──────►│                          │
  │◄── 402 Payment ───────┤                          │
  │     Required           │                          │
  │                        │                          │
  ├── POST /facilitator/verify ──────────────────────►│
  │◄── Verified + Receipt ───────────────────────────┤
  │                        │                          │
  ├── GET /api/data ──────►│                          │
  │     (x402 header)      │                          │
  │◄── 200 OK + Data ─────┤                          │
```

## Supported Networks

| Network | Facilitator | Token | Chain ID |
|---------|-------------|-------|----------|
| Algorand | GoPlausible | ALGO | algorand:localnet |
| Robinhood Chain | Naven Network | USDG | `eip155:4663` |
| Base | CDP Facilitator | USDC | `eip155:8453` |

## GenTech Kit Tools

```python
from gentech_agent_kit.plugins.algorand_x402 import register_gentech_plugin
from gentech_agent_kit.plugins.robinhood_x402 import register_gentech_plugin
```

Tools auto-discovered. No manual config needed.

## Session Management

Payments open a 60-minute session. Session token (HMAC-signed) is passed on subsequent calls:

```python
session = algorand_verify_payment(payment_proof)
# session_token = "agent_1234567890_abc123:1712345678:signature"
data = algorand_get_quote("BTC", session_token=session_token)
```

## Pricing Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Exact | Fixed price per call | $0.001 USDG per quote |
| Tiered | Different prices for different data | $0.001 crypto, $0.005 stocks |
| Subscription | Batch pricing, session-based | 10 queries for $0.01 |

## Best Practices

- Always validate session tokens before serving paid data
- Return clear 402 errors with machine-readable challenge bodies
- Log all payment verifications for audit trails
- Use the Output Enforcer to validate paid response schemas
