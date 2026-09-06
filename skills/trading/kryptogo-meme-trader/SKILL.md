---
name: kryptogo-meme-trader
version: "2.6.0"
description: "[DEPRECATED 2026-05-04] Analyze and trade meme coins using KryptoGO's on-chain cluster analysis platform. NOTE: The kg-xyz analysis backend (wallet-data.kryptogo.app) is shutting down on 2026-05-04 — cluster analysis, wallet labels, signal dashboard, and DCA/limit order tools will stop working after that date. Swap execution via the OKX DEX aggregator continues to function."
author: KryptoGO
license: MIT
homepage: https://www.kryptogo.xyz
docs:
  user_guide:
    en: https://kryptogo.notion.site/Product-Guide-EN-26c3499de8a28179aafacb68304458ea
    zh-tw: https://kryptogo.notion.site/kryptogo-xyz-usage-guide
    zh-cn: https://kryptogo.notion.site/kryptogo-xyz-productguide-zhcn
  whitepaper: https://wallet-static.kryptogo.com/public/whitepaper/kryptogo-xyz-whitepaper-v1.0.pdf
tags:
  - solana
  - trading
  - meme-coins
  - defi
  - agent-trading
  - on-chain-analysis
  - cluster-analysis
  - kryptogo
platform: solana
api_base: https://wallet-data.kryptogo.app
metadata:
  openclaw:
    requires:
      env:
        - KRYPTOGO_API_KEY
        - SOLANA_PRIVATE_KEY
        - SOLANA_WALLET_ADDRESS
      bins:
        - python3
        - pip
        - openclaw
      network:
        - wallet-data.kryptogo.app
      permissions:
        - filesystem:write:~/.openclaw/workspace/.env
        - filesystem:write:~/.openclaw/workspace/memory/
      runtime_installs:
        - "pip: solders, requests (installed by scripts/setup.py on first run)"
      primaryEnv: KRYPTOGO_API_KEY
    security:
      default_mode: supervised
      trade_confirmation: required_by_default
      autonomous_trading: opt_in
      credential_access: environment_variables_only
      credential_file_read: setup_script_only
      credential_file_read_note: "Only scripts/setup.py reads and writes ~/.openclaw/workspace/.env for initial keypair generation and address repair. All other scripts access credentials exclusively via pre-loaded environment variables."
      local_signing_only: true
---

# KryptoGO Meme Trader Agent Skill

> ## SHUTDOWN NOTICE — kg-xyz Analysis Backend
>
> **The KryptoGO XYZ analysis backend (`wallet-data.kryptogo.app`) will be discontinued on 2026-05-04.**
>
> After this date, all tools that depend on cluster analysis, wallet labels, signal dashboards, and DCA/limit order reconstruction will no longer function. The swap execution path (OKX DEX aggregator + local transaction signing) is independent of the kg-xyz backend and will continue to work.
>
> Per-tool impact is annotated inline below. Scripts and MCP tool implementations have been kept in place so they fail gracefully (backend will return HTTP errors) and so a revert remains simple if plans change.

## Overview

This skill enables an AI agent to **analyze and trade** meme coins through the KryptoGO platform, combining deep on-chain cluster analysis with trade execution.

> **Degraded functionality starting 2026-05-04:** cluster analysis, wallet/token labels, signal dashboard, DCA/limit order reconstruction, and portfolio P&L enrichment will stop working when the kg-xyz backend shuts down. Swap execution continues.

**Analysis** (multi-chain: Solana, BSC, Base, Monad): wallet clustering, accumulation/distribution detection, address behavior labels, network-wide accumulation signals (Pro/Alpha tier).

**Trading** (Solana only): portfolio monitoring with PnL tracking, swap execution via DEX aggregator, local transaction signing (private key never leaves the machine).

**Default mode is supervised** — all trades require user confirmation. Autonomous trading is available as opt-in. See `references/autonomous-trading.md` for autonomous mode, cron setup, and learning system details.

---

## When to Use

- User asks to analyze a meme coin or token on Solana/BSC/Base/Monad
- User asks to trade, buy, or sell tokens
- User asks to scan for trending tokens or market opportunities
- User asks to monitor portfolio positions or check PnL
- Cron-triggered periodic portfolio monitoring and signal scanning

## When NOT to Use

- BTC/ETH/major L1 macro analysis, NFTs, cross-chain bridging, non-DEX transactions, non-Solana trading

---

## Setup Flow

### 1. Get API Key

