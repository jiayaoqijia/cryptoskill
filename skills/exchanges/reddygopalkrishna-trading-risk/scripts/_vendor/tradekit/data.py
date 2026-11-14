"""Market data providers with a local cache.

Providers
    yahoo  Free, no API key. Unofficial Yahoo Finance chart endpoint. Covers most
           global stocks, ETFs, indices (^GSPC), FX (EURUSD=X), crypto (BTC-USD).
           Exchange suffixes follow Yahoo conventions (e.g. .L, .TO, .NS, .T, .HK).
           Data can be delayed, adjusted or rate limited - verify before trading.
    csv    Your own files: <csv_dir>/<SYMBOL>.csv with date,open,high,low,close,volume.
    kite   Zerodha Kite Connect historical API (requires the paid data plan).
           Symbols as EXCHANGE:TRADINGSYMBOL, e.g. NSE:INFY.
"""

from __future__ import annotations

import datetime as dt
import json
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from . import config, http
from .frame import Bars, normalize_date

INTERVALS = ("1m", "2m", "5m", "15m", "30m", "60m", "1h", "1d", "1wk", "1mo")
PERIODS = ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max")

# Yahoo intraday history limits (days)
_YAHOO_INTRADAY_MAX_DAYS = {"1m": 7, "2m": 60, "5m": 60, "15m": 60, "30m": 60, "60m": 730, "1h": 730}


class DataError(RuntimeError):
    pass


def period_days(period: str) -> int:
    table = {"1d": 1, "5d": 5, "1mo": 31, "3mo": 92, "6mo": 183, "1y": 366, "2y": 731,
             "5y": 1827, "10y": 3653, "max": 36500}
    if period not in table:
        raise DataError(f"unknown period {period!r}; use one of {', '.join(PERIODS)}")
    return table[period]


def _local(epoch: int, gmtoff: int, fmt: str = "%Y-%m-%dT%H:%M") -> str:
    return dt.datetime.fromtimestamp(int(epoch) + int(gmtoff), dt.timezone.utc).strftime(fmt)


