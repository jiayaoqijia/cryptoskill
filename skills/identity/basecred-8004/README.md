# basecred-8004-registration

Interactive ERC-8004 agent registration for [OpenClaw](https://openclaw.ai) agents. Register your AI agent on the [ERC-8004](https://8004.org) on-chain identity registry through a guided chat experience.

## Features

- 🗂️ **Auto-prefill** — fills from agent identity files, `.env`, and context
- 📋 **Full draft preview** — all fields with ✅/⚠️ status before submitting
- ✏️ **Inline section editing** — tap buttons to edit Basic Info, Endpoints, Skills, or Config
- 💬 **Instant button feedback** — immediate acknowledgment on every tap
- 🔘 **Multi-select toggles** — skills, domains, and trust models as toggleable buttons
- ⛓️ **Multi-chain** — Base (default), Ethereum, Polygon, BNB, Arbitrum, Celo, Gnosis, Scroll
- 💾 **Fully onchain** — default storage on-chain, no IPFS dependency
- 🔑 **Wallet flexibility** — paste an address or auto-detect from private key
- 🔐 **EIP-712 wallet linking** — sets agent wallet after registration
- 📄 **8004.org compatible** — imports/exports the standard 8004.org JSON template
- ⏳ **Progress updates** — step-by-step feedback during on-chain registration

## How It Works

1. **Auto-prefill** — agent fills every field it can from identity files and `.env`
2. **Config explainer** — explains defaults (chain, storage, trust, x402, wallet) with alternatives
3. **Draft + buttons** — shows full draft as single message with inline edit/register buttons
4. **Edit sections** — tap to edit any section, with back-to-draft navigation
5. **Register** — on confirmation, mints agent NFT, sets endpoints, links wallet
6. **Result** — shows Agent ID, TX hash, and link to 8004.org

## Quick Start

### 1. Install

```bash
bash scripts/setup.sh
```

### 2. Set Environment

Add to your `.env`:

```bash
# Required (one of these):
PRIVATE_KEY=0x...
# or
AGENT_PRIVATE_KEY=0x...
# or
MAIN_WALLET_PRIVATE_KEY=0x...

# Optional:
RPC_URL=https://mainnet.base.org
CHAIN_ID=8453
PINATA_JWT=...  # only needed for IPFS storage
```

### 3. Register via Chat

Tell your OpenClaw agent: **"Register me on ERC-8004"**

The agent handles everything — prefill, draft, editing, and on-chain submission.

### 4. Register via CLI

```bash
# From JSON template (8004.org format)
node scripts/register.mjs --json registration.json --chain 8453 --yes

# From CLI args
node scripts/register.mjs \
  --name "MyAgent" \
  --description "What my agent does" \
  --a2a "https://my-agent.xyz/a2a" \
  --wallet "0x..." \
  --skills "NLP,Code Generation" \
  --domains "Technology,Blockchain" \
  --trust "reputation" \
  --chain 8453 \
  --yes

# Dry run (preview only, no private key needed)
node scripts/register.mjs --json registration.json --dry-run

# Output blank 8004.org template
node scripts/register.mjs --template
```

## Registration Fields

### Basic Info

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| Agent Name | ✅ | — | Display name |
| Description | ✅ | — | What the agent does |
| Agent Address | No | auto from `.env` | Wallet address (paste or auto-detect) |
| Image | No | — | Avatar URL |
| Version | No | `1.0.0` | Agent version |
| Author | No | — | Creator name |
| License | No | `MIT` | Software license |

### Endpoints

| Field | Required | Description |
|-------|----------|-------------|
| A2A Endpoint | No | Agent-to-Agent messaging URL |
| MCP Endpoint | No | Model Context Protocol URL |

### Skills & Domains

| Field | Description |
|-------|-------------|
| Selected Skills | OASF taxonomy (NLP, Summarization, Q&A, Code Gen, etc.) |
| Selected Domains | OASF taxonomy (Blockchain, Technology, Finance, etc.) |
| Custom Skills | Non-standard skills |
| Custom Domains | Non-standard domains |

### Advanced Config

| Field | Default | Options |
|-------|---------|---------|
| Chain | Base (8453) | Ethereum, Polygon, BNB, Arbitrum, Celo, Gnosis, Scroll |
| Storage | Fully onchain | IPFS |
| Trust | — | Reputation, Crypto-Economic, TEE Attestation |
| x402 | Off | On (payment protocol) |
| Active | On | Off (hidden from discovery) |

## Wallet Setup

Two ways to link your wallet:

| Option | How | Best for |
|--------|-----|----------|
| **A: Paste address** | Provide your `0x...` address via `--wallet` or in chat | Simple display/linking |
| **B: Private key in .env** | Set `PRIVATE_KEY=0x...` in `.env` | Auto-detect + signing + EIP-712 wallet linking |

## Supported Chains

| Chain | ID | Default |
|-------|----|---------|
| **Base** | 8453 | ✅ |
| Ethereum | 1 | |
| Polygon | 137 | |
| BNB Chain | 56 | |
| Arbitrum | 42161 | |
| Celo | 42220 | |
| Gnosis | 100 | |
| Scroll | 534352 | |

All chains use the same deterministic ERC-8004 contract addresses:
- Identity Registry: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- Reputation Registry: `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

## Other Operations

```bash
# Search agents
node scripts/search.mjs --name "AgentName" --chain 8453

# Update agent
node scripts/update.mjs --agent-id "8453:42" --name "NewName" --yes

# Give feedback
node scripts/feedback.mjs --agent-id "8453:42" --value 5 --tag1 "reliable" --yes
```

## JSON Template

Compatible with [8004.org](https://8004.org) export format:

```json
{
  "basicInfo": {
    "agentName": "",
    "agentAddress": "",
    "description": "",
    "image": "",
    "version": "1.0.0",
    "author": "",
    "license": "MIT"
  },
  "endpoints": {
    "mcpEndpoint": "",
    "a2aEndpoint": ""
  },
  "skillsDomains": {
    "selectedSkills": [],
    "selectedDomains": [],
    "customSkills": [],
    "customDomains": []
  },
  "advancedConfig": {
    "supportedTrusts": [],
    "x402support": false,
    "storageMethod": "http",
    "active": true
  },
  "version": "1.0.0"
}
```

## Safety

- **Duplicate check** — before registering, the script checks if your wallet already owns agents on the target chain and warns you. Prevents accidental double-registration.
- **Draft preview** — always shows full draft before any on-chain action
- **Explicit confirmation** — nothing submits without your approval
- **Burn duplicates** — if a duplicate is created, transfer to `0x...dEaD` via the contract's `transferFrom`

## Known Limitations

- **setWallet on public RPCs**: Public RPCs (e.g. `mainnet.base.org`) don't support `eth_signTypedData_v4`. If wallet linking fails, you can set it manually at [8004.org](https://8004.org). The agent registration itself is not affected.
- **SDK chain support**: The `agent0-sdk` only ships with Ethereum Mainnet registry addresses. This skill adds `registryOverrides` for all supported chains using deterministic contract addresses.

## Tech Stack

- [agent0-sdk](https://github.com/agent0lab/agent0-ts) v1.5.2
- [viem](https://viem.sh) (wallet/chain operations)
- [OpenClaw](https://openclaw.ai) skill system

## License

MIT
