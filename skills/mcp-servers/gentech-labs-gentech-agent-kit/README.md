# GenTech Agent Kit

**One install. Full stack. Your agent, running.**

[![Release](https://img.shields.io/github/v/release/Gentech-Labs/genTech-agent-kit?style=flat&label=release)](https://github.com/Gentech-Labs/genTech-agent-kit/releases)
[![License](https://img.shields.io/github/license/Gentech-Labs/genTech-agent-kit?style=flat)](LICENSE)
[![Language](https://img.shields.io/github/languages/top/Gentech-Labs/genTech-agent-kit?style=flat)](https://github.com/Gentech-Labs/genTech-agent-kit/tree/main)
[![Skills](https://img.shields.io/badge/skills-npx%20install-blue?style=flat)](https://github.com/Gentech-Labs/genTech-agent-kit/tree/main/skills)
[![x402](https://img.shields.io/badge/payments-x402-8A2BE2?style=flat)](https://www.x402.org)
[![Q402](https://img.shields.io/badge/gasless-Q402-00D4AA?style=flat)](https://q402.quackai.ai)
[![Self-Evolution](https://img.shields.io/badge/evolve-harness-FF6B9D?style=flat)](https://github.com/erenciracioglu-dotcom/hermes-self-evolution)

The GenTech Agent Kit packages the entire GenTech stack into a single installable MCP server. One command gives any AI agent real-time market data, DeFi intelligence, payment rails, agent identity infrastructure, and self-evolution capabilities.

```bash
uvx --from git+https://github.com/Gentech-Labs/genTech-agent-kit.git gentech-kit
```

**Requires:** Hermes Agent v0.19.0+ | CMC_API_KEY env var (free at coinmarketcap.com/api)

---

## Quick Start

```bash
# Install and run
uvx --from git+https://github.com/Gentech-Labs/genTech-agent-kit.git gentech-kit

# Set your API key
export CMC_API_KEY="your-key-here"
```

The MCP server starts and exposes all GenTech tools to your agent.

---

## Install as Agent Skills

```bash
# Main skill
npx skills add Gentech-Labs/genTech-agent-kit

# Specific skills
npx skills add Gentech-Labs/genTech-agent-kit --skill x402-payments
npx skills add Gentech-Labs/genTech-agent-kit --skill robinhood-chain
npx skills add Gentech-Labs/genTech-agent-kit --skill output-enforcer
npx skills add Gentech-Labs/genTech-agent-kit --skill context-cycle-proactive
npx skills add Gentech-Labs/genTech-agent-kit --skill handoff-mesh
npx skills add Gentech-Labs/genTech-agent-kit --skill desktop-mesh
```

---

## What's Included

### Payment Rails

| Component | What It Does | Status |
|-----------|-------------|--------|
| **x402-payments** | Solana micropayments via x402 gateway — pay-per-call API access | Live |
| **Q402 Gasless** | Gasless USDC/USDT on 12 chains via EIP-7702 (trial on BNB) | Live |
| **Pay Wallet** | Solana wallet for x402 income collection | Live |

### Self-Evolution (Harness)

Four cron jobs that make your Hermes instance measurably better over time. Uses the [hermes-self-evolution](https://github.com/erenciracioglu-dotcom/hermes-self-evolution) framework.

| Role | Schedule | Job |
|------|----------|-----|
| Evolution | Every 4h | Proposes one grounded improvement from real user friction |
| Critic | Every 4h (offset) | Reviews proposals — different model prevents collusion |
| Verifier | Every 2 days | Checks if predictions actually came true |
| Gardener | Every 7 days | Prunes dormant skills, checks credential health |

Witness log auto-fed from context-weight nightly. No bookkeeping theatre (Article II).

### Agent Infrastructure

| Skill | What It Does |
|-------|-------------|
| **output-enforcer** | Structured output enforcement with circuit breaker |
| **robinhood-chain** | Robinhood Chain integration (USDG, tokenized stocks) |
| **wakeup-protocol** | Session wakeup — loads .env, reports configured services |
| **context-cycle-proactive** | Save → route → load → resume at 80-90% context; keeps every agent synced to the second brain |
| **safe-update-restart** | Safe update/restart for a production VPS: backup → controlled window → restart → verify every service & endpoint after |
| **fleet-update-container** | The container-correct update companion: why `hermes update` refuses in a Docker image, reading the real version from the image's install stamp (not the stale `__init__.py`), the s6 service model, the boot trap that false-flags lost ports, and the four-phase prep→watch→swap→settle-audit sequence |
| **handoff-mesh** | Built-in communication layer for multi-agent setups: full-mesh handoff folders, 15-min watcher (open handoffs + recent completions + tappable Obsidian deep-links), weekly archive cleanup, and a completion-reporting loop so every handoff is handled AND verified. Includes a second-brain setup preset to wire a new agent's brain in one go |
| **fed-council** | Fleet identity + synthesis layer: your agents deliberate as a governing council (Chair, Steward, Governors — names stay, personality layers on), the overnight maintenance force runs as the **Council Overnight Session**, and a nightly synthesis loop turns stored-but-forgotten notes into **Council Minutes** — clusters, completions, and retirements — so ideas finish other ideas instead of dying in the vault. Includes the Elder Statesman Chair voice spec (ElevenLabs, radio post-chain) and member onboarding steps |
| **desktop-mesh** | Connect an always-on server to a desktop/laptop Hermes over a private network (Tailscale) so agents on **different machines** become real peers — DM each other and **wake each other when a handoff lands**. Covers the loopback bind that silently blocks it (`127.0.0.1` works same-host, fails cross-machine), fail-soft push-on-handoff, the bidirectional wiring most setups get half-right, and the security rules that keep an agent API off the public internet |

### Modules

- **a2a — Agent-to-Agent Communication** — the full A2A lifecycle: [discover](a2a/discovery/README.md) new agents on the ERC-8004 registry → [talk](a2a/workspace/README.md) to them in the Buzz workspace → [self-audit](a2a/self-audit/README.md) your own execution. Includes on-chain [identity registration](a2a/identity/register.py) across 7+ chains
- **Poker Tournament Daemon** — Automated tournament loop with LAG strategy
- **Context Weight Generator** — Cross-group context sync nightly
- **genTech-shop MCP** — Gaming intelligence (deals, releases, POE2 builds)
- **Obliteratus** — ML refusal removal for local models (RTX 3070+)

---

## Platform Support

| Component | Hermes v0.19+ | Claude Code | Cursor | Codex |
|-----------|:---:|:---:|:---:|:---:|
| MCP Server | ✅ | ✅ | ✅ | ✅ |
| Agent Skills | ✅ | ✅ | ✅ | ✅ |
| Self-Evolution | ✅ | Cron only | Cron only | Cron only |
| x402 Payments | ✅ | ✅ | ✅ | ✅ |

---

## Discover the Gateway

The GenTech Labs x402 Gateway is listed on **PayAPI Market** (verified, free discovery — buyers still pay your wallet directly). Agents can find the route from the warehouse as well as from this repo:

- **Search:** https://payapi.market/mcp
- **Listing:** https://payapi.market/api/gentech-labs-x402-gateway

Paste into **Claude Desktop** or **Cursor**:

```json
{
  "mcpServers": {
    "payapi": {
      "url": "https://payapi.market/mcp"
    }
  }
}
```


---

## Environment Variables

```bash
# Required
CMC_API_KEY=your-key-here

# Payment Rails
PAY_SECRET_KEY_PATH=/path/to/solana-keypair.json
Q402_TRIAL_API_KEY=your-trial-key
Q402_MULTICHAIN_API_KEY=your-multichain-key

# Optional
ELEVENLABS_API_KEY=your-elevenlabs-key
GITHUB_TOKEN=your-github-token
```

---

## Key Addresses

| Asset | Address |
|-------|---------|
| Pay Wallet (Solana) | pX1FTLyXAskfD4y8pRwx7Go58GpM9t2PtGZGj6Lq2hR |
| TREASURY Token | 0x56D03C0f4167cC2c26B781dE47E608d660F13ba3 |

---

## License

MIT | Built by [GenTech Labs](https://gentechlabs.net)
