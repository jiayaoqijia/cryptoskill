---
name: emblem-memecoin-scout
description: >
  Memecoin discovery and risk assessment via EmblemAI. Trending memecoins on Solana, Base,
  and Hedera. Pump.fun and LaunchLab new token alerts, Clanker discovery, rug-pull detection,
  holder analysis, and smart money tracking. Use when the user wants to find new memecoins,
  check if a token is a rug pull, or scout trending low-cap tokens.
license: MIT
compatibility: >
  Requires Node.js >= 18.0.0, @emblemvault/agentwallet CLI, and internet access.
  Works on Claude Code, Cursor, Codex, OpenClaw, and other agents following the Agent Skills spec.
metadata:
  author: EmblemAI
  version: "1.1.0"
  homepage: https://emblemvault.ai
  docs: https://emblemvault.ai/docs
  docs-interactive: https://emblemvault.dev
---

# Emblem Memecoin Scout

Memecoin discovery and risk assessment powered by **EmblemAI**. Real-time new token alerts, trending memecoins, rug-pull detection, holder analysis, and smart money tracking across Solana, Base, and Hedera.

**Requires**: `npm install -g @emblemvault/agentwallet`

---

## What This Skill Can Do

| Capability | Tools Used | Chains |
|-----------|------------|--------|
| Pump.fun new token launches | `getPumpFunTokens` | Solana |
| LaunchLab / Bonk.fun new tokens | `discoverLaunchLabTokens` | Solana |
| Trending memecoins | `findSolanaGems`, `birdeyeTrendingTokens` | Solana, multi-chain |
| Clanker token discovery | `baseFindClankerTokens` | Base |
| Hedera memecoin discovery | `hederaFindMemeCoins` | Hedera |
| Rug-pull detection | `rugcheck` | Solana |
| Token deep dive (volume, trades) | `birdeyeTradeData` | Multi-chain |
| Smart money memecoin tracking | `nansen_smart_money_trades` | Multi-chain |
| CoinGecko trending | `getTrendingCoins` | All |
| Token search | `searchCryptoByName`, `findSolanaSwapToken` | All |

### Not Supported

These features have no backing tools:

- Social sentiment (Twitter, Telegram, Discord monitoring) — no social API tools exist
- Exit strategy generation — LLM-generated advice only, not data-driven
- Price charts / technical levels — no charting tools exist
- BSC/FourMeme discovery — `bscfindMemeCoinsViaFourMeme` returns 404 (API broken)

---

## Quick Start

```bash
npm install -g @emblemvault/agentwallet

# What's hot on Pump.fun (uses getPumpFunTokens)
emblemai --agent --profile default -m "Use getPumpFunTokens to show tokens about to graduate on Pump.fun with holder data"

# Risk check a token (uses rugcheck)
emblemai --agent --profile default -m "Use rugcheck to analyze token [TOKEN_ADDRESS] on Solana"
```

**Trigger phrases:**
- "What memecoins are trending?"
- "Find new tokens on Pump.fun"
- "Is this token a rug pull?"
- "Scout memecoins on Solana"
- "What new tokens launched today?"

---

## Supported Platforms

| Platform | Tool | Chain | Data |
|----------|------|-------|------|
| **Pump.fun** | `getPumpFunTokens` | Solana | New launches, graduating tokens, holder data, dev hold %, sniper/bundle detection |
| **LaunchLab** | `discoverLaunchLabTokens` | Solana | New token launches with curve data |
| **Clanker** | `baseFindClankerTokens` | Base | New tokens with market cap, creator info |
| **MemeJob** | `hederaFindMemeCoins` | Hedera | Memecoins with market cap, socials, DEX links |
| **Birdeye** | `birdeyeTradeData`, `birdeyeTrendingTokens` | Multi-chain | Volume, price action, trade data |
| **Rugcheck** | `rugcheck` | Solana | Risk score, holder concentration, insider networks, freeze/mint authority |

---

## Workflow: Scout and Evaluate

