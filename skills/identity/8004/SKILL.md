---
name: 8004
description: ERC-8004 Agent Trust Protocol for AI agent identity, reputation, and validation on Celo. Use when building AI agents that need identity registration, reputation tracking, or trust verification across organizational boundaries.
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# ERC-8004: Agent Trust Protocol

ERC-8004 establishes trust infrastructure for autonomous AI agents, enabling them to discover, identify, and evaluate other agents across organizational boundaries.

## When to Use

- Registering an AI agent's identity on-chain
- Building reputation systems for AI agents
- Verifying agent identity before interactions
- Querying agent reputation and feedback
- Implementing trust-based agent interactions

## Core Concepts

### The Three Registries

| Registry | Purpose | Key Functions |
|----------|---------|---------------|
| **Identity Registry** | Agent discovery via ERC-721 NFTs | `register()`, `agentURI()` |
| **Reputation Registry** | Feedback and attestations | `giveFeedback()`, `getSummary()` |
| **Validation Registry** | Verification hooks | Custom validators |

### Protocol Stack Position

```
Application Layer (Agent Apps, Marketplaces)
    ↓
Trust Layer (ERC-8004) ← This skill
    ↓
Payment Layer (x402)
    ↓
Communication Layer (A2A, MCP)
```

## Installation

```bash
# JavaScript/TypeScript
npm install @chaoschain/sdk

# Python
pip install chaoschain-sdk
```

## Contract Addresses

### Celo Mainnet

| Contract | Address |
|----------|---------|
| Identity Registry | Coming Soon (Q1 2026) |
| Reputation Registry | Coming Soon (Q1 2026) |

### Celo Sepolia (Testnet)

| Contract | Address |
|----------|---------|
| Identity Registry | Coming Soon |
| Reputation Registry | Coming Soon |

## Agent Registration

### 1. Create Registration File

Create an agent registration file describing endpoints and capabilities:

```json
{
  "type": "Agent",
  "name": "My AI Agent",
  "description": "Description of capabilities",
  "image": "ipfs://Qm...",
  "endpoints": [
    {
      "type": "a2a",
      "url": "https://example.com/.well-known/agent.json"
    },
    {
      "type": "mcp",
      "url": "https://example.com/mcp"
    },
    {
      "type": "wallet",
      "address": "0x...",
      "chainId": 42220
    }
  ],
  "supportedTrust": ["reputation", "validation", "tee"]
}
```

### 2. Upload to IPFS

```javascript
import { upload } from "@chaoschain/sdk";

const agentMetadata = {
  type: "Agent",
  name: "My AI Agent",
  description: "AI agent for DeFi operations",
  // ...
};

const agentURI = await upload(agentMetadata);
// Returns: ipfs://QmYourRegistrationFile
```

### 3. Register Agent

```javascript
import { IdentityRegistry } from '@chaoschain/sdk';
import { createPublicClient, http } from 'viem';
import { celo } from 'viem/chains';

const client = createPublicClient({
  chain: celo,
  transport: http('https://forno.celo.org'),
});

const registry = new IdentityRegistry(client);

// Register and get agent ID
const tx = await registry.register(agentURI);
const agentId = tx.events.Transfer.returnValues.tokenId;

console.log('Agent registered with ID:', agentId);
```

## Reputation System

### Give Feedback

```javascript
import { ReputationRegistry } from '@chaoschain/sdk';

const reputation = new ReputationRegistry(client);

await reputation.giveFeedback(
  agentId,           // Agent ID to review
  85,                // score (0-100)
  0,                 // decimals
  'starred',         // tag1: category
  '',                // tag2: optional
  'https://agent.example.com',  // endpoint used
  'ipfs://QmDetailedFeedback',  // detailed feedback URI
  feedbackHash       // keccak256 of feedback content
);
```

### Common Feedback Tags

| Tag | Measures | Example |
|-----|----------|---------|
| `starred` | Quality rating (0-100) | 87/100 |
| `uptime` | Endpoint uptime % | 99.77% |
| `successRate` | Task success rate % | 89% |
| `responseTime` | Response time (ms) | 560ms |
| `reachable` | Endpoint reachable | true/false |

### Query Reputation

