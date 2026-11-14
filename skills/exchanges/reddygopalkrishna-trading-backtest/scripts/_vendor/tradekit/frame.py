"""Bars: a tiny columnar OHLCV container (no pandas needed)."""

from __future__ import annotations

import csv
import datetime as dt
import io
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

FIELDS = ("date", "open", "high", "low", "close", "volume")

_DATE_KEYS = ("date", "datetime", "timestamp", "time", "dt")
_ALIASES = {
    "o": "open", "h": "high", "l": "low", "c": "close", "v": "volume",
    "vol": "volume", "last": "close", "price": "close",
}


class Bars:
    """Columnar OHLCV series sorted by date ascending.

    Dates are ISO strings: "YYYY-MM-DD" for daily+ bars, "YYYY-MM-DDTHH:MM" intraday.
    """

    __slots__ = ("symbol", "interval", "date", "open", "high", "low", "close", "volume", "meta")

    def __init__(self, symbol: str, interval: str, date: List[str], open: List[float],
                 high: List[float], low: List[float], close: List[float],
                 volume: List[float], meta: Optional[Dict] = None):
        n = len(date)
        for name, col in (("open", open), ("high", high), ("low", low), ("close", close), ("volume", volume)):
            if len(col) != n:
                raise ValueError(f"column {name} has {len(col)} rows, expected {n}")
        self.symbol = symbol
        self.interval = interval
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.meta = meta or {}

    # ------------------------------------------------------------ basics
    def __len__(self) -> int:
        return len(self.date)

    def __repr__(self) -> str:
        rng = f"{self.date[0]}..{self.date[-1]}" if self.date else "empty"
        return f"Bars({self.symbol}, {self.interval}, {len(self)} bars, {rng})"

    def col(self, name: str) -> List[float]:
        name = name.lower()
        if name in ("open", "high", "low", "close", "volume"):
            return getattr(self, name)
        if name == "hl2":
            return [(h + l) / 2 for h, l in zip(self.high, self.low)]
        if name == "hlc3":
            return [(h + l + c) / 3 for h, l, c in zip(self.high, self.low, self.close)]
        if name == "ohlc4":
            return [(o + h + l + c) / 4 for o, h, l, c in zip(self.open, self.high, self.low, self.close)]
        raise KeyError(name)

    def slice(self, start: int = 0, end: Optional[int] = None) -> "Bars":
        s = slice(start, end)
        return Bars(self.symbol, self.interval, self.date[s], self.open[s], self.high[s],
                    self.low[s], self.close[s], self.volume[s], dict(self.meta))

    def tail(self, n: int) -> "Bars":
        return self.slice(max(0, len(self) - n))

    def since(self, date: str) -> "Bars":
        i = next((k for k, d in enumerate(self.date) if d >= date), len(self))
        return self.slice(i)

    def until(self, date: str) -> "Bars":
        i = next((k for k, d in enumerate(self.date) if d > date), len(self))
        return self.slice(0, i)

    def last(self) -> Dict[str, float]:
        if not self.date:
            raise IndexError("no bars")
        return {f: getattr(self, f)[-1] for f in FIELDS}

    def rows(self) -> List[Dict]:
        return [{f: getattr(self, f)[i] for f in FIELDS} for i in range(len(self))]

    @property
    def intraday(self) -> bool:
        return bool(self.date) and "T" in self.date[-1]

    # ------------------------------------------------------------ construction
    @classmethod
    def from_rows(cls, symbol: str, interval: str, rows: Iterable[Dict], meta: Optional[Dict] = None) -> "Bars":
        clean: Dict[str, Dict] = {}
        for r in rows:
            try:
                d = normalize_date(r["date"])
                o, h, l, c = (float(r[k]) for k in ("open", "high", "low", "close"))
            except (KeyError, TypeError, ValueError):
                continue
            if c != c or c <= 0:  # NaN or non-positive
                continue
            v = r.get("volume")
            try:
                v = float(v) if v not in (None, "") else 0.0
            except ValueError:
                v = 0.0
            h = max(h, o, c)
            l = min(l, o, c)
            clean[d] = {"date": d, "open": o, "high": h, "low": l, "close": c, "volume": v}
        ordered = [clean[k] for k in sorted(clean)]
        return cls(symbol, interval, [r["date"] for r in ordered], [r["open"] for r in ordered],
                   [r["high"] for r in ordered], [r["low"] for r in ordered],
                   [r["close"] for r in ordered], [r["volume"] for r in ordered], meta)

    @classmethod
    def from_csv(cls, path_or_text, symbol: Optional[str] = None, interval: str = "1d") -> "Bars":
        if isinstance(path_or_text, Path) or (isinstance(path_or_text, str) and "\n" not in path_or_text):
            p = Path(path_or_text)
            text = p.read_text()
            symbol = symbol or p.stem.upper()
        else:
            text = path_or_text
        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        mapping = {}
        for name in reader.fieldnames:
            key = name.strip().lower().replace(" ", "_")
            if key in _DATE_KEYS:
                mapping[name] = "date"
            elif key in ("open", "high", "low", "close", "volume"):
                mapping[name] = key
            elif key in _ALIASES:
                mapping[name] = _ALIASES[key]
        if "date" not in mapping.values() or "close" not in mapping.values():
            raise ValueError(f"CSV needs date and close columns, got {reader.fieldnames}")
        rows = []
        for raw in reader:
            r = {mapping[k]: v for k, v in raw.items() if k in mapping}
            for f in ("open", "high", "low"):
                r.setdefault(f, r.get("close"))
            rows.append(r)
        return cls.from_rows(symbol or "UNKNOWN", interval, rows)

    def to_csv(self, path: Optional[Path] = None) -> str:
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(FIELDS)
        for i in range(len(self)):
            w.writerow([self.date[i], _fmt(self.open[i]), _fmt(self.high[i]), _fmt(self.low[i]),
                        _fmt(self.close[i]), _fmt(self.volume[i])])
        text = buf.getvalue()
        if path is not None:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(text)
        return text

    # ------------------------------------------------------------ resampling
    def resample(self, rule: str) -> "Bars":
        """Resample daily bars to weekly ("1wk") or monthly ("1mo")."""
        if rule not in ("1wk", "1mo"):
            raise ValueError("rule must be 1wk or 1mo")
        groups: Dict[str, List[int]] = {}
        order: List[str] = []
        for i, d in enumerate(self.date):
            day = dt.date.fromisoformat(d[:10])
            if rule == "1wk":
                y, w, _ = day.isocalendar()
                key = f"{y}-W{w:02d}"
            else:
                key = d[:7]
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(i)
        rows = []
        for key in order:
            idx = groups[key]
            rows.append({
                "date": self.date[idx[-1]][:10],
                "open": self.open[idx[0]],
                "high": max(self.high[i] for i in idx),
                "low": min(self.low[i] for i in idx),
                "close": self.close[idx[-1]],
                "volume": sum(self.volume[i] for i in idx),
            })
        return Bars.from_rows(self.symbol, rule, rows, dict(self.meta))


