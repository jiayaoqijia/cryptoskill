"""Higher-level analysis: technical snapshot, support/resistance, market regime."""

from __future__ import annotations

from typing import Dict, List, Optional

from . import indicators as ind
from .frame import Bars
from .patterns import swings, trend_template


def _r(x, n=4):
    return None if x is None else round(x, n)


def levels(b: Bars, swing_pct: float = 3.0, max_levels: int = 4, cluster_pct: float = 1.5) -> Dict:
    """Support/resistance from clustered swing pivots, weighted by touches and recency."""
    piv = swings(b.high, b.low, swing_pct)
    price = b.close[-1]
    pts = [(p["price"], p["i"]) for p in piv]
    pts += [(max(b.high[-252:]), len(b) - 1), (min(b.low[-252:]), len(b) - 1)]
    clusters: List[Dict] = []
    for px, i in sorted(pts):
        if clusters and abs(px / clusters[-1]["price"] - 1) * 100 <= cluster_pct:
            c = clusters[-1]
            c["prices"].append(px)
            c["last_i"] = max(c["last_i"], i)
            c["price"] = sum(c["prices"]) / len(c["prices"])
        else:
            clusters.append({"price": px, "prices": [px], "last_i": i})
    n = len(b)
    for c in clusters:
        c["touches"] = len(c["prices"])
        c["strength"] = round(c["touches"] + (c["last_i"] / n) * 2, 2)
    sup = sorted([c for c in clusters if c["price"] < price], key=lambda c: -c["price"])[:max_levels]
    res = sorted([c for c in clusters if c["price"] > price], key=lambda c: c["price"])[:max_levels]
    fmt = lambda cs: [{"price": _r(c["price"]), "touches": c["touches"], "strength": c["strength"],
                       "distance_pct": _r((c["price"] / price - 1) * 100, 2)} for c in cs]
    return {"support": fmt(sup), "resistance": fmt(res)}


