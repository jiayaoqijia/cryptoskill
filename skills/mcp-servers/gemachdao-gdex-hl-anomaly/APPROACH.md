# Approach — HyperLiquid anomaly events

## What is being detected

Three things a risk consumer cares about on a perpetual market, each from public HyperLiquid data:

1. **Oracle divergence.** The mark trades away from the oracle. HyperLiquid publishes the
   hourly `premium` directly. That is the basis a liquidation engine and every open position
   are exposed to.
2. **Funding extremity.** The carry cost positions pay becomes extreme. HyperLiquid funding is
   `premium + clamp(interest − premium, ±0.05%)`, so while the premium sits in roughly
   [−0.04%, +0.06%] funding is pinned to the interest rate and says nothing. We only score
   funding outside that band, and we always ship the premium with it.
3. **Liquidity shock.** Traded volume or the high/low range of a bar spikes.

## The model: a learned baseline for each market

For every market and every feature, the baseline is that market's own trailing 7 days
(168 hours). It uses the **median** and the **median absolute deviation (MAD)**, not the mean
and standard deviation. A single past spike cannot inflate the baseline and hide the next one.

    z = (x − median(history)) / max(1.4826 · MAD(history), floor)

- 1.4826 · MAD matches one standard deviation on normal data, so z reads like a familiar z-score.
- The **floor** stops a perfectly flat history from turning a trivial move into an infinite z:
  - premium: 0.005%
  - funding: the base interest rate, 0.00125%/h. A move smaller than what every position
    already pays is not extreme.
  - log-volume: 0.25
  - log-range: 0.025
- Volume and range are scored in logs because they are multiplicative.
- Funding is scored as a trailing **8-hour mean** against a baseline of the same 8-hour means.
  A single hourly print is noisy; the carry over several hours is what hurts.
- A market with fewer than 72 hourly observations of history is **not scored**, and the
  coverage record says so. It is never reported as calm.
- A delisted market reports exact zeros forever. Three trailing zero rows are treated as
  missing data, not as calm.

"Unusual" therefore always means **unusual for this market, recently**. BTC and a new memecoin
are held to their own histories, not to one shared threshold.

## Thresholds and how they were chosen

v1 used a single a-priori threshold of z ≥ 6 for everything. The backtest showed that this was
fine for liquidity but far too loose for premium and funding: alt-perp premiums are heavy-tailed,
and pinned funding collapses the funding MAD. On control markets v1 produced 0.54–1.1 false
alarms per market-day.

v2 calibrates one threshold per category **on control markets only**:

- Markets: 20 liquid core markets.
- Windows: May 2025 and August 2025 for premium, funding and 4h bars; August 2026 for 1h bars.
- Separation from the events: none of these windows overlaps any backtest event or the 14 days
  before it.
- Target rate: at most **0.02 events per market-day per category**, about one per market every
  50 days.
- Minimum: no threshold goes below the a-priori 6.0.

| Category | Threshold (robust z) | Fire rate at z = 6 in calibration |
|---|---|---|
| oracle_divergence | 10.24 | 0.274 / market-day |
| funding_extremity | 10.17 | 0.165 / market-day |
| liquidity_shock (4h bars) | 6.00 | 0.002 / market-day |
| liquidity_shock (1h bars) | 6.18 | 0.022 / market-day |

`backtest/calibrate.py` reproduces these into `backtest/calibration.json`. The events were never
used to set a threshold.

## Scores

`anomaly_score = 100 · (1 − exp(−(|z| − threshold) / 6))`.

- 0 exactly at the threshold.
- 63 at 6 z past it, 86 at 12 z past it.
- Monotonic, so it ranks events. It is **not a probability**, and it is not calibrated to one.

That is why the record has no `confidence` field. A 0–1 confidence would need a calibrated
probability that an event is real. With three labelled events there is nothing to calibrate
against, so the field is left out rather than filled with a number that looks like one.

## Events, not alerts

- Every threshold crossing is emitted as an event with its z and `anomaly_score`. The consumer decides
  what to alert on.
- `detected_at` is when the anomaly happened: the funding hour, or the close of the bar,
  because a bar is only observable once closed. It is never the time the job ran.
- Every run ends with one coverage record naming the window and exactly which markets were and
  were not scored.
- `evidence_ref` pins the public endpoint, the coin, the timestamp and a sha256 of the exact
  baseline series, so anyone can recompute the z.

## Known limits

- **Detection follows onset; it does not predict it.** The features are observable only once
  the move is under way. On JELLY the first 1h detection came one bar after onset. Nothing fired
  on JELLY in the hours before onset.
- **A pumping new listing is noisy.** JELLY fired 84 times on 1h bars in the 14 days before the
  attack, during its own post-listing pump. The model cannot tell a manipulation from an organic
  mania using price and volume alone. Position concentration (large single-account open
  interest) would be the discriminating feature. It is not in public history, only as a live
  snapshot.
- **Market-wide events flag every market.** Every baseline is per market, so a crash that moves
  everything fires on nearly everything. A cross-sectional feature (this market versus the
  median market) would separate idiosyncratic events from systemic ones. It is not built yet.
- **Backfill depth.** 1h candles reach ~7 months back and 4h candles ~2 years.
  Premium/funding history is hourly and deeper.
- **Scope.** Only core HyperLiquid perps. Builder-deployed DEX markets (equities, FX,
  commodities) are held out, as in the `hl_markets` feed.
- **Three events is a small test.** The hit rate is 3/3 on known events. That shows the detector
  sees them; it does not establish a recall figure.
