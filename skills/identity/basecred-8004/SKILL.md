---
name: basecred-8004-registration
description: Interactive ERC-8004 agent registration via chat. Guides users through a prefill form, shows draft, confirms, then registers on-chain using agent0-sdk.
---

# Basecred ERC-8004 Registration

Register AI agents on the [ERC-8004](https://8004.org) on-chain registry through a guided chat experience.

## Registration Flow

### Step 1: Auto-Prefill

When the user triggers registration, **auto-fill every field you can** from:
- Agent identity files (IDENTITY.md, SOUL.md, USER.md)
- Environment (`.env` — wallet address derived from private key)
- Previous context (A2A endpoint, description, image, etc.)
- Sensible defaults (version: 1.0.0, license: MIT, chain: Base, storage: onchain)

**Do NOT ask questions one by one.** Prefill first, ask later.

### Step 1.5: Explain Config Defaults

Before showing the draft, briefly explain the config so users understand what's pre-selected and what alternatives exist:

```
⚙️ Config defaults (you can change these later):

Chain:    Base (8453) — where your agent lives on-chain
          Others: Ethereum, Polygon, BNB, Arbitrum, Celo, Gnosis, Scroll

Storage:  Fully onchain — agent data stored directly on-chain
          Alternative: IPFS — data pinned to IPFS, hash stored on-chain

Trust:    Reputation — other agents/users rate your agent on-chain
          Others: Crypto-Economic (staking/slashing guarantees)
                  TEE Attestation (hardware-level trust proof)

x402:     Off — no payment protocol
          On: agent can charge for services via x402 payment protocol

Active:   On — agent is discoverable and accepting requests
          Off: registered but hidden from discovery

Wallet:   Your agent's on-chain identity address
          Two ways to set it:

          Option A: Paste your wallet address
          → Just paste your 0x... address
          → Agent will be linked to this address on-chain

          Option B: Add private key to .env (for signing)
          → Set PRIVATE_KEY=0x... in your .env file
          → Wallet auto-detected + can sign transactions
          → Enables setWallet() via EIP-712 after registration

          💡 Option A is easier. Option B is needed if you want
             the agent to sign transactions on your behalf.
```

Show this once at the start, not repeated on every draft.

### Step 2: Show Full Draft with Buttons (Single Message)

Send the **entire draft + buttons as one message** using the `message` tool. This keeps buttons directly below the draft.

**Important:** Use `message action=send` with both `message` (the draft text) and `buttons` (inline buttons). Do NOT split into reply + separate button message. After sending, reply with `NO_REPLY` to avoid duplicate.

Use ✅ (filled) and ⚠️ (missing/needs attention):

```
📋 Agent Registration Draft

── Basic Info ──
✅ Name:        Mr. Tee
✅ Description: AI agent with a CRT monitor...
✅ Image:       pbs.twimg.com/...
✅ Version:     1.0.0
✅ Author:      0xdas
✅ License:     MIT

── Endpoints ──
✅ A2A:         a2a.teeclaw.xyz/a2a
⚠️ MCP:         (none)

── Skills & Domains ──
✅ Skills (5):  natural_language_processing/natural_language_processing, 
                natural_language_processing/natural_language_generation/summarization,
                natural_language_processing/information_retrieval_synthesis/question_answering,
                analytical_skills/coding_skills/coding_skills,
                images_computer_vision/images_computer_vision
✅ Domains (5): technology/blockchain/blockchain, technology/blockchain/defi,
                technology/technology, technology/software_engineering/software_engineering,
                technology/software_engineering/devops
✅ Custom:      agent_orchestration/agent_coordination, 
                social_media/content_management

── Config ──
✅ Chain:       Base (8453)
✅ Storage:     Fully onchain
✅ Active:      true
✅ Trust:       reputation
✅ x402:        false
✅ Wallet:      0x1348...e41 (auto .env)

Tap to edit a section or register:
```

Buttons (attached to same message):
```
Row 1: [✏️ Basic Info] [✏️ Endpoints]
Row 2: [✏️ Skills & Domains] [✏️ Config]
Row 3: [✅ Register] [❌ Cancel]
```

### Step 3: Section Editing (on button tap)

**Instant feedback:** When any button is tapped, immediately acknowledge before doing anything else:

| Button | Instant Feedback |
|--------|-----------------|
| ✏️ Basic Info | "📝 Editing Basic Info..." |
| ✏️ Endpoints | "🔗 Editing Endpoints..." |
| ✏️ Skills & Domains | "🏷️ Editing Skills & Domains..." |
| ✏️ Config | "⚙️ Editing Config..." |
| ✅ Register | "⏳ Starting registration on Base..." |
| ❌ Cancel | "❌ Registration cancelled." |
| ↩️ Back to Draft | "📋 Back to draft..." |

Then show the edit form. Always include **↩️ Back to Draft** button.

#### Edit Basic Info
```
Current values:
• Name: Mr. Tee
• Description: AI agent with a CRT...
• Image: pbs.twimg.com/...
• Version: 1.0.0
• Author: 0xdas
• License: MIT

Type field name and new value, e.g. "name: CoolBot"
Or type "done" to go back.
```
Buttons: `[↩️ Back to Draft]`

#### Edit Endpoints
```
Current:
• A2A: https://a2a.teeclaw.xyz/a2a
• MCP: (none)

Paste a URL to set, or "clear mcp" / "clear a2a" to remove.
```
Buttons: `[↩️ Back to Draft]`

#### Edit Skills & Domains
Toggleable inline buttons (multi-select). Each button shows a **human-readable label** but stores the full **OASF taxonomy path** as the value.

**Skills:** (OASF taxonomy paths)
```
[NLP ✅] → natural_language_processing/natural_language_processing
[Summarization ✅] → natural_language_processing/natural_language_generation/summarization
[Q&A ✅] → natural_language_processing/information_retrieval_synthesis/question_answering
[Code Gen ✅] → analytical_skills/coding_skills/coding_skills
[CV ✅] → images_computer_vision/images_computer_vision
[Data Analysis] → analytical_skills/data_analysis/data_analysis
[Web Search] → natural_language_processing/information_retrieval_synthesis/web_search
[Image Gen] → images_computer_vision/image_generation/image_generation
[Translation] → natural_language_processing/natural_language_generation/translation
[Task Automation] → tool_interaction/workflow_automation
[+ Custom] [↩️ Back to Draft]
```

**Domains:** (OASF taxonomy paths)
```
[Blockchain ✅] → technology/blockchain/blockchain
[DeFi ✅] → technology/blockchain/defi
[Technology ✅] → technology/technology
[SE ✅] → technology/software_engineering/software_engineering
[DevOps ✅] → technology/software_engineering/devops
[Finance] → finance/finance
[Healthcare] → healthcare/healthcare
[Education] → education/education
[Entertainment] → entertainment/entertainment
[Science] → science/science
[Creative Arts] → creative_arts/creative_arts
[Dev Tools] → technology/software_engineering/development_tools
[+ Custom] [↩️ Back to Draft]
```

**Display behavior:**
- Buttons show **short labels** (e.g., "NLP", "Blockchain") for readability
- Values stored are **full OASF paths** (e.g., `natural_language_processing/natural_language_processing`)
- Tapping toggles ✅ on/off
- `+ Custom` prompts user to type a custom OASF path or label

#### Edit Config
**Trust models** (multi-select):
```
[Reputation ✅] [Crypto-Economic] [TEE Attestation]
```

**Other config:**
```
[Chain: Base ▼] [Storage: Onchain ▼] [x402: Off ▼]
[↩️ Back to Draft]
```

| Trust Model | Description |
|-------------|-------------|
| **Reputation** | On-chain feedback & scoring. Default for most agents. |
| **Crypto-Economic** | Staking/slashing guarantees. For financial agents. |
| **TEE Attestation** | Hardware-level trust proof. For high-security agents. |

### Step 4: Back to Draft

After any edit, re-send the updated full draft as a **single message with buttons** (same as Step 2). Repeat until user taps **✅ Register**.

### Step 5: Execute

Only after explicit ✅ Register confirmation.

1. Write the registration JSON to a temp file
2. Run the script:

```bash
source /path/to/.env
node scripts/register.mjs --json /tmp/registration.json --chain 8453 --yes
```

The script handles: `register()` → `setA2A()`/`setMCP()` → `addSkill()`/`addDomain()` → `setWallet()`

### Step 5.5: Progress Updates

Send progress updates during registration:

```
⏳ Step 1/3: Minting agent NFT on Base...
✅ Agent minted! ID: 8453:42

⏳ Step 2/3: Setting endpoints & metadata...
✅ Endpoints configured

⏳ Step 3/3: Linking wallet via EIP-712...
✅ Wallet linked!
```

### Step 6: Report Result

```
✅ Agent Registered on Base!

  Agent ID:    8453:42
  Wallet:      0x1348...e41
  A2A:         a2a.teeclaw.xyz/a2a
  TX:          0xabc...def

  View: https://8004.org/agent/8453:42
```

## Error Handling

### Missing Required Fields
If **Name** or **Description** are empty after prefill, mark them ⚠️ and block registration. Show: "Please fill required fields first."

### No Wallet
```
⚠️ No wallet detected. You need one to register:
  Option A: Paste your 0x... address
  Option B: Add PRIVATE_KEY to your .env file
```

### Transaction Failures
Show error clearly and offer retry:
```
❌ Registration failed: insufficient funds for gas
[🔄 Retry] [❌ Cancel]
```

### setWallet Failure
Public RPCs (e.g. mainnet.base.org) don't support `eth_signTypedData_v4`. If setWallet fails:
```
⚠️ Wallet linking failed (public RPC limitation).
You can link your wallet manually at https://8004.org
```
This is non-blocking — the agent is registered, just wallet isn't linked on-chain yet.

### Duplicate Registration Prevention
The script checks if the wallet already owns agent(s) on the target chain **before** submitting. If detected:
```
⚠️ Warning: This wallet already owns 1 agent(s) on Base.
   Registering again will create a duplicate.
   Use update.mjs to modify an existing agent instead.
```
In chat flow, warn the user and suggest updating instead of re-registering. The check is non-blocking if `--yes` is passed.

### Already Registered
If the agent already has an agentId, offer to **update** instead of register.

## Technical Notes

### Registry Overrides
The SDK only ships with Ethereum Mainnet registry addresses. For Base and other chains, the script passes `registryOverrides` with deterministic contract addresses:
- Identity Registry: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- Reputation Registry: `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

### Transaction Handling
The SDK returns `TransactionHandle` objects. Use `.waitMined()` (not `.wait()`) to await confirmation.

## All Fields Reference

### Basic Info
| Field | Required | Default | Auto-source |
|-------|----------|---------|-------------|
| **Agent Name** | ✅ | — | IDENTITY.md |
| **Agent Address** | auto | — | `.env` private key or pasted |
| **Description** | ✅ | — | IDENTITY.md / SOUL.md |
| **Image** | No | — | Profile image URL |
| **Version** | No | `1.0.0` | — |
| **Author** | No | — | USER.md |
| **License** | No | `MIT` | — |

### Endpoints
| Field | Required | Default | Auto-source |
|-------|----------|---------|-------------|
| **A2A Endpoint** | No | — | IDENTITY.md |
| **MCP Endpoint** | No | — | — |

### Skills & Domains
| Field | Required | Default |
|-------|----------|---------|
| **Selected Skills** | No | `[]` |
| **Selected Domains** | No | `[]` |
| **Custom Skills** | No | `[]` |
| **Custom Domains** | No | `[]` |

### Advanced Config
| Field | Required | Default |
|-------|----------|---------|
| **Trust Models** | No | `[]` (suggest: reputation) |
| **x402 Support** | No | `false` |
| **Storage** | No | `http` (fully onchain) |
| **Active** | No | `true` |
| **Chain** | No | `8453` (Base) |

## Supported Chains

| Chain | ID | Default |
|-------|-----|---------|
| **Base** | 8453 | ✅ |
| Ethereum | 1 | |
| Polygon | 137 | |
| BNB Chain | 56 | |
| Arbitrum | 42161 | |
| Celo | 42220 | |
| Gnosis | 100 | |
| Scroll | 534352 | |

All chains use the same deterministic contract addresses.

## JSON Template (8004.org format)

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

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PRIVATE_KEY` / `AGENT_PRIVATE_KEY` / `MAIN_WALLET_PRIVATE_KEY` | Yes | Wallet private key |
| `RPC_URL` | No | Custom RPC (auto-detected per chain) |
| `CHAIN_ID` | No | Default chain (8453) |

## Other Operations

```bash
# Search agents
node scripts/search.mjs --name "AgentName" --chain 8453

# Update agent
node scripts/update.mjs --agent-id "8453:42" --name "NewName" --yes

# Give feedback
node scripts/feedback.mjs --agent-id "8453:42" --value 5 --tag1 "reliable" --yes
```

## Setup

```bash
bash scripts/setup.sh
```