def snapshot(b: Bars) -> Dict:
    """Trend, momentum, volatility and volume read-out with a -100..+100 bias score."""
    if len(b) < 30:
        raise ValueError(f"{b.symbol}: need at least 30 bars, have {len(b)}")
    c, h, l, v = b.close, b.high, b.low, b.volume
    price = c[-1]
    s20, s50, s200 = ind.sma(c, 20)[-1], ind.sma(c, 50)[-1], ind.sma(c, 200)[-1]
    e21 = ind.ema(c, 21)[-1]
    s200_prev = ind.sma(c, 200)[-21] if len(c) > 220 else None
    rsi14 = ind.rsi(c, 14)[-1]
    macd_l, macd_s, macd_h = (x[-1] for x in ind.macd(c))
    macd_h_prev = ind.macd(c)[2][-2]
    adx_v, pdi, mdi = (x[-1] for x in ind.adx(h, l, c, 14))
    atr14 = ind.atr(h, l, c, 14)[-1]
    bbw = ind.bbands(c, 20, 2)
    bb_width = None if bbw[0][-1] in (None, 0) else (bbw[1][-1] - bbw[2][-1]) / bbw[0][-1] * 100
    bbw_series = [None if m in (None, 0) or u is None else (u - lo) / m * 100 for m, u, lo in zip(*bbw)]
    bbw_rank = ind.percentile_rank(bbw_series, min(120, len(c) - 20))[-1] if len(c) > 40 else None
    st_line, st_dir = ind.supertrend(h, l, c, 10, 3)
    vol50 = ind.sma(v, 50)[-1] if len(v) >= 50 else None
    rel_vol = v[-1] / vol50 if vol50 else None
    obv_s = ind.obv(c, v)
    obv_slope = ind.slope(obv_s, 20)[-1] if len(obv_s) > 20 and obv_s[-1] else None
    hi52 = max(h[-252:])
    lo52 = min(l[-252:])
    roc = {k: _r(ind.roc(c, n)[-1], 2) for k, n in (("1w", 5), ("1m", 21), ("3m", 63), ("6m", 126), ("12m", 252))
           if len(c) > n}

    score = 0
    reasons: List[str] = []

    def add(pts, why):
        nonlocal score
        score += pts
        reasons.append(f"{'+' if pts > 0 else ''}{pts}: {why}")

    if s200:
        add(15 if price > s200 else -15, f"price {'above' if price > s200 else 'below'} 200-SMA")
        if s200_prev:
            add(10 if s200 > s200_prev else -10, f"200-SMA {'rising' if s200 > s200_prev else 'falling'}")
    if s50:
        add(10 if price > s50 else -10, f"price {'above' if price > s50 else 'below'} 50-SMA")
    if s50 and s200:
        add(10 if s50 > s200 else -10, "50-SMA " + ("above" if s50 > s200 else "below") + " 200-SMA")
    if s20:
        add(5 if price > s20 else -5, f"price {'above' if price > s20 else 'below'} 20-SMA")
    if rsi14 is not None:
        if rsi14 >= 70:
            add(5, f"RSI {rsi14:.0f} strong (overbought zone)")
        elif rsi14 >= 55:
            add(10, f"RSI {rsi14:.0f} bullish momentum")
        elif rsi14 <= 30:
            add(-5, f"RSI {rsi14:.0f} weak (oversold zone)")
        elif rsi14 <= 45:
            add(-10, f"RSI {rsi14:.0f} bearish momentum")
    if macd_h is not None and macd_h_prev is not None:
        add(10 if macd_h > 0 else -10, f"MACD histogram {'positive' if macd_h > 0 else 'negative'}"
            + (" and rising" if macd_h > macd_h_prev else " and falling"))
    if adx_v is not None and pdi is not None:
        if adx_v >= 20:
            add(10 if pdi > mdi else -10, f"ADX {adx_v:.0f} trending {'up' if pdi > mdi else 'down'}")
        else:
            reasons.append(f"0: ADX {adx_v:.0f} - weak trend / range")
    if st_dir[-1] is not None:
        add(5 if st_dir[-1] > 0 else -5, f"Supertrend {'up' if st_dir[-1] > 0 else 'down'}")
    if obv_slope is not None:
        add(5 if obv_slope > 0 else -5, f"OBV {'accumulation' if obv_slope > 0 else 'distribution'} (20 bars)")
    score = max(-100, min(100, score))
    bias = ("strong bullish" if score >= 60 else "bullish" if score >= 25 else "neutral" if score > -25
            else "bearish" if score > -60 else "strong bearish")

    if s50 and s200 and s200_prev:
        if price > s50 > s200 and s200 > s200_prev:
            stage = "stage 2 - advancing"
        elif price < s50 < s200 and s200 < s200_prev:
            stage = "stage 4 - declining"
        elif s200 > s200_prev:
            stage = "stage 3 - topping / choppy" if price < s50 else "stage 2 - advancing (extended?)"
        else:
            stage = "stage 1 - basing" if price > s50 else "stage 4 - declining"
    else:
        stage = "unknown (needs 220+ bars)"

    tt = trend_template(b) if len(b) >= 223 else None
    return {
        "symbol": b.symbol, "date": b.date[-1], "interval": b.interval, "price": _r(price),
        "bias": bias, "score": score, "stage": stage, "reasons": reasons,
        "trend": {"sma20": _r(s20), "sma50": _r(s50), "sma200": _r(s200), "ema21": _r(e21),
                  "adx": _r(adx_v, 1), "plus_di": _r(pdi, 1), "minus_di": _r(mdi, 1),
                  "supertrend": _r(st_line[-1]), "supertrend_dir": st_dir[-1],
                  "trend_template": f"{tt['passed']}/{tt['total']}" if tt else None},
        "momentum": {"rsi14": _r(rsi14, 1), "macd": _r(macd_l), "macd_signal": _r(macd_s), "macd_hist": _r(macd_h),
                     "roc_pct": roc},
        "volatility": {"atr14": _r(atr14), "atr_pct": _r(atr14 / price * 100 if atr14 else None, 2),
                       "bb_width_pct": _r(bb_width, 2), "bb_width_percentile": _r(bbw_rank, 0),
                       "squeeze": bool(bbw_rank is not None and bbw_rank <= 10)},
        "volume": {"last": v[-1], "avg50": _r(vol50, 0), "relative": _r(rel_vol, 2),
                   "obv_trend": None if obv_slope is None else ("up" if obv_slope > 0 else "down")},
        "range_52w": {"high": _r(hi52), "low": _r(lo52), "pct_from_high": _r((price / hi52 - 1) * 100, 2),
                      "pct_from_low": _r((price / lo52 - 1) * 100, 2)},
        "levels": levels(b),
    }


