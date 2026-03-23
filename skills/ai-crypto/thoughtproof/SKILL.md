---
name: thoughtproof-reasoning-check
description: Verify whether an AI agent's decision is well-reasoned before executing. Adversarial multi-model critique (Claude, Grok, DeepSeek) returns ALLOW or HOLD with a JWKS-signed attestation. Use before any high-value trade, autonomous action, or agent-to-agent payment.
metadata: {"openclaw":{"emoji":"🧠","homepage":"https://thoughtproof.ai","primaryEnv":"THOUGHTPROOF_API_KEY"}}
---

# ThoughtProof Reasoning Verification

Adversarial multi-model reasoning check before agent actions settle. Claude, Grok, and DeepSeek challenge each other on every decision — returns ALLOW or HOLD with confidence score and EdDSA-signed attestation.

## Quick Test with purl

```bash
purl -X POST https://api.thoughtproof.ai/v1/check \
  -H "Content-Type: application/json" \
  -d '{"claim": "Swap $2K USDC to ETH. ETH at $2180, RSI 34, 6% below 30d MA.", "stakeLevel": "medium", "domain": "financial"}'
```

[purl](https://purl.dev) handles x402 payment automatically. No manual payment flow needed.

## SDK

```bash
npm install thoughtproof-sdk
```

```javascript
import { check } from 'thoughtproof-sdk';

const result = await check({
  claim: "Swap $2K USDC to ETH. RSI 34, 6% below 30d MA.",
  stakeLevel: "medium",
  domain: "financial"
});

if (result.verdict === "ALLOW") {
  // execute the trade
} else if (result.paymentRequired) {
  // pay $0.05 USDC on Base, then retry
} else {
  // HOLD — material defects found, review reasoning
}
```

## Verdict Reference

| Verdict | Meaning | Action |
|---------|---------|--------|
| `ALLOW` | Reasoning is sound | Execute |
| `HOLD` | Material defects found | Do not execute, review |
| `UNCERTAIN` | Insufficient evidence | Gather more context |
| `DISSENT` | Models strongly disagree | Require human review |

## Pricing (stake-proportional, USDC on Base)

| Stake Level | Cost | Use case |
|-------------|------|----------|
| `low` | $0.008-$0.02 | Swaps under $2K |
| `medium` | $0.02-$0.05 | Trades $2K-$10K |
| `high` | $0.05-$0.15 | Large trades $10K-$25K |
| `critical` | $0.15-$1.00 | High-value trades over $25K |

## Multi-Attestation Stack

ThoughtProof is the `reasoning_integrity` layer in the Combined Attestation Format:

- InsumerAPI → wallet_state (does the agent have the assets?)
- RNWY → behavioral_trust (is the agent trustworthy?)
- **ThoughtProof → reasoning_integrity (is the decision sound?)**
- Maiat → job_performance (does the agent deliver?)

Reference verifier: [github.com/douglasborthwick-crypto/insumer-examples](https://github.com/douglasborthwick-crypto/insumer-examples)

## Links

- API: https://api.thoughtproof.ai/v1/check
- Skill: https://thoughtproof.ai/skill.md
- JWKS: https://api.thoughtproof.ai/.well-known/jwks.json
- MCP: `npx thoughtproof-mcp`
- ERC-8004: Agent #28388 on Base mainnet
