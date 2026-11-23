#!/usr/bin/env python3
"""Scan the liquid universe for coins that match a chart label's price level.

Use when a screenshot shows a TradingView setup (e.g. "1,8742 (765,98%) 18.742") with the
ticker removed, and the user asks: "is there a coin with that price and a chart like that?"

Usage (bare python3 -u, NEVER inside a heredoc: URLs contain '&' and the terminal guard
rejects those as backgrounding):

    python3 -u coin_candidate_scan.py 1.8742                 # coins within +-12% of the level
    python3 -u coin_candidate_scan.py 1.8742 --band 0.25     # wider band
    python3 -u coin_candidate_scan.py 1.8742 --at 2026-10-03T08:55:00Z
        # which pairs' 1h candle on that timestamp actually CONTAINED that level
        # (the level often equals the price when the chart was drawn)

Output: one line per candidate with current price, 2025 peak (+date), peak/now ratio,
2026 low (+date), a double-bottom verdict with neckline, and coverage notes.

Data sources (no API key): Binance ticker/price + klines, OKX SPOT tickers,
CoinPaprika /v1/tickers. CoinGecko /coins/markets is optional (--cg-pages N) and
rate-limits hard: needs sleep >= 8s per page, retries=2, timeout=45.

Reality checks learned the hard way:
  * Klines window must start 2025-01-01 (startTime=1735689600000), not "last 420 days":
    the January-2025 peak falls outside a 420-day window and the ratio test goes wrong.
  * A delisted token (MLN, ALCX) simply STOPS in klines; short series = "no longer listed",
    not "no price".
  * Price match is not shape match: DEXE traded exactly at the label level yet its 2026
    pump-dump (Jun $23 -> Jul $2.6) disqualifies it. Always print the shape column too.
  * Print progressively (flush=True) and/or append to a jsonl; buffered output is lost
    when a long scan hits the command timeout.
"""

import argparse
import datetime as dt
import json
import sys
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
SEC_2025 = 1735689600000  # 2025-01-01T00:00:00Z in ms


def get(url, tries=3, timeout=25):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())
        except Exception as exc:  # noqa: BLE001 - retry any transport/rate error
            print("   retry %s %s" % (type(exc).__name__, url.split("?")[0]), flush=True)
            time.sleep(2 + 2 * i)
    return None


STABLE = {"USDC", "FDUSD", "TUSD", "BUSD", "DAI", "USDP", "EURI", "AEUR", "USDT", "XUSD",
          "USD1", "BFUSD", "PAXG", "USDE", "USDS", "USDY", "SUSD"}
LEVER = ("UP", "DOWN", "BULL", "BEAR", "3L", "3S", "5L", "5S", "2L", "2S")


def binance_pairs(lo, hi):
    d = get("https://api.binance.com/api/v3/ticker/price")
    out = []
    for row in d or []:
        sym = row["symbol"]
        if not sym.endswith("USDT"):
            continue
        base = sym[:-4]
        if base in STABLE or base.endswith(LEVER) or len(base) > 12:
            continue
        try:
            px = float(row["price"])
        except ValueError:
            continue
        if lo <= px <= hi:
            out.append((base, px))
    return out


def okx_pairs(lo, hi):
    d = get("https://www.okx.com/api/v5/market/tickers?instType=SPOT")
    out = []
    if not d or d.get("code") != "0":
        return out
    for row in d["data"]:
        inst = row["instId"]
        if not inst.endswith("-USDT"):
            continue
        base = inst[:-5]
        if base in STABLE:
            continue
        try:
            px = float(row["last"])
        except ValueError:
            continue
        if lo <= px <= hi:
            out.append((base, px))
    return out


def paprika_pairs(lo, hi, limit=2000):
    d = get("https://api.coinpaprika.com/v1/tickers?quotes=USD", timeout=40)
    out = []
    for c in (d or [])[:limit]:
        px = (c.get("quotes") or {}).get("USD", {}).get("price") or 0
        if lo <= px <= hi:
            out.append(("%s (cp rank %s)" % (c.get("symbol"), c.get("rank")), px))
    return out


def klines(sym, interval="1d", start=SEC_2025, limit=700):
    url = ("https://api.binance.com/api/v3/klines?symbol=%sUSDT&interval=%s"
           "&startTime=%d&limit=%d" % (sym, interval, start, limit))
    return get(url)


def double_bottom(ts, hi, lo, now):
    """Two 2026 lows within 15%, >=18 days apart, neckline >= 1.10x the higher low."""
    idx = [i for i, t in enumerate(ts) if dt.datetime.utcfromtimestamp(t).year >= 2026]
    mins = [i for i in idx
            if 10 <= i < len(lo) - 5 and lo[i] == min(lo[i - 7:i + 8])]
    ded = []
    for i in mins:
        if not ded or i - ded[-1] > 14:
            ded.append(i)
        elif lo[i] < lo[ded[-1]]:
            ded[-1] = i
    if len(ded) < 2:
        return None
    a, b = ded[-2], ded[-1]
    l1, l2 = lo[a], lo[b]
    if max(l1, l2) <= 0 or abs(l1 - l2) / max(l1, l2) >= 0.15 or b - a < 18:
        return None
    neck = max(hi[a:b + 1]) if b > a else 0
    if neck < max(l1, l2) * 1.10:
        return None
    return (l1, ts[a], l2, ts[b], neck, (now / neck - 1) * 100 if neck else 0)