def parse_yahoo_chart(payload: Dict, symbol: str, interval: str = "1d") -> Bars:
    """Yahoo v8 chart JSON -> Bars. Times are the exchange's local time. meta carries the
    exchange's regular sessions (sessions: [{date, open, close}]) so intraday tools need no
    holiday tables: a day with no session is a day the market was closed."""
    chart = (payload or {}).get("chart", {})
    if chart.get("error"):
        raise DataError(f"Yahoo error for {symbol}: {chart['error'].get('description', chart['error'])}")
    results = chart.get("result") or []
    if not results:
        raise DataError(f"no data returned for {symbol}")
    r = results[0]
    ts = r.get("timestamp") or []
    q = (r.get("indicators", {}).get("quote") or [{}])[0]
    adj = (r.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose")
    meta = r.get("meta", {})
    gmtoff = int(meta.get("gmtoffset") or 0)
    daily = interval in ("1d", "1wk", "1mo")
    rows = []
    for i, t in enumerate(ts):
        o, h, l, c, v = (q.get(k, [None] * len(ts))[i] for k in ("open", "high", "low", "close", "volume"))
        if c is None:
            continue
        factor = 1.0
        if adj and adj[i] and daily:
            factor = adj[i] / c if c else 1.0
        d = _local(t, gmtoff, "%Y-%m-%d" if daily else "%Y-%m-%dT%H:%M")
        rows.append({"date": d,
                     "open": (o if o is not None else c) * factor,
                     "high": (h if h is not None else c) * factor,
                     "low": (l if l is not None else c) * factor,
                     "close": c * factor, "volume": v or 0})
    sessions = []
    for day in meta.get("tradingPeriods") or []:
        for per in (day if isinstance(day, list) else [day]):
            if isinstance(per, dict) and per.get("start"):
                off = int(per.get("gmtoffset", gmtoff))
                sessions.append({"date": _local(per["start"], off, "%Y-%m-%d"), "open": _local(per["start"], off, "%H:%M"),
                                 "close": _local(per["end"], off, "%H:%M")})
    reg = (meta.get("currentTradingPeriod") or {}).get("regular") or {}
    info = {"currency": meta.get("currency"), "exchange": meta.get("fullExchangeName") or meta.get("exchangeName"),
            "timezone": meta.get("exchangeTimezoneName"), "instrument_type": meta.get("instrumentType"),
            "name": meta.get("longName") or meta.get("shortName"), "gmtoffset": gmtoff,
            "adjusted": daily, "source": "yahoo", "sessions": sessions,
            "previous_close": meta.get("chartPreviousClose") if interval == "1d" else meta.get("previousClose"),
            "last_price": meta.get("regularMarketPrice"),
            "market_time": _local(meta["regularMarketTime"], gmtoff) if meta.get("regularMarketTime") else None}
    if reg.get("start"):
        off = int(reg.get("gmtoffset", gmtoff))
        info["current_session"] = {"date": _local(reg["start"], off, "%Y-%m-%d"), "open": _local(reg["start"], off, "%H:%M"),
                                   "close": _local(reg["end"], off, "%H:%M")}
    return Bars.from_rows(symbol, interval, rows, info)


# ------------------------------------------------------------------ providers

class Provider:
    name = "base"

    def bars(self, symbol: str, interval: str = "1d", period: str = "2y",
             start: Optional[str] = None, end: Optional[str] = None) -> Bars:
        raise NotImplementedError

    def quote(self, symbol: str) -> Dict:
        b = self.bars(symbol, "1d", "5d")
        if not len(b):
            raise DataError(f"no data for {symbol}")
        last = b.last()
        prev = b.close[-2] if len(b) > 1 else last["close"]
        return {"symbol": symbol, "price": last["close"], "date": last["date"],
                "change_pct": round((last["close"] / prev - 1) * 100, 3) if prev else None,
                "source": self.name}


class YahooProvider(Provider):
    name = "yahoo"
    BASE = "https://query1.finance.yahoo.com/v8/finance/chart/"

    def bars(self, symbol, interval="1d", period="2y", start=None, end=None) -> Bars:
        if interval not in INTERVALS:
            raise DataError(f"interval must be one of {', '.join(INTERVALS)}")
        yint = "60m" if interval == "1h" else interval
        params: Dict = {"interval": yint, "includePrePost": "false", "events": "div,splits"}
        if start:
            s = dt.datetime.fromisoformat(start[:10]).replace(tzinfo=dt.timezone.utc)
            e = dt.datetime.fromisoformat(end[:10]).replace(tzinfo=dt.timezone.utc) + dt.timedelta(days=1) \
                if end else dt.datetime.now(dt.timezone.utc)
            params["period1"] = int(s.timestamp())
            params["period2"] = int(e.timestamp())
        else:
            if yint in _YAHOO_INTRADAY_MAX_DAYS:
                maxd = _YAHOO_INTRADAY_MAX_DAYS[yint]
                if period_days(period) > maxd:
                    period = {7: "5d", 60: "1mo", 730: "2y"}[maxd]
            params["range"] = period
        url = self.BASE + urllib.parse.quote(symbol)
        try:
            payload = http.get_json(url, params=params)
        except http.HTTPError as e:
            if e.status == 404:
                raise DataError(f"symbol not found on Yahoo: {symbol}") from None
            raise DataError(f"Yahoo request failed for {symbol}: {e}") from None
        bars = parse_yahoo_chart(payload, symbol, interval)
        if end and not start:
            bars = bars.until(end)
        return bars

    def quote(self, symbol: str) -> Dict:
        b = self.bars(symbol, "1d", "5d")
        if not len(b):
            raise DataError(f"no data for {symbol}")
        q = {
            "symbol": symbol, "price": b.close[-1], "date": b.date[-1],
            "change_pct": round((b.close[-1] / b.close[-2] - 1) * 100, 3) if len(b) > 1 else None,
            "source": self.name,
        }
        q["currency"] = b.meta.get("currency")
        q["delayed"] = True
        return q


class CSVProvider(Provider):
    name = "csv"

    def __init__(self, directory: Optional[str] = None):
        cfg = config.load()
        d = directory or cfg["data"].get("csv_dir")
        if not d:
            raise DataError("csv provider needs data.csv_dir (folder of SYMBOL.csv files). "
                            "Set it with: setup.py set data.csv_dir /path/to/folder")
        self.dir = Path(d).expanduser()

    def _file(self, symbol: str, interval: str) -> Path:
        safe = symbol.replace(":", "_").replace("/", "_")
        for cand in (f"{safe}_{interval}.csv", f"{safe}.csv", f"{safe.upper()}.csv", f"{safe.lower()}.csv"):
            p = self.dir / cand
            if p.exists():
                return p
        raise DataError(f"no CSV for {symbol} in {self.dir} (expected {safe}.csv)")

    def bars(self, symbol, interval="1d", period="2y", start=None, end=None) -> Bars:
        b = Bars.from_csv(self._file(symbol, interval), symbol=symbol, interval=interval)
        b.meta["source"] = "csv"
        if interval in ("1wk", "1mo") and not b.intraday and len(b) > 1:
            # if the file is daily, resample
            d0 = dt.date.fromisoformat(b.date[0][:10])
            d1 = dt.date.fromisoformat(b.date[1][:10])
            if (d1 - d0).days < 5:
                b = b.resample(interval)
        if start:
            b = b.since(start)
        elif period != "max" and len(b):
            cutoff = (dt.date.fromisoformat(b.date[-1][:10]) - dt.timedelta(days=period_days(period))).isoformat()
            b = b.since(cutoff)
        if end:
            b = b.until(end)
        return b


class KiteProvider(Provider):
    """Kite Connect historical candles. Requires the Connect (data) plan."""
    name = "kite"
    _INTERVALS = {"1m": "minute", "5m": "5minute", "15m": "15minute", "30m": "30minute",
                  "60m": "60minute", "1h": "60minute", "1d": "day"}
    _MAX_DAYS = {"minute": 60, "5minute": 100, "15minute": 200, "30minute": 200, "60minute": 400, "day": 2000}

    def __init__(self):
        from .brokers.kite import KiteClient
        self.client = KiteClient()

    def bars(self, symbol, interval="1d", period="2y", start=None, end=None) -> Bars:
        resample = None
        if interval in ("1wk", "1mo"):
            resample, interval = interval, "1d"
        if interval not in self._INTERVALS:
            raise DataError(f"kite supports intervals {', '.join(self._INTERVALS)}")
        kint = self._INTERVALS[interval]
        token = self.client.instrument_token(symbol)
        end_d = dt.datetime.fromisoformat(end[:10]) if end else dt.datetime.now()
        start_d = dt.datetime.fromisoformat(start[:10]) if start else end_d - dt.timedelta(days=period_days(period))
        rows: List[Dict] = []
        chunk = dt.timedelta(days=self._MAX_DAYS[kint])
        cur = start_d
        while cur < end_d:
            nxt = min(cur + chunk, end_d)
            data = self.client.historical(token, kint, cur.strftime("%Y-%m-%d %H:%M:%S"),
                                          nxt.strftime("%Y-%m-%d %H:%M:%S"))
            for c in data:
                rows.append({"date": normalize_date(c[0][:16].replace(" ", "T")) if kint != "day" else c[0][:10],
                             "open": c[1], "high": c[2], "low": c[3], "close": c[4], "volume": c[5]})
            cur = nxt + dt.timedelta(seconds=1)
        b = Bars.from_rows(symbol, interval, rows, {"source": "kite", "adjusted": False})
        return b.resample(resample) if resample else b

    def quote(self, symbol: str) -> Dict:
        q = self.client.ltp([symbol])
        item = q.get(symbol) or next(iter(q.values()), None)
        if not item:
            raise DataError(f"no quote for {symbol}")
        return {"symbol": symbol, "price": item["last_price"], "date": dt.datetime.now().isoformat(timespec="minutes"),
                "change_pct": None, "source": "kite", "delayed": False}


def get_provider(name: Optional[str] = None) -> Provider:
    name = (name or config.load()["data"]["provider"] or "yahoo").lower()
    if name == "yahoo":
        return YahooProvider()
    if name == "csv":
        return CSVProvider()
    if name == "kite":
        return KiteProvider()
    raise DataError(f"unknown data provider {name!r} (yahoo | csv | kite)")


# ------------------------------------------------------------------ cache + public API

def _cache_file(provider: str, symbol: str, interval: str, period: str, start, end) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in symbol)
    tag = f"{period}" if not start else f"{start}_{end or 'now'}"
    return config.path("cache", provider, f"{safe}__{interval}__{tag}.csv")


