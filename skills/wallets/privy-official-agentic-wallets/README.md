# Privy Agentic Wallets Skill

Create crypto wallets with [Privy](https://privy.io) that AI agents can control autonomously with policy-based guardrails.

## What This Is

A skill (structured instructions + reference docs) that teaches AI agents how to use the **Privy API** to:

- Create Privy server wallets on Ethereum, Solana, and 10+ other chains
- Set up Privy policies (spending limits, allowed contracts, chain restrictions)
- Execute transactions through Privy's wallet infrastructure
- Manage wallets via the Privy API

Built on [Privy's Server Wallets](https://docs.privy.io/guide/server-wallets) — wallets designed for autonomous, programmatic use without requiring user interaction.

## Use Cases

What can autonomous agents do with their own wallets?

**Trading & DeFi**
- Execute swaps on DEXs based on market conditions
- Rebalance portfolios automatically
- Claim and compound yield farming rewards
- Manage liquidity positions

**Payments & Commerce**
- Pay for API calls and services autonomously
- Tip content creators or contributors
- Split payments across multiple recipients
- Handle subscriptions and recurring payments

**On-chain Automation**
- Monitor and execute governance votes
- Auto-renew ENS domains
- Trigger smart contract functions on schedule
- Bridge assets across chains when conditions are met

**Agent-to-Agent Transactions**
- Pay other agents for completed tasks
- Escrow funds for multi-agent workflows
- Pool resources for collective purchases
- Settle debts between collaborating agents

**NFTs & Digital Assets**
- Mint NFTs on behalf of users
- Purchase NFTs matching specific criteria
- Manage collections and metadata
- List and sell assets on marketplaces

## Quick Start

### 1. Get Your Privy Credentials

1. Go to [dashboard.privy.io](https://dashboard.privy.io)
2. Create a Privy app (or use existing)
3. Go to **Settings → Basics** and copy your **App ID** and **App Secret**

### 2. Set Environment Variables

```bash
export PRIVY_APP_ID="your-app-id"
export PRIVY_APP_SECRET="your-app-secret"
```

### 3. Give the Skill to Your Agent

See platform-specific instructions below.

---

## Usage by Platform

### Claude (claude.ai / Claude Desktop)

Copy the contents of `SKILL.md` into your conversation or project instructions. For complex tasks, also share the relevant reference files:

```
Hey Claude, here's a skill for using Privy agentic wallets:

[paste SKILL.md contents]

When I ask about Privy policies, also reference this:

[paste references/policies.md contents]
```

Or attach the files directly if using Claude with file uploads.

### Cursor

Add the skill to your project:

```bash
# Clone into your project
git clone https://github.com/tedim52/privy-agentic-wallets-skill.git .cursor/skills/privy
```

Then reference it in your Cursor rules or just ask:

> "Read the Privy skill in .cursor/skills/privy and help me create an agentic wallet"

### OpenClaw

Install into your workspace skills folder:

```bash
# Option 1: Clone directly
git clone https://github.com/tedim52/privy-agentic-wallets-skill.git ~/.openclaw/workspace/skills/privy

# Option 2: If published to ClawHub
clawhub install privy
```

Add your Privy credentials to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "env": {
    "vars": {
      "PRIVY_APP_ID": "your-app-id",
      "PRIVY_APP_SECRET": "your-app-secret"
    }
  }
}
```

The agent will automatically use the skill when you ask about Privy wallets.

### Windsurf / Codeium

Add to your workspace and reference in cascade:

```bash
git clone https://github.com/tedim52/privy-agentic-wallets-skill.git .windsurf/skills/privy
```

### Other Agents (GPT, Gemini, etc.)

Copy `SKILL.md` into your system prompt or conversation. The skill is just markdown — any agent that can read text can use it to interact with Privy.

---

## What's Included

```
privy/
├── SKILL.md                 # Main Privy API instructions + quick reference
└── references/
    ├── setup.md             # Privy dashboard setup guide
    ├── wallets.md           # Privy wallet CRUD operations
    ├── policies.md          # Privy policy rules and conditions
    └── transactions.md      # Privy transaction examples (EVM + Solana)
```

## Chains Supported by Privy

| Chain | Type | CAIP-2 |
|-------|------|--------|
| Ethereum | `ethereum` | `eip155:1` |
| Base | `ethereum` | `eip155:8453` |
| Polygon | `ethereum` | `eip155:137` |
| Arbitrum | `ethereum` | `eip155:42161` |
| Optimism | `ethereum` | `eip155:10` |
| Solana | `solana` | `solana:mainnet` |

Privy also supports: Cosmos, Stellar, Sui, Aptos, Tron, Bitcoin (SegWit), NEAR, TON, Starknet

## Example: Create a Privy Wallet with Spending Limit

Ask your agent:

> "Create an Ethereum wallet using Privy with a policy that limits transactions to 0.1 ETH max, only on Base mainnet"

The agent will use the skill to:
1. Create a Privy policy with the constraints
2. Create a Privy server wallet with that policy attached
3. Return the wallet address

## Why Privy for Agentic Wallets?

- **Server-side control** — No user signatures required, agents can transact autonomously
- **Policy guardrails** — Constrain what agents can do (spending limits, allowed addresses, chain restrictions)
- **Multi-chain** — One API for Ethereum, Solana, and many more
- **Battle-tested** — Privy powers wallets for major crypto apps

## Links

- [Privy Website](https://privy.io)
- [Privy Dashboard](https://dashboard.privy.io)
- [Privy Documentation](https://docs.privy.io)
- [Privy Server Wallets Guide](https://docs.privy.io/guide/server-wallets)

## License

MIT
