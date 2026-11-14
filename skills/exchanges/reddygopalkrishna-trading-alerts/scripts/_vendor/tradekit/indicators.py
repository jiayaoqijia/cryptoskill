"""Technical indicators on plain Python lists.

Every function returns a list the same length as its input, padded with None
during warm-up. None propagates: any calculation touching None yields None.
Formulas follow the standard definitions (Wilder smoothing for RSI/ATR/ADX).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

Series = List[Optional[float]]


def _n(n) -> int:
    n = int(n)
    if n < 1:
        raise ValueError("period must be >= 1")
    return n


# ------------------------------------------------------------------ averages

def sma(x: Sequence[Optional[float]], n: int) -> Series:
    n = _n(n)
    out: Series = [None] * len(x)
    s = 0.0
    count = 0
    window: List[Optional[float]] = []
    for i, v in enumerate(x):
        window.append(v)
        if v is not None:
            s += v
            count += 1
        if len(window) > n:
            old = window.pop(0)
            if old is not None:
                s -= old
                count -= 1
        if len(window) == n and count == n:
            out[i] = s / n
    return out


def ema(x: Sequence[Optional[float]], n: int) -> Series:
    """EMA seeded with the SMA of the first n valid values."""
    n = _n(n)
    out: Series = [None] * len(x)
    k = 2.0 / (n + 1)
    prev = None
    seed: List[float] = []
    for i, v in enumerate(x):
        if v is None:
            if prev is not None:
                out[i] = None
            continue
        if prev is None:
            seed.append(v)
            if len(seed) == n:
                prev = sum(seed) / n
                out[i] = prev
        else:
            prev = v * k + prev * (1 - k)
            out[i] = prev
    return out


def rma(x: Sequence[Optional[float]], n: int) -> Series:
    """Wilder's moving average (alpha = 1/n), seeded with SMA."""
    n = _n(n)
    out: Series = [None] * len(x)
    prev = None
    seed: List[float] = []
    for i, v in enumerate(x):
        if v is None:
            continue
        if prev is None:
            seed.append(v)
            if len(seed) == n:
                prev = sum(seed) / n
                out[i] = prev
        else:
            prev = (prev * (n - 1) + v) / n
            out[i] = prev
    return out


def wma(x: Sequence[Optional[float]], n: int) -> Series:
    n = _n(n)
    out: Series = [None] * len(x)
    denom = n * (n + 1) / 2
    for i in range(n - 1, len(x)):
        w = x[i - n + 1:i + 1]
        if any(v is None for v in w):
            continue
        out[i] = sum(v * (j + 1) for j, v in enumerate(w)) / denom
    return out


# ------------------------------------------------------------------ dispersion

def stdev(x: Sequence[Optional[float]], n: int) -> Series:
    """Population standard deviation over a rolling window (as used by Bollinger Bands)."""
    n = _n(n)
    out: Series = [None] * len(x)
    for i in range(n - 1, len(x)):
        w = x[i - n + 1:i + 1]
        if any(v is None for v in w):
            continue
        m = sum(w) / n
        out[i] = math.sqrt(sum((v - m) ** 2 for v in w) / n)
    return out


def bbands(x: Sequence[Optional[float]], n: int = 20, k: float = 2.0) -> Tuple[Series, Series, Series]:
    mid = sma(x, n)
    sd = stdev(x, n)
    up = [None if m is None or s is None else m + k * s for m, s in zip(mid, sd)]
    lo = [None if m is None or s is None else m - k * s for m, s in zip(mid, sd)]
    return mid, up, lo


def zscore(x: Sequence[Optional[float]], n: int) -> Series:
    m = sma(x, n)
    sd = stdev(x, n)
    return [None if v is None or a is None or s in (None, 0) else (v - a) / s for v, a, s in zip(x, m, sd)]


# ------------------------------------------------------------------ momentum

def rsi(close: Sequence[Optional[float]], n: int = 14) -> Series:
    n = _n(n)
    gains: Series = [None]
    losses: Series = [None]
    for i in range(1, len(close)):
        a, b = close[i - 1], close[i]
        if a is None or b is None:
            gains.append(None)
            losses.append(None)
            continue
        d = b - a
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    ag = rma(gains, n)
    al = rma(losses, n)
    out: Series = []
    for g, l in zip(ag, al):
        if g is None or l is None:
            out.append(None)
        elif l == 0:
            out.append(100.0 if g > 0 else 50.0)
        else:
            out.append(100.0 - 100.0 / (1.0 + g / l))
    return out


def roc(x: Sequence[Optional[float]], n: int) -> Series:
    """Rate of change in percent."""
    n = _n(n)
    out: Series = [None] * len(x)
    for i in range(n, len(x)):
        a, b = x[i - n], x[i]
        if a is None or b is None or a == 0:
            continue
        out[i] = (b / a - 1.0) * 100.0
    return out