def get_bars(symbol: str, interval: str = "1d", period: str = "2y", start: Optional[str] = None,
             end: Optional[str] = None, provider: Optional[str] = None, use_cache: bool = True,
             min_bars: int = 0) -> Bars:
    """Fetch bars through the configured provider, with a TTL file cache."""
    cfg = config.load()
    pname = (provider or cfg["data"]["provider"] or "yahoo").lower()
    ttl = float(cfg["data"].get("cache_ttl_minutes", 60)) * 60
    if pname == "csv":
        use_cache = False
    cf = _cache_file(pname, symbol, interval, period, start, end)
    meta_f = cf.with_suffix(".json")
    if use_cache and cf.exists() and (time.time() - cf.stat().st_mtime) < ttl:
        b = Bars.from_csv(cf, symbol=symbol, interval=interval)
        if meta_f.exists():
            try:
                b.meta = json.loads(meta_f.read_text())
            except json.JSONDecodeError:
                pass
    else:
        b = get_provider(pname).bars(symbol, interval, period, start, end)
        if use_cache and len(b):
            b.to_csv(cf)
            meta_f.write_text(json.dumps(b.meta))
    if len(b) < min_bars:
        raise DataError(f"{symbol}: only {len(b)} bars available, need at least {min_bars}")
    return b


