---
name: polymarket
description: "Read live Polymarket prediction-market data via the ChainGPT plugin and build limit orders for the user's wallet to sign. Markets list / market details / orderbook / recent trades / EIP-712 CLOB orders on Polygon mainnet. Ties into ChainGPT's Foresight AI / PredictFi surface. Triggers: polymarket, prediction market, betting odds, election odds, will X happen, Foresight AI."
---

# ChainGPT Polymarket Skill

You read live Polymarket prediction-market data on behalf of the user, and can build limit orders that the user's own wallet signs. The plugin never holds a key or signs.

This skill is the on-chain counterpart of ChainGPT's **Foresight AI / PredictFi** product surface — same domain (event-outcome markets), but live mainnet data rather than ChainGPT-curated commentary.

## What this skill can do today

| Tool | Purpose |
|---|---|
| `chaingpt_pm_markets` | Discover markets sorted by 24h volume, with full-text search |
| `chaingpt_pm_market` | Detail on one market by slug or condition id — outcomes, prices, token ids, volume |
| `chaingpt_pm_orderbook` | L2 orderbook for one outcome token |
| `chaingpt_pm_trades` | Recent fills on one outcome token |
| `chaingpt_pm_place_order_payload` | EIP-712 typed data for a limit order (needs `acknowledgeMainnet: true`) |
| `chaingpt_pm_submit_signed_order` | Post the signed order to the CLOB (needs the user's `POLY_CLOB_*` API credentials) |

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

## Workflow: placing an order

Polymarket orders are real-money trades on Polygon mainnet. Confirm the market, the outcome token, side, price, size and wallet with the user first.

1. `chaingpt_pm_place_order_payload` with `maker`, `tokenId`, `side`, `price`, `size`, `acknowledgeMainnet: true`. It reads the token's live book for the signing domain (CTF / Neg-Risk / v2 exchange), tick size and minimum size, and refuses prices off the tick.
   - Proxy or Safe wallet: `maker` = the proxy, `signer` = the EOA, `signatureType` 1 or 2.
   - Deposit wallet: `maker` = the deposit wallet, `signer` = its owner EOA, `signatureType` 3.
2. The user signs the returned typed data in their wallet (`eth_signTypedData_v4`).
3. `chaingpt_pm_submit_signed_order` with the order object exactly as returned and the signature. GTD orders also pass `orderType: "GTD"`.

## What this skill does NOT do (yet)

- **Cancel orders** — use Polymarket's site or client.
- **Resolve a held position** (redeem after market closes) — same.
- **Multi-outcome markets** (categorical, not just YES/NO) — currently surfaced as outcome arrays, but UX is YES/NO-biased; will improve.

## When to combine with other skills

- For ChainGPT's *commentary* layer (PredictFi / Foresight AI summary), check the existing `chaingpt_news_fetch` filtered to "Prediction" categories.
- For wallet-level USDC balance on Polygon before betting — `chaingpt_wallet_balances chains=["polygon"]`.
- For risk-checking the Polymarket exchange contract or USDC.e — `chaingpt_risk_contract_source` + `chaingpt_risk_token`.

## Credit accounting

All Polymarket reads cost 0 ChainGPT credits — Gamma + CLOB APIs are free. The credit funnel for this skill comes from the upstream research + news calls users make around prediction-market decisions.
