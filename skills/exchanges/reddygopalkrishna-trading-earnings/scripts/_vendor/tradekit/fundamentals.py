"""Quarterly results for any listed company, and what changed.

Sources
    yahoo  Yahoo Finance's fundamentals time series: free, no key, works for any market Yahoo
           covers (AAPL, RELIANCE.NS, SHEL.L, 7203.T ...). Usually the last 5 quarters.
    sec    SEC EDGAR XBRL facts (US companies only): the numbers the company filed, many years
           deep. Needs data.sec_user_agent (see tradekit.sec).
"""

from __future__ import annotations

import datetime as dt
import json
import time
import urllib.parse
from typing import Dict, List, Optional

from . import config, http

YAHOO_URL = "https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{sym}"
YAHOO_TYPES = {
    "quarterlyTotalRevenue": "revenue", "quarterlyGrossProfit": "gross_profit",
    "quarterlyOperatingIncome": "operating_income", "quarterlyNetIncome": "net_income",
    "quarterlyDilutedEPS": "eps",
}


def yahoo_url(symbol: str, years: int = 6) -> str:
    end = int(time.time()) + 86400
    start = end - years * 366 * 86400
    return YAHOO_URL.format(sym=urllib.parse.quote(symbol)) + "?" + urllib.parse.urlencode(
        {"type": ",".join(YAHOO_TYPES), "period1": start, "period2": end})


def parse_yahoo(payload: Dict) -> List[Dict]:
    rows: Dict[str, Dict] = {}
    for res in (payload.get("timeseries") or {}).get("result") or []:
        kind = ((res.get("meta") or {}).get("type") or [None])[0]
        field = YAHOO_TYPES.get(kind)
        if not field:
            continue
        for pt in res.get(kind) or []:
            if not pt or not pt.get("asOfDate"):
                continue
            val = (pt.get("reportedValue") or {}).get("raw")
            r = rows.setdefault(pt["asOfDate"], {"period_end": pt["asOfDate"], "derived": False,
                                                 "currency": pt.get("currencyCode")})
            r[field] = float(val) if val is not None else None
            if pt.get("currencyCode"):
                r["currency"] = pt["currencyCode"]
    out = []
    for end in sorted(rows):
        r = rows[end]
        for f in YAHOO_TYPES.values():
            r.setdefault(f, None)
        if r.get("revenue") is not None or r.get("net_income") is not None:
            out.append(r)
    return out


def yahoo_quarters(symbol: str, use_cache: bool = True) -> List[Dict]:
    f = config.path("cache", "fundamentals", "".join(c if c.isalnum() or c in "-_." else "_" for c in symbol) + ".json")
    if use_cache and f.exists() and (time.time() - f.stat().st_mtime) < 12 * 3600:
        try:
            return parse_yahoo(json.loads(f.read_text()))
        except json.JSONDecodeError:
            pass
    payload = http.get_json(yahoo_url(symbol))
    f.write_text(json.dumps(payload))
    return parse_yahoo(payload)


def _pct(a: Optional[float], b: Optional[float]) -> Optional[float]:
    if a is None or b is None or b == 0:
        return None
    return round((a / b - 1) * 100 * (1 if b > 0 else -1), 1)


def _margin(x: Optional[float], rev: Optional[float]) -> Optional[float]:
    if x is None or not rev:
        return None
    return round(x / rev * 100, 1)


def _same_quarter_last_year(rows: List[Dict], i: int) -> Optional[Dict]:
    end = dt.date.fromisoformat(rows[i]["period_end"])
    for r in rows[:i]:
        d = (end - dt.date.fromisoformat(r["period_end"])).days
        if 350 <= d <= 380:
            return r
    return None


def analyse(rows: List[Dict], symbol: str, source: str, name: Optional[str] = None) -> Dict:
    """Add margins, quarter-on-quarter and year-on-year changes, TTM and plain-words notes."""
    table = []
    for i, r in enumerate(rows):
        prev = rows[i - 1] if i else None
        ly = _same_quarter_last_year(rows, i)
        rev = r.get("revenue")
        table.append({
            **r,
            "gross_margin_pct": _margin(r.get("gross_profit"), rev),
            "operating_margin_pct": _margin(r.get("operating_income"), rev),
            "net_margin_pct": _margin(r.get("net_income"), rev),
            "revenue_qoq_pct": _pct(rev, prev.get("revenue")) if prev else None,
            "revenue_yoy_pct": _pct(rev, ly.get("revenue")) if ly else None,
            "net_income_yoy_pct": _pct(r.get("net_income"), ly.get("net_income")) if ly else None,
            "eps_yoy_pct": _pct(r.get("eps"), ly.get("eps")) if ly else None,
        })
    out: Dict = {"symbol": symbol, "name": name, "source": source, "quarters": table, "notes": []}
    if not table:
        out["notes"].append("no quarterly results found")
        return out
    last = table[-1]
    out["latest"] = last
    if len(table) >= 4:
        last4 = table[-4:]
        span = (dt.date.fromisoformat(last4[-1]["period_end"]) - dt.date.fromisoformat(last4[0]["period_end"])).days
        if 250 <= span <= 300:
            ttm = {}
            for f in ("revenue", "net_income", "eps"):
                vals = [q.get(f) for q in last4]
                ttm[f] = round(sum(vals), 4) if all(v is not None for v in vals) else None
            out["ttm"] = ttm
    notes = out["notes"]
    ni, oi = last.get("net_income"), last.get("operating_income")
    if ni is not None and oi is not None and oi > 0 and ni > oi:
        notes.append("net income is above operating income: gains outside the core business "
                     "(investments, tax items, one-offs) are inside it")
    if last.get("gross_profit") is None and last.get("revenue") is not None:
        notes.append("no gross margin reported (normal for banks, insurers and some service companies)")
    if any(q.get("derived") for q in table):
        notes.append("rows marked derived: a fourth quarter worked out as the full year minus three quarters; "
                     "derived EPS is approximate")
    if last.get("revenue_yoy_pct") is None:
        notes.append("no same quarter a year earlier in this data, so no year-on-year growth for the latest quarter")
    age = (dt.date.today() - dt.date.fromisoformat(last["period_end"])).days
    if age > 135:
        notes.append(f"latest quarter ended {age} days ago: a newer report may be out but not in this data yet; "
                     "check the company's filing or results page")
    return out
