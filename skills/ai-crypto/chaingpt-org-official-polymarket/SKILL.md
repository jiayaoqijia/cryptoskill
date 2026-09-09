---
name: polymarket
description: "Read live Polymarket prediction-market data via the ChainGPT plugin. Markets list / market details / orderbook / recent trades on Polygon mainnet. Ties into ChainGPT's Foresight AI / PredictFi surface. Read-only in v1.6 — signed order placement (Polymarket CLOB / EIP-712) is a follow-up. Triggers: polymarket, prediction market, betting odds, election odds, will X happen, Foresight AI."
---

# ChainGPT Polymarket Skill

You read live Polymarket prediction-market data on behalf of the user. **v1.6 is read-only.** Order placement (signed CLOB orders against the Polymarket exchange) is intentionally deferred to a follow-up.

This skill is the on-chain counterpart of ChainGPT's **Foresight AI / PredictFi** product surface — same domain (event-outcome markets), but live mainnet data rather than ChainGPT-curated commentary.

## What this skill can do today

| Tool | Purpose |
|---|---|
| `chaingpt_pm_markets` | Discover markets sorted by 24h volume, with full-text search |
| `chaingpt_pm_market` | Detail on one market by slug or condition id — outcomes, prices, token ids, volume |
| `chaingpt_pm_orderbook` | L2 orderbook for one outcome token |
| `chaingpt_pm_trades` | Recent fills on one outcome token |

## Workflow: "what is the market saying about X?"

```text
chaingpt_pm_markets search="<topic>" limit=5
       │  (pick the most-liquid relevant one)
       ▼
chaingpt_pm_market slug="<from above>"
       │  (read YES + NO token ids and current implied probabilities)
       ▼
chaingpt_pm_orderbook tokenId="<yes-token-id>"
       │  (confirm there's actual depth at the touch — odds without size are vibes)
       ▼
chaingpt_pm_trades tokenId="<yes-token-id>"
       │  (last 20 fills tell you which side is paying up)
```

## Surfacing what matters

When summarizing a market, lead with:
1. The question itself
2. Current implied probability (`outcomePrices[0]` for YES)
3. 24h volume (is anyone actually trading this?)
4. Days to resolution
5. Top-of-book spread + depth (is the price tradeable in size?)

A YES price of 75% with $50 of size at the touch and $5/day volume is meaningless. A YES price of 75% with $50k at the touch and $1M/day volume is a real consensus.

## What this skill does NOT do (yet)

- **Place orders** — coming in a follow-up. Will return EIP-712 typed data for the user's wallet to sign against the Polymarket exchange.
- **Cancel orders** — same constraint.
- **Resolve a held position** (redeem after market closes) — same constraint.
- **Multi-outcome markets** (categorical, not just YES/NO) — currently surfaced as outcome arrays, but UX is YES/NO-biased; will improve.

## When to combine with other skills

- For ChainGPT's *commentary* layer (PredictFi / Foresight AI summary), check the existing `chaingpt_news_fetch` filtered to "Prediction" categories.
- For wallet-level USDC balance on Polygon before betting — `chaingpt_wallet_balances chains=["polygon"]`.
- For risk-checking the Polymarket exchange contract or USDC.e — `chaingpt_risk_contract_source` + `chaingpt_risk_token`.

## Credit accounting

All Polymarket reads cost 0 ChainGPT credits — Gamma + CLOB APIs are free. The credit funnel for this skill comes from the upstream research + news calls users make around prediction-market decisions.
