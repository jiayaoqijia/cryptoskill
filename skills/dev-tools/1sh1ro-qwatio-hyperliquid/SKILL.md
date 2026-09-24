---
name: qwatio-hyperliquid
description: Use when the user wants to inspect or discuss Qwatio's public Hyperliquid trading history, real fills, inactive-vs-active status, or aggressive directional style. Covers best-effort public attribution to wallet 0x9018960618eFF55F5852e345B7Cb5661fd2928e1.
---

# Qwatio Hyperliquid

Use this skill when the user asks about `Qwatio`, wants to know whether he is still trading on Hyperliquid, or wants a read on his execution pattern.

## Read First

- `references/profile.md`
- `../hyperliquid-public-trader-watch/SKILL.md`

## Workflow

1. Treat wallet `0x9018960618eFF55F5852e345B7Cb5661fd2928e1` as the current best-effort public attribution.
2. Run:

```bash
python3 skills/hyperliquid-public-trader-watch/scripts/fetch_trader_snapshot.py \
  --address 0x9018960618eFF55F5852e345B7Cb5661fd2928e1 \
  --name "Qwatio"
```

3. If current positions are empty, frame the answer around `recent observable history` instead of pretending there is a live stance.
4. Call out repeated same-side fills and whether the behavior looks like scaling, reloading, or forced exit.

## Output Bias

Describe him as:

- fast and directional
- capable of concentrated bets
- not a low-risk template for beginners

## Hard Rule

If the wallet is flat or stale, say `这个 skill 更适合做行为复盘，不适合拿来抄今天的方向`.
