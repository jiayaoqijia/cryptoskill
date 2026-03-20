---
name: 8004-skill
description: Register and manage ERC-8004 Identity NFTs on Monad. Use when the agent needs to mint an on-chain identity for CEO Protocol registration or other ERC-8004–integrated protocols.
---

# ERC-8004 Identity Skill

Use this skill when the agent must register on the ERC-8004 Identity Registry to obtain an on-chain identity NFT. This identity is **required** to register as an agent in The CEO Protocol (CEOVault).

Reference: [EIP-8004 Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004)

## Contract Address (Monad Mainnet)

| Contract | Address |
|----------|---------|
| ERC-8004 Identity | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |

## Interface Summary

The Identity Registry is ERC-721 based. Registering mints an NFT to `msg.sender`; the token ID is the agent ID.

### Write Functions

| Function | Purpose |
|----------|---------|
| `register(string agentURI)` | Register with a URI; mints NFT, returns `agentId` |
| `register(string agentURI, MetadataEntry[] metadata)` | Register with URI and on-chain metadata |
| `register()` | Register with no URI (set later via `setAgentURI`) |
| `setAgentURI(uint256 agentId, string newURI)` | Update the agent's URI |
| `setMetadata(uint256 agentId, string metadataKey, bytes metadataValue)` | Set on-chain metadata |

### Read Functions (view)

| Function | Returns | Use |
|----------|---------|-----|
| `ownerOf(uint256 tokenId)` | `address` | Check who owns an agent NFT |
| `tokenURI(uint256 tokenId)` | `string` | Get agent URI (same as agentURI) |
| `getAgentWallet(uint256 agentId)` | `address` | Get wallet linked to agent |
| `getMetadata(uint256 agentId, string metadataKey)` | `bytes` | Get on-chain metadata |

### Events

| Event | Use |
|-------|-----|
| `Registered(uint256 indexed agentId, string agentURI, address indexed owner)` | Emitted on mint |
| `URIUpdated(uint256 indexed agentId, string newURI, address indexed updatedBy)` | Emitted on URI change |
| `MetadataSet(uint256 indexed agentId, string indexed metadataKey, string metadataKey, bytes metadataValue)` | Emitted on metadata set |

## Registration Data Template

The `agentURI` must resolve to a JSON document conforming to EIP-8004 registration. Use this template and replace placeholders before hosting (IPFS or data URI):

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "AGENT_NAME",
  "description": "AGENT_DESCRIPTION",
  "image": "https://example.com/agent-image.png",
  "services": [
    {
      "name": "A2A",
      "endpoint": "https://YOUR_DOMAIN/.well-known/agent-card.json",
      "version": "0.3.0"
    },
    {
      "name": "MCP",
      "endpoint": "https://YOUR_DOMAIN/mcp",
      "version": "2025-06-18"
    }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [],
  "supportedTrust": [
    "reputation"
  ]
}
```

| Field | Replace with |
|-------|--------------|
| `AGENT_NAME` | Agent display name |
| `AGENT_DESCRIPTION` | Short description of capabilities |
| `image` | URL to agent avatar/image |
| `YOUR_DOMAIN` | Your domain for A2A/MCP endpoints (or omit services if not applicable) |
| `supportedTrust` | Trust models (e.g. `["reputation"]` for CEO Protocol) |

For a minimal CEO Protocol–only registration, you can omit `services` or set them to empty; `supportedTrust: ["reputation"]` is typical.

## Automated Scripts (preferred)

The Docker image includes production-ready scripts at:

`/opt/erc8004-scripts`

Source in workspace:

`/root/.openclaw/workspace/skills/8004-skill/scripts`

### Required env vars for script flow

- `MONAD_RPC_URL`
- `MONAD_CHAIN_ID=143` (or pass `--chainId`)
- `AGENT_PRIVATE_KEY`
- `PINATA_JWT`
- `PINATA_GATEWAY` (recommended for verification fetch)

### Script commands

```bash
# 1) Register on-chain with empty URI -> returns agentId
node /opt/erc8004-scripts/register.mjs --network monad-mainnet

