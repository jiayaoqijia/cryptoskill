#!/usr/bin/env python3
"""Decision memory, modelled on TradingAgents' decision log.

Each finished analysis is appended as one JSON line. On the next analysis of
the same ticker, `review` scores the earlier calls against the current price so
the Portfolio Manager can learn from what worked and what didn't.

Log path: --log, else $TRADING_AGENTS_LOG, else ./trading_agents_log.jsonl

  python decision_log.py add --ticker BBCA.JK --date 2026-09-29 --rating Overweight \
      --price 9800 --confidence medium --horizon "1-3 months" --stop 9450 --target 10850 \
      --thesis "Loan growth re-accelerating; valuation back to 5y average"
  python decision_log.py review --ticker BBCA.JK --price 10150 --date 2026-11-02 \
      [--bench-then 7100 --bench-now 7350]
  python decision_log.py lesson --id 3 --text "Ignored foreign outflow signal; weigh it more."
  python decision_log.py list
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import date

DIRECTION = {"buy": 1, "overweight": 1, "hold": 0, "underweight": -1, "sell": -1}


def path_of(a) -> str:
    return a.log or os.environ.get("TRADING_AGENTS_LOG") or "trading_agents_log.jsonl"


def load(p: str) -> list:
    if not os.path.exists(p):
        return []
    with open(p) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def save(p: str, rows: list):
    with open(p, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def verdict(rating: str, ret: float) -> str:
    d = DIRECTION.get(rating.lower().strip(), 0)
    if d == 0:
        return "HOLD held up (move < 5%)" if abs(ret) < 5 else f"HOLD missed a {ret:+.1f}% move"
    right = (d > 0 and ret > 0) or (d < 0 and ret < 0)
    return "direction right" if right else "direction wrong"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ad = sub.add_parser("add")
    for f in ("ticker", "rating", "thesis"):
        ad.add_argument(f"--{f}", required=True)
    ad.add_argument("--date", default=date.today().isoformat())
    ad.add_argument("--price", type=float, required=True)
    ad.add_argument("--confidence", default="medium")
    ad.add_argument("--horizon", default="")
    ad.add_argument("--stop", type=float)
    ad.add_argument("--target", type=float)
    ad.add_argument("--bench-price", type=float, help="benchmark level at decision time")
    rv = sub.add_parser("review")
    rv.add_argument("--ticker", required=True)
    rv.add_argument("--price", type=float, help="current price of the ticker")
    rv.add_argument("--date", default=date.today().isoformat())
    rv.add_argument("--bench-now", type=float, help="current benchmark level (for alpha)")
    rv.add_argument("--limit", type=int, default=5)
    ls = sub.add_parser("lesson")
    ls.add_argument("--id", type=int, required=True)
    ls.add_argument("--text", required=True)
    sub.add_parser("list")
    a = ap.parse_args()

    p = path_of(a)
    rows = load(p)

    if a.cmd == "add":
        rid = (max((r["id"] for r in rows), default=0) + 1)
        row = {"id": rid, "ticker": a.ticker.upper(), "date": a.date, "rating": a.rating,
               "price": a.price, "confidence": a.confidence, "horizon": a.horizon,
               "stop": a.stop, "target": a.target, "bench_price": a.bench_price,
               "thesis": a.thesis, "lesson": None}
        rows.append(row)
        save(p, rows)
        print(json.dumps({"saved": row, "log": os.path.abspath(p)}, indent=2, ensure_ascii=False))
        return

    if a.cmd == "lesson":
        for r in rows:
            if r["id"] == a.id:
                r["lesson"] = a.text
                save(p, rows)
                print(json.dumps(r, indent=2, ensure_ascii=False))
                return
        raise SystemExit(f"id {a.id} not found in {p}")

    if a.cmd == "list":
        for r in rows:
            print(f"#{r['id']} {r['date']} {r['ticker']} {r['rating']} @ {r['price']} | {r['thesis'][:80]}")
        if not rows:
            print(f"(empty log at {os.path.abspath(p)})")
        return

    # review
    t = a.ticker.upper()
    same = [r for r in rows if r["ticker"] == t and r["date"] < a.date][-a.limit:]
    reviewed = []
    for r in same:
        item = dict(r)
        if a.price:
            ret = (a.price / r["price"] - 1) * 100
            item["realized_return_pct"] = round(ret, 2)
            item["verdict"] = verdict(r["rating"], ret)
            if r.get("stop") and ((DIRECTION.get(r["rating"].lower(), 0) > 0 and a.price <= r["stop"]) or
                                  (DIRECTION.get(r["rating"].lower(), 0) < 0 and a.price >= r["stop"])):
                item["stop_status"] = "current price is beyond the stop"
            if a.bench_now and r.get("bench_price"):
                bret = (a.bench_now / r["bench_price"] - 1) * 100
                item["alpha_pct"] = round(ret - bret, 2)
        reviewed.append(item)
    lessons = [{"ticker": r["ticker"], "date": r["date"], "lesson": r["lesson"]}
               for r in rows if r.get("lesson")][-5:]
    print(json.dumps({"log": os.path.abspath(p), "ticker": t, "prior_decisions": reviewed,
                      "recent_lessons_all_tickers": lessons}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
