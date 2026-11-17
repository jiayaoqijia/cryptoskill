# Signal Format Reference

Complete field specification for signals returned by the Trading Signals API.

## Response envelope (`GET /signals`)

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` on success |
| `signals` | object[] | Live signals (see Signal Object) |
| `returned` | number | Signals in this response |
| `totalMatching` | number | Live signals matching the filters (can exceed `returned`) |
| `sortedBy` | string | The order used: live PnL (default), or `createdAt, newest first` with `sort=newest` |
| `filtersApplied` | object | The filters the server understood |
| `meta` | object | `plan` (`free` or `pro`), `limit`, `days`, `filter` |
| `upgrade` | object | Free plan only: `title`, `message`, `proUnlocks`, `price`, `upgradeUrl` (and `subscribeUrl` when the key has an account) |
| `notice` | object | Only in the last days of a trial: `type: "trial_ending"`, `message`, `upgradeUrl` |
| `marketNotice` | object | Only while new shorts are paused during a BTC rally |
| `feedNote` | string | Only while the feed is one-sided (for example almost all shorts) |

`GET /signals/:id` returns `{ success, signal }` with the same Signal Object.

## Signal Object

Fields marked **Pro** are `null` on the free plan and without a key, and
`requiresSubscription` is `true`. That is the plan, not an error.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique signal identifier |
| `coin` | string | Ticker symbol (e.g. "BTC", "ETH", "SOL") |
| `direction` | string | `"bullish"` (long) or `"bearish"` (short) |
| `confidence` | number | 0-100: the model's own conviction. Not a calibrated probability (see Confidence) |
| `type` | string | Signal type (see Signal Types below) |
| `tags` | string[] | All contributing factors (multi-factor attribution) |
| `summary` | string | Human-readable analysis summary |
| `transmissionChain` | object[] | Reasoning steps: `{ factor, direction, logic, dataPoint }`. Can be empty |
| `invalidationConditions` | object[] | What would make the idea wrong: `{ type, description, threshold }`. Can be empty |
| `executionHints` | object[] | Execution notes: `{ type, description, parameter }`. Can be empty |
| `anomalyChain` | object\|null | The market anomaly that triggered the signal, when there was one |
| `entryPrice` | number\|null | **Pro.** Suggested entry price in USD |
| `stopLoss` | number\|null | **Pro.** Stop-loss level in USD |
| `takeProfit` | number\|null | **Pro.** Take-profit target in USD |
| `leverage` | number\|null | **Pro.** Suggested leverage (1-10x) |
| `riskRewardRatio` | number\|null | **Pro.** Target distance ÷ stop distance. Often below 1: the stop is further away than the target |
| `positionSize` | string\|null | **Pro.** Suggested position size (e.g. "2-3%") |
| `livePrice` | number\|null | Latest price seen by the server |
| `livePnlPct` | number\|null | **Pro.** Unleveraged move from entry to `livePrice`, in the signal's direction (%) |
| `requiresSubscription` | boolean | `true` when the Pro fields above were withheld |
| `roi` | number\|null | Leverage-adjusted ROI % (resolved signals only; see ROI Calculation) |
| `createdAt` | string | ISO 8601 timestamp |

## Verification Object

Nested under `verification` in each signal:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"unverified"`, `"pending"` (both live), `"success"`, `"failed"`, `"expired"` (all final) |
| `priceChangePct` | number\|null | Actual price change at verification (%) |
| `maxFavorablePct` | number\|null | Maximum favorable price movement (%) |
| `theoreticalProfitPct` | number\|null | Theoretical profit with leverage (%) |
| `stopLossHit` | boolean\|null | Whether stop-loss was hit |
| `takeProfitHit` | boolean\|null | Whether take-profit was hit |
| `directionCorrect` | boolean\|null | Whether price moved in the signal's direction |
| `tpProgressPct` | number\|null | How far price got toward the target (%) |
| `verifiedAt` | string\|null | ISO 8601 timestamp when verified |

`success` means the target was hit, or the signal closed in profit at the end
of its window. `failed` means the stop was hit, or it closed at a loss.

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

Read these two limits before quoting `roi`:

- `success` includes signals that closed in profit without reaching the target. For those, `roi` books the **best** move seen (capped at the target distance), not the closing price, so it overstates them.
- `cumulativeROI` in stats is a plain **sum** of leveraged per-signal percentages. It is not a return anyone could have earned.

For an honest figure use `perSignal.avgNetPct` from stats: per resolved signal, no leverage, after 0.12% fees, valued at the level that filled (target or stop) or else at the close. The public scoreboards on signals.x70.ai use the same rule.

## Confidence

`confidence` is 0–100 in responses. It is the model's own conviction, not a
probability of profit, and it is not calibrated: in our own data, higher
confidence has not meant better results. Signals below 70 are returned too.
Don't rank or size by it alone.

The REST filters `confidenceMin` / `confidenceMax` accept either scale: `0.7`
and `70` mean the same (the server reads values above 1 as percent). The MCP
tool `get_signals` takes them on the 0–1 scale.

## Stats Response

| Field | Type | Description |
|-------|------|-------------|
| `period` | string | e.g. "30d" |
| `totalSignals` | number | Total signals in period |
| `verifiedSignals` | number | Signals with verification outcome |
| `hitRate` | number | Success rate (0-100%). Quote it with `perSignal.avgNetPct`: stops can sit further away than targets |
| `perSignal` | object | `avgNetPct`, `avgWinPct`, `avgLossPct`: average result per resolved signal, no leverage, after 0.12% fees (target or stop when hit, else the close) |
| `avgConfidence` | number | Average confidence (0-100) |
| `cumulativeROI` | number | Plain sum of leveraged per-signal ROIs (%). Not an achievable return |
| `avgLeverage` | number | Average leverage used |
| `byDirection` | object | Breakdown per direction (total, hits, hitRate) |
| `byMonth` | object[] | Hit rate for this month, the two before and all time (the figures on signals.x70.ai) |
