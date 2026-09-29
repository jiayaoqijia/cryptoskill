#!/usr/bin/env python3
"""Turn a trade idea into exact, exchange-valid numbers.

The Trader and Portfolio Manager use this so stops, targets, reward/risk and
position size are computed rather than guessed. Prices are rounded to valid
ticks (IDX fraksi harga) and sizes to whole lots (IDX: 1 lot = 100 shares).

Examples:
  # ATR-based stop, targets at 1.5R and 3R
  python risk_tools.py --ticker BBCA.JK --entry 9800 --atr 160 --stop-atr 2 --targets-r 1.5,3

  # explicit stop and targets, plus sizing for a Rp100 jt account risking 1%
  python risk_tools.py --ticker BBCA.JK --entry 9800 --stop 9300 --targets 10500,11200 \
      --equity 100000000 --risk-pct 1 --max-position-pct 25

  # short idea on a US stock
  python risk_tools.py --ticker AAPL --side short --entry 210 --stop 222 --targets 190
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import detect_market, lot_size, round_to_tick  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--side", choices=["long", "short"], default="long")
    ap.add_argument("--entry", type=float, required=True)
    ap.add_argument("--stop", type=float)
    ap.add_argument("--atr", type=float, help="ATR14 from technical.json")
    ap.add_argument("--stop-atr", type=float, default=2.0, help="stop distance in ATRs if --stop not given")
    ap.add_argument("--targets", help="comma-separated explicit targets")
    ap.add_argument("--targets-r", default="1.5,3", help="targets as R multiples if --targets not given")
    ap.add_argument("--equity", type=float, help="account size in the instrument's currency")
    ap.add_argument("--risk-pct", type=float, default=1.0, help="%% of equity risked at the stop")
    ap.add_argument("--max-position-pct", type=float, default=25.0, help="cap on position value as %% of equity")
    a = ap.parse_args()

    mkt = detect_market(a.ticker)["market"]
    sign = 1 if a.side == "long" else -1
    entry = round_to_tick(a.entry, mkt)

    if a.stop is not None:
        stop = a.stop
    elif a.atr:
        stop = entry - sign * a.stop_atr * a.atr
    else:
        sys.exit("Provide --stop or --atr.")
    stop = round_to_tick(stop, mkt, "down" if a.side == "long" else "up")
    risk_ps = (entry - stop) * sign
    if risk_ps <= 0:
        sys.exit("Stop is on the wrong side of entry.")

    if a.targets:
        raw_targets = [float(x) for x in a.targets.split(",") if x.strip()]
    else:
        raw_targets = [entry + sign * float(r) * risk_ps for r in a.targets_r.split(",") if r.strip()]
    targets = []
    for t in raw_targets:
        tt = round_to_tick(t, mkt, "down" if a.side == "long" else "up")
        reward = (tt - entry) * sign
        targets.append({"price": tt, "move_pct": round((tt / entry - 1) * 100, 2),
                        "reward_to_risk": round(reward / risk_ps, 2)})

    out = {
        "ticker": a.ticker, "market": mkt, "side": a.side, "entry": entry, "stop": stop,
        "stop_distance_pct": round((stop / entry - 1) * 100, 2), "risk_per_share": round(risk_ps, 6),
        "targets": targets,
    }
    if a.atr:
        out["stop_distance_in_atr"] = round(risk_ps / a.atr, 2)

    if a.equity:
        lot = lot_size(mkt)
        risk_budget = a.equity * a.risk_pct / 100
        shares = math.floor(risk_budget / risk_ps / lot) * lot
        cap_shares = math.floor(a.equity * a.max_position_pct / 100 / entry / lot) * lot
        capped = shares > cap_shares
        shares = min(shares, cap_shares)
        out["sizing"] = {
            "equity": a.equity, "risk_pct": a.risk_pct, "risk_budget": round(risk_budget, 2),
            "units": shares, "lots": shares // lot if lot > 1 else None,
            "position_value": round(shares * entry, 2),
            "position_pct_of_equity": round(shares * entry / a.equity * 100, 2),
            "money_at_risk": round(shares * risk_ps, 2),
            "capped_by_max_position": capped,
        }
        if shares == 0:
            out["sizing"]["note"] = "Risk budget too small for one lot/unit at this stop distance."
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
