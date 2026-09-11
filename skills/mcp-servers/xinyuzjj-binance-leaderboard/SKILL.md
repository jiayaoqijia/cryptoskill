---
name: binance-leaderboard
description: |
  On-chain wallet leaderboard and Gem Hunter analysis on Binance Web3. Query top trader
  rankings by PnL, win rate, volume, trade count, or token count across BSC/Solana/Base/ETH.
  Analyze individual wallet addresses with a 6-dimension scoring model (winrate/stability/drawdown/
  tags/pnl/follow_friendly) plus AI archetype overlay. Query Gem Hunter to find wallets holding
  specific tokens. Save and load preset filter conditions and Gem Hunter configs.
  Trigger whenever the user mentions leaderboard, top traders, wallet analysis,
  Address Analysis, AddressScore, Gem Hunter, or wants to evaluate a wallet's trading quality — even if they
  don't say "leaderboard" explicitly.
metadata:
  author: binance-web3-team
  version: "1.1"
  openclaw:
    requires:
      bins:
        - baw
    install:
      - kind: node
        package: '@binance/agentic-wallet'
        bins: [baw]
        label: Install Binance Agentic Wallet CLI (npm)
---

# Binance Leaderboard Skill

On-chain wallet leaderboard ranking and address analysis. Query top traders by PnL, win rate, and more. Evaluate wallet quality with a 6-dimension scoring model.

## Prerequisites

This skill requires the `baw` CLI (`@binance/agentic-wallet` npm package). If `baw` is not found:

```bash
npm install -g @binance/agentic-wallet
```

Verify: `baw --version` should print `1.6.2` or higher. If installation fails or the user doesn't have Node.js, inform them that Node.js >= 18 is required.

## When to Use

| User intent | Command |
|-------------|---------|
| Query top traders by PnL/win rate/volume | `baw leaderboard query` |
| Analyze a single wallet address (6-dim score + AI archetype) | `baw leaderboard analyze` |
| Find wallets holding specific tokens (Gem Hunter) | `baw leaderboard alpha-radar` |
| Save/load preset filter conditions | `baw leaderboard preset save/list` |
| Save/load Gem Hunter configs | `baw leaderboard alpha-radar-config save/list` |

## Supported Chains

| Chain | chainId |
|-------|---------|
| BSC | `56` |
| Solana | `CT_501` |
| Base | `8453` |
| Ethereum | `1` |

## Command Tree

```
baw leaderboard
  query                     # Leaderboard query (Public, no auth)
  analyze                   # Single address analysis (6-dim score + AI overlay)
  alpha-radar              # Gem Hunter query (Private, agentSessionId)
  preset
    save                    # Save preset filters (Private)
    list                    # List preset filters (Private)
  alpha-radar-config
    save                    # Save Gem Hunter config (Private)
    list                    # List Gem Hunter config (Private)
```

All commands support `--json` for structured output.

## Leaderboard Query

```bash
# Basic query — top 20 by PnL on BSC, 7d period
baw leaderboard query -c 56 -p 7d -t ALL --json

# Sort by win rate, KOL tag only
baw leaderboard query -c 56 -p 30d -t KOL --sort-by 20 --json

# Pagination (page from 0, size max 20)
baw leaderboard query -c 56 -p 7d --page 0 --size 20 --json
```

**Public endpoint** — no auth required. Returns per-address PnL, win rate, volume, trade count, token distribution, daily PNL, and top earning tokens.

Key query parameters: `-c/--chain-id` (required), `-p/--period` (7d/30d/90d), `-t/--tag` (ALL/KOL/MPC), `--sort-by` (0=PnL · 20=Win Rate · 30=Total Volume · 50=Trade Count · 60=Recent Activity · 70=Profit Rate · 80=Token Count), `--order-by` (0/2=Descending · 1=Ascending), `--page` (from 0), `--size` (max 20).

Full parameter and return field reference: [`references/cli.md`](references/cli.md)

## Single Address Analyze

```bash
# Analyze a wallet address — 6-dim scoring + AI archetype
# Default scans top 1000 entries
baw leaderboard analyze -c 56 -a 0xabc... --json

# Scan more entries (up to 5000) for long-tail addresses
baw leaderboard analyze -c 56 -a 0xabc... --top-n 5000 --json
```

Evaluates the address across 6 dimensions (winrate 25 + stability 20 + drawdown 20 + tags 15 + pnl 10 + follow_friendly 10 = 100), then applies an AI overlay (archetype + behavior_flags + ai_adjustment ±10).

**Flow**: Query leaderboard top 1000 (configurable via `--top-n`) → reverse-lookup the target address → compute scores → apply AI overlay → output rating.

**Rating**: ⭐⭐⭐ ≥ 80 · ⭐⭐ ≥ 65 · ⭐ ≥ 50 · ❌ < 50

If the address is not in the top N (default 1000), returns "N beyond top". Use `--top-n` to increase scan range up to 5000.

Full scoring model details: [`references/scoring.md`](references/scoring.md)

## Gem Hunter

```bash
# Find wallets holding specific tokens
baw leaderboard alpha-radar -c 56 \
  -t 0xtoken1,0xtoken2 \
  -m 1 --json
```

**Private endpoint** — requires `agentSessionId`. Extra required params: `-t/--tokens` (comma-separated token addresses), `-m/--match-count` (≥ 1). Supports `-p/--period`, `--page`, `--size` like query.