def normalize_date(value) -> str:
    """Accept ISO strings, epoch seconds/millis, or date/datetime objects."""
    if isinstance(value, dt.datetime):
        return value.strftime("%Y-%m-%dT%H:%M") if (value.hour or value.minute) else value.strftime("%Y-%m-%d")
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, (int, float)):
        ts = float(value)
        if ts > 1e11:
            ts /= 1000.0
        d = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
        return normalize_date(d.replace(tzinfo=None))
    s = str(value).strip()
    if s.isdigit() and len(s) >= 9:
        return normalize_date(int(s))
    s = s.replace("/", "-")
    if len(s) >= 16 and (s[10] in ("T", " ")):
        base = s[:10] + "T" + s[11:16]
        return base[:10] if base.endswith("T00:00") else base
    if len(s) >= 10:
        # support DD-MM-YYYY
        if s[2] == "-" and s[5] == "-":
            return f"{s[6:10]}-{s[3:5]}-{s[0:2]}"
        return s[:10]
    raise ValueError(f"unrecognized date {value!r}")


def _fmt(x: float) -> str:
    if x is None:
        return ""
    if float(x).is_integer():
        return str(int(x))
    return f"{x:.6f}".rstrip("0").rstrip(".")


def align(series: Sequence[Bars]) -> List[str]:
    """Sorted union of all dates."""
    s = set()
    for b in series:
        s.update(b.date)
    return sorted(s)
