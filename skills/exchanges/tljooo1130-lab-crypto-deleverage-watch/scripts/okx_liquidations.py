#!/usr/bin/env python3
"""Bucket OKX filled SWAP liquidation orders by hour (local tz).

Uses the public endpoint:
  GET https://www.okx.com/api/v5/public/liquidation-orders
  params: instType=SWAP, uly={CCY}-USDT, state=filled, limit=100, after=<ts>

Contract value (sz multiplier): BTC-USDT-SWAP 0.01 BTC, ETH-USDT-SWAP 0.1 ETH.
USD notional ~= sz * contract_value * bkPx.

Binance allForceOrders is not a public endpoint and is not used here.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sys
import time

import requests

OKX_LIQ = "https://www.okx.com/api/v5/public/liquidation-orders"
DEFAULT_CTVAL = {"BTC": 0.01, "ETH": 0.1}


def side_of(row: dict) -> str:
    ps = row.get("posSide", "")
    if ps == "long":
        return "long"
    if ps == "short":
        return "short"
    # net mode: a sell-side fill liquidates a long
    if ps == "net" and row.get("side") == "sell":
        return "long"
    return "short"


def fetch_filled(ccy: str, start_ms: int, session: requests.Session, max_pages: int = 300) -> tuple[list, int]:
    recs: list = []
    after = None
    pages = 0
    while pages < max_pages:
        params = {
            "instType": "SWAP",
            "uly": f"{ccy}-USDT",
            "state": "filled",
            "limit": 100,
        }
        if after:
            params["after"] = after
        payload = session.get(OKX_LIQ, params=params, timeout=25).json()
        if payload.get("code") != "0":
            raise RuntimeError(f"OKX liquidation-orders {ccy}: code={payload.get('code')} msg={payload.get('msg')}")
        data = payload.get("data") or []
        if not data or not data[0].get("details"):
            break
        details = data[0]["details"]
        recs.extend(details)
        after = details[-1]["ts"]
        pages += 1
        if int(after) < start_ms:
            break
        time.sleep(0.15)
    recs = [x for x in recs if int(x["ts"]) >= start_ms]
    return recs, pages


def summarize(ccy: str, recs: list, ctval: float, tz: dt.tzinfo) -> dict:
    hours = collections.defaultdict(lambda: {"n_long": 0, "usd_long": 0.0, "n_short": 0, "usd_short": 0.0})
    totals = {
        "long": {"n": 0, "usd": 0.0},
        "short": {"n": 0, "usd": 0.0},
        "big_long_100k": {"n": 0, "usd": 0.0},
        "big_short_100k": {"n": 0, "usd": 0.0},
    }
    for row in recs:
        usd = float(row["sz"]) * ctval * float(row["bkPx"])
        hour = dt.datetime.fromtimestamp(int(row["ts"]) / 1000, tz).hour
        side = side_of(row)
        if side == "long":
            hours[hour]["n_long"] += 1
            hours[hour]["usd_long"] += usd
            totals["long"]["n"] += 1
            totals["long"]["usd"] += usd
            if usd >= 100_000:
                totals["big_long_100k"]["n"] += 1
                totals["big_long_100k"]["usd"] += usd
        else:
            hours[hour]["n_short"] += 1
            hours[hour]["usd_short"] += usd
            totals["short"]["n"] += 1
            totals["short"]["usd"] += usd
            if usd >= 100_000:
                totals["big_short_100k"]["n"] += 1
                totals["big_short_100k"]["usd"] += usd

    def round_tot(d):
        return {"n": d["n"], "usd": round(d["usd"], 2)}

    hourly = []
    for h in sorted(hours):
        row = hours[h]
        hourly.append({
            "hour": h,
            "n_long": row["n_long"],
            "usd_long": round(row["usd_long"], 2),
            "n_short": row["n_short"],
            "usd_short": round(row["usd_short"], 2),
        })
    earliest = None
    latest = None
    if recs:
        earliest = dt.datetime.fromtimestamp(min(int(x["ts"]) for x in recs) / 1000, tz).isoformat(timespec="seconds")
        latest = dt.datetime.fromtimestamp(max(int(x["ts"]) for x in recs) / 1000, tz).isoformat(timespec="seconds")
    return {
        "ccy": ccy,
        "records": len(recs),
        "earliest": earliest,
        "latest": latest,
        "totals": {k: round_tot(v) for k, v in totals.items()},
        "hourly": hourly,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Hourly buckets of OKX filled SWAP liquidations")
    p.add_argument("--coins", default="BTC,ETH", help="Comma-separated coins, default BTC,ETH")
    p.add_argument("--tz", default="Asia/Bangkok")
    p.add_argument("--start", default=None, help="Window start, YYYY-MM-DD or ISO datetime in --tz (default: today 00:00)")
    p.add_argument("--json", action="store_true", dest="as_json")
    args = p.parse_args(argv)

    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo(args.tz)
    except Exception:
        tz = dt.timezone(dt.timedelta(hours=7))

    now = dt.datetime.now(tz)
    if args.start:
        raw = args.start.strip()
        if len(raw) == 10:
            start = dt.datetime.fromisoformat(raw).replace(tzinfo=tz)
        else:
            start = dt.datetime.fromisoformat(raw)
            if start.tzinfo is None:
                start = start.replace(tzinfo=tz)
    else:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_ms = int(start.timestamp() * 1000)

    session = requests.Session()
    session.headers.update({"User-Agent": "crypto-deleverage-watch/1.0"})
    coins = [c.strip().upper() for c in args.coins.split(",") if c.strip()]
    out = {"start": start.isoformat(timespec="seconds"), "tz": args.tz, "coins": {}}
    for ccy in coins:
        recs, pages = fetch_filled(ccy, start_ms, session)
        summary = summarize(ccy, recs, DEFAULT_CTVAL.get(ccy, 1.0), tz)
        summary["pages"] = pages
        out["coins"][ccy] = summary
        if not args.as_json:
            tot = summary["totals"]
            print(f"{ccy} records={summary['records']} pages={pages} earliest={summary['earliest']}")
            print(f"  long {tot['long']['n']} ${tot['long']['usd']:.0f} | short {tot['short']['n']} ${tot['short']['usd']:.0f}")
            for row in summary["hourly"]:
                print(
                    f"  {row['hour']:02d}h L {row['n_long']} {row['usd_long']/1e3:.0f}k "
                    f"| S {row['n_short']} {row['usd_short']/1e3:.0f}k"
                )
    if args.as_json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