def day(ts):
    return dt.datetime.utcfromtimestamp(ts).date()


def probe_at(level, when_iso):
    """Which pairs' 1h candle on `when` had low <= level <= high."""
    t0 = int(dt.datetime.fromisoformat(when_iso.replace("Z", "+00:00")).timestamp() * 1000)
    hits = []
    for base, px in binance_pairs(level * 0.4, level * 2.5):
        k = (get("https://api.binance.com/api/v3/klines?symbol=%sUSDT&interval=1h"
                 "&startTime=%d&limit=6" % (base, t0)) or [])
        dev = 1e9
        for c in k:
            low, high = float(c[3]), float(c[2])
            if low <= level <= high:
                dev = 0.0
                break
            dev = min(dev, abs(low - level) / level, abs(high - level) / level)
        hits.append((dev, base, px))
        time.sleep(0.15)
    hits.sort()
    print("\n=== pairs whose 1h bar contained %.4f around %s ===" % (level, when_iso))
    for dev, base, px in hits[:12]:
        print("  %-8s now=$%-9.4f dev=%6.2f%%" % (base, px, dev * 100))


def report(level, band):
    lo, hi = level * (1 - band), level * (1 + band)
    print("level=$%.4f band=+-%.0f%% -> window $%.4f-$%.4f" % (level, band * 100, lo, hi),
          flush=True)
    seen = {}
    for base, px in binance_pairs(lo, hi):
        seen.setdefault(base, px)
    for base, px in okx_pairs(lo, hi):
        seen.setdefault(base, px)
    for name, px in paprika_pairs(lo, hi):
        seen.setdefault(name, px)
    print("candidates found: %d" % len(seen), flush=True)
    print("\n%-10s %-10s %-10s %-7s %-22s %s" %
          ("coin", "now", "peak2025", "ratio", "2026 low (date)", "double bottom / neckline"))
    rows = []
    for base, px in sorted(seen.items()):
        sym = base.split(" ")[0]
        k = klines(sym)
        if not k or len(k) < 200:
            print("%-10s %-10.4f %s" % (sym, px, "no klines (delisted/not on Binance?) - okx/cp"
                                        " price only, shape unverified"))
            continue
        ts = [int(c[0]) / 1000 for c in k]
        hi_s = [float(c[2]) for c in k]
        lo_s = [float(c[3]) for c in k]
        cl = [float(c[4]) for c in k]
        now = cl[-1]
        i25 = [i for i, t in enumerate(ts) if dt.datetime.utcfromtimestamp(t).year == 2025]
        ipk = max(i25, key=lambda i: hi_s[i]) if i25 else max(range(len(hi_s)), key=lambda i: hi_s[i])
        peak = hi_s[ipk]
        i26 = [i for i, t in enumerate(ts) if dt.datetime.utcfromtimestamp(t).year == 2026]
        ilow = min(i26, key=lambda i: lo_s[i]) if i26 else min(range(len(lo_s)), key=lambda i: lo_s[i])
        db = double_bottom(ts, hi_s, lo_s, now)
        db_txt = ("DB $%.3f(%s)/$%.3f(%s) neck $%.3f now/neck %+.0f%%" %
                  (db[0], day(db[1]), db[2], day(db[3]), db[4], db[5])) if db else "no clean DB"
        rows.append((sym, now, peak, peak / now if now else 0, lo_s[ilow], day(ts[ilow]), db_txt))
        print("%-10s %-10.4f %-10.3f %-7.1fx $%-8.4f %-12s %s" %
              (sym, now, peak, peak / now, lo_s[ilow], day(ts[ilow]), db_txt), flush=True)
        time.sleep(0.2)
    print("\n--- sorted by 2025 peak / now ratio (closest to the chart's implied drawdown) ---")
    for r in sorted(rows, key=lambda r: abs(r[3] - 20)):
        print("  %-10s %5.1fx  now=$%-9.4f peak2025=$%-9.3f %s" % (r[0], r[3], r[1], r[2], r[6]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("level", type=float, help="price level read off the chart label")
    ap.add_argument("--band", type=float, default=0.12, help="fractional price band (default .12)")
    ap.add_argument("--at", help="ISO timestamp; also probe which pairs' 1h bar contained the level")
    args = ap.parse_args()
    rows = report(args.level, args.band)
    if args.at:
        probe_at(args.level, args.at)
    print("\nRemember: price match != shape match. A 2026 pump-dump disqualifies a candidate;"
          " say your confidence level and what is still unverified.", flush=True)
    return 0 if rows else 1


if __name__ == "__main__":
    sys.exit(main())
