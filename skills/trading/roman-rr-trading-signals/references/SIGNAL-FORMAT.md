# Signal Format Reference

Complete field specification for signals returned by the Trading Signals API.

## Signal Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique signal identifier |
| `coin` | string | Ticker symbol (e.g. "BTC", "ETH", "SOL") |
| `direction` | string | `"bullish"` (long) or `"bearish"` (short) |
| `confidence` | number | 0-100 confidence score. Higher = stronger conviction |
| `type` | string | Signal type (see Signal Types below) |
| `tags` | string[] | All contributing factors (multi-factor attribution) |
| `summary` | string | Human-readable analysis summary |
| `entryPrice` | number | Suggested entry price in USD |
| `stopLoss` | number | Stop-loss level in USD |
| `takeProfit` | number | Take-profit target in USD |
| `leverage` | number | Suggested leverage (1-10x) |
| `riskRewardRatio` | number | Risk/reward ratio (e.g. 2.5 means 2.5:1) |
| `positionSize` | string | Suggested position size (e.g. "2-3%") |
| `roi` | number\|null | Leverage-adjusted ROI % (only for verified signals) |
| `createdAt` | string | ISO 8601 timestamp |

## Verification Object

Nested under `verification` in each signal:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"unverified"`, `"pending"`, `"success"`, `"failed"` |
| `priceChangePct` | number\|null | Actual price change at verification (%) |
| `maxFavorablePct` | number\|null | Maximum favorable price movement (%) |
| `theoreticalProfitPct` | number\|null | Theoretical profit with leverage (%) |
| `stopLossHit` | boolean\|null | Whether stop-loss was hit |
| `takeProfitHit` | boolean\|null | Whether take-profit was hit |
| `verifiedAt` | string\|null | ISO 8601 timestamp when verified |

## Signal Types

| Type | Description |
|------|-------------|
| `funding_anomaly` | Extreme funding rates indicating overcrowded positioning |
| `volume_spike` | Abnormal volume indicating institutional activity |
| `price_breakout` | Significant move with volume confirmation |
| `whale_activity` | Large trades, sudden OI jumps, order book sweeps |
| `liquidation_cascade` | Price approaching liquidation clusters |
| `momentum_shift` | RSI/price divergence, MACD crossover, trend reversal |

The `type` field is free-form — the AI may create additional descriptive types like `trend_reversal`, `mean_reversion`, `oi_divergence`, etc.

## ROI Calculation

- **Wins** (status=success): `min(maxFavorablePct, TP_distance%) * leverage`
- **Losses** (status=failed): SL-aware capping, multiplied by leverage, always negative
- **Pending/Unverified**: `roi` is `null`

## Confidence Interpretation

| Range | Meaning |
|-------|---------|
| 90-100 | Very high conviction — rare |
| 80-89 | Strong setup with multiple confirming factors |
| 70-79 | Moderate setup — acceptable for lower leverage |
| Below 70 | Filtered out by the system (not returned) |

## Stats Response

| Field | Type | Description |
|-------|------|-------------|
| `period` | string | e.g. "30d" |
| `totalSignals` | number | Total signals in period |
| `verifiedSignals` | number | Signals with verification outcome |
| `hitRate` | number | Success rate (0-100%) |
| `avgConfidence` | number | Average confidence (0-100) |
| `cumulativeROI` | number | Sum of all per-signal ROIs (%) |
| `avgLeverage` | number | Average leverage used |
| `byDirection` | object | Breakdown per direction (total, hits, hitRate) |