# 2) Build card JSON with registrations[] embedded
node /opt/erc8004-scripts/build-card.mjs \
  --network monad-mainnet \
  --agentId 42 \
  --template /root/.openclaw/workspace/skills/8004-skill/assets/registration-template.json \
  --name "CEO-1" \
  --description "Autonomous strategist for The CEO Protocol" \
  --out /tmp/agent-42.json

# 3) Upload to Pinata -> returns ipfs://CID
node /opt/erc8004-scripts/upload-pinata.mjs --file /tmp/agent-42.json

# 4) Set token URI on-chain
node /opt/erc8004-scripts/set-agent-uri.mjs \
  --network monad-mainnet \
  --agentId 42 \
  --uri ipfs://CID

# 5) Verify owner, tokenURI, wallet, and registrations[] match
node /opt/erc8004-scripts/verify.mjs --network monad-mainnet --agentId 42
```

### One-shot command

```bash
node /opt/erc8004-scripts/full-register.mjs \
  --network monad-mainnet \
  --name "CEO-1" \
  --description "Autonomous strategist for The CEO Protocol" \
  --template /root/.openclaw/workspace/skills/8004-skill/assets/registration-template.json \
  --outCard /tmp/agent-card.json \
  --identityFile /root/.openclaw/workspace/AGENT_IDENTITY.md
```

This executes all 4 registration steps (register -> build card -> upload -> set URI) and writes identity state for later CEO Protocol onboarding.

## Registration Flow

1. **Prerequisites**
   - Wallet with MON for gas (use `viem-local-signer address` to confirm signer).
   - `agentURI`: a URI pointing to your registration JSON (use the template above). Use IPFS (`ipfs://...`) or a data URI (`data:application/json;base64,...`).

2. **Call `register(agentURI)`**
   - Encode calldata with `encodeFunctionData`.
   - Send via `viem-local-signer send-contract`.
   - Parse `Registered` event or return value for `agentId`.

3. **Store `agentId`**
   - The returned `agentId` (token ID) is required for CEO Protocol `registerAgent(metadataURI, ceoAmount, erc8004Id)`.
   - Persist it in an identity file (see below).

## Identity File Template

After registration, persist the on-chain identity so the agent can reference it for CEO Protocol and other flows. Use this template:

```markdown
# Agent Identity
- **Address**: `<NOT SET>`
- **Agent ID**: `<NOT SET>`
- **Agent Registry**: `<NOT SET>`
- **Chain ID**: `<NOT SET>`
```

### How to fill it

| Field | Source | Example |
|-------|--------|---------|
| **Address** | `viem-local-signer address` (signer wallet) | `0xB4AF3708DA37a485E84b4F09c146eD0A8B7Df5c4` |
| **Agent ID** | Return value from `register(agentURI)` | `42` |
| **Agent Registry** | ERC-8004 Identity contract (Monad: `eip155:143:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`) | `eip155:143:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| **Chain ID** | Monad mainnet | `143` |

### How to use it

1. **After registration**: Write the identity file to `workspace/IDENTITY.md` or `workspace/AGENT_IDENTITY.md` so it is in the agent's context.
2. **Before CEO Protocol `registerAgent`**: Read `Agent ID` from the file — that is `erc8004Id`.
3. **Consistency check**: Ensure `Address` matches `viem-local-signer address` and `ownerOf(agentId)` on the registry.

Example filled identity:

```markdown
# Agent Identity
- **Address**: `0xB4AF3708DA37a485E84b4F09c146eD0A8B7Df5c4`
- **Agent ID**: `42`
- **Agent Registry**: `eip155:143:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Chain ID**: `143`
```

## ABI (minimal)

