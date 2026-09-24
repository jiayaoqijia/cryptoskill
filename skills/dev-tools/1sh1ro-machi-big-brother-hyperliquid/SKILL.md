---
name: machi-big-brother-hyperliquid
description: Use when the user wants to inspect or discuss Machi Big Brother's public Hyperliquid positions, fill history, leverage posture, or oversized conviction style. Covers best-effort public attribution to wallet 0x020ca66c30bec2c4fe3861a94e4db4a498a35872.
---

# Machi Big Brother Hyperliquid

Use this skill when the user asks about `Machi Big Brother`, his open Hyperliquid bets, or wants a plain-language read on how he is positioning.

## Read First

- `references/profile.md`
- `../hyperliquid-public-trader-watch/SKILL.md`

## Workflow

1. Treat wallet `0x020ca66c30bec2c4fe3861a94e4db4a498a35872` as the current best-effort public attribution.
2. Run:

```bash
python3 skills/hyperliquid-public-trader-watch/scripts/fetch_trader_snapshot.py \
  --address 0x020ca66c30bec2c4fe3861a94e4db4a498a35872 \
  --name "Machi Big Brother"
```

3. Focus the analysis on:
- concentration in BTC, ETH, or HYPE
- leverage and liquidation distance
- whether he is adding into strength or averaging into heat
- whether the current setup is educational or simply too late to follow

## Output Bias

Describe him in practical terms:

- size-first and conviction-first
- accepts huge notional exposure
- can sit in oversized winners
- dangerous to imitate without deep margin cushion

## Hard Rule

Do not recommend blind copying if the account is already heavily in profit and far from the user's likely entry. Late copy-trading changes the whole risk profile.
