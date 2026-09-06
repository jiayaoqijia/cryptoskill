# Agent0 SDK Usage Examples

TypeScript examples using the [Agent0 SDK](https://github.com/agent0labs/agent0-ts) (v1.6.0+) for ERC-8004 on-chain operations.

## Installation

```bash
npm install agent0-ts ethers
# or
pnpm add agent0-ts ethers
```

## Quick Start

```typescript
import { Agent } from "agent0-ts";

const agent = new Agent({
  chainId: 11155111, // Ethereum Sepolia
  rpcUrl: "https://rpc.sepolia.org",
  privateKey: process.env.ERC8004_PRIVATE_KEY!,
});
```

## Identity Registry

### Register an Agent

```typescript
// 1. Create registration file (JSON hosted on IPFS/HTTPS)
const registrationFile = {
  name: "My AI Agent",
  description: "A helpful coding assistant",
  image: "https://example.com/avatar.png",
  services: {
    mcp: { url: "https://agent.example.com/mcp" },
  },
  skills: ["code-review", "testing"],
  domains: ["software-engineering"],
  supportedTrust: ["reputation"],
  active: true,
};

// 2. Host it (e.g., IPFS via Pinata, or any HTTPS URL)
const agentUri = "https://example.com/agent.json";

// 3. Mint the agent NFT
const { tokenId, txHash } = await agent.identity.register(agentUri);
console.log(`Registered: ${agent.chainId}:${tokenId}`);
```

### Read Agent Data

```typescript
// Get agentURI
const uri = await agent.identity.agentURI(42);

// Get owner address
const owner = await agent.identity.ownerOf(42);

// Fetch and parse the registration file
const response = await fetch(uri);
const metadata = await response.json();
console.log(`Agent: ${metadata.name}`);
console.log(`Services: ${Object.keys(metadata.services).join(", ")}`);
```

### Update Agent URI

```typescript
await agent.identity.setAgentURI(42, "https://example.com/agent-v2.json");
```

### Transfer Ownership

```typescript
await agent.identity.transfer(42, "0xNewOwnerAddress...");
```

## Reputation Registry

### Submit Star Rating

```typescript
// Star scale: 1★=20, 2★=40, 3★=60, 4★=80, 5★=100
await agent.reputation.submitFeedback({
  tokenId: 42,
  value: 100,       // 5 stars
  decimals: 0,
  tag: "starred",
  payload: "",       // Optional IPFS hash
});
```

### Submit Metric Feedback

```typescript
// Uptime percentage
await agent.reputation.submitFeedback({
  tokenId: 42,
  value: 9977,       // 99.77%
  decimals: 2,
  tag: "uptime",
  payload: "",
});

// Response time in milliseconds
await agent.reputation.submitFeedback({
  tokenId: 42,
  value: 250,
  decimals: 0,
  tag: "responseTime",
  payload: "",
});
```

### Submit Negative Feedback

```typescript
await agent.reputation.submitFeedback({
  tokenId: 42,
  value: -50,
  decimals: 0,
  tag: "dispute",
  payload: "bafybei...",  // IPFS hash with details
});
```

### Read Feedback

```typescript
const feedbacks = await agent.reputation.getFeedbacks(42);

for (const fb of feedbacks) {
  console.log(`From: ${fb.submitter}`);
  console.log(`Value: ${fb.value}, Tag: ${fb.tag}`);
  console.log(`Timestamp: ${new Date(fb.timestamp * 1000).toISOString()}`);
}
```

### Aggregate and Label

```typescript
function computeTrustLabel(count: number, avg: number): string {
  if (count >= 5 && avg < -50) return `🔴 Untrusted -- ${avg}/100 (${count} reviews)`;
  if (avg < 0) return `🟠 Caution -- ${avg}/100 (${count} reviews)`;
  if (count >= 20 && avg >= 80) return `⭐ Highly Trusted -- ${avg}/100 (${count} reviews)`;
  if (count >= 10 && avg >= 70) return `🟢 Trusted -- ${avg}/100 (${count} reviews)`;
  if (count >= 5 && avg >= 50) return `🟢 Established -- ${avg}/100 (${count} reviews)`;
  if (count > 0) return `🔵 Emerging -- ${avg}/100 (${count} reviews)`;
  return `⚪ No Data -- 0/100 (0 reviews)`;
}

const feedbacks = await agent.reputation.getFeedbacks(42);
const starFeedbacks = feedbacks.filter((f) => f.tag === "starred");
const avg = starFeedbacks.reduce((sum, f) => sum + f.value, 0) / starFeedbacks.length;
console.log(computeTrustLabel(starFeedbacks.length, avg));
```

### Revoke Feedback

```typescript
// Only the original submitter can revoke
await agent.reputation.revokeFeedback(42, feedbackId);
```

## Validation Registry

### Request Validation

```typescript
await agent.validation.requestValidation({
  tokenId: 42,
  validatorAddress: "0xTrustedValidator...",
});
```

### Submit Validation (Validator Side)

```typescript
await agent.validation.submitResponse({
  tokenId: 42,
  score: 85,
  proof: "0x...",  // TEE attestation or staking proof
});
```

### Read Validations

```typescript
const validations = await agent.validation.getValidations(42);
for (const v of validations) {
  console.log(`Validator: ${v.validator}, Score: ${v.score}/100`);
}
```

## Agent Wallet (EIP-712)

### Set Agent Wallet

```typescript
// Links a hot wallet to the agent NFT for x402 payments
// Uses EIP-712 typed data with 300s deadline
await agent.identity.setMetadata(42, "agentWallet", "0xHotWallet...");
```

### Verify Wallet Signature

```typescript
const metadata = await agent.identity.getMetadata(42, "agentWallet");
// metadata contains { value, signature, deadline }
// Verify EIP-712 signature before trusting the wallet
```

## Batch Operations

### Register Multiple Agents

```typescript
const uris = [
  "https://example.com/agent1.json",
  "https://example.com/agent2.json",
  "https://example.com/agent3.json",
];

const results = [];
for (const uri of uris) {
  const result = await agent.identity.register(uri);
  results.push(result);
  console.log(`Registered: ${agent.chainId}:${result.tokenId}`);
}
```

### Multi-Chain Deployment

```typescript
const chains = [
  { chainId: 11155111, rpc: "https://rpc.sepolia.org" },      // Sepolia
  { chainId: 84532, rpc: "https://sepolia.base.org" },         // Base Sepolia
  { chainId: 421614, rpc: "https://sepolia-rollup.arbitrum.io/rpc" }, // Arbitrum Sepolia
];

for (const chain of chains) {
  const chainAgent = new Agent({
    chainId: chain.chainId,
    rpcUrl: chain.rpc,
    privateKey: process.env.ERC8004_PRIVATE_KEY!,
  });
  const { tokenId } = await chainAgent.identity.register(agentUri);
  console.log(`${chain.chainId}:${tokenId} registered`);
}
```

## Using with 8004scan API

### Combine On-Chain + API Data

```typescript
// On-chain: get raw registration
const uri = await agent.identity.agentURI(42);

// 8004scan API: get enriched data (reputation, leaderboard, search)
const resp = await fetch(
  `https://www.8004scan.io/api/v1/public/agents/${agent.chainId}/42`,
  { headers: { "X-API-Key": process.env.EIGHTSCAN_API_KEY ?? "" } }
);
const enriched = await resp.json();
console.log(`Trust: ${enriched.data.trustLabel}`);
console.log(`Rank: ${enriched.data.leaderboardRank}`);
```

## Error Handling

```typescript
try {
  await agent.identity.register(agentUri);
} catch (error) {
  if (error.code === "INSUFFICIENT_FUNDS") {
    console.error("Not enough ETH for gas. Fund your wallet first.");
  } else if (error.code === "CALL_EXCEPTION") {
    console.error("Contract call failed. Check chain ID and contract address.");
  } else {
    throw error;
  }
}
```

## Environment Variables

```bash
# Required
ERC8004_PRIVATE_KEY=0x...     # Wallet private key for signing
ERC8004_CHAIN_ID=11155111     # Target chain
ERC8004_RPC_URL=https://...   # RPC endpoint

# Optional
EIGHTSCAN_API_KEY=...         # For elevated API rate limits
```
