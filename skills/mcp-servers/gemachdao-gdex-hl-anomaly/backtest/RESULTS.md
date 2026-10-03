# Backtest — gemach-hl-anomaly/robust-baseline-v2

## What was tested

- **Events.** Three real HyperLiquid events, each scanned from 14 days before onset to the end
  of the event window.
- **Controls.** The same 20 liquid core markets every time (BTC, ETH, SOL, XRP, DOGE, AVAX,
  LINK, ARB, OP, SUI, APT, INJ, TIA, WIF, kPEPE, BNB, LTC, HYPE, TRUMP, ADA).
- **Bar size.** Liquidity signals use 4h bars everywhere, because 1h candles do not reach back
  to March 2025. JELLY is also run on 1h bars to show what live operation adds.
- **Thresholds.** Calibrated beforehand on control markets over May and August 2025. Those
  windows overlap no event and no event's 14-day run-up (see `../APPROACH.md`). Nothing below
  was used to set a threshold.
- **Reproduce.** `python3 calibrate.py && python3 backtest.py`. Raw output is in
  `results.json`, including every in-window event.

## Detection

| Event | Onset used | First detection | Categories in window |
|---|---|---|---|
| JELLY short-squeeze manipulation | 2025-03-26 12:00 UTC (first 100× volume hour) | **13:00** on 1h bars (liquidity_shock, bar range); 16:00 on 4h bars | liquidity_shock, oracle_divergence |
| POPCAT pump-and-dump | 2025-11-12, premium +2.0% in the 16:00 hour | **16:00** in the same hour (oracle_divergence z = 108, funding_extremity z = 25, liquidity_shock z = 9) | all three |
| 10 Oct 2025 market-wide liquidation cascade | ~21:00 UTC | **22:00**, the first funding hour after the crash, on 12 markets; all 19 by 00:00 | all three |

**Hit rate: 3/3 events.** The 10 Oct crash flagged **19 of 20** control markets. BTC was not
flagged: its worst premium was −0.056%, which is inside its own normal range.

Hours after onset:

- JELLY: 1h after onset on 1h bars, 4h after on 4h bars.
- POPCAT: detected in the same hour as the dislocation. The 4h gap in `results.json` comes from
  the approximate onset of 12:00 entered for the scan, not from a detection lag.
- 10 Oct: about 1h after onset.

## False alarms

These are events on control markets in the 14 days before each event. Every market-day in
these windows was treated as "should be quiet", which is conservative: some of those events
may be real.

| Pre-event window | Market-days | Events | Rate / market-day | By category |
|---|---|---|---|---|
| 2025-03-12 → 03-26 (JELLY) | 280 | 1 | 0.004 | oracle_divergence 1 |
| 2025-09-26 → 10-10 (crash) | 280 | 12 | 0.043 | oracle_divergence 11, liquidity_shock 1 |
| 2025-10-29 → 11-12 (POPCAT) | 280 | 24 | 0.086 | oracle_divergence 16, funding_extremity 7, liquidity_shock 1 |
| **All** | **840** | **37** | **0.044** | |

The calibration target was 0.02 per market-day per category, so about 0.06 in total. The
pooled 0.044 sits under that target, but the late-October window ran higher, at 0.086.

At the scale of all ~180 active core markets, 0.044 per market-day means about **8 events on
a quiet day**.

v1 used a single z ≥ 6 for every category. On the same windows it produced 150, 310 and 273
control events: **0.54–1.1 per market-day**, driven by funding and premium. That is why v2
exists.

## Findings a consumer should know

1. **No lead time.** Nothing fired on JELLY before the 12:00 volume explosion. The detector
   reports anomalies as they happen; it does not forecast them.
2. **The event market's own run-up is noisy.** JELLY produced **84 events on 1h bars** (78 on
   4h) in the 14 days before the attack, during its post-listing pump. POPCAT produced **0**.
   A newly listed coin that is already running looks anomalous, and this model cannot tell
   organic mania from a setup using price and volume alone. Large single-account open interest
   would tell them apart. That is available only live, not historically.
3. **Premium lags volume on a squeeze.** JELLY's premium only crossed at 16:00, four hours
   after the volume did. Its baseline week was volatile (premium −0.38% to +0.97%), so a +0.10%
   premium at 14:00 scored z ≈ 3. Liquidity carried the early detection.
4. **Systemic events flag everything.** On 10 Oct nearly every market fired, so the stream
   alone does not separate "this market" from "the whole market". A cross-sectional feature is
   the next improvement.
5. **Three events is not a recall estimate.** 3/3 shows these three known events are visible to
   the detector. More labelled events are needed before quoting a detection rate.

## Samples

- `../sample/anomaly_sample.ndjson` holds two real records for contract tests:
  - JELLY `liquidity_shock` at 2025-03-26 13:00 (1h bars)
  - POPCAT `funding_extremity` at 2025-11-12 16:00, which carries the premium fields
- `../sample/anomaly_coverage_sample.json` holds the coverage record from the POPCAT run. That
  run emitted 3 events; the sample keeps one of them.
