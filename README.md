<div align="center">

# CryptoSkill

**The App Store Moment for Crypto AI Agents**

Before the App Store, iPhone developers distributed apps through ad hoc channels. Before npm, JavaScript developers emailed zip files. Every platform ecosystem goes through the same phase transition: fragmented distribution, then a registry, then an explosion of building. Crypto AI agents are at the registry moment.

[![Skills](https://img.shields.io/badge/skills-1938-6366f1)]() [![MCP Servers](https://img.shields.io/badge/MCP%20servers-156-f59e0b)]() [![Official](https://img.shields.io/badge/official-1368-22c55e)]() [![Categories](https://img.shields.io/badge/categories-14-22d3ee)]() [![License](https://img.shields.io/badge/license-AGPL--3.0-green)]()

[Website](https://cryptoskill.org) · [Browse Skills](#skills-overview) · [MCP Servers](#mcp-servers) · [Quality Scores](#quality-scores) · [Contributing](CONTRIBUTING.md)

</div>

> [!CAUTION]
> **This project is under active development.** None of the skills or MCP servers listed here have been audited. This is a community-compiled directory of projects shared on social media, listed on skill hubs, and found across public repositories. We make no guarantees about their safety, integrity, or intentions. Exercise extreme caution with anything that touches wallets, private keys, seed phrases, or transaction signing -- a malicious skill can compromise your agent and drain your funds. Always review the source code, verify the authors, and do your own research (DYOR) before installing or granting permissions to any skill or MCP server.

---

## Why CryptoSkill Exists

A developer building a crypto AI agent today has to hunt through Binance's repo, Kraken's repo, Uniswap's repo, and 50 others just to assemble a working skill set. Different formats. No security review. No way to tell official from unofficial.

CryptoSkill is the crypto-native answer:

- **1938 skills** covering the full crypto stack -- exchanges, DeFi, wallets, analytics, trading, identity, payments
- **156 MCP servers** for direct protocol integration with Claude, Cursor, Codex, and other AI tools
- **1368 official skills** according to the recorded source classification (Kraken, Binance, OKX, Uniswap, Coinbase, MoonPay, Nethermind, and more)
- **Quality scored** -- every skill rated 0-100 across documentation, security, and depth
- **Security-scanned** -- credential detection (160+ patterns), code safety, permission analysis
- **Auto-updated** -- a scheduled workflow refreshes recorded sources every 6 hours, rescores skills, and reports failed or blocked updates

## Skills Overview

| Category | Skills |
|---|---:|
| DeFi | 310 |
| Trading | 250 |
| Exchanges | 247 |
| AI x Crypto | 220 |
| Chains | 168 |
| MCP Servers | 156 |
| Analytics | 145 |
| Dev Tools | 107 |
| Payments | 106 |
| Wallets | 100 |
| Prediction Markets | 75 |
| Identity | 37 |
| Social | 15 |
| Dex | 2 |

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
| **A** | 80-100 | 35 | Production-ready, well-documented, secure |
| **B** | 60-79 | 764 | Good quality, minor gaps |
| **C** | 40-59 | 1134 | Usable but significant gaps |
| **D** | 20-39 | 5 | Minimal quality, use with caution |

**Risk Gate**: 99% pass (1911/1938). Optional LLM evaluation scripts follow the [crypto-skill-benchmark](https://github.com/Minara-AI/crypto-skill-benchmark) methodology; they are separate from the scheduled heuristic scoring run. See [EVALUATION.md](docs/EVALUATION.md) for the full framework.

## MCP Servers

**156 MCP servers** for crypto -- the largest curated collection focused on the crypto ecosystem.

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

**1230 skills** classified as official in the source metadata:

| Project | Source |
|---|---|
| [Robinhood](https://robinhood.com/) | [Official Trading MCP documentation](https://robinhood.com/us/en/support/articles/agentic-trading-overview/) |
| [pump.fun](https://pump.fun/) | [pump-fun/pump-fun-skills](https://github.com/pump-fun/pump-fun-skills) |
| [Kraken](https://www.kraken.com/) | [krakenfx/kraken-cli](https://github.com/krakenfx/kraken-cli) |
| [MoonPay](https://www.moonpay.com/) | [moonpay/skills](https://github.com/moonpay/skills) |
| [Binance](https://www.binance.com/) | [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub) |
| [Bankr](https://bankr.bot/) | [BankrBot/skills](https://github.com/BankrBot/skills) |
| [Ottie](https://github.com/jiayaoqijia/ottie) | Crypto DeFi, wallets, market data |
| [OKX](https://www.okx.com/) | [okx/onchainos-skills](https://github.com/okx/onchainos-skills) |
| [Gate.io](https://www.gate.io/) | ClawHub: gate-exchange |
| [DefiLlama](https://defillama.com/) | [DefiLlama/defillama-skills](https://github.com/DefiLlama/defillama-skills) |
| [Nansen](https://www.nansen.ai/) | ClawHub: nansen-devops |
| [Base](https://base.org/) | [base/skills](https://github.com/base/skills) |
| [Circle (USDC)](https://www.circle.com/) | [circlefin/skills](https://github.com/circlefin/skills) |
| [Coinbase Wallet](https://www.coinbase.com/) | [coinbase/agentic-wallet-skills](https://github.com/coinbase/agentic-wallet-skills) |
| [Uniswap](https://uniswap.org/) | [Uniswap/uniswap-ai](https://github.com/Uniswap/uniswap-ai) |
| [Bitget](https://www.bitget.com/) | [BitgetLimited/agent_hub](https://github.com/BitgetLimited/agent_hub) |
| [KuCoin](https://www.kucoin.com/) | [Kucoin/kucoin-skills-hub](https://github.com/Kucoin/kucoin-skills-hub) |
| [Rocket Pool](https://rocketpool.net/) | [rocket-pool/skills](https://github.com/rocket-pool/skills) |
| [CoinMarketCap](https://coinmarketcap.com/) | ClawHub: bryan-cmc |
| [KyberSwap](https://kyberswap.com/) | [KyberNetwork/kyberswap-skills](https://github.com/KyberNetwork/kyberswap-skills) |
| [Pendle](https://www.pendle.finance/) | [pendle-finance/pendle-ai](https://github.com/pendle-finance/pendle-ai) |
| [MetaMask](https://metamask.io/) | [MetaMask/openclaw-skills](https://github.com/MetaMask/openclaw-skills) |
| [GMX](https://gmx.io/) | [gmx-io/gmx-ai](https://github.com/gmx-io/gmx-ai) |
| [Nethermind](https://nethermind.io/) | [NethermindEth/defi-skills](https://github.com/NethermindEth/defi-skills) |
| [GMGN](https://gmgn.ai/) | [GMGNAI/gmgn-skills](https://github.com/GMGNAI/gmgn-skills) |
| [Chainlink](https://chain.link/) | [smartcontractkit/chainlink-agent-skills](https://github.com/smartcontractkit/chainlink-agent-skills) |
| [Helius](https://helius.dev/) | [helius-labs/core-ai](https://github.com/helius-labs/core-ai) |
| [QuickNode](https://www.quicknode.com/) | [quiknode-labs/blockchain-skills](https://github.com/quiknode-labs/blockchain-skills) |
| [Worldcoin](https://worldcoin.org/) | [worldcoin/agentkit](https://github.com/worldcoin/agentkit) |
| [Aptos](https://aptoslabs.com/) | [aptos-labs/aptos-agent-skills](https://github.com/aptos-labs/aptos-agent-skills) |
| [SendAI](https://sendai.fun/) | [sendaifun/skills](https://github.com/sendaifun/skills) |
| [Crypto.com](https://crypto.com/) | [crypto-com/crypto-agent-trading](https://github.com/crypto-com/crypto-agent-trading) |
| [Blockscout](https://www.blockscout.com/) | [blockscout/agent-skills](https://github.com/blockscout/agent-skills) |
| [Celo](https://celo.org/) | [celo-org/agent-skills](https://github.com/celo-org/agent-skills) |
| [CoinPaprika](https://coinpaprika.com/) | [coinpaprika/claude-marketplace](https://github.com/coinpaprika/claude-marketplace) |
| [Trail of Bits](https://trailofbits.com/) | [trailofbits/slither-mcp](https://github.com/trailofbits/slither-mcp) |
| [Polymarket](https://polymarket.com/) | [Polymarket/agent-skills](https://github.com/Polymarket/agent-skills) |
| [Dune Analytics](https://dune.com/) | [duneanalytics/skills](https://github.com/duneanalytics/skills) |
| [Bybit](https://www.bybit.com/) | [bybit-exchange/skills](https://github.com/bybit-exchange/skills) |

Plus: Alchemy, Virtual Protocol, Privy, OpenSea, Minara, Heurist, Towns, Elsa, Venus, Lightning Labs, SushiSwap, Tenderly, Reown, Bitget Wallet, ChainGPT, SpoonOS, AIBTC, AElf ecosystem (TomorrowDAO, AelfScan, Portkey, Awaken), ICP/dfinity, Hedera, Injective, Flow, XMTP, OpenOcean, and [156 MCP servers](#mcp-servers).

## Submit a Skill

The easiest way: **[Open a GitHub Issue](https://github.com/jiayaoqijia/cryptoskill/issues/new?template=skill_submission.md&title=%5BSubmit%5D+)**

Or email maintainers+cryptoskills@altresear.ch with the skill name, GitHub URL, and category.

## Auto-Update Bot

A GitHub Actions workflow runs every six hours:

1. Refreshes recorded GitHub and ClawHub sources, including bundled libraries and references
2. Finds real skills in configured repositories and searches GitHub for new candidates
3. Checks changed bundles with the registry's security gate and preserves local edits
4. Records upstream revisions, file hashes, and per-source failures
5. Rebuilds the catalog, scores, trust manifests, pages, and statistics
6. Runs regression and browser tests before committing skills and generated artifacts together

Run `bash scripts/run-bot.sh` for a local refresh, or add `--dry-run` to preview.
See [Maintenance](docs/MAINTENANCE.md) for setup and update modes and
[the latest source report](docs/sync-report.json) for coverage and unresolved sources.

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
