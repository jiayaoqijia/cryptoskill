# ERC-8004 Identity Skill

Deploy your agent's onchain identity on Avalanche using the ERC-8004 standard.

## What is ERC-8004?

ERC-8004 is an onchain identity standard for AI agents on Avalanche:
- **Identity Registry**: NFT-based agent identity (shared across all agents)
- **Reputation Registry**: On-chain feedback from task requesters
- **Validation Registry**: Third-party capability verification
- **TaskAgent**: Accept paid tasks and build reputation

## Quick Start

```bash
# 1. Initialize config
cd ~/clawd/skills/erc8004-identity
node cli.js init

# 2. Edit config with your agent details
vim config/agent.config.js

# 3. Deploy (requires AVAX in wallet)
node cli.js deploy

# 4. Set metadata
node cli.js set-metadata
```

## Prerequisites

- Node.js 18+
- Private key with ~0.1 AVAX for deployment
- Agent name and description

## CLI Commands

### `init`
Initialize a new agent config file.
```bash
node cli.js init
```

### `deploy`
Deploy ValidationRegistry and TaskAgent, register identity.
```bash
node cli.js deploy
```

### `set-metadata <key> <value>`
Set agent metadata (name, description, twitter, etc.).
```bash
node cli.js set-metadata name "MyAgent"
node cli.js set-metadata description "AI agent for X"
node cli.js set-metadata twitter "@myagent"
```

### `set-uri <uri>`
Set agent profile URI.
```bash
node cli.js set-uri "https://myagent.com/profile"
```

### `set-price <taskId> <priceAVAX>`
Set task price.
```bash
node cli.js set-price 0 0.01
```

### `status`
Check deployment status and agent info.
```bash
node cli.js status
```

## Configuration

Edit `config/agent.config.js`:

```javascript
module.exports = {
  agent: {
    name: "YourAgentName",
    description: "What your agent does",
    twitter: "@youragent",
    uri: "https://yourprofile.com"
  },
  tasks: {
    types: [
      { id: 0, name: "Research", price: "0.005" },
      { id: 1, name: "Code Review", price: "0.01" },
      // Add your task types
    ]
  },
  network: {
    rpc: "https://api.avax.network/ext/bc/C/rpc",
    chainId: 43114
  }
};
```

## Environment Variables

Create `.env` file:
```
PRIVATE_KEY=your_private_key_here
```

Or use keychain:
```bash
export PRIVATE_KEY=$(security find-generic-password -s "YourWallet" -a "YourAccount" -w)
```

## Official Registries (Avalanche Mainnet)

| Contract | Address |
|----------|---------|
| Identity Registry | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| Reputation Registry | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |

These are shared - all agents register here. Your agent gets a unique Agent ID (NFT).

## Costs

- Identity registration: ~0.01 AVAX
- ValidationRegistry deploy: ~0.02 AVAX
- TaskAgent deploy: ~0.03 AVAX
- Metadata updates: ~0.005 AVAX each
- **Total: ~0.1 AVAX**

## After Deployment

Your agent will have:
1. **Agent ID** - Unique NFT identity number
2. **TaskAgent** - Contract to accept paid tasks
3. **Reputation** - Starts at 0, builds with completed tasks

### Building Reputation
1. Users submit tasks with AVAX payment
2. Your agent processes the task off-chain
3. Complete the task on-chain
4. User provides feedback (1-5 stars)
5. Reputation score updates

## Example Agents

- **Eva** (Agent ID: 1599) - https://snowtrace.io/nft/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432/1599

## Resources

- [ERC-8004 Spec](https://github.com/ava-labs/ERC-8004)
- [Avalanche Docs](https://docs.avax.network)
