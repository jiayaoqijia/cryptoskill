# Nansen — AI-agent skill

> **Generated distribution mirror.** The canonical source, issues, and releases live in [https://github.com/Vo1ganin/crypto-claude-skills](https://github.com/Vo1ganin/crypto-claude-skills). Do not hand-edit generated files in this repository.

AI-agent skill for cross-chain wallet and Smart Money analytics with cost and credential safeguards.

- Canonical skill: [https://github.com/Vo1ganin/crypto-claude-skills/tree/main/skills/nansen](https://github.com/Vo1ganin/crypto-claude-skills/tree/main/skills/nansen)
- Collection: [https://github.com/Vo1ganin/crypto-claude-skills](https://github.com/Vo1ganin/crypto-claude-skills)
- Provenance: [`.source.json`](.source.json)

## Skill documentation

Smart Money, wallet profiling, and token intelligence via [Nansen API](https://docs.nansen.ai) — 37 blockchains including Solana and Hyperliquid.

## What it does

- Access to all Nansen endpoint categories: Smart Money, Profiler, Token God Mode, Portfolio, Prediction Markets, Hyperliquid
- Credit budget awareness — costs differ **150×** between endpoint tiers
- Multi-key rotation with x402 pay-per-call as last-resort fallback
- Live credit balance tracking via `X-Nansen-Credits-Remaining` header

## When it triggers

Any request involving "smart money", institutional wallet activity, DeFi funds behavior, Nansen Score, token holders with labels, Hyperliquid perp trader analysis, on-chain PnL leaderboards.

## Files

| File | Purpose |
|------|---------|
| [`SKILL.md`](SKILL.md) | Three hard rules, workflow, error handling |
| [`references/endpoints.md`](references/endpoints.md) | Full catalog with credit cost per endpoint + Solana support matrix |
| [`references/credits.md`](references/credits.md) | Budget rules, Pro/Free tier math, x402 fallback, credit traps |
| [`references/filters.md`](references/filters.md) | Chain enum, smart money labels, filter schemas, sort fields |
| [`references/examples/smart_money_flows.py`](references/examples/smart_money_flows.py) | "What are funds accumulating?" on any chain |
| [`references/examples/wallet_pnl_batch.py`](references/examples/wallet_pnl_batch.py) | PnL summary for N wallets with auto-stop on low credits |
| [`references/examples/token_holders.py`](references/examples/token_holders.py) | Top holders with explicit `premium_labels` warning |

## Key rules

1. **150× cost trap: `premium_labels: true`** — default cost is 5, with premium labels is 150. Never set unless explicitly asked
2. **Smart Money endpoints: 5 credits each** — use `per_page: 1000` to consolidate
3. **Free tier consumes 10× faster** — 1 Pro credit = 10 Free credits
4. **Credit thresholds: 50 warn, 200 block** per operation
5. **Agent endpoints: 200/750 credits** — always confirm with user first

## Solana coverage update (2026-04-24)

**Important:** old notes said "Solana ~14 smart money wallets". **Out of date.** Current Solana support:
- Smart Money: full (netflow, dex-trades, holdings, historical) ✅
- TGM: full (flows, transfers, holders, pnl) ✅
- Profiler: full (balances, tx, pnl, related wallets) ✅
- NOT supported: single-tx lookup by hash, labels endpoints

Nansen is now a strong option for Solana smart money research.

## Quick example

```
> "What are funds buying on Solana this week?"

Skill:
  → POST /smart-money/netflow
  → chains: ["solana"], labels: ["Fund"], sort: net_flow_7d_usd DESC
  → 5 credits
  → Returns top 30 tokens with net flows, trader counts, ages
```

## Setup

Set `NANSEN_API_KEY` in `.env`. Get key at [dashboard.nansen.ai](https://app.nansen.ai).

For multi-key rotation set `NANSEN_API_KEY_2`, etc. (optional).

Pay-per-call via [x402 protocol](https://docs.nansen.ai/x402) supported but requires explicit user consent before use.