def regime(index: Bars, universe: Optional[Dict[str, Bars]] = None) -> Dict:
    """Classify market regime from an index (and optional breadth universe)."""
    if len(index) < 220:
        raise ValueError("regime needs 220+ daily bars of the index")
    c = index.close
    price = c[-1]
    s50 = ind.sma(c, 50)
    s200 = ind.sma(c, 200)
    e21 = ind.ema(c, 21)[-1]
    s200_up = s200[-1] > s200[-21]
    vol = ind.realized_vol(c, 20)
    vol_rank = ind.percentile_rank(vol, min(252, len(c) - 25))[-1]
    dd = (price / max(index.high[-252:]) - 1) * 100
    roc3 = ind.roc(c, 63)[-1]
    points = 0
    notes = []
    for cond, pts, yes, no in (
        (price > s200[-1], 2, "index above its 200-SMA", "index below its 200-SMA"),
        (s200_up, 1, "200-SMA rising", "200-SMA falling"),
        (price > s50[-1], 1, "index above its 50-SMA", "index below its 50-SMA"),
        (s50[-1] > s200[-1], 1, "50-SMA above 200-SMA", "50-SMA below 200-SMA"),
        (price > e21, 1, "index above its 21-EMA", "index below its 21-EMA"),
        ((roc3 or 0) > 0, 1, "3-month momentum positive", "3-month momentum negative"),
    ):
        points += pts if cond else -pts
        notes.append(f"{'+' if cond else '-'}{pts} {yes if cond else no}")
    breadth = None
    if universe:
        above50 = above200 = highs = lows = valid = 0
        for b in universe.values():
            if len(b) < 210:
                continue
            valid += 1
            cc = b.close
            a50 = ind.sma(cc, 50)[-1]
            a200 = ind.sma(cc, 200)[-1]
            above50 += cc[-1] > a50
            above200 += cc[-1] > a200
            highs += cc[-1] >= max(b.high[-252:]) * 0.98
            lows += cc[-1] <= min(b.low[-252:]) * 1.02
        if valid:
            p50 = above50 / valid * 100
            p200 = above200 / valid * 100
            breadth = {"symbols": valid, "pct_above_sma50": round(p50, 1), "pct_above_sma200": round(p200, 1),
                       "near_52w_highs": highs, "near_52w_lows": lows}
            points += 1 if p50 > 60 else -1 if p50 < 40 else 0
            points += 1 if p200 > 60 else -1 if p200 < 40 else 0
            notes.append(f"{'+1' if p50 > 60 else '-1' if p50 < 40 else ' 0'} {p50:.0f}% of universe above 50-SMA")
            notes.append(f"{'+1' if p200 > 60 else '-1' if p200 < 40 else ' 0'} {p200:.0f}% of universe above 200-SMA")
    hi_vol = vol_rank is not None and vol_rank >= 80
    if points >= 6 and not hi_vol:
        label, exposure = "risk-on uptrend", 100
    elif points >= 4:
        label, exposure = "uptrend, selective" if not hi_vol else "uptrend, volatile", 75
    elif points >= 0:
        label, exposure = "pullback / choppy", 50
    elif points >= -4:
        label, exposure = "correction", 25
    else:
        label, exposure = "downtrend / risk-off", 0
    if hi_vol and exposure > 25:
        exposure -= 25
        notes.append("volatility in the top 20% of the last year: exposure cut one notch")
    return {"index": index.symbol, "date": index.date[-1], "regime": label, "score": points,
            "suggested_exposure_pct": exposure, "drawdown_from_52w_high_pct": round(dd, 2),
            "realized_vol_20d_pct": _r(vol[-1], 2), "vol_percentile_1y": _r(vol_rank, 0),
            "momentum_3m_pct": _r(roc3, 2), "breadth": breadth, "notes": notes}
