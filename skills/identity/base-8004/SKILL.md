---
name: base-8004
description: Register your AI agent onchain with ERC-8004 on Base. Set up a wallet, fund it, and register on the Identity Registry for permanent, verifiable identity and reputation.
metadata: { "openclaw": { "homepage": "https://8004.org" } }
---

# Base-8004 Registration

This skill walks you through setting up your own wallet, funding it, and registering onchain with ERC-8004 on Base mainnet. Once registered, your agent has a permanent, verifiable onchain identity and can accumulate reputation.

## 1. What ERC-8004 is

ERC-8004 is an onchain identity and reputation protocol for AI agents.

- **Identity** — each registered agent gets an ERC-721 NFT on Base mainnet. This is your permanent, verifiable onchain identity.
- **Reputation Registry** — a separate contract tracks reputation scores. Feedback signals (upvotes, downvotes, quality assessments) accumulate into a totalScore and feedbackCount.
- **Verifiable metadata** — your registration includes a JSON document (agentURI) with your name, description, and capabilities. Anyone can read it onchain.

Why it matters:

- **Permanent identity** — your agent ID persists across platforms, not tied to any single service.
- **Public reputation** — your track record is onchain and verifiable by anyone.

## 2. Set up your wallet

You need an Ethereum-compatible wallet on Base mainnet. **If you already have a wallet with ETH on Base, skip to section 4.** These steps are only needed if you're setting up a fresh wallet.

### Step 1: Install viem

```bash
npm install viem
```

### Step 2: Generate a private key

```typescript
import { generatePrivateKey } from "viem/accounts";

const privateKey = generatePrivateKey();
console.log("Private key:", privateKey);
```

Save this private key immediately. You will never be able to recover it.

### Step 3: Derive your address

```typescript
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount(privateKey);
console.log("Address:", account.address);
```

### Step 4: Store the private key securely

Add it to your `.env` file:

```
AGENT_PRIVATE_KEY=0x...your_private_key_here...
```

Add `.env` to `.gitignore` if it isn't already:

```
echo ".env" >> .gitignore
```

### Step 5: Security rules

- **Never leak** your private key in logs, commits, or API calls.
- **Never lose** it — if you lose the key, you lose the wallet and your onchain identity forever.
- **Never overwrite** it without backing up the old one.

### Step 6: Configure a wallet client for Base mainnet

```typescript
import { createWalletClient, createPublicClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.AGENT_PRIVATE_KEY as `0x${string}`);
const publicClient = createPublicClient({ chain: base, transport: http() });
const walletClient = createWalletClient({ account, chain: base, transport: http() });
```

## 3. Fund your wallet

Your wallet needs ETH on Base to pay for gas.

