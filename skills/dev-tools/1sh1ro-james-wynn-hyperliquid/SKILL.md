---
name: james-wynn-hyperliquid
description: Use when the user wants to inspect or discuss James Wynn's public Hyperliquid trading behavior, wallet-level real positions, recent fills, or high-conviction momentum style. Covers best-effort public attribution to wallet 0x5078C2fBeA2b2aD61bc840Bc023E35Fce56BeDb6.
---

# James Wynn Hyperliquid

Use this skill when the user asks about `James Wynn`, his Hyperliquid account, whether he is still active, or whether his style is worth copying.

## Read First

- `references/profile.md`
- `../hyperliquid-public-trader-watch/SKILL.md`

## Workflow

1. Treat wallet `0x5078C2fBeA2b2aD61bc840Bc023E35Fce56BeDb6` as the current best-effort public attribution.
2. Run:

```bash
python3 skills/hyperliquid-public-trader-watch/scripts/fetch_trader_snapshot.py \
  --address 0x5078C2fBeA2b2aD61bc840Bc023E35Fce56BeDb6 \
  --name "James Wynn"
```

3. Emphasize:
- whether he currently has risk on
- whether recent history shows large directional conviction
- whether recent losses/profits came from trend continuation or stubborn re-entry
4. If the account is flat, say so directly. Do not hallucinate an active view.

## Output Bias

When the user asks for style, summarize him as:

- high-conviction
- majors-focused
- willing to take aggressive leverage
- follower-unfriendly if entry is already gone

## Copy-Trading Warning

If the user asks whether to follow him, default to `看方法，不追同价`. His style is useful for studying conviction and timing, but poor for delayed copy-trading.
