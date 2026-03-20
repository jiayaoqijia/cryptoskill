<div align="center">

# CryptoSkill

**The Crypto Skill Hub for AI Agents**

Discover, install, and build AI agent skills and MCP servers for every crypto protocol, exchange, and tool.

[![Skills](https://img.shields.io/badge/skills-477-6366f1)]() [![MCP Servers](https://img.shields.io/badge/MCP%20servers-56-f59e0b)]() [![Official](https://img.shields.io/badge/official-221-22c55e)]() [![Categories](https://img.shields.io/badge/categories-13-22d3ee)]() [![License](https://img.shields.io/badge/license-AGPL--3.0-green)]()

[Website](https://cryptoskill.org) · [Browse Skills](#skills-overview) · [MCP Servers](#mcp-servers) · [Submit a Skill](#submit-a-skill) · [Contributing](CONTRIBUTING.md)

</div>

> [!CAUTION]
> **This project is under active development.** None of the skills or MCP servers listed here have been audited. This is a community-compiled directory of projects shared on social media, listed on skill hubs, and found across public repositories. We make no guarantees about their safety, integrity, or intentions. Exercise extreme caution with anything that touches wallets, private keys, seed phrases, or transaction signing -- a malicious skill can compromise your agent and drain your funds. Always review the source code, verify the authors, and do your own research (DYOR) before installing or granting permissions to any skill or MCP server.

---

## What is CryptoSkill?

CryptoSkill is the largest curated registry of AI agent skills and MCP servers for the crypto ecosystem. Each skill is a self-contained module that teaches an AI agent how to interact with a specific protocol, exchange, or tool -- from placing trades on Binance to monitoring DeFi positions on Aave.

Whether you're building an autonomous trading agent, a portfolio tracker, or a research assistant, CryptoSkill gives you production-ready building blocks so you don't have to start from scratch.

### Why CryptoSkill?

- **477 skills** covering the full crypto stack -- exchanges, DeFi, wallets, analytics, and more
- **56 MCP servers** for direct protocol integration with Claude, Cursor, and other AI tools
- **221 official skills** from verified project teams (Binance, OKX, Kraken, KuCoin, Uniswap, Gate.io, Nansen, and more)
- **Plug and play** -- works with Claude Code (`.claude/skills/`), OpenClaw (`clawhub install`), and any SKILL.md-based agent
- **Auto-updated** -- bot scans 128+ projects every 6 hours for new skills and MCP servers
- **Security scanned** -- all skills checked for malicious code before inclusion

## Skills Overview

| Category | Skills | Highlights |
|---|---|---|
| **Exchanges** | 172 | Binance (official), OKX (official), Kraken (official 50 skills), KuCoin (official), Gate.io (official), Bitget (official), Hyperliquid, Bybit, Coinbase, MEXC |
| **DeFi** | 46 | Uniswap (official 8), GMX (official), Rocket Pool (official 7), Venus (official), Lido, Aave, SushiSwap, PancakeSwap, Raydium, OpenSea, Pump.fun |
| **MCP Servers** | 45 | Alchemy, Solana, CoinGecko, EigenLayer, Blockscout, Alpaca, NEAR, deBridge, Kraken CLI, Jupiter, CCXT, Chainlink |
| **Chains** | 41 | Ethereum, Solana, Bitcoin, Lightning Network, BNB Chain, Arbitrum, Base, Sui, Polygon, Cosmos, Monad, Aptos, TON |
| **Analytics** | 36 | CoinMarketCap (official 7), CoinGecko, Nansen (official 10), DefiLlama, Dune, Etherscan, The Graph, Zapper, Zerion |
| **Trading** | 25 | Grid trading, copy trading, whale tracking, yield scanning, airdrop hunting, DCA, signals |
| **Identity** | 17 | ERC-8004, 8004scan, 8004scan-webhooks, self-agent-id, on-chain reputation |
| **Payments** | 16 | x402 protocol, mpp, tempo, agent marketplace, paywall kit |
| **Wallets** | 14 | MetaMask, Bitget Wallet (official), crypto-wallet, Cobo TSS, WalletConnect, MPC |
| **Dev Tools** | 12 | CryptoSkill registry, Alchemy, Moralis, Foundry, Hardhat, Viem, Wagmi |
| **Prediction Markets** | 12 | Polymarket API, trading bots, whale copying, sports edge, CLI trading |
| **AI x Crypto** | 10 | Bittensor, Virtuals Protocol, ElizaOS, privacy-layer, venice-private-ai |
| **Social** | 7 | Farcaster, Nostr, XMTP (official) |

## MCP Servers

CryptoSkill maintains **56 MCP (Model Context Protocol) servers** for crypto -- the largest curated collection focused on the crypto ecosystem.

### Official MCP Servers

| MCP Server | Project | Install |
|---|---|---|
| [Alchemy](skills/mcp-servers/alchemy-mcp/) | Alchemy | `claude mcp add alchemy` |
| [Alpaca](skills/mcp-servers/alpaca-mcp/) | Alpaca | `git clone alpacahq/alpaca-mcp-server` |
| [Aptos](skills/mcp-servers/aptos-mcp/) | Aptos Labs | `git clone aptos-labs/aptos-npm-mcp` |
| [Base](skills/mcp-servers/base-mcp/) | Coinbase | `git clone base/base-mcp` |
| [Blockscout](skills/mcp-servers/blockscout-mcp/) | Blockscout | `claude mcp add blockscout https://mcp.blockscout.com/mcp` |
| [BNB Chain](skills/mcp-servers/bnbchain-mcp/) | BNB Chain | `git clone bnb-chain/bnbchain-mcp` |
| [Coinbase AgentKit](skills/mcp-servers/coinbase-agentkit/) | Coinbase | `npm create onchain-agent@latest` |
| [CoinGecko](skills/mcp-servers/coingecko-mcp-official/) | CoinGecko | `npx @coingecko/coingecko-mcp` |
| [DefiLlama](skills/mcp-servers/defillama-mcp/) | dcSpark | `git clone dcSpark/mcp-server-defillama` |
| [DexPaprika](skills/mcp-servers/dexpaprika-mcp/) | CoinPaprika | `git clone coinpaprika/dexpaprika-mcp` |
| [EigenLayer](skills/mcp-servers/eigenlayer-mcp/) | Layr-Labs | `claude mcp add --transport sse eigenlayer https://eigenlayer-mcp-server-sand.vercel.app/sse` |
| [Kraken CLI](skills/mcp-servers/kraken-cli-mcp/) | Kraken | `git clone krakenfx/kraken-cli` |
| [Monad](skills/mcp-servers/monad-mcp/) | Monad | `git clone monad-developers/monad-mcp` |
| [NEAR](skills/mcp-servers/near-mcp/) | NEAR | `git clone nearai/near-mcp` |
| [Solana](skills/mcp-servers/solana-mcp-official/) | Solana Foundation | `git clone solana-foundation/solana-mcp-official` |

### Community MCP Servers

| MCP Server | Description |
|---|---|
| [Alby NWC](skills/mcp-servers/alby-nwc-mcp/) | Lightning Network wallet connect |
| [Bitcoin](skills/mcp-servers/bitcoin-mcp/) | Bitcoin blockchain tools |
| [CCXT](skills/mcp-servers/ccxt-mcp/) | Unified exchange API (100+ exchanges) |
| [Chainlink Feeds](skills/mcp-servers/chainlink-feeds-mcp/) | Oracle price feed data |
| [CoinStats](skills/mcp-servers/coinstats-mcp/) | Portfolio and market tracking |
| [deBridge](skills/mcp-servers/debridge-mcp/) | Cross-chain bridging |
| [DEXScreener](skills/mcp-servers/dexscreener-mcp/) | Real-time DEX pair tracking |
| [Dune Analytics](skills/mcp-servers/dune-analytics-mcp/) | On-chain analytics queries |
| [EVM](skills/mcp-servers/evm-mcp/) | Universal EVM chain tools (30+ chains) |
| [Funding Rates](skills/mcp-servers/funding-rates-mcp/) | Perpetual funding rate data |
| [GOAT Onchain](skills/mcp-servers/goat-onchain/) | 200+ on-chain actions |
| [Helius](skills/mcp-servers/helius-mcp/) | Solana RPC and DAS API |
| [Hive Intelligence](skills/mcp-servers/hive-crypto-mcp/) | Crypto + macro analytics |
| [Jupiter](skills/mcp-servers/jupiter-mcp/) | Solana swap aggregation |
| [Lightning](skills/mcp-servers/lightning-mcp/) | Lightning Network payments |
| [Nodit](skills/mcp-servers/nodit-mcp/) | Multi-chain node infrastructure |
| [Solana Agent Kit](skills/mcp-servers/solana-agent-kit/) | Full Solana agent toolkit |
| [StarkNet](skills/mcp-servers/starknet-mcp/) | StarkNet L2 integration |
| [Tatum](skills/mcp-servers/tatum-blockchain-mcp/) | Multi-chain API (130+ networks) |
| [The Graph Token API](skills/mcp-servers/thegraph-token-api/) | Subgraph token data |
| [Web3 MCP](skills/mcp-servers/web3-mcp/) | Multi-chain Web3 tools |
| [Whale Tracker](skills/mcp-servers/whale-tracker-mcp/) | Large transaction monitoring |

> **Looking for an MCP server that's not listed?** [Submit it!](#submit-a-skill)

## Quick Start

### Install the CryptoSkill Skill

Give your AI agent access to the full registry:

```bash
git clone https://github.com/jiayaoqijia/cryptoskill.git /tmp/cs
cp -r /tmp/cs/skills/dev-tools/cryptoskill .claude/skills/
```

### Install a Skill (Claude Code)

```bash
# Copy a skill into your project's Claude Code skills
cp -r /tmp/cs/skills/exchanges/binance-spot-api .claude/skills/
cp -r /tmp/cs/skills/defi/uniswap-official-swap-integration .claude/skills/
```

### Install an MCP Server

```bash
# Add a hosted MCP server
claude mcp add blockscout https://mcp.blockscout.com/mcp

# Or install from npm
npx @coingecko/coingecko-mcp

# Or clone and run locally
git clone https://github.com/solana-foundation/solana-mcp-official.git
cd solana-mcp-official && npm install && npm start
```

### Install via ClawHub CLI (OpenClaw)

```bash
npm i -g clawhub
clawhub install binance-spot-api
```

## Official Skills

**221 skills** from verified project teams with official GitHub repos:

| Project | Skills | Source |
|---|---|---|
| [Kraken](https://www.kraken.com/) | 50 | [krakenfx/kraken-cli](https://github.com/krakenfx/kraken-cli) |
| [Binance](https://www.binance.com/) | 20+ | [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub) |
| [OKX](https://www.okx.com/) | 16+ | [okx/onchainos-skills](https://github.com/okx/onchainos-skills) |
| [Gate.io](https://www.gate.io/) | 13 | ClawHub: gate-exchange |
| [Nansen](https://www.nansen.ai/) | 10 | ClawHub: nansen-devops |
| [Uniswap](https://uniswap.org/) | 8 | [Uniswap/uniswap-ai](https://github.com/Uniswap/uniswap-ai) |
| [CoinMarketCap](https://coinmarketcap.com/) | 7 | ClawHub: bryan-cmc |
| [Bitget](https://www.bitget.com/) | 7 | [BitgetLimited/agent_hub](https://github.com/BitgetLimited/agent_hub) |
| [KuCoin](https://www.kucoin.com/) | 7 | [Kucoin/kucoin-skills-hub](https://github.com/Kucoin/kucoin-skills-hub) |
| [Rocket Pool](https://rocketpool.net/) | 7 | [rocket-pool/skills](https://github.com/rocket-pool/skills) |
| [Ottie](https://github.com/jiayaoqijia/ottie) | 18 | Crypto DeFi, wallets, market data, mpp, tempo |
| [Lightning Labs](https://lightning.engineering/) | 3 | ClawHub: roasbeef (CTO) |
| [GMX](https://gmx.io/) | 2 | [gmx-io/gmx-ai](https://github.com/gmx-io/gmx-ai) |
| [OpenSea](https://opensea.io/) | 2 | ClawHub: dfinzer (CEO) |
| [SushiSwap](https://www.sushi.com/) | 2 | ClawHub: 0xmasayoshi (CTO) |
| [Venus Protocol](https://venus.io/) | 1 | [VenusProtocol/venus-agent-skills](https://github.com/VenusProtocol/venus-agent-skills) |
| + MCP servers | 45 | Alchemy, Coinbase, Solana, EigenLayer, Blockscout, Alpaca, NEAR, Base, Monad, CoinGecko, and more |

## Submit a Skill

We welcome contributions from the community. Submit via:

1. **GitHub PR** -- Fork, add your skill, open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md)
2. **Quick Submit** -- Email maintainers@altresear.ch with the skill name, GitHub URL, category, and description
3. **Website** -- Use the submit form at [cryptoskill.org](https://cryptoskill.org)

All submissions are reviewed for security and quality before merging.

## Auto-Update Bot

CryptoSkill runs an automated bot every 6 hours that:

1. Scans 128+ project GitHub orgs for new skills and MCP servers
2. Checks 17 official repos for updates (SHA-tracked, only clones changed repos)
3. Searches GitHub API for trending crypto MCP repos
4. Security scans all new skills (static analysis + AI review)
5. Copies new skills, updates existing ones, regenerates the catalog
6. Commits and pushes changes automatically

See [scripts/auto-update.py](scripts/auto-update.py) and [scripts/watchlist.json](scripts/watchlist.json).

## Roadmap

See [ROADMAP.md](ROADMAP.md) for development plans including a CLI installer, search API, community ratings, and more.

## Legal

- [Terms of Service](https://cryptoskill.org/terms.html)
- [Privacy Policy](https://cryptoskill.org/privacy.html)

## License

This project is licensed under **AGPL-3.0** -- see [LICENSE](LICENSE) for details.

Individual skills retain their original licenses (mostly **MIT-0**). See [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES).

## Acknowledgments

- [ClawHub](https://clawhub.ai) -- Skill registry where community skills originate
- [OpenClaw](https://github.com/nicholasgriffintn/openclaw) -- Agent framework powering skills
- [Ottie](https://github.com/jiayaoqijia/ottie) -- Self-evolving crypto AI agent
- All original skill authors -- see `SOURCE.md` in each skill directory
