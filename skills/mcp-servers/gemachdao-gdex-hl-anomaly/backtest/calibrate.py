#!/usr/bin/env python3
"""Calibrate per-category z thresholds on control markets, away from every backtest event.

For each category we collect the detector's z-scores over the calibration windows and choose
the smallest threshold (never below the a-priori 6.0) at which the category fires at most
TARGET_RATE times per market-day. The events in backtest.py are not in these windows, and
neither are their 14-day run-ups, so the thresholds cannot have been fitted to them.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import hl_anomaly as H  # noqa: E402

UTC = timezone.utc
CONTROLS = ["BTC", "ETH", "SOL", "XRP", "DOGE", "AVAX", "LINK", "ARB", "OP", "SUI",
            "APT", "INJ", "TIA", "WIF", "kPEPE", "BNB", "LTC", "HYPE", "TRUMP", "ADA"]
# Event windows (with run-ups) are 2025-03-12..03-26, 2025-09-26..10-11, 2025-10-29..11-13.
WINDOWS = [("2025-05-01", "2025-05-31"), ("2025-08-01", "2025-08-31")]
WINDOW_1H = [("2026-08-01", "2026-08-31")]   # 1h candles only reach back ~7 months
TARGET_RATE = 0.02                            # events per market-day per category
FLOOR_Z = 6.0


def ms(d):
    return int(datetime.fromisoformat(d).replace(tzinfo=UTC).timestamp() * 1000)


def pick(zs: list[float], market_days: float) -> float:
    allowed = int(TARGET_RATE * market_days)
    zs = sorted((abs(z) for z in zs), reverse=True)
    t = zs[allowed] + 0.01 if len(zs) > allowed else FLOOR_Z
    return round(max(FLOOR_Z, t), 2)


def collect(windows, interval_h, want_pf):
    prem, fund, liq, days = [], [], [], 0.0
    for a, b in windows:
        s, e = ms(a), ms(b)
        fetch = s - (H.BASELINE_HOURS + 24) * 3600_000
        for c in CONTROLS:
            if want_pf:
                for r, zp, zf, *_ in H.premium_funding_z(c, H.funding_history(c, fetch, e), s):
                    prem.append(zp)
                    p = float(r["premium"])
                    if not (H.CLAMP_BAND[0] <= p <= H.CLAMP_BAND[1]):
                        fund.append(zf)
            bars = [x for x in H.candles(c, f"{interval_h}h", fetch, e) if x["t"] < e]
            got = False
            for _b, _c, zv, zr, *_ in H.liquidity_z(c, bars, interval_h, s):
                liq.append(max(zv, zr, 0.0)); got = True
            if got:
                days += (e - s) / 86_400_000
            print(f"  {a} {interval_h}h {c}", file=sys.stderr, flush=True)
    return prem, fund, liq, days


def main():
    prem, fund, liq4, days = collect(WINDOWS, 4, True)
    _, _, liq1, days1 = collect(WINDOW_1H, 1, False)
    out = {
        "target_events_per_market_day": TARGET_RATE, "controls": CONTROLS,
        "windows": WINDOWS, "windows_1h": WINDOW_1H, "market_days": days, "market_days_1h": days1,
        "thresholds": {
            "oracle_divergence": pick(prem, days),
            "funding_extremity": pick(fund, days),
            "liquidity_shock/4h": pick(liq4, days),
            "liquidity_shock/1h": pick(liq1, days1),
        },
        "rate_at_6": {
            "oracle_divergence": round(sum(abs(z) >= 6 for z in prem) / days, 4),
            "funding_extremity": round(sum(abs(z) >= 6 for z in fund) / days, 4),
            "liquidity_shock/4h": round(sum(z >= 6 for z in liq4) / days, 4),
            "liquidity_shock/1h": round(sum(z >= 6 for z in liq1) / days1, 4),
        },
    }
    Path(__file__).with_name("calibration.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
