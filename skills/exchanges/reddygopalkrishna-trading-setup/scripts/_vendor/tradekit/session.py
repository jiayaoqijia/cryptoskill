"""Exchange sessions and intraday entry triggers, for any market.

Session times come from the data itself (Yahoo reports each exchange's regular session per day),
so NYSE, NSE, LSE, TSE ... all work without holiday tables. A weekday with no session is a day
the exchange was closed. Times are the exchange's local time, written "HH:MM".

The entry rule is bar-by-bar and never early: a bar counts only once it has CLOSED, and the
trigger is the first closed bar whose close is beyond the level (above for a long, below for a
short). A wick through the level is not a trigger. A close exactly at the level is not beyond it.
"""

from __future__ import annotations

import datetime as dt
from typing import Dict, List, Optional

from .frame import Bars


def hm(s: str) -> int:
    h, m = s.split(":")[:2]
    return int(h) * 60 + int(m)


def clock(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def interval_minutes(interval: str) -> int:
    table = {"1m": 1, "2m": 2, "5m": 5, "15m": 15, "30m": 30, "60m": 60, "1h": 60}
    if interval not in table:
        raise ValueError("intraday interval must be one of 1m, 2m, 5m, 15m, 30m, 60m")
    return table[interval]


def now_local(bars: Bars, override: Optional[str] = None) -> str:
    """Exchange-local 'YYYY-MM-DDTHH:MM'. --now (already local) wins; else the system clock
    shifted by the exchange's UTC offset."""
    if override:
        return override.replace(" ", "T")[:16]
    off = int(bars.meta.get("gmtoffset") or 0)
    t = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=off)
    return t.strftime("%Y-%m-%dT%H:%M")


def session_for(bars: Bars, day: str) -> Optional[Dict]:
    for s in bars.meta.get("sessions") or []:
        if s["date"] == day:
            return s
    cur = bars.meta.get("current_session")
    if cur and cur.get("date") == day:
        return cur
    # no session data (CSV, Kite): infer from that day's bars
    day_bars = [d for d in bars.date if d[:10] == day]
    if day_bars:
        return {"date": day, "open": day_bars[0][11:16], "close": None, "inferred": True}
    return None


def market_status(bars: Bars, now: str) -> Dict:
    """open | pre-open | closed for the exchange in `bars`, with the session used."""
    day, t = now[:10], hm(now[11:16])
    s = session_for(bars, day)
    if not s or s.get("inferred") and not s.get("close"):
        nxt = next((x for x in sorted(bars.meta.get("sessions") or [], key=lambda x: x["date"]) if x["date"] > day), None)
        if s and s.get("inferred"):
            return {"status": "open?", "session": s, "note": "session times unknown for this data source"}
        return {"status": "closed", "session": None, "next": nxt,
                "note": "no session today (weekend or exchange holiday)" if dt.date.fromisoformat(day).weekday() < 5
                else "weekend"}
    o, c = hm(s["open"]), hm(s["close"])
    if t < o:
        return {"status": "pre-open", "session": s, "minutes_to_open": o - t}
    if t >= c:
        return {"status": "closed", "session": s, "note": "after the close"}
    return {"status": "open", "session": s, "minutes_to_close": c - t}


def day_bars(bars: Bars, day: str) -> List[Dict]:
    return [r for r in bars.rows() if r["date"][:10] == day]


def closed_bars(rows: List[Dict], now_min: int, step: int) -> List[Dict]:
    """Bars whose end (start + step) is at or before now. Off-grid bars (a live tick) are dropped."""
    out = []
    for r in rows:
        start = hm(r["date"][11:16])
        if start % step:
            continue
        if start + step <= now_min:
            out.append(r)
    return out


def opening_range(rows: List[Dict], open_min: int, minutes: int) -> Optional[Dict]:
    rng = [r for r in rows if open_min <= hm(r["date"][11:16]) < open_min + minutes]
    if not rng:
        return None
    return {"high": round(max(r["high"] for r in rng), 4), "low": round(min(r["low"] for r in rng), 4), "bars": len(rng),
            "volume_avg": sum(r["volume"] for r in rng) / len(rng),
            "from": clock(open_min), "to": clock(open_min + minutes)}


