#!/usr/bin/env python3
"""Backtest of hl_anomaly over three known real HyperLiquid events.

The detector's parameters were fixed before this was written (see scripts/hl_anomaly.py) and are
not tuned here. For each event we scan the 14 days before it plus the event itself, across the
event market and a set of liquid control markets, and report:

  hit            did the detector flag the event market (or, for the market-wide event, how
                 many markets) inside the event window, and how soon
  run-up         events on the event market in the 14 days BEFORE the event window
  false alarms   events on control markets in the pre-event period, per market-day

4h bars are used for liquidity signals throughout: 1h candles only reach back ~7 months, and
mixing resolutions across markets would make the false-alarm rate incomparable. JELLY is also
run at 1h (its candles survive delisting) to show what live 1h operation adds.
"""
from __future__ import annotations

import collections
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import hl_anomaly as H  # noqa: E402

UTC = timezone.utc
T = lambda s: datetime.fromisoformat(s).replace(tzinfo=UTC)

EVENTS = [
    {"name": "JELLY manipulation", "kind": "single", "market": "JELLY",
     "onset": T("2025-03-26T12:00"), "window_end": T("2025-03-26T18:00"),
     "controls": ["BTC", "ETH", "SOL", "XRP", "DOGE", "AVAX", "LINK", "ARB", "OP", "SUI",
                  "APT", "INJ", "TIA", "WIF", "kPEPE", "BNB", "LTC", "HYPE", "TRUMP", "ADA"]},
    {"name": "POPCAT manipulation", "kind": "single", "market": "POPCAT",
     "onset": T("2025-11-12T12:00"), "window_end": T("2025-11-13T06:00"),
     "controls": ["BTC", "ETH", "SOL", "XRP", "DOGE", "AVAX", "LINK", "ARB", "OP", "SUI",
                  "APT", "INJ", "TIA", "WIF", "kPEPE", "BNB", "LTC", "HYPE", "TRUMP", "ADA"]},
    {"name": "10 Oct 2025 market-wide crash", "kind": "market", "market": None,
     "onset": T("2025-10-10T20:00"), "window_end": T("2025-10-11T04:00"),
     "controls": ["BTC", "ETH", "SOL", "XRP", "DOGE", "AVAX", "LINK", "ARB", "OP", "SUI",
                  "APT", "INJ", "TIA", "WIF", "kPEPE", "BNB", "LTC", "HYPE", "TRUMP", "ADA"]},
]
PRE_DAYS = 14


def scan(markets, start, end, interval):
    recs = H.run(markets, start, end, interval)
    return [r for r in recs if r["signal_type"] == "anomaly"], recs[-1]


def evaluate(ev, interval="4h"):
    start = ev["onset"] - timedelta(days=PRE_DAYS)
    markets = ([ev["market"]] if ev["market"] else []) + ev["controls"]
    events, cov = scan(markets, start, ev["window_end"], interval)
    on, end = ev["onset"].strftime("%Y-%m-%dT%H:%M:%SZ"), ev["window_end"].strftime("%Y-%m-%dT%H:%M:%SZ")
    in_win = [e for e in events if on <= e["detected_at_utc"] <= end]
    pre = [e for e in events if e["detected_at_utc"] < on]
    scored = cov["markets_scored"]
    out = {"event": ev["name"], "interval": interval, "scan_start": start.isoformat(),
           "onset": on, "window_end": end, "markets_scored": scored,
           "markets_not_scored": cov["markets_not_scored"]}
    if ev["kind"] == "single":
        m = f"hl-{ev['market']}"
        hits = sorted((e for e in in_win if e["entity_id"] == m), key=lambda e: e["detected_at_utc"])
        out["hit"] = bool(hits)
        if hits:
            first = hits[0]
            lag = (T(first["detected_at_utc"][:16]) - ev["onset"]).total_seconds() / 3600
            out["first_detection"] = {"at": first["detected_at_utc"], "hours_after_onset": lag,
                                      "category": first["anomaly_category"], "anomaly_score": first["anomaly_score"]}
            out["categories_in_window"] = sorted({e["anomaly_category"] for e in hits})
        out["runup_events_on_market"] = [
            {"at": e["detected_at_utc"], "category": e["anomaly_category"], "z": e["z"]}
            for e in pre if e["entity_id"] == m]
        controls_pre = [e for e in pre if e["entity_id"] != m]
        n_controls = scored - (1 if m.split("-", 1)[1] not in cov["markets_not_scored"] else 0)
        # controls that also fired inside the event window (possible contagion or noise)
        out["controls_firing_in_window"] = sorted({e["symbol"] for e in in_win if e["entity_id"] != m})
    else:
        fired = sorted({e["symbol"] for e in in_win})
        out["markets_flagged_in_window"] = f"{len(fired)}/{scored}"
        out["flagged"] = fired
        controls_pre = pre
        n_controls = scored
    days = PRE_DAYS * max(n_controls, 1)
    out["false_alarm_rate_per_market_day"] = round(len(controls_pre) / days, 4)
    out["false_alarms_by_category"] = dict(collections.Counter(e["anomaly_category"] for e in controls_pre))
    out["false_alarms_total"] = len(controls_pre)
    out["market_days_observed"] = days
    out["in_window_events"] = [
        {k: e[k] for k in ("detected_at_utc", "symbol", "anomaly_category", "z", "anomaly_score")} for e in in_win]
    if ev["kind"] == "market":
        first = {}
        for e in sorted(in_win, key=lambda e: e["detected_at_utc"]):
            first.setdefault(e["symbol"], e["detected_at_utc"])
        out["first_detection_by_market"] = first
    return out, in_win


def main():
    results = []
    for ev in EVENTS:
        r, _ = evaluate(ev, "4h")
        results.append(r)
        print(json.dumps(r, indent=1), flush=True)
    jelly_1h, _ = evaluate({**EVENTS[0], "controls": []}, "1h")
    results.append(jelly_1h)
    print(json.dumps(jelly_1h, indent=1))
    Path(__file__).with_name("results.json").write_text(json.dumps(results, indent=1) + "\n")


if __name__ == "__main__":
    main()
