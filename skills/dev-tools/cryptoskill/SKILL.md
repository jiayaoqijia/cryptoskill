---
name: cryptoskill
description: Search, browse, and install crypto AI agent skills and MCP servers from cryptoskill.org — the largest curated registry of crypto skills with 450+ skills and 40+ MCP servers across 13 categories.
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    emoji: "🔐"
    tags: [crypto, skills, mcp, registry, search, install]
    requires:
      bins: [git]
---

# CryptoSkill — Crypto Skill Registry

Search, browse, and install crypto AI agent skills and MCP servers from [cryptoskill.org](https://cryptoskill.org).

## When to Use

Use this skill when:
- The user asks to find crypto/blockchain/DeFi/exchange skills
- The user wants to install a skill for a specific protocol (e.g., "install Binance trading skill")
- The user asks about available MCP servers for crypto
- The user wants to search for skills by category (exchanges, DeFi, chains, analytics, etc.)
- The user says "cryptoskill", "/cryptoskill", or asks about crypto agent capabilities

## Available Categories

| Category | Skills | Examples |
|---|---|---|
| exchanges | 168 | Binance, OKX, Kraken, KuCoin, Hyperliquid, Gate.io |
| defi | 46 | Uniswap, Aave, GMX, Rocket Pool, Venus, Lido |
| mcp-servers | 45 | Alchemy, Solana, CoinGecko, EigenLayer, Blockscout |
| chains | 41 | Ethereum, Solana, Bitcoin, Lightning, Base, Monad |
| analytics | 36 | CoinMarketCap, Nansen, Dune, DefiLlama, Etherscan |
| trading | 25 | Grid trading, whale tracking, yield scanning, signals |
| identity | 17 | ERC-8004, 8004scan, self-agent-id |
| payments | 16 | x402, mpp, tempo |
| wallets | 14 | MetaMask, Bitget Wallet, Cobo TSS, MPC |
| prediction-markets | 12 | Polymarket API, trading bots, whale copying |
| dev-tools | 12 | Alchemy, Moralis, Foundry, Hardhat, Wagmi |
| social | 7 | Farcaster, Nostr, XMTP |
| ai-crypto | 7 | Bittensor, Virtuals, ElizaOS, privacy-layer |

## How to Search

### Search by name
```
Find skills related to "uniswap"
```
The agent will search the registry at https://github.com/jiayaoqijia/cryptoskill/tree/main/skills

### Search by category
```
Show me all DeFi skills
List available MCP servers
What exchange skills are available?
```

### Search by protocol
```
Find Binance official skills
Are there Solana MCP servers?
What skills does Kraken have?
```

## How to Install

### Install a Skill (for Claude Code)

```bash
# Clone the registry (one time)
git clone https://github.com/jiayaoqijia/cryptoskill.git /tmp/cs

# Copy a skill into your project
cp -r /tmp/cs/skills/exchanges/binance-spot-api .claude/skills/

# Or copy multiple skills
cp -r /tmp/cs/skills/defi/uniswap-official-swap-integration .claude/skills/
cp -r /tmp/cs/skills/analytics/coingecko-price .claude/skills/
```

### Install an MCP Server (for Claude Code)

```bash
# Add a hosted MCP server
claude mcp add blockscout https://mcp.blockscout.com/mcp

# Or add via SSE
claude mcp add --transport sse eigenlayer-mcp https://eigenlayer-mcp-server-sand.vercel.app/sse

# Or install from npm
npx @coingecko/coingecko-mcp

# Or clone and run locally
git clone https://github.com/solana-foundation/solana-mcp-official.git
cd solana-mcp-official && npm install && npm start
```

### Install via ClawHub CLI (for OpenClaw)

```bash
npm i -g clawhub
clawhub install binance-spot-api
```

## Official Skills

These skills come from verified project teams:

| Project | Skills | Source |
|---|---|---|
| Kraken | 50 | krakenfx/kraken-cli |
| Binance | 20+ | binance/binance-skills-hub |
| OKX | 16+ | okx/onchainos-skills |
| Gate.io | 13 | ClawHub: gate-exchange |
| Nansen | 10 | ClawHub: nansen-devops |
| Uniswap | 8 | Uniswap/uniswap-ai |
| KuCoin | 7 | Kucoin/kucoin-skills-hub |
| Bitget | 7 | BitgetLimited/agent_hub |
| CoinMarketCap | 7 | coinmarketcap |
| Rocket Pool | 7 | rocket-pool/skills |

## Contributing

Submit new skills at [cryptoskill.org](https://cryptoskill.org) or open a PR at https://github.com/jiayaoqijia/cryptoskill

## Links

- Website: https://cryptoskill.org
- GitHub: https://github.com/jiayaoqijia/cryptoskill
- Submit: maintainers@altresear.ch