def load_bars(symbol: Optional[str] = None, csv_path: Optional[str] = None, interval: str = "1d",
              period: str = "2y", provider: Optional[str] = None, min_bars: int = 0) -> Bars:
    """Bars from an explicit CSV file if given, else from the provider."""
    if csv_path:
        b = Bars.from_csv(Path(csv_path).expanduser(), symbol=symbol, interval=interval)
        b.meta.setdefault("source", "csv-file")
        if len(b) < min_bars:
            raise DataError(f"{b.symbol}: only {len(b)} bars in {csv_path}, need {min_bars}")
        return b
    if not symbol:
        raise DataError("give a symbol or --csv FILE")
    return get_bars(symbol, interval, period, provider=provider, min_bars=min_bars)


def add_data_args(p, period: str = "2y") -> None:
    """Standard data arguments for skill scripts."""
    p.add_argument("--interval", default="1d", choices=INTERVALS)
    p.add_argument("--period", default=period, choices=PERIODS)
    p.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    p.add_argument("--csv", help="load bars from this CSV file instead of the provider")


def get_many(symbols: Sequence[str], interval: str = "1d", period: str = "2y", provider: Optional[str] = None,
             min_bars: int = 0, workers: int = 4, start: Optional[str] = None, end: Optional[str] = None):
    """Fetch many symbols concurrently. Returns (dict symbol->Bars, dict symbol->error)."""
    from concurrent.futures import ThreadPoolExecutor
    out: Dict[str, Bars] = {}
    errors: Dict[str, str] = {}

    def one(sym):
        try:
            return sym, get_bars(sym, interval, period, start=start, end=end, provider=provider, min_bars=min_bars), None
        except Exception as e:  # noqa: BLE001 - report per-symbol failures
            return sym, None, str(e)

    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        for sym, bars, err in ex.map(one, symbols):
            if err:
                errors[sym] = err
            else:
                out[sym] = bars
    return out, errors


def load_universe(spec: Optional[str] = None, symbols: Optional[Iterable[str]] = None) -> List[str]:
    """Symbols from a comma list, a text/CSV file (one per line or a 'symbol' column), or both."""
    syms: List[str] = []
    if spec:
        p = Path(spec).expanduser()
        if p.exists():
            text = p.read_text()
            lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
            if lines and "," in lines[0]:
                header = [h.strip().lower() for h in lines[0].split(",")]
                col = next((i for i, h in enumerate(header) if h in ("symbol", "ticker", "tradingsymbol")), 0)
                start = 1 if header[col] in ("symbol", "ticker", "tradingsymbol") else 0
                syms += [ln.split(",")[col].strip() for ln in lines[start:]]
            else:
                syms += [ln.split()[0] for ln in lines]
        else:
            syms += [s.strip() for s in spec.split(",") if s.strip()]
    if symbols:
        syms += [s.strip() for s in symbols if s and s.strip()]
    seen = set()
    out = []
    for s in syms:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def fresh_bars(symbol: str, interval: str = "5m", period: str = "1d", provider: Optional[str] = None,
               offline: Optional[str] = None) -> Bars:
    """Bars straight from the source, never from the cache (prices that must be current).

    offline: a saved Yahoo chart JSON file, or a folder holding chart-<SYMBOL>-<interval>.json
    (used by tests and to replay a past session)."""
    if offline:
        p = Path(offline).expanduser()
        if p.is_dir():
            p = p / f"chart-{symbol}-{interval}.json"
        if not p.exists():
            raise DataError(f"no saved chart for {symbol} at {p}")
        text = p.read_bytes()
        if p.suffix == ".gz":
            import gzip
            text = gzip.decompress(text)
        return parse_yahoo_chart(json.loads(text.decode("utf-8")), symbol, interval)
    return get_provider(provider).bars(symbol, interval, period)


def live_quote(symbol: str, provider: Optional[str] = None, offline: Optional[str] = None) -> Dict:
    """Price, previous close, exchange session and status for one symbol (delayed on free data)."""
    from . import session as _session
    b = fresh_bars(symbol, "5m", "5d", provider, offline)
    if not len(b):
        raise DataError(f"no intraday data for {symbol}")
    price = b.meta.get("last_price") or b.close[-1]
    # previous close = last bar of the session before the latest one (Yahoo's meta field is unreliable after hours)
    last_day = b.date[-1][:10]
    before = [i for i, d in enumerate(b.date) if d[:10] < last_day]
    prev = b.close[before[-1]] if before else b.meta.get("previous_close")
    return {"symbol": symbol, "price": float(price), "previous_close": prev,
            "name": b.meta.get("name"), "currency": b.meta.get("currency"), "exchange": b.meta.get("exchange"),
            "timezone": b.meta.get("timezone"), "market_time": b.meta.get("market_time") or b.date[-1],
            "gmtoffset": b.meta.get("gmtoffset"), "bars": b, "source": b.meta.get("source", "yahoo"),
            "delayed": b.meta.get("source", "yahoo") == "yahoo"}
