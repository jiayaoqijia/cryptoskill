# Leaderboard Scoring Model

6-dimension scoring model for wallet address analysis, plus AI archetype overlay.

---

## Overview

```
totalScore = winrate(25) + stability(20) + drawdown(20) + tags(15) + pnl(10) + follow_friendly(10) = 100
finalScore = totalScore + ai_adjustment(±10)
```

Rating: ⭐⭐⭐ ≥ 80 · ⭐⭐ ≥ 65 · ⭐ ≥ 50 · ❌ < 50

---

## Dimension 1: Win Rate (25 points)

| Win Rate | Score |
|----------|-------|
| ≥ 70% | 25 |
| 60-69% | 20 |
| 50-59% | 15 |
| 40-49% | 8 |
| < 40% | 0 |

Source field: `winRate` (0-100).

---

## Dimension 2: Stability (20 points)

Based on `dailyPNL[]` array — daily profit distribution + concentration penalty.

**Scoring logic**:
1. Compute daily PnL values from `dailyPNL[]` (field: `realizedPnl` per day)
2. Base score: consistency of positive days (positive days / total days × 20)
3. Concentration penalty: if single-day PnL > 50% of total, penalize proportionally

**Note**: These ranges are guidance for AI-judgment, not deterministic formulas. The backend does not expose the exact penalty formula. Use the ranges as scoring anchors and adjust based on the overall profit distribution shape.

| Stability Profile | Score |
|-------------------|-------|
| Consistent daily profits, no single-day dominance | 18-20 |
| Mostly consistent, some concentration | 12-17 |
| Inconsistent or high concentration | 6-11 |
| Erratic | 0-5 |

---

## Dimension 3: Drawdown (20 points)

Based on `tokenDistribution{}` — four buckets of token PnL:

| Bucket | Description |
|--------|-------------|
| `gt500Cnt` | Tokens with PnL > $500 |
| `between0And500Cnt` | Tokens with PnL $0-$500 |
| `between0AndNegative50Cnt` | Tokens with PnL -$50 to $0 |
| `ltNegative50Cnt` | Tokens with PnL < -$50 |

**Scoring logic**:
- Reward `gt500Cnt` and `between0And500Cnt` (profitable tokens)
- Penalize `ltNegative50Cnt` (heavy losses)
- Rug penalty: if `ltNegative50Cnt` > 30% of total tokens, additional penalty

**Note**: Like Stability, these ranges are AI-judgment guidance. The exact rug penalty formula is not exposed by the backend. Use the bucket distribution to assess overall drawdown health.

| Drawdown Profile | Score |
|------------------|-------|
| Minimal losses, mostly profitable tokens | 16-20 |
| Some losses but manageable | 10-15 |
| Significant losses | 4-9 |
| Heavy losses / rug pattern | 0-3 |

---

## Dimension 4: Tags (15 points)

Based on `tags[]` and `genericAddressTagList[]`.

| Tag | Score |
|-----|-------|
| Smart Money | +15 |
| KOL | +10 |
| MPC | +5 |
| No notable tags | 0 |

**Stacking rule**: If multiple tags present, take the highest single tag score (do not stack).

---

## Dimension 5: PnL (10 points)

Based on `realizedPnl` (USD).

| PnL Range | Score |
|-----------|-------|
| ≥ $100K | 10 |
| $10K-$100K | 7 |
| $1K-$10K | 4 |
| $0-$1K | 2 |
| < $0 (loss) | 0 |

---

## Dimension 6: Follow-Friendly (10 points)

Based on `avgBuyVolume` — the "sweet spot" for copy-trading.

| Avg Buy Volume | Score | Rationale |
|----------------|-------|-----------|
| $5K-$50K | 10 | Large enough to matter, small enough to follow |
| $1K-$5K | 7 | Meaningful but small |
| $50K-$100K | 5 | Too large for most followers |
| > $100K | 3 | Whale — hard to follow |
| < $1K | 2 | Too small to be meaningful |

---

## AI Overlay (±10)

Applied after the 6-dimension base score.

### Archetype Classification

| Archetype | Description |
|-----------|-------------|
| `sniper` | High-frequency, small tickets, short holding periods |
| `swing` | Medium-frequency, medium holding periods |
| `accumulator` | Gradual position building over time |
| `farmer` | Airdrop/liquidity farming patterns |
| `mixed` | No dominant pattern |

### Behavior Flags

Detected patterns that inform the AI adjustment:
- `High Frequency Small Amount` — high frequency, small amounts
- `Nocturnal Active` — predominantly nocturnal trading
- `Concentrated Building` — concentrated position building
- `Round-Trip` — rapid round-trip trades
- `Long Holding` — long holding periods
- `Multi-Chain` — active on multiple chains

### AI Adjustment

| Adjustment | Condition |
|------------|-----------|
| +5 to +10 | Consistent archetype with clear edge (e.g., sniper with consistently high win rate) |
| -5 to -10 | Red flags (e.g., bot-like patterns, wash trading indicators) |
| 0 | Neutral or ambiguous |

**Required**: `aiReason` must be filled for audit trail whenever adjustment ≠ 0.

---

## Rating Thresholds

| Rating | finalScore | Meaning |
|--------|------------|---------|
| ⭐⭐⭐ | ≥ 80 | Excellent — strong track record, worth following |
| ⭐⭐ | ≥ 65 | Good — above average, consider following |
| ⭐ | ≥ 50 | Average — proceed with caution |
| ❌ | < 50 | Poor — not recommended |

---

## Single Address Analyze Flow

1. **Query top N**: Internally call `leaderboard query` with pagination to fetch the top N entries for the specified chain + period. Default N=1000, configurable via `--top-n` (max 5000).
2. **Reverse lookup**: Search for the target `address` in the results.
3. **If found**: Compute 6-dimension scores from the record fields → apply AI overlay → output `finalScore` + `rating`.
4. **If not found**: Return "N beyond top" (beyond top N). Long-tail wallets can only be analyzed from already-imported groups — use `binance-wallet-tracker` skill's `address list` to check if the address is tracked locally.

### Limitation & Guidance

- Default scans top **1000** entries. If the target address is not found, inform the user: "Address not in top 1000. To expand search range, use `--top-n 5000` to fetch more data, or check on-chain data in `binance-wallet-tracker`."
- The backend API supports arbitrary pagination (`pageSize` max 20, `pageNo` from 0). The `--top-n` flag controls how many entries to scan.
- Known backend bug: page 0 and page 1 return identical data. The CLI automatically deduplicates.
