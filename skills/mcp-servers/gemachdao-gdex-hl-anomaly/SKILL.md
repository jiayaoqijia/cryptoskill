---
name: gdex-hl-anomaly
description: Scored, time-stamped anomaly events for HyperLiquid perps (oracle divergence, funding extremity, liquidity shock) against per-market learned baselines, with coverage records
---

# GDEX: HyperLiquid Anomaly Events

Detects unusual behaviour on the HyperLiquid perpetual markets that GDEX trades, and emits it as
**events** (NDJSON, one record per event), not alerts. Each event says what was unusual, when it
happened, how unusual it was against that market's own recent history, and where to re-derive it.

Standard library only — no API key, no Gemach infrastructure. Reads the public HyperLiquid
`info` endpoint directly.

## When to Use

- Building a risk feed that needs market anomalies with an event time and a score
- Screening HyperLiquid markets for manipulation, oracle stress or liquidity shocks
- Backfilling anomaly history for a window (1h bars reach ~7 months back, 4h ~2 years)

## Run

```bash
python3 scripts/hl_anomaly.py                                   # last 24h, every active core market
python3 scripts/hl_anomaly.py --coins BTC ETH SOL --hours 72
python3 scripts/hl_anomaly.py --start 2025-03-20 --end 2025-03-27 --coins JELLY --interval 1h
```

Output is NDJSON: zero or more `signal_type: "anomaly"` records, then exactly **one**
`signal_type: "anomaly_coverage"` record.

## Categories

| `anomaly_category` | Fires when | Source |
|---|---|---|
| `oracle_divergence` | hourly mark-vs-oracle premium is far from the market's baseline | `fundingHistory` |
| `funding_extremity` | 8h mean funding is far from baseline **and** premium is outside HyperLiquid's clamp band (inside it funding is pinned to the interest rate and carries no information). Always carries the premium fields. | `fundingHistory` |
| `liquidity_shock` | bar volume or bar range spikes far above baseline (spikes only) | `candleSnapshot` |

`large_outflow`, `governance_concentration` and `security_flag_change` are part of the contract
enum but are not produced by this skill (they need on-chain or token-security sources).

## Event record

Each event carries the 15-column anomaly contract shape, plus the model's own features.

| Field | Meaning |
|---|---|
| `anomaly_id` | stable id: sha256 of entity, category, event time and data source (first 32 hex). Re-running the same window gives the same id |
| `entity_id` | `hl-<coin>`, same key as the `hl_markets` feed |
| `entity_type` | `market` (a perpetual market) |
| `chain` | `hyperliquid` |
| `anomaly_category` | `oracle_divergence`, `funding_extremity` or `liquidity_shock` |
| `anomaly_score` | 0–100. It is 0 at the calibrated threshold and rises monotonically above it. A ranking, **not a probability** |
| `confidence` | **not emitted.** Nothing in the model is a calibrated probability, and the field is left out rather than faked |
| `detection_method` | `statistical`: robust z against a learned per-market baseline |
| `model_version` | changes whenever thresholds or features change |
| `baseline_window` | `7d` |
| `observed_metric` | the quantity that fired: `premium_pct`, `funding_8h_mean_hourly_pct`, `volume_base` or `bar_range_pct` |
| `observed_value`, `expected_value` | that quantity, and its baseline median (the model's expectation) |
| `detected_at` | epoch seconds when the anomaly **happened** (the funding hour, or the bar close), not when the job ran. `detected_at_utc` gives the same instant in ISO-8601 |
| `evidence_ref` | the public endpoint, coin, time, and a sha256 of the exact baseline used |
| `summary` | one-line description |
| `z`, `z_threshold`, feature fields | the robust z and the threshold it crossed; premium/funding or volume/range values and their baselines |

## Coverage record — read this before trusting an empty result

Every run states `detector_window_start`, `detector_window_end`, `markets_scored` and `markets_not_scored`
(too little history, delisted, or no data). **No event for a scored market means nothing
crossed a threshold in that window; it does not mean the market was normal.** Markets in
`markets_not_scored` were not evaluated at all.

## Method and evidence

- `APPROACH.md` — the model, why each choice was made, and its known limits
- `backtest/RESULTS.md` — hit rate and false-alarm rate on three real events
- `backtest/calibrate.py`, `backtest/backtest.py` — reproduce both
- `sample/anomaly_sample.ndjson` — records for contract tests