Returns records with the same fields as leaderboard query, but `topEarningTokens` replaced by `marchedTokens` (matched tokens).

**Note**: The field is spelled `marchedTokens` (not "matched") in the CLI output.

## Preset & Gem Hunter Config

```bash
# Save preset filter conditions (pass null/empty to clear all)
baw leaderboard preset save --config '[{"name":"MyPreset","period":"7d","winRateMin":50}]' --json

# List saved presets
baw leaderboard preset list --json

# Save Gem Hunter config (pass null/empty to clear)
baw leaderboard alpha-radar-config save -c 56 \
  --config '[{"uuid":"u1","name":"MyRadar","matchTokenCount":2,"tokenAddressList":[{"tokenAddress":"0xabc"}]}]' --json

# List saved configs
baw leaderboard alpha-radar-config list -c 56 --json
```

## Core Rules

### Scoring Model Overview

6-dimension model (total 100) + AI overlay (±10). Dimensions: winrate (25), stability (20), drawdown (20), tags (15), pnl (10), follow_friendly (10). Full tiered scoring tables and AI overlay rules: [`references/scoring.md`](references/scoring.md).

### Top-N Reverse Lookup

`analyze` queries the leaderboard's top 1000 entries (configurable via `--top-n`, max 5000) and reverse-looks-up the target address. If not found, returns "N beyond top" — inform the user they can increase `--top-n` or use `binance-wallet-tracker`'s address list for long-tail wallets.

### Preset & Config Clearing

Passing `null` or empty array to `preset save` or `alpha-radar-config save` clears all saved items.

### Cross-Skill Scenarios

Some scenarios require both leaderboard and wallet-tracker skills:
- **evaluate follow list**: Use `binance-wallet-tracker`'s `tracker follow` to get the user's followed addresses, then `leaderboard analyze` each one.
- **leaderboard diff**: Query leaderboard top N, then diff against `binance-wallet-tracker`'s `address list` to find untracked wallets.
- **batch import**: Query leaderboard with filters → output address list → feed to `binance-wallet-tracker`'s `address batch` command.

### Write-Back Confirmation

After preset/config save operations, re-fetch via `list` to confirm the operation succeeded — don't assume success from the API response alone. If readback shows the saved data is missing, tell the user "Save may not have taken effect, please try again later" — never mention backend bugs or silent failures.

### User-Facing Presentation

This skill serves end users, not developers. Internal field names, error codes, and CLI internals must never appear in user-facing output.

**1. Term Mapping (internal → user-facing)**

| Internal value | User-facing term | Notes |
|----------------|-------------------|-------|
| `archetype: sniper` | Sniper | |
| `archetype: swing` | Swing Trader | |
| `archetype: accumulator` | Accumulator | |
| `archetype: farmer` | Farmer | |
| `archetype: mixed` | Mixed | |
| `sort-by: 0` | Sort by PnL | |
| `sort-by: 20` | Sort by Win Rate | |
| `sort-by: 30` | Sort by Total Volume | |
| `sort-by: 50` | Sort by Trade Count | |
| `sort-by: 60` | Sort by Recent Activity | |
| `sort-by: 70` | Sort by Profit Rate | |
| `sort-by: 80` | Sort by Token Count | |
| `address` (in display) | omit | Don't show raw address unless user asks; use `{addressLabel}` |
| `finalScore` | Score | Don't show the formula `totalScore + aiAdjustment` |

Raw enum values (`sniper`, `swing`, etc.) may appear in CLI syntax examples and internal lookup tables, but never in user-facing replies.

**2. Never expose internal identifiers**

- `groupId`, `displayOrder` — internal IDs, never shown to users
- Error codes (`70001001`, etc.) — translate to natural-language messages only
- Backend behavior details (e.g. preset save returning `data: true` without persisting) — never mention "backend bug" or "silent failure"

**3. Display template hygiene**

Use user-facing terms in all output. The `archetype` field should be translated to its Chinese term (Sniper, Swing Trader, etc.) — never show the raw English enum value. Score should be shown as a number, not as a formula.

## Error Codes

Error codes are for internal lookup only — never show numeric codes or internal names to users. Translate to natural-language messages.

| Code | Internal Name | User-Facing Message |
|------|---------------|---------------------|
| 70001001 | TRACKER_API_ERROR | Query failed, please try again later |
| 70004001 | TRACKER_LEADERBOARD_EMPTY | Leaderboard data is empty |
| 70004002 | TRACKER_ADDRESS_NOT_RANKED | Address not ranked (beyond top 250) |

## Display Templates

**Leaderboard entry**:
```
{addressLabel} | PnL: {realizedPnl} ({realizedPnlPercent}%) | Win Rate: {winRate}% | Trades: {totalTxCnt} | Tokens: {totalTradedTokens}
```

**Address analysis rating**:
```
📊 {addressLabel} Address Analysis

Rating: ⭐⭐⭐ (85/100)
Trading Style: Sniper
Behavior Patterns: High Frequency Small Amount, Nocturnal Active

Dimension Scores:
  Win Rate: 22/25 | Stability: 18/20 | Drawdown: 16/20
  Tags: 15/15 | PnL: 8/10 | Trackability: 6/10

AI Adjustment: +5 (consistent trading style, stable pattern)
```

## Full CLI Reference

- [`references/cli.md`](references/cli.md) — All commands with parameter tables, return field tables, and examples
- [`references/scoring.md`](references/scoring.md) — 6-dimension scoring model, AI overlay, rating standards
