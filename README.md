<div align="center">

# CryptoSkill

**The App Store Moment for Crypto AI Agents**

Before the App Store, iPhone developers distributed apps through ad hoc channels. Before npm, JavaScript developers emailed zip files. Every platform ecosystem goes through the same phase transition: fragmented distribution, then a registry, then an explosion of building. Crypto AI agents are at the registry moment.

[![Skills](https://img.shields.io/badge/skills-550-6366f1)]() [![MCP Servers](https://img.shields.io/badge/MCP%20servers-56-f59e0b)]() [![Official](https://img.shields.io/badge/official-221-22c55e)]() [![Categories](https://img.shields.io/badge/categories-13-22d3ee)]() [![License](https://img.shields.io/badge/license-AGPL--3.0-green)]()

[Website](https://cryptoskill.org) · [Browse Skills](#skills-550overview) · [MCP Servers](#mcp-servers) · [Submit a Skill](#submit-a-skill) · [Contributing](CONTRIBUTING.md)

</div>

> [!CAUTION]
> **This project is under active development.** None of the skills or MCP servers listed here have been audited. This is a community-compiled directory of projects shared on social media, listed on skill hubs, and found across public repositories. We make no guarantees about their safety, integrity, or intentions. Exercise extreme caution with anything that touches wallets, private keys, seed phrases, or transaction signing -- a malicious skill can compromise your agent and drain your funds. Always review the source code, verify the authors, and do your own research (DYOR) before installing or granting permissions to any skill or MCP server.

---

## Why CryptoSkill Exists

The MCP ecosystem crossed **97 million monthly SDK downloads**. Over 5,800 MCP servers exist. But a developer building a crypto AI agent today has to hunt through Binance's repo, Kraken's repo, Uniswap's repo, and 50 others just to assemble a working skill set. Different formats. No security review. No way to tell official from unofficial. In a typical organization, **38% of deployed MCP servers come from unknown authors** (Clutch Security).

The general-purpose skill registries (SkillsMP with 500K+ skills, SkillHub with 7K+) are too broad. They list crypto alongside cooking recipes and email templates. Crypto needs its own vertical registry for the same reason iOS and Android have separate app stores: the security model, the domain expertise, and the user expectations are fundamentally different.

CryptoSkill is the crypto-native answer:

- **477 skills** covering the full crypto stack -- exchanges, DeFi, wallets, analytics, trading, identity, payments
- **56 MCP servers** for direct protocol integration with Claude, Cursor, Codex, and other AI tools
- **221 official skills** from verified project teams (Kraken, Binance, OKX, Uniswap, Gate.io, Nansen, and more)
- **Security-scanned** -- every skill checked for hardcoded credentials, RCE, exfiltration, and prompt injection
- **Auto-updated** -- bot scans 128+ projects every 6 hours for new skills and changes
- **Open standard** -- SKILL.md + _meta.json + SOURCE.md, works with Claude Code, OpenClaw, and any SKILL.md agent

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
| [Binance](https://www.binance.com/) | 20+ | [binance/binance-skills-550hub](https://github.com/binance/binance-skills-hub) |
| [OKX](https://www.okx.com/) | 16+ | [okx/onchainos-skills](https://github.com/okx/onchainos-skills) |
| [Gate.io](https://www.gate.io/) | 13 | ClawHub: gate-exchange |
| [Nansen](https://www.nansen.ai/) | 10 | ClawHub: nansen-devops |
| [Uniswap](https://uniswap.org/) | 8 | [Uniswap/uniswap-ai](https://github.com/Uniswap/uniswap-ai) |
| [CoinMarketCap](https://coinmarketcap.com/) | 7 | ClawHub: bryan-cmc |
| [Bitget](https://www.bitget.com/) | 7 | [BitgetLimited/agent_hub](https://github.com/BitgetLimited/agent_hub) |
| [KuCoin](https://www.kucoin.com/) | 7 | [Kucoin/kucoin-skills-550hub](https://github.com/Kucoin/kucoin-skills-hub) |
| [Rocket Pool](https://rocketpool.net/) | 7 | [rocket-pool/skills](https://github.com/rocket-pool/skills) |
| [Ottie](https://github.com/jiayaoqijia/ottie) | 18 | Crypto DeFi, wallets, market data, mpp, tempo |
| [Lightning Labs](https://lightning.engineering/) | 3 | ClawHub: roasbeef (CTO) |
| [GMX](https://gmx.io/) | 2 | [gmx-io/gmx-ai](https://github.com/gmx-io/gmx-ai) |
| [OpenSea](https://opensea.io/) | 2 | ClawHub: dfinzer (CEO) |
| [SushiSwap](https://www.sushi.com/) | 2 | ClawHub: 0xmasayoshi (CTO) |
| [Venus Protocol](https://venus.io/) | 1 | [VenusProtocol/venus-agent-skills](https://github.com/VenusProtocol/venus-agent-skills) |
| [Circle](https://github.com/circlefin/skills) | 9 USDC/wallet skills | Official Circle stablecoin & wallet tools |
| [MetaMask](https://github.com/MetaMask/openclaw-skills) | 2 wallet skills | Official MetaMask smart accounts & gator CLI |
| [MoonPay](https://github.com/moonpay/skills) | 35 payment/trading skills | Official MoonPay crypto onramp, trading, & wallet tools |
| [MoonPay](https://www.moonpay.com/) | 35 | [moonpay/skills](https://github.com/moonpay/skills) |
| + MCP servers | 45 | Alchemy, Coinbase, Solana, EigenLayer, Blockscout, Alpaca, NEAR, Base, Monad, CoinGecko, and more |

## Submit a Skill

We welcome contributions from the community. Submit via:

1. **GitHub PR** -- Fork, add your skill, open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md)
2. **Quick Submit** -- Email maintainers@altresear.ch with the skill name, GitHub URL, category, and description
3. **Website** -- Use the submit form at [cryptoskill.org](https://cryptoskill.org)

All submissions are reviewed for security and quality before merging.

## Why Not General Registries?

| Challenge | General Registry | CryptoSkill |
|---|---|---|
| **Private key handling** | No awareness. Skills may leak keys. | Scans for hardcoded keys, mnemonics, credential patterns |
| **Exchange provenance** | Mixes official and unofficial wrappers | 221 verified from project teams. Official vs community clearly labeled. |
| **Chain-specific tooling** | No chain filtering | 41 chain-specific skills, filterable by network |
| **DeFi protocol risk** | No protocol-level security context | Dependency scanning, RCE detection, prompt injection checks |
| **MCP server trust** | 38% from unknown authors | Every server has SOURCE.md with provenance chain |
| **Update freshness** | Manual submission, often outdated | 6-hour bot cycle scanning 128+ projects |

## Auto-Update

CryptoSkill is not a static directory. A bot scans 128+ projects every 6 hours across four channels -- official GitHub repos (SHA-tracked), GitHub trending search, AI-powered discovery, and ClawHub community skills. Every new skill is security-scanned before inclusion. See [scripts/auto-update.py](scripts/auto-update.py) for details.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for development plans including a CLI installer, search API, community ratings, and bounty program.

## Legal

- [Terms of Service](https://cryptoskill.org/terms.html)
- [Privacy Policy](https://cryptoskill.org/privacy.html)

## License

This project is licensed under **AGPL-3.0** -- see [LICENSE](LICENSE) for details.

Individual skills retain their original licenses (mostly **MIT-0**). See [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES).

## The Crypto AI Agent Stack

CryptoSkill is one layer in a broader stack. Agents need skills to be useful, identity to be trusted, and payments to be monetized.

| Layer | Project | Role |
|---|---|---|
| **Agents** | [Ottie](https://github.com/jiayaoqijia/ottie), Claude Code, OpenClaw, Codex | Execute tasks using skills |
| **Skills** | **CryptoSkill** | Discover, install, and verify crypto-specific skills |
| **Identity** | [ERC-8004](https://github.com/jiayaoqijia/8004), 8004scan | On-chain agent identity and reputation |
| **Payments** | [x402](https://github.com/coinbase/x402), USDC | Agent-to-agent micropayments |

## Acknowledgments

We gratefully acknowledge the following projects and teams whose skills and tools are included in this registry:

### Skill Sources

| Source | Skills | Link |
|---|---|---|
| [ClawHub](https://clawhub.ai) | 200+ community skills | Skill registry for OpenClaw agents |
| [Ottie](https://github.com/jiayaoqijia/ottie) | 18 crypto/DeFi skills | Self-evolving crypto AI agent |
| [Binance Skills Hub](https://github.com/binance/binance-skills-550hub) | 20+ exchange skills | Official Binance AI skills |
| [OKX OnchainOS](https://github.com/okx/onchainos-skills) | 16+ exchange skills | Official OKX AI skills |
| [Kraken CLI](https://github.com/krakenfx/kraken-cli) | 50 trading skills | Official Kraken AI-native CLI |
| [KuCoin Skills Hub](https://github.com/Kucoin/kucoin-skills-550hub) | 7 exchange skills | Official KuCoin AI skills |
| [Uniswap AI](https://github.com/Uniswap/uniswap-ai) | 8 DeFi skills | Official Uniswap agent tools |
| [Rocket Pool Skills](https://github.com/rocket-pool/skills) | 7 staking skills | Official Rocket Pool agent skills |
| [GMX AI](https://github.com/gmx-io/gmx-ai) | 2 DeFi skills | Official GMX trading + liquidity |
| [Venus Agent Skills](https://github.com/VenusProtocol/venus-agent-skills) | 1 lending skill | Official Venus Protocol toolkit |
| [Circle](https://github.com/circlefin/skills) | 9 USDC/wallet skills | Official Circle stablecoin & wallet tools |
| [MetaMask](https://github.com/MetaMask/openclaw-skills) | 2 wallet skills | Official MetaMask smart accounts & gator CLI |
| [MoonPay](https://github.com/moonpay/skills) | 35 payment/trading skills | Official MoonPay crypto onramp, trading, & wallet tools |
| [MoonPay](https://www.moonpay.com/) | 35 | [moonpay/skills](https://github.com/moonpay/skills) |
| [Polyhub Skills](https://github.com/HubbleVision/polyhub-skills) | 3 trading skills | Copy-trading and portfolio tools |
| [Circle](https://github.com/circlefin/skills) | 9 USDC/wallet skills | Official Circle stablecoin & wallet tools |
| [MetaMask](https://github.com/MetaMask/openclaw-skills) | 2 wallet skills | Official MetaMask smart accounts & gator CLI |
| [MoonPay](https://github.com/moonpay/skills) | 35 payment/trading skills | Official MoonPay crypto onramp, trading, & wallet tools |
| [MoonPay](https://www.moonpay.com/) | 35 | [moonpay/skills](https://github.com/moonpay/skills) |
| [BitgetLimited/agent_hub](https://github.com/BitgetLimited/agent_hub) | 7 exchange skills | Official Bitget AI skills |
| [Awesome Ethereum AI Skills](https://github.com/rickkdev/awesome-ethereum-ai-skills) | 24 skills/MCPs | Curated Ethereum AI skill directory |
| [Trail of Bits](https://github.com/trailofbits/skills) | Security skills | Smart contract security testing |
| [OpenZeppelin](https://mcp.openzeppelin.com) | MCP server | Solidity security best practices |

### MCP Server Sources

| Source | Servers | Link |
|---|---|---|
| [Solana Foundation](https://github.com/solana-foundation/solana-mcp-official) | 3 MCP servers | Official Solana MCP |
| [Coinbase](https://github.com/coinbase/agentkit) | AgentKit + Base MCP | Official wallet + Base tools |
| [Alchemy](https://github.com/alchemyplatform/alchemy-mcp-server) | 1 MCP server | Multi-chain RPC + APIs |
| [EigenLayer](https://github.com/Layr-Labs/eigenlayer-mcp-server) | 1 MCP server | Restaking protocol docs |
| [Blockscout](https://github.com/blockscout/mcp-server) | 1 MCP server | Multi-chain block explorer |
| [CoinGecko](https://github.com/coingecko/coingecko-typescript) | 1 MCP server | Market data + token info |
| [BNB Chain](https://github.com/bnb-chain/bnbchain-mcp) | 1 MCP server | BSC + opBNB + Greenfield |
| [Monad](https://github.com/monad-developers/monad-mcp) | 1 MCP server | Monad blockchain tools |
| [NEAR](https://github.com/nearai/near-mcp) | 1 MCP server | NEAR protocol integration |
| [Aptos](https://github.com/aptos-labs/aptos-npm-mcp) | 1 MCP server | Aptos blockchain tools |
| [Alpaca](https://github.com/alpacahq/alpaca-mcp-server) | 1 MCP server | Stocks + crypto trading |
| [Awesome Blockchain MCPs](https://github.com/royyannick/awesome-blockchain-mcps) | Reference | Curated MCP directory |
| [Awesome Crypto MCP Servers](https://github.com/hive-intel/awesome-crypto-mcp-servers) | Reference | Community MCP collection |

### Frameworks & Standards

- [OpenClaw](https://github.com/nicholasgriffintn/openclaw) -- Agent framework powering the SKILL.md format
- [ERC-8004](https://github.com/jiayaoqijia/8004) -- On-chain agent identity standard
- [x402](https://github.com/coinbase/x402) -- HTTP 402 agent payment protocol

Every skill includes a `SOURCE.md` file crediting its original author and source repository.
