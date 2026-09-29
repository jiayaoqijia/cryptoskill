#!/usr/bin/env python3
"""Compute a verified technical snapshot from an OHLCV price file.

Every number the Technical Analyst quotes must come from this output, so the
agents never have to estimate indicators "by eye".

Accepts CSVs exported from Yahoo Finance, Investing.com (English or Indonesian
headers such as Tanggal/Terakhir/Pembukaan/Tertinggi/Terendah/Vol.),
TradingView, Nasdaq.com, broker apps, or produced by fetch_data.py.

Usage:
  python indicators.py --csv prices.csv --ticker BBCA.JK --date 2026-09-29 \
      [--benchmark-csv ihsg.csv] [--locale auto|id|en] \
      [--out technical.json] [--md technical.md]

Only rows dated on or before --date are used (no look-ahead).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from datetime import date, datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import detect_market, fmt_num  # noqa: E402

# ------------------------------------------------------------------ parsing
ALIASES = {
    "date": ["date", "tanggal", "tgl", "datetime", "time", "timestamp", "waktu", "day"],
    "open": ["open", "pembukaan", "buka", "open price", "opening"],
    "high": ["high", "tertinggi", "high price", "max"],
    "low": ["low", "terendah", "low price", "min"],
    "close": ["close", "terakhir", "penutupan", "tutup", "price", "harga", "close price",
              "last", "close/last", "closing", "harga penutupan"],
    "adj_close": ["adj close", "adj. close", "adj_close", "adjclose", "adjusted close"],
    "volume": ["volume", "vol.", "vol", "volume (lot)", "volume lembar", "volume (shares)"],
}
INDONESIAN_HEADERS = {"tanggal", "terakhir", "pembukaan", "tertinggi", "terendah", "penutupan"}
SUFFIX_MULT = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}


def _norm_header(h: str) -> str:
    return re.sub(r"\s+", " ", str(h).replace("*", "").replace("\ufeff", "").strip().lower())


def parse_number(val, locale: str = "auto") -> float:
    if val is None:
        return np.nan
    if isinstance(val, (int, float, np.integer, np.floating)):
        return float(val)
    s = str(val).strip().replace("\u00a0", "").replace(" ", "")
    s = s.replace("$", "").replace("Rp", "").replace("rp", "").replace("%", "")
    if s in ("", "-", "\u2014", "null", "None", "nan", "NaN", "N/A"):
        return np.nan
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    mult = 1.0
    if s and s[-1].upper() in SUFFIX_MULT:
        mult = SUFFIX_MULT[s[-1].upper()]
        s = s[:-1]
    if locale == "id":
        s = s.replace(".", "").replace(",", ".")
    elif locale == "en":
        s = s.replace(",", "")
    else:
        if "," in s and "." in s:
            if s.rfind(",") > s.rfind("."):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
        elif "," in s:
            if re.fullmatch(r"-?\d{1,3}(,\d{3})+", s):
                s = s.replace(",", "")
            else:
                s = s.replace(",", ".")
        elif s.count(".") > 1:
            s = s.replace(".", "")
    try:
        x = float(s) * mult
    except ValueError:
        return np.nan
    return -x if neg else x


def _detect_dayfirst(raw_dates: pd.Series, locale: str) -> bool:
    """Decide dd/mm vs mm/dd from the data itself; fall back to locale."""
    m = raw_dates.str.extract(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})").dropna()
    if m.empty:
        return False  # ISO or textual dates
    first, second = m[0].astype(int), m[1].astype(int)
    if (first > 12).any():
        return True
    if (second > 12).any():
        return False
    return locale == "id"


def load_prices(path: str, locale: str = "auto", warnings: list | None = None) -> pd.DataFrame:
    warnings = warnings if warnings is not None else []
    df = pd.read_csv(path, sep=None, engine="python", dtype=str)
    headers = {_norm_header(c): c for c in df.columns}
    if locale == "auto" and INDONESIAN_HEADERS & set(headers):
        locale = "id"
    colmap = {}
    for field, names in ALIASES.items():
        for n in names:
            if n in headers and headers[n] not in colmap.values():
                colmap[field] = headers[n]
                break
    if "date" not in colmap:
        # fall back to first column
        colmap["date"] = df.columns[0]
    if "close" not in colmap and "adj_close" in colmap:
        colmap["close"] = colmap["adj_close"]
    if "close" not in colmap:
        raise SystemExit(f"Could not find a close/price column in {path}. Columns: {list(df.columns)}")
    if "volume" in colmap and "lot" in _norm_header(colmap["volume"]):
        warnings.append("Volume column is in lots (1 lot = 100 shares on IDX).")

    out = pd.DataFrame()
    raw_dates = df[colmap["date"]].astype(str).str.strip()
    # drop timezone offsets so a +07:00 bar keeps its local trading date
    raw_dates = raw_dates.str.replace(r"(\d{2}:\d{2}(?::\d{2})?)(?:\.\d+)?(?:[+-]\d{2}:?\d{2}|Z)$", r"\1", regex=True)
    dayfirst = _detect_dayfirst(raw_dates, locale)
    out["date"] = pd.to_datetime(raw_dates, format="mixed", dayfirst=dayfirst, errors="coerce")
    for field in ("open", "high", "low", "close", "adj_close", "volume"):
        if field in colmap:
            out[field] = df[colmap[field]].map(lambda v: parse_number(v, locale))
    out = out.dropna(subset=["date", "close"])
    out["date"] = out["date"].dt.normalize()
    out = out.sort_values("date").drop_duplicates("date", keep="last").set_index("date")
    return out


# --------------------------------------------------------------- indicators
def wilder(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    gain, loss = d.clip(lower=0), -d.clip(upper=0)
    rs = wilder(gain, n) / wilder(loss, n)
    return 100 - 100 / (1 + rs)


def true_range(df: pd.DataFrame) -> pd.Series:
    pc = df["close"].shift(1)
    return pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)


def adx(df: pd.DataFrame, n: int = 14):
    up = df["high"].diff()
    down = -df["low"].diff()
    plus_dm = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=df.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=df.index)
    atr_ = wilder(true_range(df), n)
    pdi = 100 * wilder(plus_dm, n) / atr_
    mdi = 100 * wilder(minus_dm, n) / atr_
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    return wilder(dx, n), pdi, mdi


def last(s: pd.Series):
    s = s.dropna()
    return float(s.iloc[-1]) if len(s) else None


def bars_since_cross(a: pd.Series, b: pd.Series):
    """Bars since the sign of (a-b) last changed, and direction ('up'/'down')."""
    diff = (a - b).dropna()
    if len(diff) < 2:
        return None, None
    sign = np.sign(diff.values)
    changes = np.where(sign[1:] != sign[:-1])[0]
    if len(changes) == 0:
        return None, "above" if sign[-1] > 0 else "below"
    i = changes[-1] + 1
    return int(len(sign) - 1 - i), ("up" if sign[i] > 0 else "down")


def pivot_levels(df: pd.DataFrame, lookback: int = 180, k: int = 5, tol_pct: float = 1.5):
    d = df.tail(lookback)
    hi = d["high"] if "high" in d else d["close"]
    lo = d["low"] if "low" in d else d["close"]
    highs, lows = [], []
    for i in range(k, len(d) - k):
        if hi.iloc[i] == hi.iloc[i - k:i + k + 1].max():
            highs.append(float(hi.iloc[i]))
        if lo.iloc[i] == lo.iloc[i - k:i + k + 1].min():
            lows.append(float(lo.iloc[i]))

    def cluster(levels):
        levels = sorted(levels)
        groups = []
        for lv in levels:
            if groups and abs(lv - np.mean(groups[-1])) / np.mean(groups[-1]) * 100 <= tol_pct:
                groups[-1].append(lv)
            else:
                groups.append([lv])
        return [{"level": float(np.mean(g)), "touches": len(g)} for g in groups]

    return cluster(highs + lows)


def max_drawdown(close: pd.Series) -> float | None:
    if len(close) < 2:
        return None
    peak = close.cummax()
    return float(((close / peak) - 1).min() * 100)


def pct(a, b):
    if a is None or b is None or b == 0 or (isinstance(b, float) and math.isnan(b)):
        return None
    return (a / b - 1) * 100


def clean(o):
    """Recursively convert numpy / NaN to JSON-safe values and round floats."""
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        f = float(o)
        if not math.isfinite(f):
            return None
        return round(f, 4) if abs(f) < 1e6 else round(f, 1)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, (pd.Timestamp, datetime, date)):
        return o.strftime("%Y-%m-%d")
    return o


# ------------------------------------------------------------------ snapshot
def build_snapshot(df: pd.DataFrame, ticker: str, analysis_date: pd.Timestamp,
                   bench: pd.DataFrame | None = None, warnings: list | None = None) -> dict:
    warnings = list(warnings or [])
    info = detect_market(ticker) if ticker else {"market": "other", "periods_per_year": 252}
    ppy = info.get("periods_per_year", 252)
    crypto = info.get("market") == "crypto"

    df = df[df.index <= analysis_date].copy()
    if df.empty:
        raise SystemExit("No price rows on or before the analysis date.")
    c = df["close"]
    has_hl = {"high", "low"} <= set(df.columns) and df[["high", "low"]].notna().mean().min() > 0.9
    has_vol = "volume" in df and df["volume"].notna().mean() > 0.9 and df["volume"].sum() > 0
    if not has_hl:
        warnings.append("No reliable high/low columns: ATR, ADX, stochastic and pivots use close only or are skipped.")
    if not has_vol:
        warnings.append("No reliable volume column: volume and liquidity metrics skipped.")

    n = len(df)
    last_date = df.index[-1]
    gap_days = (analysis_date - last_date).days
    stale_limit = 3 if crypto else 5
    if gap_days > stale_limit:
        warnings.append(f"Last price bar is {gap_days} days before the analysis date; data may be stale.")
    if n < 200:
        warnings.append(f"Only {n} bars available; SMA200 and 1-year stats may be missing.")
    ret_src = df["adj_close"] if "adj_close" in df and df["adj_close"].notna().all() else c

    # moving averages & trend
    sma = {w: c.rolling(w).mean() for w in (10, 20, 50, 100, 200)}
    ema = {w: c.ewm(span=w, adjust=False).mean() for w in (12, 20, 26, 50)}
    price = float(c.iloc[-1])
    prev = float(c.iloc[-2]) if n > 1 else None
    s20, s50, s200 = last(sma[20]), last(sma[50]), last(sma[200])
    slope20 = pct(last(sma[20]), float(sma[20].dropna().iloc[-11])) if sma[20].dropna().size > 11 else None
    score_items = {
        "price>SMA20": None if s20 is None else price > s20,
        "price>SMA50": None if s50 is None else price > s50,
        "price>SMA200": None if s200 is None else price > s200,
        "SMA50>SMA200": None if (s50 is None or s200 is None) else s50 > s200,
        "SMA20 rising (10 bars)": None if slope20 is None else slope20 > 0,
    }
    known = [v for v in score_items.values() if v is not None]
    score, available = sum(known), len(known)
    ratio = score / available if available else 0.5
    if ratio >= 0.8:
        trend = "uptrend"
    elif ratio <= 0.2:
        trend = "downtrend"
    else:
        trend = "mixed/sideways"

    # momentum
    macd_line = ema[12] - ema[26]
    signal = macd_line.ewm(span=9, adjust=False).mean()
    hist = macd_line - signal
    r14 = rsi(c, 14)
    momentum = {
        "rsi14": last(r14),
        "rsi14_5bars_ago": float(r14.dropna().iloc[-6]) if r14.dropna().size > 6 else None,
        "macd": last(macd_line), "macd_signal": last(signal), "macd_hist": last(hist),
        "macd_hist_prev": float(hist.dropna().iloc[-2]) if hist.dropna().size > 1 else None,
        "roc_10": pct(price, float(c.iloc[-11])) if n > 11 else None,
    }
    if has_hl:
        ll, hh = df["low"].rolling(14).min(), df["high"].rolling(14).max()
        k = 100 * (c - ll) / (hh - ll)
        momentum["stoch_k14"] = last(k)
        momentum["stoch_d3"] = last(k.rolling(3).mean())

    # volatility
    mid, sd = c.rolling(20).mean(), c.rolling(20).std(ddof=0)
    upper, lower = mid + 2 * sd, mid - 2 * sd
    logr = np.log(ret_src / ret_src.shift(1))
    vol = {
        "bb_upper": last(upper), "bb_middle": last(mid), "bb_lower": last(lower),
        "bb_percent_b": ((price - last(lower)) / (last(upper) - last(lower)) * 100) if last(upper) and last(upper) != last(lower) else None,
        "bb_width_pct": ((last(upper) - last(lower)) / last(mid) * 100) if last(mid) else None,
        "hist_vol_20_ann_pct": float(logr.tail(20).std() * math.sqrt(ppy) * 100) if n > 21 else None,
        "hist_vol_60_ann_pct": float(logr.tail(60).std() * math.sqrt(ppy) * 100) if n > 61 else None,
        "max_drawdown_1y_pct": max_drawdown(c.tail(ppy)),
    }
    trend_block = {
        "classification": trend, "score": f"{score}/{available}", "checks": score_items,
        "sma10": last(sma[10]), "sma20": s20, "sma50": s50, "sma100": last(sma[100]), "sma200": s200,
        "ema20": last(ema[20]), "ema50": last(ema[50]),
        "sma20_slope_10bars_pct": slope20,
        "dist_from_sma50_pct": pct(price, s50), "dist_from_sma200_pct": pct(price, s200),
    }
    if has_hl:
        tr = true_range(df)
        atr14 = wilder(tr, 14)
        a, pdi, mdi = adx(df, 14)
        vol["atr14"] = last(atr14)
        vol["atr14_pct_of_price"] = last(atr14) / price * 100 if last(atr14) else None
        trend_block.update({"adx14": last(a), "plus_di": last(pdi), "minus_di": last(mdi)})

    # returns
    horizons = {"1w": 7, "1m": 30, "3m": 90, "6m": 180, "1y": 365} if crypto else \
               {"1w": 5, "1m": 21, "3m": 63, "6m": 126, "1y": 252}
    returns = {}
    for label, b in horizons.items():
        returns[label] = pct(float(ret_src.iloc[-1]), float(ret_src.iloc[-1 - b])) if n > b else None
    ytd_rows = ret_src[ret_src.index.year == analysis_date.year]
    prior = ret_src[ret_src.index.year < analysis_date.year]
    if len(prior):
        returns["ytd"] = pct(float(ret_src.iloc[-1]), float(prior.iloc[-1]))
    elif len(ytd_rows) and ytd_rows.index[0].dayofyear <= 7:
        returns["ytd"] = pct(float(ret_src.iloc[-1]), float(ytd_rows.iloc[0]))
    else:
        returns["ytd"] = None

    # levels
    window = c.tail(ppy)
    hi_series = df["high"].tail(ppy) if has_hl else window
    lo_series = df["low"].tail(ppy) if has_hl else window
    hi52, lo52 = float(hi_series.max()), float(lo_series.min())
    levels_all = pivot_levels(df if has_hl else df.assign(high=c, low=c))
    supports = sorted([l for l in levels_all if l["level"] < price], key=lambda l: -l["level"])[:3]
    resist = sorted([l for l in levels_all if l["level"] > price], key=lambda l: l["level"])[:3]
    levels = {
        "high_52w": hi52, "low_52w": lo52,
        "dist_from_52w_high_pct": pct(price, hi52), "dist_from_52w_low_pct": pct(price, lo52),
        "pivot_supports": supports, "pivot_resistances": resist,
    }

    # volume & liquidity
    volume = {}
    if has_vol:
        v = df["volume"]
        avg20 = float(v.tail(20).mean())
        volume = {
            "last_volume": float(v.iloc[-1]), "avg_volume_20": avg20,
            "rel_volume_vs_20d": float(v.iloc[-1]) / avg20 if avg20 else None,
            "avg_traded_value_20d": float((c * v).tail(20).mean()),
        }
        obv = (np.sign(c.diff()).fillna(0) * v).cumsum()
        volume["obv_change_20bars"] = float(obv.iloc[-1] - obv.iloc[-21]) if n > 21 else None
        up_vol = v[c.diff() > 0].tail(20).sum()
        dn_vol = v[c.diff() < 0].tail(20).sum()
        volume["up_down_volume_ratio_20"] = float(up_vol / dn_vol) if dn_vol else None
        thr = {"idx": 1e9, "us": 5e6}.get(info.get("market"))
        if thr and volume["avg_traded_value_20d"] < thr:
            warnings.append("Low liquidity: 20-day average traded value is below the rough heuristic "
                            f"threshold ({fmt_num(thr)} {info.get('currency') or ''}). Slippage risk.")

    # events
    events = []
    b, d = bars_since_cross(sma[50], sma[200])
    if d in ("up", "down"):
        events.append(f"{'Golden' if d == 'up' else 'Death'} cross (SMA50 vs SMA200) {b} bars ago")
    b, d = bars_since_cross(macd_line, signal)
    if d in ("up", "down"):
        events.append(f"MACD crossed {'above' if d == 'up' else 'below'} signal {b} bars ago")
    b, d = bars_since_cross(c, sma[50])
    if d in ("up", "down"):
        events.append(f"Price crossed {'above' if d == 'up' else 'below'} SMA50 {b} bars ago")
    r = momentum["rsi14"]
    if r is not None:
        if r >= 70:
            events.append(f"RSI14 overbought ({r:.1f})")
        elif r <= 30:
            events.append(f"RSI14 oversold ({r:.1f})")
    if last(upper) and price > last(upper):
        events.append("Close above upper Bollinger Band")
    if last(lower) and price < last(lower):
        events.append("Close below lower Bollinger Band")
    recent_hi = float(hi_series.tail(5).max())
    recent_lo = float(lo_series.tail(5).min())
    if recent_hi >= hi52:
        events.append("New 52-week high within the last 5 bars")
    if recent_lo <= lo52:
        events.append("New 52-week low within the last 5 bars")
    if volume.get("rel_volume_vs_20d") and volume["rel_volume_vs_20d"] >= 2:
        events.append(f"Volume spike: {volume['rel_volume_vs_20d']:.1f}x the 20-day average")
    if "open" in df and prev and pd.notna(df["open"].iloc[-1]):
        gap = pct(float(df["open"].iloc[-1]), prev)
        if gap is not None and abs(gap) >= 3:
            events.append(f"Opening gap of {gap:+.1f}% on the last bar")

    # relative strength vs benchmark
    relative = {}
    if bench is not None and not bench.empty:
        bc = bench["adj_close"] if "adj_close" in bench and bench["adj_close"].notna().all() else bench["close"]
        bc = bc[bc.index <= analysis_date]
        joined = pd.concat([ret_src.rename("a"), bc.rename("b")], axis=1, join="inner").dropna()
        if len(joined) > 30:
            rets = joined.pct_change().dropna().tail(ppy)
            var = rets["b"].var()
            relative["beta_1y"] = float(rets["a"].cov(rets["b"]) / var) if var else None
            relative["corr_1y"] = float(rets["a"].corr(rets["b"]))
            for label, bb in horizons.items():
                if len(joined) > bb:
                    ra = pct(joined["a"].iloc[-1], joined["a"].iloc[-1 - bb])
                    rb = pct(joined["b"].iloc[-1], joined["b"].iloc[-1 - bb])
                    relative[f"excess_{label}_pct"] = ra - rb if ra is not None and rb is not None else None
                    relative[f"benchmark_{label}_pct"] = rb
        else:
            warnings.append("Benchmark overlap too short for beta/relative strength.")

    snap = {
        "meta": {
            "ticker": ticker, "market": info.get("market"), "currency": info.get("currency"),
            "analysis_date": analysis_date, "last_bar_date": last_date, "bars": n,
            "first_bar_date": df.index[0], "uses_adjusted_close_for_returns": ret_src is not c,
            "generated_by": "trading-agents/scripts/indicators.py",
        },
        "price": {
            "last_close": price, "prev_close": prev, "change_pct": pct(price, prev),
            "open": float(df["open"].iloc[-1]) if "open" in df and pd.notna(df["open"].iloc[-1]) else None,
            "high": float(df["high"].iloc[-1]) if has_hl else None,
            "low": float(df["low"].iloc[-1]) if has_hl else None,
        },
        "returns_pct": returns, "trend": trend_block, "momentum": momentum,
        "volatility": vol, "levels": levels, "volume": volume,
        "relative_to_benchmark": relative, "events": events, "warnings": warnings,
        "recent_closes": {d.strftime("%Y-%m-%d"): float(x) for d, x in c.tail(10).items()},
    }
    return clean(snap)


# ------------------------------------------------------------------ markdown
def to_markdown(s: dict) -> str:
    m, p, t, mo, v, lv, vo, rel = (s["meta"], s["price"], s["trend"], s["momentum"],
                                    s["volatility"], s["levels"], s["volume"], s["relative_to_benchmark"])
    f = fmt_num

    def pc(x):
        return "n/a" if x is None else f"{x:+.2f}%"

    lines = [
        f"# Technical snapshot: {m['ticker']} (as of {m['analysis_date']})",
        f"Last bar {m['last_bar_date']} · {m['bars']} bars since {m['first_bar_date']} · market {m['market']} · currency {m['currency']}",
        "",
        f"**Price** {f(p['last_close'])} ({pc(p['change_pct'])} d/d) · O {f(p['open'])} H {f(p['high'])} L {f(p['low'])}",
        "**Returns** " + " · ".join(f"{k} {pc(x)}" for k, x in s["returns_pct"].items()),
        "",
        f"**Trend: {t['classification']}** (score {t['score']}) · SMA20 {f(t['sma20'])} · SMA50 {f(t['sma50'])} · "
        f"SMA200 {f(t['sma200'])} · EMA20 {f(t['ema20'])} · dist SMA50 {pc(t['dist_from_sma50_pct'])} · "
        f"dist SMA200 {pc(t['dist_from_sma200_pct'])}"
        + (f" · ADX14 {t['adx14']:.1f} (+DI {t['plus_di']:.1f} / -DI {t['minus_di']:.1f})" if t.get("adx14") is not None else ""),
        f"**Momentum** RSI14 {f(mo['rsi14'])} (5 bars ago {f(mo['rsi14_5bars_ago'])}) · MACD {f(mo['macd'])} / "
        f"signal {f(mo['macd_signal'])} / hist {f(mo['macd_hist'])} (prev {f(mo['macd_hist_prev'])}) · ROC10 {pc(mo['roc_10'])}"
        + (f" · Stoch %K {f(mo['stoch_k14'])} %D {f(mo['stoch_d3'])}" if mo.get("stoch_k14") is not None else ""),
        f"**Volatility** BB {f(v['bb_lower'])} / {f(v['bb_middle'])} / {f(v['bb_upper'])} (%B {f(v['bb_percent_b'])}) · "
        f"HV20 {f(v['hist_vol_20_ann_pct'])}% · HV60 {f(v['hist_vol_60_ann_pct'])}% · MaxDD 1y {pc(v['max_drawdown_1y_pct'])}"
        + (f" · ATR14 {f(v['atr14'])} ({v['atr14_pct_of_price']:.2f}% of price)" if v.get("atr14") is not None else ""),
        f"**Levels** 52w high {f(lv['high_52w'])} ({pc(lv['dist_from_52w_high_pct'])}) · 52w low {f(lv['low_52w'])} "
        f"({pc(lv['dist_from_52w_low_pct'])})",
        "Supports: " + (", ".join(f"{f(x['level'])} ({x['touches']}x)" for x in lv["pivot_supports"]) or "none found"),
        "Resistances: " + (", ".join(f"{f(x['level'])} ({x['touches']}x)" for x in lv["pivot_resistances"]) or "none found"),
    ]
    if vo:
        lines.append(f"**Volume** last {f(vo['last_volume'])} · avg20 {f(vo['avg_volume_20'])} · rel {f(vo['rel_volume_vs_20d'])}x · "
                     f"avg traded value 20d {f(vo['avg_traded_value_20d'])} · up/down vol 20 {f(vo['up_down_volume_ratio_20'])}")
    if rel:
        lines.append("**vs benchmark** beta1y " + f(rel.get("beta_1y")) + " · corr " + f(rel.get("corr_1y")) + " · " +
                     " · ".join(f"excess {k.split('_')[1]} {pc(x)}" for k, x in rel.items() if k.startswith("excess_")))
    lines += ["", "**Events**"] + ([f"- {e}" for e in s["events"]] or ["- none"])
    if s["warnings"]:
        lines += ["", "**Data warnings**"] + [f"- {w}" for w in s["warnings"]]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--ticker", default="")
    ap.add_argument("--date", default=date.today().isoformat(), help="analysis date YYYY-MM-DD")
    ap.add_argument("--benchmark-csv")
    ap.add_argument("--locale", default="auto", choices=["auto", "id", "en"])
    ap.add_argument("--out", help="write JSON here")
    ap.add_argument("--md", help="write markdown summary here")
    a = ap.parse_args()

    warnings: list = []
    df = load_prices(a.csv, a.locale, warnings)
    bench = load_prices(a.benchmark_csv, a.locale) if a.benchmark_csv else None
    snap = build_snapshot(df, a.ticker, pd.Timestamp(a.date), bench, warnings)
    js = json.dumps(snap, indent=2, ensure_ascii=False)
    md = to_markdown(snap)
    if a.out:
        with open(a.out, "w") as fh:
            fh.write(js)
    if a.md:
        with open(a.md, "w") as fh:
            fh.write(md)
    print(md)


if __name__ == "__main__":
    main()