def change(x: Sequence[Optional[float]], n: int = 1) -> Series:
    out: Series = [None] * len(x)
    for i in range(n, len(x)):
        if x[i] is not None and x[i - n] is not None:
            out[i] = x[i] - x[i - n]
    return out


def macd(close: Sequence[Optional[float]], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[Series, Series, Series]:
    ef = ema(close, fast)
    es = ema(close, slow)
    line = [None if a is None or b is None else a - b for a, b in zip(ef, es)]
    sig = ema(line, signal)
    hist = [None if a is None or b is None else a - b for a, b in zip(line, sig)]
    return line, sig, hist


def stoch(high, low, close, n: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> Tuple[Series, Series]:
    n = _n(n)
    raw: Series = [None] * len(close)
    for i in range(n - 1, len(close)):
        hh = max(high[i - n + 1:i + 1])
        ll = min(low[i - n + 1:i + 1])
        raw[i] = 50.0 if hh == ll else (close[i] - ll) / (hh - ll) * 100.0
    k = sma(raw, smooth_k)
    d = sma(k, smooth_d)
    return k, d


def cci(high, low, close, n: int = 20) -> Series:
    tp = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    m = sma(tp, n)
    out: Series = [None] * len(tp)
    for i in range(n - 1, len(tp)):
        if m[i] is None:
            continue
        md = sum(abs(v - m[i]) for v in tp[i - n + 1:i + 1]) / n
        out[i] = 0.0 if md == 0 else (tp[i] - m[i]) / (0.015 * md)
    return out


def mfi(high, low, close, volume, n: int = 14) -> Series:
    tp = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    out: Series = [None] * len(tp)
    for i in range(n, len(tp)):
        pos = neg = 0.0
        for j in range(i - n + 1, i + 1):
            flow = tp[j] * volume[j]
            if tp[j] > tp[j - 1]:
                pos += flow
            elif tp[j] < tp[j - 1]:
                neg += flow
        out[i] = 100.0 if neg == 0 else 100.0 - 100.0 / (1.0 + pos / neg)
    return out


# ------------------------------------------------------------------ volatility / trend

def true_range(high, low, close) -> Series:
    out: Series = []
    for i in range(len(close)):
        if i == 0:
            out.append(high[0] - low[0])
        else:
            pc = close[i - 1]
            out.append(max(high[i] - low[i], abs(high[i] - pc), abs(low[i] - pc)))
    return out


def atr(high, low, close, n: int = 14) -> Series:
    return rma(true_range(high, low, close), n)


def adx(high, low, close, n: int = 14) -> Tuple[Series, Series, Series]:
    """Returns (adx, +DI, -DI)."""
    plus_dm: Series = [None]
    minus_dm: Series = [None]
    for i in range(1, len(close)):
        up = high[i] - high[i - 1]
        dn = low[i - 1] - low[i]
        plus_dm.append(up if up > dn and up > 0 else 0.0)
        minus_dm.append(dn if dn > up and dn > 0 else 0.0)
    tr = true_range(high, low, close)
    tr[0] = None
    atr_ = rma(tr, n)
    pdm = rma(plus_dm, n)
    mdm = rma(minus_dm, n)
    pdi: Series = []
    mdi: Series = []
    dx: Series = []
    for a, p, m in zip(atr_, pdm, mdm):
        if a in (None, 0) or p is None or m is None:
            pdi.append(None)
            mdi.append(None)
            dx.append(None)
            continue
        pv = 100.0 * p / a
        mv = 100.0 * m / a
        pdi.append(pv)
        mdi.append(mv)
        dx.append(0.0 if pv + mv == 0 else 100.0 * abs(pv - mv) / (pv + mv))
    return rma(dx, n), pdi, mdi


def supertrend(high, low, close, n: int = 10, mult: float = 3.0) -> Tuple[Series, Series]:
    """Returns (line, direction) where direction is +1 (up) or -1 (down)."""
    a = atr(high, low, close, n)
    line: Series = [None] * len(close)
    direction: Series = [None] * len(close)
    fub = flb = None
    prev_dir = 1
    for i in range(len(close)):
        if a[i] is None:
            continue
        hl2 = (high[i] + low[i]) / 2
        ub = hl2 + mult * a[i]
        lb = hl2 - mult * a[i]
        if fub is None:
            fub, flb = ub, lb
        else:
            fub = ub if (ub < fub or close[i - 1] > fub) else fub
            flb = lb if (lb > flb or close[i - 1] < flb) else flb
        if prev_dir == 1 and close[i] < flb:
            d = -1
        elif prev_dir == -1 and close[i] > fub:
            d = 1
        else:
            d = prev_dir
        direction[i] = d
        line[i] = flb if d == 1 else fub
        prev_dir = d
    return line, direction


def keltner(high, low, close, n: int = 20, mult: float = 1.5, atr_n: int = 10) -> Tuple[Series, Series, Series]:
    mid = ema(close, n)
    a = atr(high, low, close, atr_n)
    up = [None if m is None or v is None else m + mult * v for m, v in zip(mid, a)]
    lo = [None if m is None or v is None else m - mult * v for m, v in zip(mid, a)]
    return mid, up, lo


# ------------------------------------------------------------------ windows

def highest(x: Sequence[Optional[float]], n: int) -> Series:
    n = _n(n)
    out: Series = [None] * len(x)
    for i in range(n - 1, len(x)):
        w = [v for v in x[i - n + 1:i + 1] if v is not None]
        if len(w) == n:
            out[i] = max(w)
    return out


def lowest(x: Sequence[Optional[float]], n: int) -> Series:
    n = _n(n)
    out: Series = [None] * len(x)
    for i in range(n - 1, len(x)):
        w = [v for v in x[i - n + 1:i + 1] if v is not None]
        if len(w) == n:
            out[i] = min(w)
    return out


def shift(x: Sequence[Optional[float]], n: int = 1) -> Series:
    n = int(n)
    if n == 0:
        return list(x)
    if n > 0:
        return [None] * n + list(x[:-n]) if n < len(x) else [None] * len(x)
    return list(x[-n:]) + [None] * (-n)


def slope(x: Sequence[Optional[float]], n: int) -> Series:
    """Least-squares slope over n bars, as percent of the latest value per bar."""
    n = _n(n)
    out: Series = [None] * len(x)
    xs = list(range(n))
    mx = (n - 1) / 2
    sxx = sum((i - mx) ** 2 for i in xs) or 1.0
    for i in range(n - 1, len(x)):
        w = x[i - n + 1:i + 1]
        if any(v is None for v in w) or not w[-1]:
            continue
        my = sum(w) / n
        sxy = sum((xs[j] - mx) * (w[j] - my) for j in range(n))
        out[i] = (sxy / sxx) / w[-1] * 100.0
    return out


def obv(close, volume) -> Series:
    out: Series = [0.0] if close else []
    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            out.append(out[-1] + volume[i])
        elif close[i] < close[i - 1]:
            out.append(out[-1] - volume[i])
        else:
            out.append(out[-1])
    return out


def vwap(high, low, close, volume, dates: Sequence[str]) -> Series:
    """Session VWAP for intraday bars (resets each calendar day). Cumulative for daily bars."""
    out: Series = []
    pv = vv = 0.0
    day = None
    for h, l, c, v, d in zip(high, low, close, volume, dates):
        if "T" in d and d[:10] != day:
            pv = vv = 0.0
            day = d[:10]
        tp = (h + l + c) / 3
        pv += tp * v
        vv += v
        out.append(pv / vv if vv else tp)
    return out


def crossed_above(a: Sequence[Optional[float]], b: Sequence[Optional[float]]) -> List[bool]:
    out = [False] * len(a)
    for i in range(1, len(a)):
        if None in (a[i], b[i], a[i - 1], b[i - 1]):
            continue
        out[i] = a[i - 1] <= b[i - 1] and a[i] > b[i]
    return out


def crossed_below(a: Sequence[Optional[float]], b: Sequence[Optional[float]]) -> List[bool]:
    out = [False] * len(a)
    for i in range(1, len(a)):
        if None in (a[i], b[i], a[i - 1], b[i - 1]):
            continue
        out[i] = a[i - 1] >= b[i - 1] and a[i] < b[i]
    return out


def percentile_rank(x: Sequence[Optional[float]], n: int) -> Series:
    """Percent of the last n values that are below the current value (0-100)."""
    n = _n(n)
    out: Series = [None] * len(x)
    for i in range(n - 1, len(x)):
        w = [v for v in x[i - n + 1:i + 1] if v is not None]
        if len(w) < n or x[i] is None:
            continue
        out[i] = 100.0 * sum(1 for v in w if v < x[i]) / (n - 1 if n > 1 else 1)
    return out


def realized_vol(close: Sequence[float], n: int = 20, periods_per_year: int = 252) -> Series:
    rets: Series = [None]
    for i in range(1, len(close)):
        rets.append(math.log(close[i] / close[i - 1]) if close[i - 1] else None)
    sd = stdev(rets, n)
    return [None if s is None else s * math.sqrt(periods_per_year) * 100.0 for s in sd]


def last_valid(x: Sequence[Optional[float]]) -> Optional[float]:
    for v in reversed(x):
        if v is not None:
            return v
    return None
