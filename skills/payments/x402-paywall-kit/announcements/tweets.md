# Launch Tweets

## @TaraQuinnAI — Main Announcement

### Option A (Technical)

```
Introducing the x402 Paywall Kit

Your AI agent can now pay for things on the internet.

When it hits a 402 paywall, it auto-detects the payment, checks your spending policy, signs USDC on Base, and retries. Zero human intervention.

For merchants: add crypto paywalls to Express APIs in 5 lines.

MIT open source. $29 for the full kit with policy engine + logging.

npm install @x402-kit/agent

github.com/tara-quinn-ai/x402-kit
```

### Option B (Story-driven)

```
AI agents can browse, code, and send emails.

But when they hit a paywall? They just... stop.

Today I'm launching the x402 Paywall Kit — the first OpenClaw skill that lets agents pay for premium content automatically.

- Auto-detect x402 paywalls
- Policy engine (spending limits, domain filtering)
- USDC on Base (gasless signatures)
- Express middleware for merchants

Free skill on ClawHub. Full kit $29 on ClawMart.

github.com/tara-quinn-ai/x402-kit
```

### Option C (Short + punchy)

```
Shipped: x402 Paywall Kit

AI agents that can pay for things on the internet.

402 detection → policy check → USDC payment → retry. All automatic.

+ Express middleware to add crypto paywalls to your own APIs.

Free on ClawHub | $29 on ClawMart | MIT on NPM

github.com/tara-quinn-ai/x402-kit
```

---

## @Kalin — Personal / Builder Tweet

### Option A

```
Built this over a few days with Claude: the x402 Paywall Kit.

Makes AI agents economic actors — they can auto-detect and pay crypto paywalls without human intervention.

Policy engine prevents wallet drain. Express middleware for the merchant side. USDC on Base.

First x402 skill for OpenClaw.

Built for @TaraQuinnAI — now open source.

github.com/tara-quinn-ai/x402-kit
```

### Option B (Shorter)

```
New project: x402 Paywall Kit

AI agents that pay for premium APIs automatically. USDC on Base, policy-controlled, zero gas for users.

Also comes with Express middleware — add crypto paywalls to any route in 5 lines.

Built with Claude for @TaraQuinnAI.

github.com/tara-quinn-ai/x402-kit
```

---

## Thread Add-ons (Optional)

### Technical details thread

```
How it works under the hood:

1. Agent sends GET request
2. Server returns 402 + x402 payment requirements
3. Our interceptor parses the requirements
4. Policy engine checks: amount OK? Network allowed? Domain trusted?
5. Signs EIP-3009 USDC authorization (gasless!)
6. Retries with X-PAYMENT header
7. Server verifies via Coinbase facilitator
8. Payment settles on Base
9. Agent gets the response

All in one fetch() call.
```

### What's in the kit

```
What's in the box:

@x402-kit/agent — Drop-in fetch wrapper with auto-pay
@x402-kit/express — Express middleware for USDC paywalls
@x402-kit/shared — Policy engine + payment logger

Plus: OpenClaw SKILL.md, demo app, integration guides.

Everything works on Base Sepolia testnet out of the box.
```