def entry_check(bars: Bars, now: str, setup: str = "orb", side: str = "long", level: Optional[float] = None,
                or_minutes: int = 15, min_volume_x: Optional[float] = None, no_entries_last_minutes: int = 30,
                interval: Optional[str] = None) -> Dict:
    """Status of an intraday entry: not-open | forming | waiting | triggered | expired | closed | no-data."""
    step = interval_minutes(interval or bars.interval)
    day, t = now[:10], hm(now[11:16])
    long = side == "long"
    res: Dict = {"symbol": bars.symbol, "now": now, "setup": setup, "side": side, "interval": f"{step}m",
                 "exchange": bars.meta.get("exchange"), "timezone": bars.meta.get("timezone"),
                 "currency": bars.meta.get("currency")}
    st = market_status(bars, now)
    s = st.get("session")
    if st["status"] == "closed" and not s:
        res.update(status="closed", message=f"Market closed: {st.get('note')}.", next_session=st.get("next"))
        return res
    o = hm(s["open"])
    c = hm(s["close"]) if s.get("close") else None
    res["session"] = s
    if st["status"] == "pre-open":
        res.update(status="not-open", message=f"Not open yet: the session opens at {s['open']} ({st['minutes_to_open']} min).")
        return res
    # only bars that had started by `now` and began inside the session (drops after-close ticks,
    # and makes a replay with --now see exactly what was visible at that moment)
    rows = [r for r in day_bars(bars, day) if hm(r["date"][11:16]) < t and (c is None or hm(r["date"][11:16]) < c)]
    if not rows:
        res.update(status="no-data", message="No bars for today yet (the data source may lag a few minutes).")
        return res
    done = closed_bars(rows, min(t, c) if c else t, step)
    if setup == "orb":
        if t < o + or_minutes:
            res.update(status="forming", message=f"The opening range is still forming until {clock(o + or_minutes)}.")
            return res
        rng = opening_range(done, o, or_minutes)
        if not rng or rng["bars"] < or_minutes // step:
            res.update(status="no-data", message="Opening-range bars are missing (halt or thin trading); no signal.")
            return res
        res["opening_range"] = rng
        lvl = rng["high"] if long else rng["low"]
        after = [r for r in done if hm(r["date"][11:16]) >= o + or_minutes]
    elif setup == "level":
        if level is None:
            raise ValueError("--setup level needs --level PRICE")
        lvl = float(level)
        start_min = o + or_minutes if or_minutes else o
        after = [r for r in done if hm(r["date"][11:16]) >= start_min]
        rng = opening_range(done, o, or_minutes) if or_minutes else None
    else:
        raise ValueError("setup must be orb or level")
    res["level"] = round(lvl, 4)
    cutoff = (c - no_entries_last_minutes) if c else None
    res["no_entries_after"] = clock(cutoff) if cutoff else None
    for i, r in enumerate(after):
        beyond = r["close"] > lvl if long else r["close"] < lvl
        if not beyond:
            continue
        bar_close = hm(r["date"][11:16]) + step
        vol_ok = True
        if min_volume_x and rng and rng["volume_avg"]:
            res.setdefault("volume_checks", []).append({"bar": r["date"][11:16], "x": round(r["volume"] / rng["volume_avg"], 2)})
            vol_ok = r["volume"] >= min_volume_x * rng["volume_avg"]
        if not vol_ok:
            continue
        if cutoff is not None and bar_close > cutoff:
            break
        res.update(status="triggered", trigger_time=clock(bar_close), trigger_bar=r["date"][11:16], price=round(r["close"], 4),
                   beyond_pct=round((r["close"] / lvl - 1) * 100, 2),
                   bars_ago=len(closed_bars(rows, t, step)) - len(closed_bars(rows, bar_close, step)))
        res["message"] = (f"TRIGGERED at {clock(bar_close)}: the {r['date'][11:16]} bar closed at {r['close']:.2f}, "
                          f"{'above' if long else 'below'} {lvl:.2f} ({res['beyond_pct']:+.2f}%). Nothing was placed.")
        if res["bars_ago"] > 1:
            res["message"] += f" That was {res['bars_ago']} bars ago: a late entry is a different trade; re-plan from the price now."
        return res
    if cutoff is not None and t >= cutoff:
        res.update(status="expired", message=f"Expired: no {'close above' if long else 'close below'} {lvl:.2f} "
                                             f"before the {clock(cutoff)} cutoff.")
        return res
    last = done[-1] if done else None
    forming = [r for r in rows if r not in done and hm(r["date"][11:16]) % step == 0]
    res["status"] = "waiting"
    if last:
        gap = (lvl - last["close"]) if long else (last["close"] - lvl)
        res["last_close"] = round(last["close"], 4)
        res["distance_pct"] = round(gap / lvl * 100, 2)
        res["message"] = (f"WAITING: last closed bar ({last['date'][11:16]}) closed at {last['close']:.2f}, "
                          f"{abs(gap):.2f} {'under' if long else 'over'} the level {lvl:.2f} ({res['distance_pct']:.2f}% away).")
    else:
        res["message"] = f"WAITING for the first closed bar after {clock(o + or_minutes)}."
    if forming:
        f = forming[-1]
        res["forming"] = {"bar": f["date"][11:16], "price": round(f["close"], 4)}
        res["message"] += (f" The {f['date'][11:16]} bar is still forming ({f['close']:.2f} so far); "
                           f"it does not count until it closes.")
    return res