```json
[
  {
    "type": "function",
    "name": "register",
    "stateMutability": "nonpayable",
    "inputs": [{ "name": "agentURI", "type": "string" }],
    "outputs": [{ "name": "agentId", "type": "uint256" }]
  },
  {
    "type": "function",
    "name": "register",
    "stateMutability": "nonpayable",
    "inputs": [
      { "name": "agentURI", "type": "string" },
      {
        "name": "metadata",
        "type": "tuple[]",
        "components": [
          { "name": "metadataKey", "type": "string" },
          { "name": "metadataValue", "type": "bytes" }
        ]
      }
    ],
    "outputs": [{ "name": "agentId", "type": "uint256" }]
  },
  {
    "type": "function",
    "name": "register",
    "stateMutability": "nonpayable",
    "inputs": [],
    "outputs": [{ "name": "agentId", "type": "uint256" }]
  },
  {
    "type": "function",
    "name": "setAgentURI",
    "stateMutability": "nonpayable",
    "inputs": [
      { "name": "agentId", "type": "uint256" },
      { "name": "newURI", "type": "string" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "name": "setMetadata",
    "stateMutability": "nonpayable",
    "inputs": [
      { "name": "agentId", "type": "uint256" },
      { "name": "metadataKey", "type": "string" },
      { "name": "metadataValue", "type": "bytes" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "name": "ownerOf",
    "stateMutability": "view",
    "inputs": [{ "name": "tokenId", "type": "uint256" }],
    "outputs": [{ "name": "", "type": "address" }]
  },
  {
    "type": "function",
    "name": "tokenURI",
    "stateMutability": "view",
    "inputs": [{ "name": "tokenId", "type": "uint256" }],
    "outputs": [{ "name": "", "type": "string" }]
  },
  {
    "type": "function",
    "name": "getAgentWallet",
    "stateMutability": "view",
    "inputs": [{ "name": "agentId", "type": "uint256" }],
    "outputs": [{ "name": "", "type": "address" }]
  },
  {
    "type": "function",
    "name": "getMetadata",
    "stateMutability": "view",
    "inputs": [
      { "name": "agentId", "type": "uint256" },
      { "name": "metadataKey", "type": "string" }
    ],
    "outputs": [{ "name": "", "type": "bytes" }]
  }
]
```

## Encoding and Sending

Use `viem` to encode, then `viem-local-signer send-contract` to broadcast. Example (Node/script):

```typescript
import { encodeFunctionData } from "viem";

const ERC8004_IDENTITY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";

const abi = [
  {
    type: "function",
    name: "register",
    stateMutability: "nonpayable",
    inputs: [{ name: "agentURI", type: "string" }],
    outputs: [{ name: "agentId", type: "uint256" }],
  },
] as const;

const agentURI = "ipfs://Qm..."; // or data:application/json;base64,...
const data = encodeFunctionData({
  abi,
  functionName: "register",
  args: [agentURI],
});

// Then run:
// viem-local-signer send-contract --to 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 --data <hex> --value-wei 0 --wait
```

## Agent Runbook

1. Confirm signer: `viem-local-signer address`
2. Ensure wallet has MON for gas.
3. Prepare `agentURI` (IPFS or data URI with registration JSON).
4. Encode `register(agentURI)` with viem.
5. Present tx summary and ask for user confirmation.
6. Run `viem-local-signer send-contract --to 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 --data <calldata> --value-wei 0 --wait`
7. Parse receipt/logs for `agentId` (or read from `Registered` event).
8. Write identity file (`workspace/AGENT_IDENTITY.md` or `workspace/IDENTITY.md`) using the template above with Address, Agent ID, Agent Registry, Chain ID.

## CEO Protocol Integration

CEOVault requires an ERC-8004 identity before `registerAgent`:

```
CEOVault.registerAgent(metadataURI, ceoAmount, erc8004Id)
```

- `erc8004Id` = the token ID from `ERC8004Identity.register(...)`.
- Caller must own that NFT (`ownerOf(erc8004Id) == msg.sender`).

## Block Explorer

- Monad: `https://monadscan.com/`
- Tx link: `https://monadscan.com/tx/<hash>`
- Contract: `https://monadscan.com/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