### Step 1: Discovery
Find what's gaining traction.
```bash
emblemai --agent --profile default -m "Use findSolanaGems with sortBy trending to show trending Solana tokens with market cap, volume, holder count, and organic score"
```

### Step 2: Risk Check
Evaluate safety before any position.
```bash
emblemai --agent --profile default -m "Use rugcheck to analyze [TOKEN_ADDRESS] — show risk score, top holders, insider networks, freeze authority, and LP status"
```

### Step 3: Volume Deep Dive
Check real trade data for the token.
```bash
emblemai --agent --profile default -m "Use birdeyeTradeData to show [TOKEN_ADDRESS] on Solana — price changes across timeframes, unique wallets, buy/sell volumes"
```

### Step 4: Smart Money Check
See if whales are involved.
```bash
emblemai --agent --profile default -m "Use nansen_smart_money_trades to check if smart money has traded [TOKEN_NAME] on solana recently"
```

---

## Scouting Patterns

### New Launches (Solana)
```bash
emblemai --agent --profile default -m "Use getPumpFunTokens with type about_to_graduate to show tokens about to graduate with volume and holder data"
emblemai --agent --profile default -m "Use discoverLaunchLabTokens to show newest LaunchLab token launches"
```

### New Launches (Base)
```bash
emblemai --agent --profile default -m "Use baseFindClankerTokens to show new Clanker tokens on Base with market cap and creator info"
```

### New Launches (Hedera)
```bash
emblemai --agent --profile default -m "Use hederaFindMemeCoins to show trending memecoins on Hedera with market cap and socials"
```

### Trending Gems
```bash
emblemai --agent --profile default -m "Use findSolanaGems to show trending tokens sorted by organic score"
emblemai --agent --profile default -m "Use birdeyeTrendingTokens on solana to show top tokens by volume"
```

### Whale Watch
```bash
emblemai --agent --profile default -m "Use nansen_smart_money_trades to show what smart money is trading on solana right now"
emblemai --agent --profile default -m "Use getCoinglassHyperliquidWhaleAlert to show large memecoin positions"
```

### Red Flag Detection
```bash
emblemai --agent --profile default -m "Use rugcheck to analyze [TOKEN_ADDRESS] — check for honeypot indicators, mint authority, concentrated holders, and locked LP"
```

---

## Risk Assessment

The `rugcheck` tool returns a `score_normalised` (0-100) plus detailed risk data:

| Score | Risk Level | What It Means |
|-------|-----------|---------------|
| 80-100 | Low | Dispersed holders, no freeze/mint authority, locked LP |
| 50-79 | Medium | Some concentration or unlocked LP — proceed with caution |
| 20-49 | High | Major red flags (concentrated holders, active mint authority) |
| 0-19 | Critical | Honeypot/rug indicators detected — do not interact |

Additional rugcheck data: top holder percentages, insider network analysis, creator token history, LP liquidity depth, freeze authority status.

---

## Communication Tips

Name the exact tool for reliable execution:

| Bad | Good |
|-----|------|
| `"memes"` | `"Use findSolanaGems with sortBy trending to show Solana memecoins"` |
| `"safe?"` | `"Use rugcheck to analyze [TOKEN_ADDRESS] on Solana"` |
| `"new coins"` | `"Use getPumpFunTokens with type about_to_graduate to show newest launches"` |

---

## Safety Notice

Memecoins are extremely high risk. This skill provides data and analysis to inform decisions — it does not guarantee safety. Always:
- Never invest more than you can afford to lose
- Verify contract addresses independently
- Check multiple data sources before acting
- Use stop-losses on any position

---

## Helper Script

```bash
bash scripts/memecoin-scan.sh [chain]
```

See [scripts/memecoin-scan.sh](scripts/memecoin-scan.sh) for trending memecoin scanning.

---

## Links

- [Agent Wallet CLI](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [EmblemVault Docs — canonical](https://emblemvault.ai/docs)
- [EmblemVault Docs — interactive](https://emblemvault.dev)