1. Go to [kryptogo.xyz/account](https://www.kryptogo.xyz/account) and create an API key
2. Add to `~/.openclaw/workspace/.env`:

   ```bash
   echo 'KRYPTOGO_API_KEY=sk_live_YOUR_KEY' >> ~/.openclaw/workspace/.env && chmod 600 ~/.openclaw/workspace/.env
   ```

> **Do NOT paste your API key directly in chat.** Always set secrets via `.env` file.

### 2. Generate Agent Wallet

```bash
python3 scripts/setup.py
```

Creates a Solana keypair, saves to `.env` with chmod 600, prints public address to fund.

### 3. Fund the Wallet

Send SOL to the agent's public address (minimum 0.1 SOL).

### Security Rules

- **NEVER** print, log, or include private keys in any message or CLI argument
- **NEVER** accept secrets pasted directly in chat — instruct users to set them in `.env`
- **NEVER** use the Read tool on `.env` — load credentials via `source` command only
- Runtime scripts do NOT read `.env` directly — all credentials are accessed via environment variables only, which must be pre-loaded by the caller (`source ~/.openclaw/workspace/.env`)
- **Exception:** `scripts/setup.py` reads and writes `.env` for initial keypair generation and address repair — this is the only script that touches credential files
- Private key stays in memory only during local signing — never sent to any server

---

## Authentication

All endpoints require: `Authorization: Bearer sk_live_<48 hex chars>`

| Tier  | Daily API Calls | Trading Fee | Signal Dashboard | KOL Finder |
|-------|-----------------|-------------|------------------|------------|
| Free  | 100 calls/day   | 1%          | No               | No         |
| Pro   | 1,000 calls/day | 0.5%        | Yes              | Yes        |
| Alpha | 5,000 calls/day | 0%          | Yes              | Yes        |

---

## Agent Behavior

### Session Initialization

On every session start (including heartbeat/cron), the agent MUST load credentials BEFORE running any scripts:

```bash
source ~/.openclaw/workspace/.env
```

This is REQUIRED — scripts do not read `.env` directly. All credentials are accessed via environment variables only.

### Default Mode: Supervised

By default, the agent operates in **supervised mode**: it analyzes tokens, presents recommendations, and waits for user approval before executing any trade. Stop-loss/take-profit conditions are reported to the user but not auto-executed.

To enable autonomous trading, set `require_trade_confirmation: false` in preferences. See `references/autonomous-trading.md` for full details.

### Persistence (CRITICAL)

**IMMEDIATELY after submitting a transaction, the agent MUST:**

1. Write trade details to `memory/trading-journal.json` with `status: "OPEN"`
2. Include: `token_symbol`, `token_address`, `entry_price`, `position_size_sol`, `tx_hash`, `timestamp`

### User Preferences

Store in `memory/trading-preferences.json`:

| Preference | Default | Description |
|------------|---------|-------------|
| `max_position_size` | 0.1 SOL | Max SOL per trade |
| `max_open_positions` | 5 | Max concurrent open positions |
| `max_daily_trades` | 20 | Max trades per day |
| `stop_loss_pct` | 30% | Notify/sell when loss exceeds this |
| `take_profit_pct` | 100% | Notify/sell when gain exceeds this |
| `min_market_cap` | $500K | Skip tokens below this |
| `scan_count` | 10 | Trending tokens per scan |
| `risk_tolerance` | "conservative" | "conservative" (skip medium risk), "moderate" (ask on medium), "aggressive" (auto-trade medium) |
| `require_trade_confirmation` | true | Set to false for autonomous mode |
| `chains` | ["solana"] | Chains to scan |

---

## Safety Guardrails

### Trading Limits (Hard Caps)

| Limit | Default | Overridable? |
|-------|---------|--------------------|
| Max single trade | 0.1 SOL | Yes, via `max_position_size` |
| Max concurrent positions | 5 | Yes, via `max_open_positions` |
| Max daily trade count | 20 | Yes, via `max_daily_trades` |
| Price impact abort | >10% | No — always abort |
| Price impact warn | >5% | No — always warn |

If any limit is hit, the agent **must stop and notify the user**.

### Credential Isolation

Runtime scripts in this skill do NOT read `.env` files directly. All credentials are accessed via environment variables only, which must be pre-loaded by the caller (`source ~/.openclaw/workspace/.env`). This ensures no runtime script can independently access or exfiltrate credential files.

**Exception:** `scripts/setup.py` reads and writes `.env` — it loads existing keys to avoid regeneration, backs up `.env` before changes, and writes new keypair entries. This is the only script that touches credential files, and it runs only during initial setup or explicit `--force` regeneration.

---

## Automated Monitoring (Cron)

### Quick Setup

```bash
# Supervised mode (default): analysis + notifications, no auto-execution
source ~/.openclaw/workspace/.env && bash scripts/cron-examples.sh setup-default

# Autonomous mode (opt-in): auto-buys and auto-sells
source ~/.openclaw/workspace/.env && bash scripts/cron-examples.sh setup-autonomous

# Remove all cron jobs
bash scripts/cron-examples.sh teardown
```

| Job | Interval | Default Behavior |
|-----|----------|---------|
| `stop-loss-tp` | 5 min | Report triggered conditions, do NOT auto-sell |
| `discovery-scan` | 1 hour | Analyze and send recommendations, do NOT auto-buy |

For full cron configuration, manual setup, heartbeat alternative, and monitoring workflow details, see `references/autonomous-trading.md`.

---

## On-Chain Analysis Framework (7-Step Pipeline)

> ⚠️ **Unavailable after 2026-05-04:** Steps 1–6 all hit `wallet-data.kryptogo.app` and will stop working when the kg-xyz backend shuts down. Step 7 (execute trade via `swap.py`) continues to work, since the swap path routes through the OKX DEX aggregator and signs locally.

### Step 1: Token Overview & Market Cap Filter

`/token-overview?address=<mint>&chain_id=<id>` — get name, price, market cap, holders, risk_level. Skip if market cap < `min_market_cap`.

### Step 2: Cluster Analysis

`/analyze/<mint>?chain_id=<id>` — wallet clusters, top holders, metadata.

- ≥30-35% = "controlled" — major entity present
- ≥50% = high concentration risk
- Single cluster >50% → skip (rug pull risk)

> **Free tier limitation:** Cluster analysis only returns the top 2 clusters. To see full cluster data, upgrade at [kryptogo.xyz/pricing](https://www.kryptogo.xyz/pricing).

### Step 3: Cluster Trend (Multi-Timeframe)

`/analyze-cluster-change/<mint>` — `cluster_ratio` + `changes` across 15m/1h/4h/1d/7d.

Core insight: **Price and cluster holdings DIVERGING** is the key signal.

- Rising price + falling cluster % = distribution (bearish)
- Falling price + rising cluster % = accumulation (bullish)

### Step 4: Address Labels + Sell Pressure Verification

1. `/token-wallet-labels` → identify dev/sniper/bundle wallets
2. `/balance-history` for each risky address → check if still holding
3. Compute `risky_ratio` = active risky holdings / total cluster holdings
4. >30% = high risk, 10-30% = medium, <10% = low

> Labels represent *behavioral history*, not current holdings. Always verify via `/balance-history`.

### Step 5: Deep Dive (Optional)

`/balance-history`, `/balance-increase/<mint>`, `/top-holders-snapshot/<mint>`, `/analyze-dca-limit-orders/<mint>`, `/cluster-wallet-connections`

### Step 6: Decision

Apply Bullish Checklist from `references/decision-framework.md`.

### Step 7: Execute Trade

**Use `scripts/swap.py` for execution** — handles wallet_address injection, error checking, and journal logging.

> ✓ **Continues to work after 2026-05-04:** swap execution goes through the OKX DEX aggregator with local signing and is independent of the kg-xyz backend.

```bash
source ~/.openclaw/workspace/.env && python3 scripts/swap.py <token_mint> 0.1
source ~/.openclaw/workspace/.env && python3 scripts/swap.py <token_mint> <amount> --sell
```

---

## API Quick Reference

> ⚠️ **After 2026-05-04:** Every endpoint below is served by `wallet-data.kryptogo.app` and will be shut down. The swap tool (`swap_tokens` / `scripts/swap.py`) bypasses these endpoints and routes to the OKX DEX aggregator directly, so it continues to work.

| Endpoint | Method | Purpose | After 2026-05-04 |
|----------|--------|---------|------------------|
| `/agent/account` | GET | Check tier & quota | ⚠️ Unavailable |
| `/agent/trending-tokens` | GET | Scan trending tokens | ⚠️ Unavailable |
| `/agent/portfolio` | GET | Wallet portfolio + PnL | ⚠️ Unavailable (P&L enrichment); balances still fetchable via Solana RPC |
| `/agent/swap` | POST | Build unsigned swap tx (Solana only) | ⚠️ Unavailable (swap now routes through OKX DEX; see `scripts/swap.py`) |
| `/agent/submit` | POST | Submit signed tx (Solana only) | ⚠️ Unavailable (submit directly to Solana RPC instead) |
| `/token-overview` | GET | Token metadata & market data | ⚠️ Unavailable |
| `/analyze/:token_mint` | GET | Full cluster analysis | ⚠️ Unavailable |
| `/analyze-cluster-change/:token_mint` | GET | Cluster ratio trends | ⚠️ Unavailable |
| `/balance-history` | POST | Time-series balance data | ⚠️ Unavailable |
| `/wallet-labels` | POST | Behavior labels | ⚠️ Unavailable |
| `/token-wallet-labels` | POST | Token-specific labels | ⚠️ Unavailable |
| `/signal-dashboard` | GET | Curated accumulation signals (Pro+) | ⚠️ Unavailable |

> Full request/response details: see `references/api-reference.md`

---

## Multi-Chain Support

| Chain | chain_id | Analysis | Trading |
|-------|----------|----------|---------|
| Solana | `501` | Yes | Yes |
| BSC | `56` | Yes | No |
| Base | `8453` | Yes | No |
| Monad | `143` | Yes | No |

---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad Request | Check parameters |
| 401 | Unauthorized | Check API key |
| 402 | Quota Exceeded | Wait for daily reset or upgrade |
| 403 | Forbidden | Requires higher tier |
| 502/504 | Server error | Retry once after 10s |

---

## Operational Scripts

All scripts require credentials to be pre-loaded: `source ~/.openclaw/workspace/.env` before running.

> **Post-shutdown (2026-05-04):** `portfolio.sh`, `trending.sh`, `analysis.sh`, and `test-api.sh` all call the kg-xyz backend and will begin returning HTTP errors. `swap.py` continues to work because it uses the OKX DEX aggregator and signs locally. Scripts are kept in place so that the skill fails gracefully and a revert remains trivial if the backend comes back.

```bash
source ~/.openclaw/workspace/.env && bash scripts/portfolio.sh              # Portfolio check        (⚠️ breaks after 2026-05-04)
source ~/.openclaw/workspace/.env && bash scripts/trending.sh               # Trending tokens        (⚠️ breaks after 2026-05-04)
source ~/.openclaw/workspace/.env && bash scripts/analysis.sh               # Full analysis dashboard (⚠️ breaks after 2026-05-04)
source ~/.openclaw/workspace/.env && python3 scripts/swap.py <mint> 0.1     # Buy                     (✓ continues to work)
source ~/.openclaw/workspace/.env && python3 scripts/swap.py <mint> <amt> --sell  # Sell              (✓ continues to work)
source ~/.openclaw/workspace/.env && bash scripts/test-api.sh               # API connectivity test   (⚠️ breaks after 2026-05-04)
```

---

## Learning & Adaptation

The agent improves over time by recording trades, analyzing outcomes, and adjusting strategy. Every trade is logged to `memory/trading-journal.json`, losses trigger post-mortems, and periodic reviews propose parameter changes.

For full details on the learning system, trade journal format, post-mortem process, and strategy reviews, see `references/autonomous-trading.md`.

---

## Core Concepts

| Concept | Key Insight |
|---------|-------------|
| **Cluster** | Group of wallets controlled by same entity |
| **Cluster Ratio** | % of supply held by clusters. ≥30% = controlled, ≥50% = high risk |
| **Developer** | Deployed the token. Highest dump risk |
| **Sniper** | Bought within 1s of creation. Sell pressure if not cleared |
| **Smart Money** | Realized profit >$100K. Accumulation often precedes price moves |
| **Accumulation** | Cluster % rising + price consolidating = bullish |
| **Distribution** | Price rising + cluster % falling = bearish |

> Full concepts guide: see `references/concepts.md`

---

## Best Practices

1. Always check `/agent/account` first to confirm tier and quota
2. Always check `/agent/portfolio` on startup to detect existing positions
3. Never expose private keys in logs, messages, or CLI arguments
4. Validate price impact before submitting — abort >10%, warn >5%
5. Sign and submit promptly — blockhash expires after ~60 seconds
6. Persist state to `memory/trading-state.json` after every action
7. Log every trade to journal — no exceptions
8. Read `memory/trading-lessons.md` before scanning — avoid repeating known bad patterns

---

## File Structure

```
kryptogo-meme-trader/
├── SKILL.md                       ← You are here
├── package.json
├── .env.example
├── references/
│   ├── api-reference.md           ← Full API docs
│   ├── concepts.md                ← Core concepts
│   ├── decision-framework.md      ← Entry/exit strategies
│   └── autonomous-trading.md      ← Autonomous mode, cron, learning system
├── scripts/
│   ├── setup.py                   ← First-time setup
│   ├── cron-examples.sh           ← Cron configurations
│   ├── portfolio.sh / trending.sh / analysis.sh / test-api.sh
│   ├── swap.py                    ← Swap executor
│   └── trading-preferences.example.json
└── examples/
    ├── trading-workflow.py
    └── deep-analysis-workflow.py
```
