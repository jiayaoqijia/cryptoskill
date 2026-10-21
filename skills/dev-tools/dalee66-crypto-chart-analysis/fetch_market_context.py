#!/usr/bin/env python3
"""Fetch multi-TF OHLCV + funding/OI for cloud-agent chart analysis.

Prefer venues reachable from restricted Cursor Cloud egress:
  OKX, Bitget, Binance data-api (binance.vision).
Main Binance / Bybit often geo-block — do not rely on them here.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

UA = {"User-Agent": "cursor-cloud-crypto-chart-analysis/1.0"}


def http_get(url: str, timeout: float = 20.0) -> Any:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def ms_to_iso(ms: int | float | str) -> str:
    return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )


def atr(candles: list[dict], period: int = 14) -> float | None:
    if len(candles) < period + 1:
        return None
    trs: list[float] = []
    for i in range(1, len(candles)):
        h, l, pc = candles[i]["h"], candles[i]["l"], candles[i - 1]["c"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    window = trs[-period:]
    return sum(window) / period if window else None


def swing_points(candles: list[dict], left: int = 2, right: int = 2) -> dict:
    highs, lows = [], []
    n = len(candles)
    for i in range(left, n - right):
        h = candles[i]["h"]
        l = candles[i]["l"]
        if all(h >= candles[i - j]["h"] for j in range(1, left + 1)) and all(
            h >= candles[i + j]["h"] for j in range(1, right + 1)
        ):
            highs.append({"i": i, "t": candles[i]["t"], "price": h})
        if all(l <= candles[i - j]["l"] for j in range(1, left + 1)) and all(
            l <= candles[i + j]["l"] for j in range(1, right + 1)
        ):
            lows.append({"i": i, "t": candles[i]["t"], "price": l})
    return {"swing_highs": highs[-6:], "swing_lows": lows[-6:]}


def structure_hint(swings: dict) -> str:
    sh = [x["price"] for x in swings.get("swing_highs", [])]
    sl = [x["price"] for x in swings.get("swing_lows", [])]
    if len(sh) < 2 or len(sl) < 2:
        return "insufficient swings — treat as unclear / possible range"
    hh = sh[-1] > sh[-2]
    hl = sl[-1] > sl[-2]
    lh = sh[-1] < sh[-2]
    ll = sl[-1] < sl[-2]
    if hh and hl:
        return "bullish structure bias (HH + HL) — confirm on HTF"
    if lh and ll:
        return "bearish structure bias (LH + LL) — confirm on HTF"
    return "mixed / range-like structure — prefer levels over trend entries"


def annualize_funding(rate: float, hours: float = 8.0) -> float:
    periods = (365.0 * 24.0) / hours
    return rate * periods * 100.0


# --- venue fetchers ---------------------------------------------------------

OKX_BAR = {
    "1d": "1D",
    "4h": "4H",
    "1h": "1H",
    "15m": "15m",
}


def okx_symbol(base: str, quote: str, market: str) -> str:
    base, quote = base.upper(), quote.upper()
    if market == "spot":
        return f"{base}-{quote}"
    return f"{base}-{quote}-SWAP"


def fetch_okx(base: str, quote: str, market: str, tfs: list[str], limit: int) -> dict:
    inst = okx_symbol(base, quote, market)
    out: dict[str, Any] = {"venue": "okx", "instrument": inst, "market": market, "tfs": {}}
    for tf in tfs:
        bar = OKX_BAR.get(tf)
        if not bar:
            continue
        path = "market/candles" if market == "perp" else "market/candles"
        # spot and swap share candles endpoint; instId differs
        url = (
            "https://www.okx.com/api/v5/market/candles?"
            + urllib.parse.urlencode({"instId": inst, "bar": bar, "limit": str(limit)})
        )
        raw = http_get(url)
        rows = raw.get("data") or []
        # OKX returns newest first: [ts,o,h,l,c,vol,volCcy,volCcyQuote,confirm]
        candles = []
        for r in reversed(rows):
            candles.append(
                {
                    "t": ms_to_iso(r[0]),
                    "o": float(r[1]),
                    "h": float(r[2]),
                    "l": float(r[3]),
                    "c": float(r[4]),
                    "v": float(r[5]),
                }
            )
        swings = swing_points(candles)
        out["tfs"][tf] = {
            "count": len(candles),
            "last": candles[-1] if candles else None,
            "atr14": atr(candles),
            "swings": swings,
            "structure_hint": structure_hint(swings),
            "candles": candles,
        }

    if market == "perp":
        fr = http_get(
            "https://www.okx.com/api/v5/public/funding-rate?"
            + urllib.parse.urlencode({"instId": inst})
        )
        oi = http_get(
            "https://www.okx.com/api/v5/public/open-interest?"
            + urllib.parse.urlencode({"instId": inst})
        )
        fr_row = (fr.get("data") or [{}])[0]
        oi_row = (oi.get("data") or [{}])[0]
        rate = float(fr_row.get("fundingRate") or 0)
        out["positioning"] = {
            "funding_rate": rate,
            "funding_apr_pct_approx": round(annualize_funding(rate), 2),
            "funding_time": ms_to_iso(fr_row["fundingTime"])
            if fr_row.get("fundingTime")
            else None,
            "next_funding_time": ms_to_iso(fr_row["nextFundingTime"])
            if fr_row.get("nextFundingTime")
            else None,
            "open_interest_contracts": float(oi_row.get("oi") or 0),
            "open_interest_coin": float(oi_row.get("oiCcy") or 0),
            "open_interest_usd": float(oi_row.get("oiUsd") or 0),
            "note": "Funding extremum ≠ auto reversal; pair with OI + structure.",
        }
    return out


BITGET_GRAN = {"1d": "1D", "4h": "4H", "1h": "1H", "15m": "15m"}


def fetch_bitget(base: str, quote: str, market: str, tfs: list[str], limit: int) -> dict:
    if market != "perp":
        raise SystemExit("bitget fetcher in this skill supports perp (USDT-FUTURES) only")
    symbol = f"{base.upper()}{quote.upper()}"
    out: dict[str, Any] = {
        "venue": "bitget",
        "instrument": symbol,
        "market": market,
        "tfs": {},
    }
    for tf in tfs:
        gran = BITGET_GRAN.get(tf)
        if not gran:
            continue
        url = (
            "https://api.bitget.com/api/v2/mix/market/candles?"
            + urllib.parse.urlencode(
                {
                    "symbol": symbol,
                    "productType": "USDT-FUTURES",
                    "granularity": gran,
                    "limit": str(limit),
                }
            )
        )
        raw = http_get(url)
        rows = raw.get("data") or []
        # Bitget: oldest→newest typically [ts,o,h,l,c,baseVol,quoteVol]
        candles = []
        for r in rows:
            candles.append(
                {
                    "t": ms_to_iso(r[0]),
                    "o": float(r[1]),
                    "h": float(r[2]),
                    "l": float(r[3]),
                    "c": float(r[4]),
                    "v": float(r[5]),
                }
            )
        swings = swing_points(candles)
        out["tfs"][tf] = {
            "count": len(candles),
            "last": candles[-1] if candles else None,
            "atr14": atr(candles),
            "swings": swings,
            "structure_hint": structure_hint(swings),
            "candles": candles,
        }

    fr = http_get(
        "https://api.bitget.com/api/v2/mix/market/current-fund-rate?"
        + urllib.parse.urlencode({"symbol": symbol, "productType": "USDT-FUTURES"})
    )
    oi = http_get(
        "https://api.bitget.com/api/v2/mix/market/open-interest?"
        + urllib.parse.urlencode({"symbol": symbol, "productType": "USDT-FUTURES"})
    )
    fr_row = (fr.get("data") or [{}])[0]
    oi_list = ((oi.get("data") or {}).get("openInterestList")) or [{}]
    rate = float(fr_row.get("fundingRate") or 0)
    interval_h = float(fr_row.get("fundingRateInterval") or 8)
    out["positioning"] = {
        "funding_rate": rate,
        "funding_interval_hours": interval_h,
        "funding_apr_pct_approx": round(annualize_funding(rate, interval_h), 2),
        "next_update": ms_to_iso(fr_row["nextUpdate"]) if fr_row.get("nextUpdate") else None,
        "open_interest_size": float(oi_list[0].get("size") or 0),
        "note": "Funding extremum ≠ auto reversal; pair with OI + structure.",
    }
    return out


VISION_INTERVAL = {"1d": "1d", "4h": "4h", "1h": "1h", "15m": "15m"}


def fetch_binance_vision(
    base: str, quote: str, market: str, tfs: list[str], limit: int
) -> dict:
    """Spot OHLCV via data-api.binance.vision (often reachable when fapi is not)."""
    if market != "spot":
        raise SystemExit(
            "binance_vision fetcher supports spot only; use okx/bitget for perp OI/funding"
        )
    symbol = f"{base.upper()}{quote.upper()}"
    out: dict[str, Any] = {
        "venue": "binance_vision",
        "instrument": symbol,
        "market": "spot",
        "tfs": {},
        "positioning": None,
        "note": "No funding/OI on spot vision endpoint.",
    }
    for tf in tfs:
        interval = VISION_INTERVAL.get(tf)
        if not interval:
            continue
        url = (
            "https://data-api.binance.vision/api/v3/klines?"
            + urllib.parse.urlencode(
                {"symbol": symbol, "interval": interval, "limit": str(limit)}
            )
        )
        rows = http_get(url)
        candles = [
            {
                "t": ms_to_iso(r[0]),
                "o": float(r[1]),
                "h": float(r[2]),
                "l": float(r[3]),
                "c": float(r[4]),
                "v": float(r[5]),
            }
            for r in rows
        ]
        swings = swing_points(candles)
        out["tfs"][tf] = {
            "count": len(candles),
            "last": candles[-1] if candles else None,
            "atr14": atr(candles),
            "swings": swings,
            "structure_hint": structure_hint(swings),
            "candles": candles,
        }
    return out


FETCHERS = {
    "okx": fetch_okx,
    "bitget": fetch_bitget,
    "binance_vision": fetch_binance_vision,
}


def summarize(payload: dict, include_candles: bool) -> dict:
    """Compact view for agent context; optionally drop full candle arrays."""
    slim = {
        "venue": payload.get("venue"),
        "instrument": payload.get("instrument"),
        "market": payload.get("market"),
        "fetched_at_utc": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "positioning": payload.get("positioning"),
        "note": payload.get("note"),
        "tfs": {},
    }
    for tf, block in (payload.get("tfs") or {}).items():
        entry = {
            "count": block["count"],
            "last": block["last"],
            "atr14": block["atr14"],
            "structure_hint": block["structure_hint"],
            "swings": block["swings"],
        }
        if include_candles:
            entry["candles"] = block["candles"]
        else:
            # keep last 8 for quick eyeballing without huge context
            entry["candles_tail"] = (block.get("candles") or [])[-8:]
        slim["tfs"][tf] = entry
    return slim


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--symbol", default="BTCUSDT", help="e.g. BTCUSDT or BTC-USDT")
    p.add_argument("--market", choices=["perp", "spot"], default="perp")
    p.add_argument(
        "--venue",
        choices=["okx", "bitget", "binance_vision", "auto"],
        default="auto",
        help="auto: okx for perp, binance_vision for spot",
    )
    p.add_argument(
        "--tfs",
        default="1d,4h,1h",
        help="comma list from 1d,4h,1h,15m",
    )
    p.add_argument("--limit", type=int, default=120, help="candles per TF")
    p.add_argument(
        "--full-candles",
        action="store_true",
        help="include full candle arrays (large)",
    )
    p.add_argument("-o", "--output", help="write JSON to path")
    args = p.parse_args()

    sym = args.symbol.replace("-", "").replace("/", "").upper()
    # split base/quote — USDT/USDC/USD quote assumed
    quote = "USDT"
    for q in ("USDT", "USDC", "USD"):
        if sym.endswith(q):
            quote = q
            base = sym[: -len(q)]
            break
    else:
        base, quote = sym, "USDT"

    venue = args.venue
    if venue == "auto":
        venue = "okx" if args.market == "perp" else "binance_vision"

    tfs = [x.strip() for x in args.tfs.split(",") if x.strip()]
    try:
        raw = FETCHERS[venue](base, quote, args.market, tfs, args.limit)
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.code}", "venue": venue}), file=sys.stderr)
        return 2
    except urllib.error.URLError as e:
        print(json.dumps({"error": str(e.reason), "venue": venue}), file=sys.stderr)
        return 2

    out = summarize(raw, include_candles=args.full_candles)
    text = json.dumps(out, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