```javascript
// Get all feedback for an agent
const feedback = await reputation.readAllFeedback(agentId);

// Get aggregated summary
const summary = await reputation.getSummary(agentId);
console.log('Average rating:', summary.averageScore);
console.log('Total reviews:', summary.totalFeedback);
```

## Trust Verification Workflow

```javascript
import { IdentityRegistry, ReputationRegistry } from '@chaoschain/sdk';

async function verifyAndInteract(targetAgentId, minReputation = 70) {
  // 1. Verify identity
  const identity = await identityRegistry.getAgent(targetAgentId);
  if (!identity) {
    throw new Error('Agent not registered');
  }

  // 2. Check reputation
  const summary = await reputationRegistry.getSummary(targetAgentId);
  if (summary.averageScore < minReputation) {
    throw new Error(`Agent reputation ${summary.averageScore} below threshold ${minReputation}`);
  }

  // 3. Get endpoint
  const agentData = await fetch(identity.agentURI).then(r => r.json());
  const endpoint = agentData.endpoints.find(e => e.type === 'a2a');

  // 4. Interact with verified agent
  const result = await interactWithAgent(endpoint.url);

  // 5. Submit feedback
  await reputationRegistry.giveFeedback(
    targetAgentId,
    result.success ? 90 : 30,
    0,
    result.success ? 'starred' : 'failed',
    '',
    endpoint.url,
    '',
    ''
  );

  return result;
}
```

## Integration with x402 Payments

ERC-8004 and x402 work together for trustworthy paid agent interactions:

```javascript
import { IdentityRegistry, ReputationRegistry } from '@chaoschain/sdk';
import { wrapFetchWithPayment } from 'thirdweb/x402';

async function payTrustedAgent(agentId, serviceUrl) {
  // 1. Verify trust
  const summary = await reputationRegistry.getSummary(agentId);
  if (summary.averageScore < 80) {
    throw new Error('Agent not trusted enough for payment');
  }

  // 2. Make paid request
  const fetchWithPayment = wrapFetchWithPayment({
    client,
    account,
    paymentOptions: { maxValue: "1000000" },
  });

  const response = await fetchWithPayment(serviceUrl);
  return response.json();
}
```

## Use Cases

### DeFi Trading Agents

Verify strategy agents before delegating funds:

```javascript
const strategyAgents = await identityRegistry.searchByCapability('defi-trading');
const trustedAgents = [];

for (const agent of strategyAgents) {
  const summary = await reputationRegistry.getSummary(agent.id);
  if (summary.averageScore >= 85 && summary.totalFeedback >= 100) {
    trustedAgents.push(agent);
  }
}
```

### Multi-Agent Workflows

Coordinate trusted agents for complex tasks:

```javascript
const workflow = {
  research: await findTrustedAgent('research', 80),
  analysis: await findTrustedAgent('analysis', 85),
  execution: await findTrustedAgent('execution', 90),
};

// Execute with trust-verified agents
await executeWorkflow(workflow);
```

## Validation Registry

For high-stakes operations, use Validation Registry for additional verification:

| Model | Mechanism | Best For |
|-------|-----------|----------|
| **Reputation-based** | Client feedback | Low-stake, frequent |
| **Crypto-economic** | Stake + slashing | Medium-stake financial |
| **zkML** | Zero-knowledge proofs | Privacy-preserving |
| **TEE Attestation** | Hardware isolation | High-assurance |

## Celo Network Reference

| Network | Chain ID | RPC Endpoint |
|---------|----------|--------------|
| Celo Mainnet | 42220 | https://forno.celo.org |
| Celo Sepolia | 11142220 | https://forno.celo-sepolia.celo-testnet.org |

## Additional Resources

- [EIP Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [Official Website](https://www.8004.org)
- [Learning Portal](https://www.8004.org/learn)
- [Contracts Repository](https://github.com/erc-8004/erc-8004-contracts)
- [Builder Program](http://bit.ly/8004builderprogram)

## Related Skills

- [x402](../x402/SKILL.md) - Payment layer for AI agents
- [celo-rpc](../celo-rpc/SKILL.md) - Celo blockchain interaction
- [viem](../viem/SKILL.md) - TypeScript Ethereum library
