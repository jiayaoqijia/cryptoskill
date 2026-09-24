---
name: hyperliquid-public-trader-watch
description: Use when the user wants to inspect a public Hyperliquid trader's real positions, recent fills, account curve, leverage posture, or execution style from wallet-level data. Covers snapshot pulls for any public address plus style inference rules from current exposure and recent fills.
---

# Hyperliquid Public Trader Watch

Use this skill when the user wants real-trading data from a public Hyperliquid address, or wants a trader's style described from observable behavior instead of opinions.

## Read First

- `references/workflow.md`
- `scripts/fetch_trader_snapshot.py`

## Inputs

Prefer one of:

- public wallet address
- Hyperliquid username plus a wallet address the user gives you
- a trader alias already defined by another persona skill in this repo

If the user gives only a name and there is no known address in local references, say the attribution is incomplete and do not invent one.

## Workflow

1. Run the bundled script with the wallet address.
2. Use the snapshot as the primary source of truth:
- `clearinghouseState` for current positions and leverage
- `userFills` for recent execution behavior
- `portfolio` for account-value and pnl history
3. Separate facts from inference.
4. When describing style, infer only from observable patterns such as:
- single-asset concentration vs basket rotation
- averaging in vs one-shot entry
- high-leverage conviction vs lower-leverage carry
- trend-following vs fade/mean-reversion behavior
- willingness to hold through volatility
5. If the account is inactive now, say that clearly and rely more on recent fill history than current positions.

## Output Shape

Default to:

```markdown
交易员：

当前状态：

当前持仓：

最近动作：

风格判断：

我会怎么跟，不会怎么跟：

风险提示：
```

## Rules

1. Do not call a trader "牛逼" just because size is large. Distinguish skill from aggression.
2. Do not treat PnL screenshots or social claims as ground truth when wallet data disagrees.
3. Do not overfit personality from one trade.
4. If attribution between alias and wallet is uncertain, label it as `低置信归因`.
5. When the user asks whether to copy-trade, explicitly discuss liquidation distance, concentration, and whether the move is already extended.
