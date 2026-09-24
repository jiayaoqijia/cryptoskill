---
name: hyperliquid-public-trader-orchestrator
description: Use when the user wants a ranked sweep of public Hyperliquid traders, such as "今天哪些公开交易员最猛", "帮我扫一圈公开仓位", or "按风格给我排一下值得看的 trader". Covers registry-based scanning, live ranking, and trader cards built from wallet-level data.
---

# Hyperliquid Public Trader Orchestrator

Use this skill when the user wants a batch scan instead of a single trader lookup.

## Read First

- `references/trader-registry.json`
- `references/scoring.md`
- `scripts/rank_public_traders.py`

## Workflow

1. Run the ranking script.
2. Treat the script output as the base ranking.
3. For the top names, explain:
- whether they are currently active
- what they are actually holding
- why they ranked high
- what can be learned from them
- why blindly copying them is still dangerous
4. If the user asks for one trader in detail, switch to `hyperliquid-public-trader-watch`.

## Commands

Default:

```bash
python3 skills/hyperliquid-public-trader-orchestrator/scripts/rank_public_traders.py
```

Top 5 only:

```bash
python3 skills/hyperliquid-public-trader-orchestrator/scripts/rank_public_traders.py --top 5
```

JSON:

```bash
python3 skills/hyperliquid-public-trader-orchestrator/scripts/rank_public_traders.py --json
```

## Output Shape

Default to:

```markdown
今天最值得看的公开交易员：

1. 名字
当前在干什么：
为什么排这：
能学什么：
别怎么抄：

2. 名字
当前在干什么：
为什么排这：
能学什么：
别怎么抄：
```

## Rules

1. Rank `worth watching`, not `most famous`.
2. Give more weight to current active risk than stale history.
3. Empty positions can still be interesting for replay, but should not top the list unless the user asked for history review.
4. Keep attribution confidence explicit.
5. If the registry is small, say so. Do not pretend the scan is full-market coverage.