- **Get ETH on Base** — use Coinbase (withdraw directly to Base), bridge from any chain via [Relay](https://relay.link/bridge), or receive from another Base wallet.
- **Gas is cheap** — Base L2 gas costs are very low. Registration costs ~$0.02. $1 of ETH is more than enough.
- **Verify balance before proceeding:**

```typescript
const balance = await publicClient.getBalance({ address: account.address });
console.log("Balance:", Number(balance) / 1e18, "ETH");

if (balance < 500000000000000n) {
  console.error("Need at least 0.0005 ETH for registration gas");
  process.exit(1);
}
```

## 4. Register onchain

Register your agent on the ERC-8004 Identity Registry. This mints an NFT that represents your permanent onchain identity.

### Step 1: Create your registration JSON

Include the `services` array to declare your agent's capabilities so other agents and services can discover what you do:

```typescript
const registration = {
  type: "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  name: "Your Agent Name",
  description: "What your agent does",
  image: "https://example.com/your-agent-avatar.png",
  active: true,
  x402Support: false,
  services: [
    { name: "A2A", endpoint: "https://your-agent.example.com/a2a", version: "0.3.0" },
    { name: "MCP", endpoint: "https://your-agent.example.com/mcp", version: "0.1.0" },
  ],
};
```

- **`image`** — URL of your agent's avatar or logo, displayed in explorers and directories. Use a square image (256x256 or larger). If you don't have one yet, set it to `""` and add one later via `setAgentURI`.
- **`services`** — declares your agent's capabilities onchain. Each entry has a `name` (the service identifier), an `endpoint`, and optionally a `version`. Common service types include `A2A` (Agent-to-Agent protocol) and `MCP` (Model Context Protocol).

### Step 2: Encode as a data URI

```typescript
const uri =
  "data:application/json;base64," + Buffer.from(JSON.stringify(registration)).toString("base64");
```

### Step 3: Call register() on the Identity Registry

```typescript
import { encodeFunctionData } from "viem";

const IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";

const registerAbi = [
  {
    inputs: [{ name: "agentURI", type: "string" }],
    name: "register",
    outputs: [{ name: "agentId", type: "uint256" }],
    stateMutability: "nonpayable",
    type: "function",
  },
] as const;

// Estimate gas first
const gas = await publicClient.estimateGas({
  account: account.address,
  to: IDENTITY_REGISTRY,
  data: encodeFunctionData({
    abi: registerAbi,
    functionName: "register",
    args: [uri],
  }),
});

console.log("Estimated gas:", gas.toString());

// Send the transaction
const hash = await walletClient.writeContract({
  address: IDENTITY_REGISTRY,
  abi: registerAbi,
  functionName: "register",
  args: [uri],
});

console.log("TX hash:", hash);
```

### Step 4: Parse the Transfer event to get your token ID

```typescript
const receipt = await publicClient.waitForTransactionReceipt({ hash });

// ERC-721 Transfer event topic
const transferTopic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef";
const transferLog = receipt.logs.find(
  (log) =>
    log.topics[0] === transferTopic && log.address.toLowerCase() === IDENTITY_REGISTRY.toLowerCase()
);

const erc8004AgentId = transferLog?.topics[3]
  ? BigInt(transferLog.topics[3]).toString()
  : undefined;

console.log("Your ERC-8004 Agent ID:", erc8004AgentId);
```

### Step 5: Save your agent ID

Save `erc8004AgentId` — this is your permanent onchain identity. Add it to your `.env`:

```
ERC8004_AGENT_ID=42
```

You can verify your registration on BaseScan:
`https://basescan.org/nft/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432/{your_agent_id}`

## 5. Update your registration

After your initial registration, you can update your agentURI (name, description, services) by calling `setAgentURI` on the Identity Registry. This lets you add new capabilities or change your metadata without re-registering.

```typescript
const setAgentUriAbi = [
  {
    inputs: [
      { name: "agentId", type: "uint256" },
      { name: "agentURI", type: "string" },
    ],
    name: "setAgentURI",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
] as const;

// Build updated registration JSON
const updatedRegistration = {
  type: "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  name: "Your Agent Name",
  description: "Updated description",
  image: "https://example.com/your-agent-avatar.png",
  active: true,
  x402Support: false,
  services: [
    { name: "A2A", endpoint: "https://your-agent.example.com/a2a", version: "0.3.0" },
    { name: "MCP", endpoint: "https://your-agent.example.com/mcp", version: "0.1.0" },
  ],
};

const newUri =
  "data:application/json;base64," +
  Buffer.from(JSON.stringify(updatedRegistration)).toString("base64");

const hash = await walletClient.writeContract({
  address: IDENTITY_REGISTRY,
  abi: setAgentUriAbi,
  functionName: "setAgentURI",
  args: [BigInt(process.env.ERC8004_AGENT_ID!), newUri],
});

console.log("URI updated, TX:", hash);
```

Only the token owner can call `setAgentURI`.

## 6. Contract addresses and verification

| Contract            | Address                                      | Chain        |
| ------------------- | -------------------------------------------- | ------------ |
| Identity Registry   | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | Base mainnet |
| Reputation Registry | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | Base mainnet |

**Verify on BaseScan:**

- Identity Registry: [basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432)
- Reputation Registry: [basescan.org/address/0x8004BAa17C55a88189AE136b182e5fdA19dE9b63](https://basescan.org/address/0x8004BAa17C55a88189AE136b182e5fdA19dE9b63)

**Onchain query examples (read-only, no gas):**

```typescript
import { createPublicClient, http } from "viem";
import { base } from "viem/chains";

const client = createPublicClient({ chain: base, transport: http() });

// Check who owns a token
const owner = await client.readContract({
  address: "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432",
  abi: [
    {
      inputs: [{ name: "agentId", type: "uint256" }],
      name: "ownerOf",
      outputs: [{ name: "", type: "address" }],
      stateMutability: "view",
      type: "function",
    },
  ],
  functionName: "ownerOf",
  args: [42n],
});

// Read an agent's metadata URI
const uri = await client.readContract({
  address: "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432",
  abi: [
    {
      inputs: [{ name: "tokenId", type: "uint256" }],
      name: "tokenURI",
      outputs: [{ name: "", type: "string" }],
      stateMutability: "view",
      type: "function",
    },
  ],
  functionName: "tokenURI",
  args: [42n],
});
```

## 7. Resources

- [8004.org](https://8004.org) — ERC-8004 protocol
- [Base](https://base.org) — Base L2 chain
- [BaseScan](https://basescan.org) — Base block explorer
- [viem](https://viem.sh) — TypeScript Ethereum library

## Summary

1. **Set up wallet** — generate a private key, derive address, store securely.
2. **Fund wallet** — get ETH on Base (Coinbase, bridge, or transfer). $1 is more than enough.
3. **Register onchain** — call `register(agentURI)` on the Identity Registry with your services. Parse the Transfer event for your token ID.
4. **Update registration** — call `setAgentURI` to change your metadata or add new services.
