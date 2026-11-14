"""Chart pattern detectors on daily (or any) bars.

Each detector returns None or a dict:
    {pattern, score 0-100, pivot (trigger price), stop (invalidation), date, details}
Detectors look at the most recent bars - they answer "is this pattern live now?".
Heuristics are transparent and parameterised; they are aids, not oracles.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from . import indicators as ind
from .frame import Bars


def swings(high: List[float], low: List[float], pct: float = 5.0) -> List[Dict]:
    """ZigZag pivots: alternating swing highs/lows that reverse by at least pct%."""
    if not high:
        return []
    piv: List[Dict] = []
    trend = 0
    hi_i, lo_i = 0, 0
    for i in range(1, len(high)):
        if high[i] > high[hi_i]:
            hi_i = i
        if low[i] < low[lo_i]:
            lo_i = i
        if trend >= 0 and low[i] <= high[hi_i] * (1 - pct / 100) and hi_i < i:
            if trend == 0 or not piv or piv[-1]["type"] != "H":
                piv.append({"type": "H", "i": hi_i, "price": high[hi_i]})
            trend = -1
            lo_i = i
        elif trend <= 0 and high[i] >= low[lo_i] * (1 + pct / 100) and lo_i < i:
            if trend == 0 or not piv or piv[-1]["type"] != "L":
                piv.append({"type": "L", "i": lo_i, "price": low[lo_i]})
            trend = 1
            hi_i = i
    return piv


def _avg(x: List[float]) -> float:
    return sum(x) / len(x) if x else 0.0


def trend_template(b: Bars) -> Dict:
    """Minervini-style stage-2 trend template checks."""
    c = b.close
    s50, s150, s200 = ind.sma(c, 50), ind.sma(c, 150), ind.sma(c, 200)
    n = len(c)
    hi = max(b.high[-252:]) if n else None
    lo = min(b.low[-252:]) if n else None
    last = c[-1] if n else None
    checks = {}
    if s200[-1] is not None and n > 222 and s200[-22] is not None:
        checks["price_above_150_200"] = last > s150[-1] and last > s200[-1]
        checks["sma150_above_sma200"] = s150[-1] > s200[-1]
        checks["sma200_rising_1m"] = s200[-1] > s200[-22]
        checks["sma50_above_150_200"] = s50[-1] > s150[-1] and s50[-1] > s200[-1]
        checks["price_above_sma50"] = last > s50[-1]
        checks["30pct_above_52w_low"] = last >= lo * 1.30
        checks["within_25pct_of_52w_high"] = last >= hi * 0.75
    passed = sum(1 for v in checks.values() if v)
    return {"passed": passed, "total": len(checks), "ok": bool(checks) and passed == len(checks), "checks": checks}


def vcp(b: Bars, lookback: int = 120, swing_pct: float = 4.0) -> Optional[Dict]:
    """Volatility contraction pattern: >=2 successively shallower pullbacks, volume drying up."""
    if len(b) < 210:
        return None
    tt = trend_template(b)
    if tt["passed"] < tt["total"] - 1:
        return None
    seg = b.tail(lookback)
    piv = swings(seg.high, seg.low, swing_pct)
    # pair each swing high with the following swing low -> contraction depth
    contractions = []
    for k in range(len(piv) - 1):
        if piv[k]["type"] == "H" and piv[k + 1]["type"] == "L":
            depth = (piv[k]["price"] - piv[k + 1]["price"]) / piv[k]["price"] * 100
            contractions.append({"high_i": piv[k]["i"], "high": piv[k]["price"], "low": piv[k + 1]["price"],
                                 "depth_pct": round(depth, 2)})
    # include the current, still-forming contraction from the last swing high
    if piv and piv[-1]["type"] == "H":
        low_since = min(seg.low[piv[-1]["i"]:])
        contractions.append({"high_i": piv[-1]["i"], "high": piv[-1]["price"], "low": low_since,
                             "depth_pct": round((piv[-1]["price"] - low_since) / piv[-1]["price"] * 100, 2)})
    if len(contractions) < 2:
        return None
    tail = contractions[-4:]
    shrinking = all(tail[i + 1]["depth_pct"] < tail[i]["depth_pct"] for i in range(len(tail) - 1))
    if not shrinking:
        # allow one violation if the overall trend is contracting strongly
        if not (tail[-1]["depth_pct"] < tail[0]["depth_pct"] * 0.5):
            return None
    last_c = tail[-1]
    if last_c["depth_pct"] > 12:
        return None
    vol50 = _avg(b.volume[-50:])
    vol10 = _avg(b.volume[-10:])
    dry = vol50 > 0 and vol10 < vol50 * 0.8
    pivot = last_c["high"]
    price = b.close[-1]
    dist = (pivot / price - 1) * 100
    if dist > 8 or price > pivot * 1.05:
        return None
    score = 40 + 10 * min(len(tail), 4) + (15 if dry else 0) + (10 if tt["ok"] else 0) - max(0, dist - 3) * 2
    return {"pattern": "vcp", "score": int(max(0, min(100, score))), "pivot": round(pivot, 4),
            "stop": round(last_c["low"], 4), "date": b.date[-1],
            "details": {"contractions_pct": [c["depth_pct"] for c in tail], "volume_dry_up": dry,
                        "volume_10_vs_50": round(vol10 / vol50, 2) if vol50 else None,
                        "distance_to_pivot_pct": round(dist, 2), "trend_template": f"{tt['passed']}/{tt['total']}"}}


def breakout(b: Bars, n: int = 20, vol_mult: float = 1.5) -> Optional[Dict]:
    """Close at a new n-bar high on above-average volume (today)."""
    if len(b) < max(n, 50) + 1:
        return None
    prior_high = max(b.high[-n - 1:-1])
    vol_avg = _avg(b.volume[-51:-1])
    c = b.close[-1]
    if c <= prior_high:
        return None
    rv = b.volume[-1] / vol_avg if vol_avg else 0
    if rv < vol_mult:
        return None
    a = ind.atr(b.high, b.low, b.close, 14)[-1] or (c * 0.02)
    score = 50 + min(30, (rv - vol_mult) * 15) + (10 if c > (ind.sma(b.close, 50)[-1] or c) else 0)
    close_pos = (c - b.low[-1]) / (b.high[-1] - b.low[-1]) if b.high[-1] > b.low[-1] else 1
    score += 10 if close_pos > 0.7 else -10
    return {"pattern": "breakout", "score": int(max(0, min(100, score))), "pivot": round(prior_high, 4),
            "stop": round(min(b.low[-1], c - 1.5 * a), 4), "date": b.date[-1],
            "details": {"lookback": n, "relative_volume": round(rv, 2), "close_in_range": round(close_pos, 2),
                        "breakout_pct": round((c / prior_high - 1) * 100, 2)}}


def bull_flag(b: Bars, pole_bars: int = 15, min_pole_pct: float = 15.0, max_flag_bars: int = 15,
              max_retrace: float = 0.5) -> Optional[Dict]:
    """Sharp advance (pole) followed by a tight, low-volume pullback (flag)."""
    if len(b) < pole_bars + max_flag_bars + 50:
        return None
    best = None
    for flag_len in range(3, max_flag_bars + 1):
        flag_start = len(b) - flag_len
        pole_end = flag_start - 1
        pole_seg_low = min(b.low[pole_end - pole_bars:pole_end + 1])
        pole_top = max(b.high[pole_end - 2:flag_start + 1])
        gain = (pole_top / pole_seg_low - 1) * 100
        if gain < min_pole_pct:
            continue
        flag_low = min(b.low[flag_start:])
        flag_high = max(b.high[flag_start:])
        if flag_high > pole_top * 1.01:
            continue
        retrace = (pole_top - flag_low) / (pole_top - pole_seg_low)
        if retrace > max_retrace:
            continue
        pole_vol = _avg(b.volume[pole_end - pole_bars:pole_end + 1])
        flag_vol = _avg(b.volume[flag_start:])
        vol_ok = pole_vol > 0 and flag_vol < pole_vol
        score = 45 + min(25, gain - min_pole_pct) + (15 if vol_ok else 0) + (15 if retrace < 0.33 else 0)
        cand = {"pattern": "bull_flag", "score": int(min(100, score)), "pivot": round(flag_high, 4),
                "stop": round(flag_low, 4), "date": b.date[-1],
                "details": {"pole_gain_pct": round(gain, 2), "flag_bars": flag_len, "retrace": round(retrace, 2),
                            "flag_volume_vs_pole": round(flag_vol / pole_vol, 2) if pole_vol else None}}
        if best is None or cand["score"] > best["score"]:
            best = cand
    return best


def cup_handle(b: Bars, min_cup: int = 30, max_cup: int = 150, min_depth: float = 12.0,
               max_depth: float = 35.0) -> Optional[Dict]:
    """Rounded base with a shallow handle in the upper half; pivot = handle high."""
    if len(b) < max_cup + 20:
        return None
    n = len(b)
    best = None
    for handle_len in range(5, 21):
        h_start = n - handle_len
        handle_high = max(b.high[h_start:])
        handle_low = min(b.low[h_start:])
        for cup_len in range(min_cup, max_cup + 1, 5):
            left_i = h_start - cup_len
            if left_i < 0:
                break
            left_peak = max(b.high[left_i:left_i + 5])
            cup_seg_low = min(b.low[left_i:h_start])
            depth = (left_peak - cup_seg_low) / left_peak * 100
            if not (min_depth <= depth <= max_depth):
                continue
            right_peak = max(b.high[h_start - 10:h_start + 1])
            if right_peak < left_peak * 0.95 or right_peak > left_peak * 1.05:
                continue
            mid = (left_peak + cup_seg_low) / 2
            if handle_low < mid:
                continue
            handle_depth = (handle_high - handle_low) / handle_high * 100
            if handle_depth > 12:
                continue
            bottom_i = left_i + min(range(cup_len), key=lambda k: b.low[left_i + k])
            roundness = 1 - abs((bottom_i - left_i) / cup_len - 0.5) * 2  # 1 = centred bottom
            if roundness < 0.3:
                continue
            score = 50 + roundness * 20 + (15 if handle_depth < 8 else 5) + (10 if b.close[-1] > mid else 0)
            cand = {"pattern": "cup_handle", "score": int(min(100, score)), "pivot": round(handle_high, 4),
                    "stop": round(handle_low, 4), "date": b.date[-1],
                    "details": {"cup_bars": cup_len, "cup_depth_pct": round(depth, 2), "handle_bars": handle_len,
                                "handle_depth_pct": round(handle_depth, 2), "roundness": round(roundness, 2)}}
            if best is None or cand["score"] > best["score"]:
                best = cand
    return best


def double_bottom(b: Bars, lookback: int = 120, tolerance_pct: float = 3.0, swing_pct: float = 5.0) -> Optional[Dict]:
    seg = b.tail(lookback)
    piv = swings(seg.high, seg.low, swing_pct)
    lows = [p for p in piv if p["type"] == "L"]
    if len(lows) < 2:
        return None
    l1, l2 = lows[-2], lows[-1]
    if l2["i"] - l1["i"] < 10:
        return None
    if abs(l2["price"] / l1["price"] - 1) * 100 > tolerance_pct:
        return None
    neck = max(seg.high[l1["i"]:l2["i"] + 1])
    if neck < max(l1["price"], l2["price"]) * 1.05:
        return None
    c = seg.close[-1]
    if c < l2["price"] or c > neck * 1.05:
        return None
    score = 55 + (15 if seg.volume[l2["i"]] < seg.volume[l1["i"]] else 0) + (15 if c > (neck + l2["price"]) / 2 else 0)
    return {"pattern": "double_bottom", "score": int(min(100, score)), "pivot": round(neck, 4),
            "stop": round(min(l1["price"], l2["price"]) * 0.99, 4), "date": b.date[-1],
            "details": {"low1": round(l1["price"], 4), "low2": round(l2["price"], 4), "bars_apart": l2["i"] - l1["i"]}}


def inside_bar(b: Bars) -> Optional[Dict]:
    if len(b) < 3:
        return None
    if b.high[-1] < b.high[-2] and b.low[-1] > b.low[-2]:
        return {"pattern": "inside_bar", "score": 50, "pivot": round(b.high[-2], 4), "stop": round(b.low[-2], 4),
                "date": b.date[-1], "details": {"mother_range": round(b.high[-2] - b.low[-2], 4)}}
    return None


def nr7(b: Bars) -> Optional[Dict]:
    if len(b) < 8:
        return None
    ranges = [h - l for h, l in zip(b.high[-7:], b.low[-7:])]
    if ranges[-1] == min(ranges) and ranges.count(ranges[-1]) == 1:
        return {"pattern": "nr7", "score": 50, "pivot": round(b.high[-1], 4), "stop": round(b.low[-1], 4),
                "date": b.date[-1], "details": {"range": round(ranges[-1], 4), "note": "narrowest range of 7 bars"}}
    return None


def pocket_pivot(b: Bars) -> Optional[Dict]:
    """Up-day volume greater than the largest down-day volume of the prior 10 bars."""
    if len(b) < 60:
        return None
    if b.close[-1] <= b.close[-2]:
        return None
    downs = [b.volume[i] for i in range(len(b) - 11, len(b) - 1) if b.close[i] < b.close[i - 1]]
    if not downs or b.volume[-1] <= max(downs):
        return None
    s50 = ind.sma(b.close, 50)[-1]
    if s50 is None or b.close[-1] < s50:
        return None
    return {"pattern": "pocket_pivot", "score": 60, "pivot": round(b.high[-1], 4), "stop": round(b.low[-1], 4),
            "date": b.date[-1], "details": {"volume_vs_max_down": round(b.volume[-1] / max(downs), 2)}}


DETECTORS = {
    "vcp": vcp, "breakout": breakout, "bull_flag": bull_flag, "cup_handle": cup_handle,
    "double_bottom": double_bottom, "inside_bar": inside_bar, "nr7": nr7, "pocket_pivot": pocket_pivot,
}


def scan(b: Bars, which: Optional[List[str]] = None) -> List[Dict]:
    out = []
    for name in which or DETECTORS:
        fn = DETECTORS.get(name)
        if not fn:
            raise ValueError(f"unknown pattern {name}; available: {', '.join(DETECTORS)}")
        try:
            r = fn(b)
        except (ValueError, ZeroDivisionError, IndexError):
            r = None
        if r:
            r["symbol"] = b.symbol
            out.append(r)
    return sorted(out, key=lambda r: r["score"], reverse=True)
