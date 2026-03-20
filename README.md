<div align="center">

# CryptoSkill

**The Crypto Skill Hub for AI Agents**

Discover, install, and build AI agent skills for every crypto protocol, exchange, and tool.

[![Skills](https://img.shields.io/badge/skills-313-6366f1)]() [![Categories](https://img.shields.io/badge/categories-13-22d3ee)]() [![License](https://img.shields.io/badge/license-AGPL--3.0-green)]()

[Website](https://cryptoskill.app) · [Browse Skills](#skills-overview) · [Contributing](CONTRIBUTING.md)

</div>

---

## What is CryptoSkill?

CryptoSkill is a curated registry of AI agent skills for the crypto ecosystem. Each skill is a self-contained module that teaches an AI agent how to interact with a specific protocol, exchange, or tool — from placing trades on Binance to monitoring DeFi positions on Aave.

Whether you're building an autonomous trading agent, a portfolio tracker, or a research assistant, CryptoSkill gives you production-ready building blocks so you don't have to start from scratch.

### Why CryptoSkill?

- **313 skills** covering the full crypto stack — exchanges, DeFi, wallets, analytics, and more
- **107 official skills** from verified project teams (Binance, OKX, Coinbase, Gate.io, Nansen, and more)
- **Plug and play** — each skill follows a standard format compatible with [OpenClaw](https://github.com/nicholasgriffintn/openclaw) agents
- **Always growing** — new skills are added regularly as the ecosystem evolves

## Skills Overview

| Category | Skills | Highlights |
|---|---|---|
| **Exchanges** | 110 | Binance (official), OKX (official), Gate.io (official), Bitget (official), Hyperliquid, Kraken, Bybit, Coinbase, KuCoin, MEXC |
| **Chains** | 39 | Ethereum, Solana, Bitcoin, Lightning Network, Arbitrum, Base, Sui, Polygon, Cosmos, Monad, TON |
| **Analytics** | 34 | CoinMarketCap (official), CoinGecko, Nansen (official), DefiLlama, Dune, Etherscan, The Graph, Zapper, Zerion |
| **Trading** | 25 | Grid trading, copy trading, whale tracking, yield scanning, airdrop hunting, signals |
| **DeFi** | 21 | Uniswap, Aave, SushiSwap, PancakeSwap, Raydium, OpenSea (official), Pump.fun, Jupiter |
| **Identity** | 14 | ERC-8004 on-chain agent identity, discovery, reputation, Pinata |
| **Payments** | 13 | x402 protocol, agent marketplace, paywall kit, private search |
| **Wallets** | 13 | MetaMask, Bitget Wallet (official), Cobo TSS, WalletConnect, MPC payments |
| **Prediction Markets** | 12 | Polymarket trading, odds, data API, whale copying, sports edge |
| **Dev Tools** | 11 | Alchemy (official MCP), Moralis, Foundry, Hardhat, Viem, Wagmi |
| **MCP Servers** | 9 | Coinbase AgentKit, Alchemy, Solana Agent Kit, GOAT, Tatum, deBridge, Web3 MCP |
| **Social** | 7 | Farcaster, Nostr, XMTP (official) |
| **AI x Crypto** | 5 | Bittensor, Virtuals Protocol (official), ElizaOS |

## Quick Start

### Browse Skills

Visit [cryptoskill.app](https://cryptoskill.app) to search and browse all skills with filtering by category, protocol, and use case.

### Install a Skill

Each skill is a directory containing a `SKILL.md` (documentation and frontmatter) and `_meta.json` (metadata). To use a skill with an OpenClaw-compatible agent:

```bash
# Clone the repository
git clone https://github.com/jiayaoqijia/cryptoskill.git
cd cryptoskill

# Copy a skill into your agent's workspace
cp -r skills/exchanges/binance-spot-api ~/my-agent/workspace/skills/
```

### Skill Format

Every skill follows a standard structure:

```
skills/{category}/{skill-name}/
  SKILL.md        # Frontmatter + documentation
  _meta.json      # Version history and ownership
  SOURCE.md       # Attribution and provenance
  index.js        # Optional: executable entry point
  skill.yaml      # Optional: additional configuration
  scripts/        # Optional: executable scripts
  references/     # Optional: reference documentation
```

The `SKILL.md` frontmatter includes the skill name, description, version, author, tags, triggers, and configuration requirements.

### Use with an AI Agent

Skills are designed to work with [OpenClaw](https://github.com/nicholasgriffintn/openclaw)-compatible agents. The agent reads the `SKILL.md` to understand what the skill does, when to invoke it, and how to use it.

```bash
# Example: configure an agent with exchange skills
cp -r skills/exchanges/binance-spot-api ~/my-agent/workspace/skills/
cp -r skills/exchanges/hyperliquid ~/my-agent/workspace/skills/
cp -r skills/analytics/coingecko-price ~/my-agent/workspace/skills/

# Start your agent — it will auto-discover the skills
my-agent start
```

## Source Attribution

All skills in this repository are sourced from the [ClawHub](https://clawhub.ai) community registry and are published under the **MIT-0** license (no attribution required). Each skill includes a `SOURCE.md` file documenting its original author and source.

We gratefully acknowledge the work of both official project teams and community contributors who created these skills.

### Official Skills

**107 skills** from verified project teams with official GitHub repos:

| Project | Skills | Source |
|---|---|---|
| [Binance](https://www.binance.com/) | 20 | [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub) |
| [OKX](https://www.okx.com/) | 16 | [okx/onchainos-skills](https://github.com/okx/onchainos-skills), [okx/agent-skills](https://github.com/okx/agent-skills) |
| [Gate.io](https://www.gate.io/) | 13 | ClawHub: gate-exchange |
| [Nansen](https://www.nansen.ai/) | 10 | ClawHub: nansen-devops |
| [CoinMarketCap](https://coinmarketcap.com/) | 7 | ClawHub: bryan-cmc |
| [Bitget](https://www.bitget.com/) | 7 | [BitgetLimited/agent_hub](https://github.com/BitgetLimited/agent_hub) |
| [Lightning Labs](https://lightning.engineering/) | 3 | ClawHub: roasbeef (CTO) |
| [OpenSea](https://opensea.io/) | 2 | ClawHub: dfinzer (CEO) |
| [SushiSwap](https://www.sushi.com/) | 2 | ClawHub: 0xmasayoshi (CTO) |
| [Coinbase](https://www.coinbase.com/) | 1 | [coinbase/agentkit](https://github.com/coinbase/agentkit) |
| [Alchemy](https://www.alchemy.com/) | 1 | [alchemyplatform/alchemy-mcp-server](https://github.com/alchemyplatform/alchemy-mcp-server) |
| + 15 more | — | Virtuals, XMTP, ElizaOS, deBridge, GOAT, Tatum, etc. |

### Community Skills

Community-contributed skills from prolific contributors including jolestar, ivangdavila, mosonchan2023, squirt11e, and many others. Each skill's `SOURCE.md` credits the original author.

## Contributing

We welcome contributions of all kinds — new skills, improvements to existing skills, documentation, and bug reports. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

Quick overview:

1. Fork the repository
2. Add or update a skill following the [skill format](#skill-format)
3. Include `SKILL.md`, `_meta.json`, and `SOURCE.md`
4. Open a pull request

## License

This project is licensed under **AGPL-3.0** — see [LICENSE](LICENSE) for details.

Individual skills retain their original **MIT-0** license as published on ClawHub. See [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES) for full attribution.

## Acknowledgments

- [ClawHub](https://clawhub.ai) — The skill registry where all skills originate
- [OpenClaw](https://github.com/nicholasgriffintn/openclaw) — The agent framework powering skills
- All original skill authors — see `SOURCE.md` in each skill directory for individual credits
