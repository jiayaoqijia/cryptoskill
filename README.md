<div align="center">

# CryptoSkill

**The App Store Moment for Crypto AI Agents**

Before the App Store, iPhone developers distributed apps through ad hoc channels. Before npm, JavaScript developers emailed zip files. Every platform ecosystem goes through the same phase transition: fragmented distribution, then a registry, then an explosion of building. Crypto AI agents are at the registry moment.

[![Skills](https://img.shields.io/badge/skills-1297-6366f1)]() [![MCP Servers](https://img.shields.io/badge/MCP%20servers-109-f59e0b)]() [![Official](https://img.shields.io/badge/official-785-22c55e)]() [![Categories](https://img.shields.io/badge/categories-13-22d3ee)]() [![License](https://img.shields.io/badge/license-AGPL--3.0-green)]()

[Website](https://cryptoskill.org) · [Browse Skills](#skills-1297overview) · [MCP Servers](#mcp-servers) · [Quality Scores](#quality-scores) · [Contributing](CONTRIBUTING.md)

</div>

> [!CAUTION]
> **This project is under active development.** None of the skills or MCP servers listed here have been audited. This is a community-compiled directory of projects shared on social media, listed on skill hubs, and found across public repositories. We make no guarantees about their safety, integrity, or intentions. Exercise extreme caution with anything that touches wallets, private keys, seed phrases, or transaction signing -- a malicious skill can compromise your agent and drain your funds. Always review the source code, verify the authors, and do your own research (DYOR) before installing or granting permissions to any skill or MCP server.

---

## Why CryptoSkill Exists

A developer building a crypto AI agent today has to hunt through Binance's repo, Kraken's repo, Uniswap's repo, and 50 others just to assemble a working skill set. Different formats. No security review. No way to tell official from unofficial.

CryptoSkill is the crypto-native answer:

- **977 skills** covering the full crypto stack -- exchanges, DeFi, wallets, analytics, trading, identity, payments
- **85 MCP servers** for direct protocol integration with Claude, Cursor, Codex, and other AI tools
- **617 official skills** from verified project teams (Kraken, Binance, OKX, Uniswap, Coinbase, MoonPay, Nethermind, and more)
- **Quality scored** -- every skill rated 0-100 across documentation, security, and depth
- **Security-scanned** -- credential detection (160+ patterns), code safety, permission analysis
- **Auto-updated** -- bot scans 128+ projects every 6 hours, rescores all skills, tracks regressions

## Skills Overview

| Category | Skills | Highlights |
|---|---|---|
| **DeFi** | 192 | Uniswap (8), Nethermind, GMX, Rocket Pool (7), Venus, Pendle (4), KyberSwap (5), Lido, Aave, OpenSea, Elsa |
| **Exchanges** | 180 | Binance, OKX, Kraken (50), KuCoin, Gate.io, Bitget, Hyperliquid, Bybit, Coinbase |
| **Analytics** | 98 | DefiLlama (11), Nansen (10), CoinMarketCap (7), CoinGecko, CoinPaprika, Dune, Etherscan, Elfa |
| **Trading** | 87 | Bankr (20), Minara, Polyhub, grid trading, whale tracking, signals |
| **MCP Servers** | 85 | Alchemy, Solana, CoinGecko, Tenderly, CoinPaprika, EigenLayer, Blockscout, NEAR, Monad, Chainflip |
| **Payments** | 75 | MoonPay (35), Circle (9), x402, mpp, tempo |
| **Chains** | 57 | Base (9), Ethereum, Solana, Bitcoin, Lightning, BNB Chain, Arbitrum, Sui, Monad |
| **AI x Crypto** | 52 | Virtual Protocol, Heurist, Bittensor, Virtuals, ElizaOS |
| **Prediction Markets** | 46 | Polymarket API, Builder, Research, trading bots, whale copying |
| **Wallets** | 38 | Coinbase Wallet (9), MetaMask (2), Privy, Bitget Wallet, Cobo TSS |
| **Dev Tools** | 33 | Alchemy, Tenderly, Moralis, Foundry, Hardhat, Trail of Bits, Cyfrin, ETH2 Quickstart |
| **Identity** | 24 | ERC-8004, 8004scan, self-agent-id, Maiat Guard, Maiat Trust |
| **Social** | 10 | Towns, Farcaster, Nostr, XMTP |

## Quality Scores

Every skill is scored 0-100 across three layers, updated every 6 hours. Scores are visible on skill cards at [cryptoskill.org](https://cryptoskill.org).

```
Quality Score (0-100) = Static (40) + Security (20) + Depth (40)
```

| Layer | Points | What it measures |
|-------|--------|-----------------|
| **Static** | 0-40 | Documentation quality, completeness, freshness, provenance, structure |
| **Security** | 0-20 | Credential safety, code safety, permission scope, supply chain |
| **Depth** | 0-40 | Actionability, specificity, examples, error handling (+ LLM eval for trading skills) |

| Grade | Score | Skills | Meaning |
|-------|-------|--------|---------|
| **A** | 80-100 | 16 | Production-ready, well-documented, secure |
| **B** | 60-79 | 361 | Good quality, minor gaps |
| **C** | 40-59 | 594 | Usable but significant gaps |
| **D** | 20-39 | 6 | Minimal quality, use with caution |

**Risk Gate**: 93% pass (918/977). Fund-moving skills also get LLM-as-judge evaluation based on the [crypto-skill-benchmark](https://github.com/Minara-AI/crypto-skill-benchmark) methodology. See [EVALUATION.md](docs/EVALUATION.md) for the full framework.

## MCP Servers

**85 MCP servers** for crypto -- the largest curated collection focused on the crypto ecosystem.

### Official MCP Servers

| MCP Server | Project | Install |
|---|---|---|
| [Alchemy](skills/mcp-servers/alchemy-mcp/) | Alchemy | `claude mcp add alchemy` |
| [Blockscout](skills/mcp-servers/blockscout-mcp/) | Blockscout | `claude mcp add blockscout https://mcp.blockscout.com/mcp` |
| [BNB Chain](skills/mcp-servers/bnbchain-mcp/) | BNB Chain | `git clone bnb-chain/bnbchain-mcp` |
| [Coinbase AgentKit](skills/mcp-servers/coinbase-agentkit/) | Coinbase | `npm create onchain-agent@latest` |
| [CoinGecko](skills/mcp-servers/coingecko-mcp-official/) | CoinGecko | `npx @coingecko/coingecko-mcp` |
| [EigenLayer](skills/mcp-servers/eigenlayer-mcp/) | Layr-Labs | `claude mcp add --transport sse eigenlayer ...` |
| [Kraken CLI](skills/mcp-servers/kraken-cli-mcp/) | Kraken | `git clone krakenfx/kraken-cli` |
| [Monad](skills/mcp-servers/monad-mcp/) | Monad | `git clone monad-developers/monad-mcp` |
| [NEAR](skills/mcp-servers/near-mcp/) | NEAR | `git clone nearai/near-mcp` |
| [Solana](skills/mcp-servers/solana-mcp-official/) | Solana Foundation | `git clone solana-foundation/solana-mcp-official` |
| [Tenderly](skills/mcp-servers/tenderly-mcp/) | Tenderly | `claude mcp add tenderly --transport http https://mcp.tenderly.co/mcp` |
| [CoinPaprika](skills/mcp-servers/coinpaprika-mcp/) | CoinPaprika | `npx @coinpaprika/mcp` |

### Community MCP Servers

CCXT (100+ exchanges), GOAT Onchain (200+ actions), Helius, Jupiter, Lightning, Chainlink Feeds, deBridge, DEXScreener, Dune Analytics, StarkNet, Tatum (130+ networks), Whale Tracker, Chainflip, and [50+ more](skills/mcp-servers/).

## Quick Start

```bash
# Clone the registry
git clone https://github.com/jiayaoqijia/cryptoskill.git /tmp/cs

# Install a skill (Claude Code)
cp -r /tmp/cs/skills/exchanges/binance-spot-api .claude/skills/

# Install an MCP server
claude mcp add blockscout https://mcp.blockscout.com/mcp

# Or via ClawHub CLI
npm i -g clawhub && clawhub install binance-spot-api
```

## Official Skills

**617 skills** from verified project teams:

| Project | Skills | Source |
|---|---|---|
| [Kraken](https://www.kraken.com/) | 50 | [krakenfx/kraken-cli](https://github.com/krakenfx/kraken-cli) |
| [MoonPay](https://www.moonpay.com/) | 35 | [moonpay/skills](https://github.com/moonpay/skills) |
| [Binance](https://www.binance.com/) | 20+ | [binance/binance-skills-1297hub](https://github.com/binance/binance-skills-hub) |
| [Bankr](https://bankr.bot/) | 20 | [BankrBot/skills](https://github.com/BankrBot/skills) |
| [Ottie](https://github.com/jiayaoqijia/ottie) | 18 | Crypto DeFi, wallets, market data |
| [OKX](https://www.okx.com/) | 16+ | [okx/onchainos-skills](https://github.com/okx/onchainos-skills) |
| [Gate.io](https://www.gate.io/) | 13 | ClawHub: gate-exchange |
| [DefiLlama](https://defillama.com/) | 11 | [DefiLlama/defillama-skills](https://github.com/DefiLlama/defillama-skills) |
| [Nansen](https://www.nansen.ai/) | 10 | ClawHub: nansen-devops |
| [Base](https://base.org/) | 9 | [base/skills](https://github.com/base/skills) |
| [Circle (USDC)](https://www.circle.com/) | 9 | [circlefin/skills](https://github.com/circlefin/skills) |
| [Coinbase Wallet](https://www.coinbase.com/) | 9 | [coinbase/agentic-wallet-skills](https://github.com/coinbase/agentic-wallet-skills) |
| [Uniswap](https://uniswap.org/) | 8 | [Uniswap/uniswap-ai](https://github.com/Uniswap/uniswap-ai) |
| [Bitget](https://www.bitget.com/) | 7 | [BitgetLimited/agent_hub](https://github.com/BitgetLimited/agent_hub) |
| [KuCoin](https://www.kucoin.com/) | 7 | [Kucoin/kucoin-skills-1297hub](https://github.com/Kucoin/kucoin-skills-hub) |
| [Rocket Pool](https://rocketpool.net/) | 7 | [rocket-pool/skills](https://github.com/rocket-pool/skills) |
| [CoinMarketCap](https://coinmarketcap.com/) | 7 | ClawHub: bryan-cmc |
| [KyberSwap](https://kyberswap.com/) | 5 | [KyberNetwork/kyberswap-skills](https://github.com/KyberNetwork/kyberswap-skills) |
| [Pendle](https://www.pendle.finance/) | 4 | [pendle-finance/pendle-ai](https://github.com/pendle-finance/pendle-ai) |
| [MetaMask](https://metamask.io/) | 2 | [MetaMask/openclaw-skills](https://github.com/MetaMask/openclaw-skills) |
| [GMX](https://gmx.io/) | 2 | [gmx-io/gmx-ai](https://github.com/gmx-io/gmx-ai) |
| [Nethermind](https://nethermind.io/) | 1 | [NethermindEth/defi-skills](https://github.com/NethermindEth/defi-skills) |

Plus: Alchemy, Virtual Protocol, Privy, OpenSea, Minara, Heurist, Towns, Elsa, Venus, Lightning Labs, SushiSwap, Tenderly, CoinPaprika, and [85 MCP servers](#mcp-servers).

## Submit a Skill

The easiest way: **[Open a GitHub Issue](https://github.com/jiayaoqijia/cryptoskill/issues/new?template=skill_submission.md&title=%5BSubmit%5D+)**

Or email maintainers+cryptoskills@altresear.ch with the skill name, GitHub URL, and category.

## Auto-Update Bot

A bot scans 128+ projects every 6 hours:
1. Checks official repos for new skills (SHA-tracked)
2. Searches GitHub API for trending crypto repos
3. AI-powered discovery via AltLLM
4. Security scans all new skills
5. Scores every skill (static + security + depth)
6. Tracks score regressions over time
7. Updates website and commits

## Legal

- [Terms of Service](https://cryptoskill.org/terms.html) · [Privacy Policy](https://cryptoskill.org/privacy.html)

## License

**AGPL-3.0** -- see [LICENSE](LICENSE). Individual skills retain their original licenses (mostly MIT-0).

## The Crypto AI Agent Stack

| Layer | Project | Role |
|---|---|---|
| **Agents** | [Ottie](https://github.com/jiayaoqijia/ottie), Claude Code, OpenClaw, Codex | Execute tasks using skills |
| **Skills** | **CryptoSkill** | Discover, install, and verify crypto-specific skills |
| **Identity** | [ERC-8004](https://github.com/jiayaoqijia/8004), 8004scan | On-chain agent identity and reputation |
| **Payments** | [x402](https://github.com/coinbase/x402), USDC | Agent-to-agent micropayments |

## Acknowledgments

### Skill Sources

| Source | Skills | Description |
|---|---|---|
| [ClawHub](https://clawhub.ai) | 200+ | Community skill registry for OpenClaw agents |
| [Awesome Ethereum AI Skills](https://github.com/rickkdev/awesome-ethereum-ai-skills) | 24 | Curated Ethereum AI skill directory |
| [Trail of Bits](https://github.com/trailofbits/skills) | Security | Smart contract security testing |
| [OpenZeppelin](https://mcp.openzeppelin.com) | MCP | Solidity security best practices |
| [Nethermind](https://github.com/NethermindEth/defi-skills) | DeFi | DeFi transaction builder (13 protocols, 53 actions) |
| [Tenderly](https://docs.tenderly.co/mcp-server) | MCP | Smart contract simulation and debugging |
| [CoinPaprika](https://github.com/coinpaprika/coinpaprika-mcp) | MCP | Crypto market data (12K+ coins, 350+ exchanges) |

### Frameworks & Standards

- [OpenClaw](https://github.com/nicholasgriffintn/openclaw) -- Agent framework powering the SKILL.md format
- [ERC-8004](https://github.com/jiayaoqijia/8004) -- On-chain agent identity standard
- [x402](https://github.com/coinbase/x402) -- HTTP 402 agent payment protocol
- [crypto-skill-benchmark](https://github.com/Minara-AI/crypto-skill-benchmark) -- Skill evaluation framework

Every skill includes a `SOURCE.md` file crediting its original author and source repository.
