#!/usr/bin/env python3
"""HyperLiquid anomaly detection — scored, time-stamped events with learned baselines.

Standard library only. For each market it learns a per-market baseline from that market's own
recent history (trailing median and median absolute deviation), then scores each new
observation by how far it sits from that baseline in robust standard deviations. Nothing here
is a fixed market-wide threshold: "unusual" means unusual *for this market, recently*.

Signals (signal_type "anomaly"):
  oracle_divergence    hourly mark-vs-oracle premium far from its learned baseline
  funding_extremity    funding far from baseline, ONLY when premium is outside HyperLiquid's
                       clamp band — inside it, funding is pinned to the interest rate and says
                       nothing. Always emitted with the premium alongside, never alone.
  liquidity_shock      traded volume or bar range far from baseline

Every run also emits ONE coverage record naming the window scanned, the markets covered, and
the markets it could not score (too little history, delisted, no data). Absence of an event
must never be read as "normal" — only as "scanned, nothing crossed the threshold".

Usage:
    hl_anomaly.py                                   # last 24h, all active core markets
    hl_anomaly.py --coins BTC ETH --hours 72
    hl_anomaly.py --start 2025-03-20 --end 2025-03-27 --coins JELLY BTC --interval 1h
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone

MODEL_VERSION = "gemach-hl-anomaly/robust-baseline-v2"
INFO = "https://api.hyperliquid.xyz/info"

BASELINE_HOURS = 168           # learn from the trailing 7 days
MIN_BASELINE_OBS = 72          # below this the market is reported as not scored
FUNDING_WINDOW_H = 8           # funding is scored as an 8h carry cost, not a single print
# MAD floors: a perfectly flat history must not turn a tiny move into an infinite score.
# The funding floor is HyperLiquid's base interest rate (0.01%/8h = 1.25e-5/h): a deviation
# smaller than the rate every position already pays is not "extreme".
FLOOR = {"premium": 5e-5, "funding": 1.25e-5, "log_volume": 0.25, "log_range": 0.025}
# Robust-z thresholds per category, calibrated on control markets over windows that contain
# none of the backtest events (backtest/calibrate.py -> backtest/calibration.json) to a target
# of ~1 event per market per 50 days per category. Never tuned on the events themselves.
Z_THRESHOLD = {"oracle_divergence": 10.24, "funding_extremity": 10.17,
               "liquidity_shock/1h": 6.18, "liquidity_shock/4h": 6.0}
Z_REF = 6.0                    # score() scale; fixed so scores stay comparable across versions
# HyperLiquid funding equals the interest rate while premium sits in roughly this band.
CLAMP_BAND = (-0.0004, 0.0006)


# ---------------------------------------------------------------------------- data

def _post(body: dict, tries: int = 7):
    """POST to the info endpoint. Backs off exponentially (1.5s..~96s) on 429s and transient errors."""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(INFO, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception as exc:  # rate limits and transient errors: back off and retry
            last = exc
            time.sleep(1.5 * 2 ** i)
    raise RuntimeError(f"HyperLiquid info {body.get('type')} failed: {last}")


def funding_history(coin: str, start_ms: int, end_ms: int) -> list[dict]:
    """Hourly funding + premium. Pages past the 500-row response cap."""
    out, cursor = [], start_ms
    while cursor < end_ms:
        page = _post({"type": "fundingHistory", "coin": coin, "startTime": cursor, "endTime": end_ms})
        if not page:
            break
        out.extend(page)
        nxt = page[-1]["time"] + 1
        if nxt <= cursor:
            break
        cursor = nxt
        if len(page) < 500:
            break
    return out


def candles(coin: str, interval: str, start_ms: int, end_ms: int) -> list[dict]:
    return _post({"type": "candleSnapshot", "req": {"coin": coin, "interval": interval,
                                                     "startTime": start_ms, "endTime": end_ms}}) or []


def active_core_markets() -> list[str]:
    meta = _post({"type": "meta"})
    return [u["name"] for u in meta["universe"] if not u.get("isDelisted")]


# ---------------------------------------------------------------------------- model

def robust_z(x: float, history: list[float], floor: float) -> tuple[float, float, float]:
    """(z, median, scale) of x against a learned baseline. Scale is 1.4826*MAD, floored."""
    med = statistics.median(history)
    mad = statistics.median(abs(h - med) for h in history)
    scale = max(1.4826 * mad, floor)
    return (x - med) / scale, med, scale


def score(z: float, threshold: float) -> float:
    """Map |z| to 0..1: 0 at the threshold, rising by 1-e^-1 per Z_REF beyond it. Monotonic, not a probability."""
    return round(1.0 - math.exp(-max(0.0, abs(z) - threshold) / Z_REF), 4)


def _iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _evidence(kind: str, coin: str, t_ms: int, baseline: list[float]) -> str:
    """Reproducible pointer: the public endpoint + a hash of the exact baseline used."""
    h = hashlib.sha256(json.dumps(baseline).encode()).hexdigest()[:16]
    return f"hyperliquid:info/{kind}?coin={coin}&t={t_ms}#baseline-sha256:{h}"


def _stale(rows: list[dict]) -> bool:
    """A delisted market reports exact zeros forever. That is missing data, not calm."""
    return len(rows) >= 3 and all(float(r["premium"]) == 0 and float(r["fundingRate"]) == 0 for r in rows[-3:])


def _live(rows: list[dict]) -> list[dict]:
    """Rows up to the point the market went flat (delisting)."""
    live = []
    for r in rows:
        live.append(r)
        if _stale(live):
            return live[:-3]
    return live


def premium_funding_z(coin: str, rows: list[dict], scan_from_ms: int):
    """Yield (row, premium z, funding z, features, premium baseline, funding baseline) per scored hour.

    Funding is scored as the trailing FUNDING_WINDOW_H-hour mean against a baseline of the same
    rolling means: one hourly print is noise; the carry a position pays over hours is the risk.
    """
    live = _live(rows)
    fmean = []
    for i, r in enumerate(live):
        w = [float(x["fundingRate"]) for x in live[max(0, i - FUNDING_WINDOW_H + 1):i + 1]]
        fmean.append(sum(w) / len(w))
    for i, r in enumerate(live):
        if r["time"] < scan_from_ms:
            continue
        idx = [j for j in range(i) if r["time"] - live[j]["time"] <= BASELINE_HOURS * 3600_000]
        if len(idx) < MIN_BASELINE_OBS:
            continue
        p = float(r["premium"])
        hp = [float(live[j]["premium"]) for j in idx]
        hf = [fmean[j] for j in idx]
        zp, mp, _ = robust_z(p, hp, FLOOR["premium"])
        zf, mf, _ = robust_z(fmean[i], hf, FLOOR["funding"])
        feats = {"premium_pct": p * 100, "funding_hourly_pct": float(r["fundingRate"]) * 100,
                 "funding_8h_mean_hourly_pct": fmean[i] * 100,
                 "premium_baseline_pct": mp * 100, "premium_z": round(zp, 2),
                 "funding_baseline_pct": mf * 100, "funding_z": round(zf, 2)}
        yield r, zp, zf, feats, hp, hf


def detect_premium_funding(coin: str, rows: list[dict], scan_from_ms: int) -> tuple[list[dict], bool]:
    """Returns (events, scored?). rows must include BASELINE_HOURS of history before scan_from."""
    events, scored = [], False
    for r, zp, zf, feats, hp, hf in premium_funding_z(coin, rows, scan_from_ms):
        scored = True
        p = float(r["premium"])
        outside_clamp = not (CLAMP_BAND[0] <= p <= CLAMP_BAND[1])
        if abs(zp) >= Z_THRESHOLD["oracle_divergence"]:
            events.append(_event(coin, "oracle_divergence", r["time"], zp, feats,
                                 _evidence("fundingHistory", coin, r["time"], hp),
                                 metric="premium_pct", source_kind="fundingHistory"))
        if abs(zf) >= Z_THRESHOLD["funding_extremity"] and outside_clamp:
            events.append(_event(coin, "funding_extremity", r["time"], zf, feats,
                                 _evidence("fundingHistory", coin, r["time"], hf),
                                 metric="funding_8h_mean_hourly_pct", source_kind="fundingHistory"))
    return events, scored


def liquidity_z(coin: str, bars: list[dict], interval_h: int, scan_from_ms: int):
    """Yield (bar, close_ms, volume z, range z, features, volume baseline) per scored bar."""
    n_base = max(MIN_BASELINE_OBS // interval_h, 12)
    for i, b in enumerate(bars):
        close_ms = b["t"] + interval_h * 3600_000   # observable once the bar has closed
        if close_ms < scan_from_ms:
            continue
        hist = [x for x in bars[:i] if b["t"] - x["t"] <= BASELINE_HOURS * 3600_000]
        if len(hist) < n_base:
            continue
        lv = math.log1p(float(b["v"]))
        lr = math.log(max(float(b["h"]), 1e-18) / max(float(b["l"]), 1e-18))
        hv = [math.log1p(float(x["v"])) for x in hist]
        hr = [math.log1p(math.log(max(float(x["h"]), 1e-18) / max(float(x["l"]), 1e-18))) for x in hist]
        zv, mv, _ = robust_z(lv, hv, FLOOR["log_volume"])
        zr, mr, _ = robust_z(math.log1p(lr), hr, FLOOR["log_range"])
        feats = {"volume_base": float(b["v"]), "volume_z": round(zv, 2),
                 "volume_baseline_base": math.expm1(mv), "bar_range_pct": lr * 100,
                 "bar_range_baseline_pct": math.expm1(mr) * 100,
                 "range_z": round(zr, 2), "bar_interval_h": interval_h, "bar_start": _iso(b["t"])}
        yield b, close_ms, zv, zr, feats, hv


def detect_liquidity(coin: str, bars: list[dict], interval_h: int, scan_from_ms: int) -> tuple[list[dict], bool]:
    events, scored = [], False
    thr = Z_THRESHOLD[f"liquidity_shock/{interval_h}h"]
    for b, close_ms, zv, zr, feats, hv in liquidity_z(coin, bars, interval_h, scan_from_ms):
        scored = True
        # Only spikes: a volume collapse on a quiet night is not a liquidity shock.
        if max(zv, zr) >= thr:
            events.append(_event(coin, "liquidity_shock", close_ms, max(zv, zr), feats,
                                 _evidence(f"candleSnapshot/{interval_h}h", coin, b["t"], hv),
                                 threshold=thr, metric="volume_base" if zv >= zr else "bar_range_pct",
                                 source_kind=f"candleSnapshot/{interval_h}h"))
    return events, scored


# observed metric -> the feature holding its learned baseline (the model's expectation)
EXPECTED = {"premium_pct": "premium_baseline_pct",
            "funding_8h_mean_hourly_pct": "funding_baseline_pct",
            "volume_base": "volume_baseline_base",
            "bar_range_pct": "bar_range_baseline_pct"}


def _event(coin, category, t_ms, z, features, evidence, metric, source_kind, threshold=None):
    """One event in the downstream contract's anomaly shape (15 columns), plus model features.

    `confidence` is deliberately absent: the score ranks events against a calibrated threshold
    and is not a probability, so there is no honest 0-1 confidence to report.
    """
    threshold = Z_THRESHOLD[category] if threshold is None else threshold
    t_s = t_ms // 1000
    entity = f"hl-{coin}"
    observed, expected = features[metric], features[EXPECTED[metric]]
    return {
        "signal_type": "anomaly", "source": "gemach",
        "anomaly_id": hashlib.sha256(f"{entity}|{category}|{t_s}|{source_kind}".encode()).hexdigest()[:32],
        "entity_id": entity, "entity_type": "market", "chain": "hyperliquid", "symbol": coin,
        "anomaly_category": category,
        "anomaly_score": round(100 * score(z, threshold), 2),
        "detection_method": "statistical",
        "model_version": MODEL_VERSION,
        "baseline_window": f"{BASELINE_HOURS // 24}d",
        "observed_metric": metric, "observed_value": observed, "expected_value": expected,
        "detected_at": t_s, "detected_at_utc": _iso(t_ms),
        "evidence_ref": evidence,
        "summary": (f"{coin} {category.replace('_', ' ')}: {metric} {observed:.4g} vs baseline "
                    f"{expected:.4g} (robust z {z:+.1f}, threshold {threshold})"),
        "z": round(z, 2), "z_threshold": threshold, **features}


def run(coins: list[str], start: datetime, end: datetime, interval: str = "1h") -> list[dict]:
    interval_h = int(interval.rstrip("h"))
    s_ms, e_ms = int(start.timestamp() * 1000), int(end.timestamp() * 1000)
    fetch_from = s_ms - (BASELINE_HOURS + 24) * 3600_000
    events, covered, unscored = [], [], []
    for coin in coins:
        pf, s1 = detect_premium_funding(coin, [r for r in funding_history(coin, fetch_from, e_ms)], s_ms)
        lq, s2 = detect_liquidity(coin, [b for b in candles(coin, interval, fetch_from, e_ms) if b["t"] < e_ms],
                                  interval_h, s_ms)
        events += [x for x in pf + lq if x["detected_at"] <= e_ms // 1000]
        (covered if (s1 or s2) else unscored).append(coin)
    events.sort(key=lambda x: (x["detected_at"], x["entity_id"], x["anomaly_category"], x["anomaly_id"]))
    coverage = {"signal_type": "anomaly_coverage", "source": "gemach", "model_version": MODEL_VERSION,
                "detector_window_start": _iso(s_ms), "detector_window_end": _iso(e_ms), "bar_interval_h": interval_h,
                "markets_scored": len(covered), "markets_not_scored": sorted(unscored),
                "events": len(events),
                "note": "Only markets in markets_scored were evaluated. No event for a scored market means "
                        "nothing crossed the threshold in this window - not that the market was normal."}
    return events + [coverage]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--coins", nargs="*", help="markets (default: all active core markets)")
    ap.add_argument("--hours", type=int, default=24, help="scan the last N hours (ignored with --start)")
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--interval", default="1h", choices=["1h", "4h"],
                    help="bar size for liquidity signals; 1h reaches back ~7 months, 4h ~2 years")
    a = ap.parse_args(argv)
    end = (datetime.fromisoformat(a.end).replace(tzinfo=timezone.utc) if a.end
           else datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0))
    start = (datetime.fromisoformat(a.start).replace(tzinfo=timezone.utc) if a.start
             else end - timedelta(hours=a.hours))
    coins = a.coins or active_core_markets()
    for rec in run(coins, start, end, a.interval):
        sys.stdout.write(json.dumps(rec, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
