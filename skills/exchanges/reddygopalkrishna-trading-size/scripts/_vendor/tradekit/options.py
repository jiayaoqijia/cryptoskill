"""Options maths and option-chain tools. Analysis only; nothing here places an order.

* Black-Scholes(-Merton) price, Greeks and implied volatility (bisection), European style.
* Multi-leg payoff at expiry: breakevens, max profit / max loss (or "unlimited").
* Chain parsing: a user-downloaded NSE option-chain CSV (by header names), Cboe's public delayed
  JSON (US), and Kite instruments + quotes (NFO etc.). Then OI totals, put/call ratio, max pain.

Assumptions to keep in mind: Black-Scholes is European and assumes constant volatility. NSE stock
options are American-style physically settled, US equity options are American: BS is an estimate there.
Index options (NIFTY, SPX) are European cash-settled, where BS is the right model.
Nothing in this module hard-codes lot sizes: pass them in from the user or the broker's instruments.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import math
import re
from typing import Dict, List, Optional, Sequence, Tuple

SQRT2 = math.sqrt(2.0)


# ---------------------------------------------------------------- Black-Scholes

def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _kind(kind: str) -> str:
    k = str(kind).lower()
    if k in ("c", "call", "ce"):
        return "call"
    if k in ("p", "put", "pe"):
        return "put"
    raise ValueError(f"option kind must be call or put, got {kind!r}")


def _d1d2(S: float, K: float, T: float, r: float, sigma: float, q: float) -> Tuple[float, float]:
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    return d1, d1 - sigma * math.sqrt(T)


def intrinsic(S: float, K: float, kind: str) -> float:
    return max(S - K, 0.0) if _kind(kind) == "call" else max(K - S, 0.0)


def bs_price(S: float, K: float, T: float, r: float, sigma: float, kind: str, q: float = 0.0) -> float:
    """Option price. T in years, r and q continuous annual rates, sigma annual volatility (0.2 = 20%)."""
    kind = _kind(kind)
    if S <= 0 or K <= 0:
        raise ValueError("spot and strike must be positive")
    if T <= 0 or sigma <= 0:
        # at expiry (or zero vol) only discounted intrinsic value is left
        if T <= 0:
            return intrinsic(S, K, kind)
        fwd = S * math.exp(-q * T)
        disc = K * math.exp(-r * T)
        return max(fwd - disc, 0.0) if kind == "call" else max(disc - fwd, 0.0)
    d1, d2 = _d1d2(S, K, T, r, sigma, q)
    if kind == "call":
        return S * math.exp(-q * T) * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S * math.exp(-q * T) * norm_cdf(-d1)


def greeks(S: float, K: float, T: float, r: float, sigma: float, kind: str, q: float = 0.0) -> Dict:
    """Price and Greeks. Units: theta per calendar day, vega per 1 volatility point (1%), rho per 1% rate."""
    kind = _kind(kind)
    price = bs_price(S, K, T, r, sigma, kind, q)
    if T <= 0 or sigma <= 0:
        itm = intrinsic(S, K, kind) > 0
        delta = (1.0 if kind == "call" else -1.0) if itm else 0.0
        return {"price": price, "delta": delta, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "rho": 0.0}
    d1, d2 = _d1d2(S, K, T, r, sigma, q)
    sq = math.sqrt(T)
    eq, er = math.exp(-q * T), math.exp(-r * T)
    pdf = norm_pdf(d1)
    gamma = eq * pdf / (S * sigma * sq)
    vega = S * eq * pdf * sq / 100.0
    if kind == "call":
        delta = eq * norm_cdf(d1)
        theta = (-S * eq * pdf * sigma / (2 * sq) - r * K * er * norm_cdf(d2) + q * S * eq * norm_cdf(d1)) / 365.0
        rho = K * T * er * norm_cdf(d2) / 100.0
    else:
        delta = -eq * norm_cdf(-d1)
        theta = (-S * eq * pdf * sigma / (2 * sq) + r * K * er * norm_cdf(-d2) - q * S * eq * norm_cdf(-d1)) / 365.0
        rho = -K * T * er * norm_cdf(-d2) / 100.0
    return {"price": price, "delta": delta, "gamma": gamma, "theta": theta, "vega": vega, "rho": rho}


def implied_vol(price: float, S: float, K: float, T: float, r: float, kind: str, q: float = 0.0,
                lo: float = 1e-4, hi: float = 5.0, tol: float = 1e-7, max_iter: int = 200) -> Optional[float]:
    """Implied volatility by bisection (price is monotonic in sigma). None if no solution exists.

    No solution when the price is below the no-arbitrage minimum (below discounted intrinsic) or above
    the maximum (spot for a call, discounted strike for a put), or when T <= 0.
    """
    kind = _kind(kind)
    if T <= 0 or price <= 0 or S <= 0 or K <= 0:
        return None
    if bs_price(S, K, T, r, lo, kind, q) - 1e-9 > price or bs_price(S, K, T, r, hi, kind, q) + 1e-9 < price:
        return None
    a, b = lo, hi
    for _ in range(max_iter):
        mid = 0.5 * (a + b)
        diff = bs_price(S, K, T, r, mid, kind, q) - price
        if abs(diff) < tol or (b - a) < 1e-10:
            return mid
        if diff > 0:
            b = mid
        else:
            a = mid
    return 0.5 * (a + b)


def years_to(expiry: str, today: Optional[dt.date] = None) -> float:
    """Calendar years from today to an expiry date (YYYY-MM-DD). Same-day expiry returns a small positive stub."""
    today = today or dt.date.today()
    days = (dt.date.fromisoformat(expiry[:10]) - today).days
    return max(days, 0) / 365.0


# ---------------------------------------------------------------- payoff

def leg(kind: str, side: str, strike: Optional[float], premium: float = 0.0, qty: float = 1.0) -> Dict:
    """One leg. kind: call | put | stock (also future). For stock/future, strike is the entry price."""
    k = str(kind).lower()
    if k in ("c", "ce", "call"):
        k = "call"
    elif k in ("p", "pe", "put"):
        k = "put"
    elif k in ("s", "stock", "f", "fut", "future", "futures"):
        k = "stock"
    else:
        raise ValueError(f"unknown leg kind {kind!r}")
    s = str(side).lower()
    if s in ("+", "long", "buy", "b"):
        s = "long"
    elif s in ("-", "short", "sell", "s"):
        s = "short"
    else:
        raise ValueError(f"unknown side {side!r}")
    if strike is None or strike <= 0:
        raise ValueError("every leg needs a positive strike (stock/future legs: entry price)")
    if qty <= 0:
        raise ValueError("qty must be positive")
    return {"kind": k, "side": s, "strike": float(strike), "premium": float(premium or 0.0), "qty": float(qty)}


def leg_pnl(lg: Dict, S: float) -> float:
    """Profit/loss of one leg at expiry spot S, per unit of underlying times qty (no lot size yet)."""
    sign = 1.0 if lg["side"] == "long" else -1.0
    if lg["kind"] == "stock":
        val = S - lg["strike"]
    elif lg["kind"] == "call":
        val = max(S - lg["strike"], 0.0) - lg["premium"]
    else:
        val = max(lg["strike"] - S, 0.0) - lg["premium"]
    return sign * val * lg["qty"]


def payoff_at(legs: Sequence[Dict], S: float, lot_size: float = 1.0) -> float:
    return sum(leg_pnl(l, S) for l in legs) * lot_size


def _slope_high(legs: Sequence[Dict]) -> float:
    """Slope of total P&L as spot goes to infinity (per unit)."""
    s = 0.0
    for l in legs:
        sign = 1.0 if l["side"] == "long" else -1.0
        if l["kind"] in ("call", "stock"):
            s += sign * l["qty"]
    return s


def analyze(legs: Sequence[Dict], lot_size: float = 1.0) -> Dict:
    """Breakevens, max profit, max loss of a multi-leg position held to expiry. Exact (piecewise linear)."""
    if not legs:
        raise ValueError("no legs")
    pts = sorted({0.0} | {l["strike"] for l in legs})
    vals = [payoff_at(legs, p, lot_size) for p in pts]
    slope = _slope_high(legs) * lot_size
    breakevens: List[float] = []
    for i in range(len(pts) - 1):
        a, b, va, vb = pts[i], pts[i + 1], vals[i], vals[i + 1]
        if va == 0 and i > 0:
            breakevens.append(a)
        elif va * vb < 0:
            breakevens.append(a + (b - a) * (-va) / (vb - va))
    last = pts[-1]
    if vals[-1] == 0:
        breakevens.append(last)
    elif slope != 0 and vals[-1] * slope < 0:
        breakevens.append(last - vals[-1] / slope)
    breakevens = sorted({round(x, 6) for x in breakevens if x > 0})
    top, bottom = max(vals), min(vals)
    if slope > 0:
        top = None
    elif slope < 0:
        bottom = None
    prem = sum((l["premium"] * l["qty"]) * (-1.0 if l["side"] == "long" else 1.0) for l in legs if l["kind"] != "stock")
    return {
        "max_profit": top, "max_loss": bottom,
        "max_profit_unlimited": top is None, "max_loss_unlimited": bottom is None,
        "breakevens": breakevens,
        "net_credit": prem * lot_size,  # >0 = money received up front, <0 = money paid
        "payoff_at_zero": vals[0],
    }


def payoff_table(legs: Sequence[Dict], lo: float, hi: float, steps: int = 21, lot_size: float = 1.0) -> List[Dict]:
    if steps < 2:
        raise ValueError("steps must be at least 2")
    out = []
    for i in range(steps):
        s = lo + (hi - lo) * i / (steps - 1)
        out.append({"spot": s, "pnl": payoff_at(legs, s, lot_size)})
    return out


def ascii_payoff(rows: Sequence[Dict], height: int = 13, spot: Optional[float] = None) -> str:
    """Tiny text chart: P&L on the vertical axis, spot at expiry along the bottom."""
    if not rows:
        return ""
    pnl = [r["pnl"] for r in rows]
    lo, hi = min(min(pnl), 0.0), max(max(pnl), 0.0)
    if hi == lo:
        hi = lo + 1.0
    lines = []
    zero_row = round((hi - 0.0) / (hi - lo) * (height - 1))
    for h in range(height):
        level = hi - (hi - lo) * h / (height - 1)
        cells = []
        for v in pnl:
            r = round((hi - v) / (hi - lo) * (height - 1))
            cells.append("#" if r == h else ("-" if h == zero_row else " "))
        lines.append(f"{level:>12,.0f} |" + "".join(cells))
    axis = " " * 13 + "+" + "-" * len(pnl)
    lab = f"{rows[0]['spot']:,.0f}".ljust(len(pnl) // 2) + f"{rows[-1]['spot']:,.0f}".rjust(len(pnl) - len(pnl) // 2)
    out = "\n".join(lines) + "\n" + axis + "\n" + " " * 14 + lab
    if spot is not None:
        out += f"\n(spot now {spot:,.2f}; '-' marks zero P&L)"
    return out


# named strategies: (description, builder(strikes) -> [(kind, side, strike_index)])
STRATEGIES: Dict[str, Tuple[int, str, List[Tuple[str, str, int]]]] = {
    "long-call": (1, "buy a call", [("call", "long", 0)]),
    "long-put": (1, "buy a put", [("put", "long", 0)]),
    "short-call": (1, "sell a naked call (unlimited risk)", [("call", "short", 0)]),
    "short-put": (1, "sell a naked put (large risk)", [("put", "short", 0)]),
    "bull-call-spread": (2, "buy low call, sell higher call", [("call", "long", 0), ("call", "short", 1)]),
    "bear-put-spread": (2, "buy high put, sell lower put", [("put", "long", 1), ("put", "short", 0)]),
    "bull-put-spread": (2, "sell high put, buy lower put (credit)", [("put", "short", 1), ("put", "long", 0)]),
    "bear-call-spread": (2, "sell low call, buy higher call (credit)", [("call", "short", 0), ("call", "long", 1)]),
    "long-straddle": (1, "buy call and put at one strike", [("call", "long", 0), ("put", "long", 0)]),
    "short-straddle": (1, "sell call and put at one strike (unlimited risk)", [("call", "short", 0), ("put", "short", 0)]),
    "long-strangle": (2, "buy lower put and higher call", [("put", "long", 0), ("call", "long", 1)]),
    "short-strangle": (2, "sell lower put and higher call (unlimited risk)", [("put", "short", 0), ("call", "short", 1)]),
    "iron-condor": (4, "sell put and call spreads around the market (strikes low to high: long put, short put, short call, long call)",
                    [("put", "long", 0), ("put", "short", 1), ("call", "short", 2), ("call", "long", 3)]),
    "iron-butterfly": (3, "sell straddle, buy wings (strikes low to high: long put, short both, long call)",
                       [("put", "long", 0), ("put", "short", 1), ("call", "short", 1), ("call", "long", 2)]),
    "long-butterfly": (3, "buy low call, sell two middle calls, buy high call",
                       [("call", "long", 0), ("call", "short", 1), ("call", "short", 1), ("call", "long", 2)]),
}


def build_strategy(name: str, strikes: Sequence[float], premiums: Optional[Sequence[Optional[float]]] = None,
                   qty: float = 1.0) -> List[Dict]:
    """Legs for a named strategy. strikes low to high. premiums optional per leg (in the strategy's leg order)."""
    key = name.lower().replace("_", "-")
    if key not in STRATEGIES:
        raise ValueError(f"unknown strategy {name!r}; choose from: {', '.join(sorted(STRATEGIES))}")
    n, _desc, spec = STRATEGIES[key]
    strikes = [float(s) for s in strikes]
    if len(strikes) != n:
        raise ValueError(f"{key} needs {n} strike(s), got {len(strikes)}")
    if key != "long-straddle" and key != "short-straddle" and strikes != sorted(strikes):
        raise ValueError("give strikes from low to high")
    if len(set(strikes)) != len(strikes):
        raise ValueError("strikes must be different")
    if premiums is not None and len(premiums) != len(spec):
        raise ValueError(f"{key} has {len(spec)} legs; give {len(spec)} premiums (or none)")
    out = []
    for i, (kind, side, idx) in enumerate(spec):
        prem = premiums[i] if premiums is not None and premiums[i] is not None else None
        l = leg(kind, side, strikes[idx], prem or 0.0, qty)
        l["premium_known"] = prem is not None
        out.append(l)
    return out


_LEG_RE = re.compile(r"^\s*([+-])\s*(\d+(?:\.\d+)?)?\s*(C|P|S|F|CE|PE)\s*(\d+(?:\.\d+)?)\s*(?:@\s*(\d+(?:\.\d+)?))?\s*$", re.I)


def parse_leg(spec: str) -> Dict:
    """'+1C100@2.5' = long 1 call strike 100 premium 2.5; '-2P90@1.2'; '+1S100' = long 1 unit stock/future bought at 100.
    Premium may be omitted (price it with Black-Scholes by passing spot, vol and days to the caller)."""
    m = _LEG_RE.match(spec)
    if not m:
        raise ValueError(f"cannot read leg {spec!r}; use e.g. +1C100@2.5 or -1P95@1.1 (+/- qty C|P|S strike @premium)")
    sign, qty, kind, strike, prem = m.groups()
    l = leg(kind.upper()[0] if kind.upper() in ("C", "P", "S", "F") else kind, sign, float(strike),
            float(prem) if prem else 0.0, float(qty) if qty else 1.0)
    l["premium_known"] = prem is not None or l["kind"] == "stock"
    return l


# ---------------------------------------------------------------- chains
# A chain is {"underlying", "spot", "expiry", "source", "rows": [row...]} where each row is
#   {"strike", "c_ltp","c_bid","c_ask","c_oi","c_chg_oi","c_volume","c_iv",  "p_...same...}
# IV is stored as a fraction (0.20 = 20%). Missing values are None.

SIDE_FIELDS = ("oi", "chg_oi", "volume", "iv", "ltp", "chg", "bid", "ask", "bid_qty", "ask_qty")

_NSE_HEADERS = {
    "OI": "oi", "CHNG IN OI": "chg_oi", "VOLUME": "volume", "IV": "iv", "LTP": "ltp", "CHNG": "chg",
    "BID QTY": "bid_qty", "BID": "bid", "ASK": "ask", "ASK QTY": "ask_qty",
}


def _num(x) -> Optional[float]:
    if x is None:
        return None
    s = str(x).strip().replace(",", "").replace('"', "")
    if s in ("", "-", "--", "NA", "N/A", "nan", "None"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_nse_csv(text: str, spot: Optional[float] = None, expiry: Optional[str] = None,
                  underlying: Optional[str] = None) -> Dict:
    """Parse the option-chain CSV downloaded from nseindia.com (Option Chain page -> Download).

    The file has a CALLS/PUTS banner row, then one header row with the columns repeated either side of
    STRIKE. Columns are matched by header name (case-insensitive, extra/missing columns tolerated);
    everything left of STRIKE is the call side, right of it the put side. The CSV carries neither the
    spot nor the expiry, so pass them. IV is in percent in the file and returned as a fraction.
    """
    rows_raw = list(csv.reader(io.StringIO(text.lstrip("﻿"))))
    hdr_i = next((i for i, r in enumerate(rows_raw) if any(c.strip().upper() == "STRIKE" for c in r)), None)
    if hdr_i is None:
        raise ValueError("no STRIKE column found: is this an NSE option-chain CSV (Option Chain page -> Download)?")
    hdr = [c.strip().upper() for c in rows_raw[hdr_i]]
    strike_i = hdr.index("STRIKE")
    colmap: Dict[int, Tuple[str, str]] = {}
    for i, h in enumerate(hdr):
        if h in _NSE_HEADERS and i != strike_i:
            colmap[i] = ("c" if i < strike_i else "p", _NSE_HEADERS[h])
    if not any(v[1] == "oi" for v in colmap.values()):
        raise ValueError("no OI columns found in the CSV header")
    out = []
    for r in rows_raw[hdr_i + 1:]:
        if len(r) <= strike_i:
            continue
        strike = _num(r[strike_i])
        if strike is None:
            continue
        row = {"strike": strike}
        for f in SIDE_FIELDS:
            row["c_" + f] = None
            row["p_" + f] = None
        for i, (side, f) in colmap.items():
            if i < len(r):
                v = _num(r[i])
                if f == "iv" and v is not None:
                    v = v / 100.0 if v > 0 else None
                row[f"{side}_{f}"] = v
        out.append(row)
    if not out:
        raise ValueError("the CSV has a header but no strike rows")
    out.sort(key=lambda x: x["strike"])
    return {"underlying": underlying, "spot": spot, "expiry": expiry, "source": "nse-csv", "rows": out}


_OCC_RE = re.compile(r"^(.+?)(\d{6})([CP])(\d{8})$")


def parse_cboe(payload: Dict, expiry: Optional[str] = None) -> Dict:
    """Parse Cboe's public delayed-quotes options JSON (US listed options). Picks the nearest expiry
    that is today or later unless expiry (YYYY-MM-DD) is given. Cboe's own IV is used (it is 0 when stale)."""
    data = payload.get("data") or {}
    opts = data.get("options") or []
    if not opts:
        raise ValueError("no options in the response")
    by_exp: Dict[str, Dict[float, Dict]] = {}
    for o in opts:
        m = _OCC_RE.match(str(o.get("option", "")))
        if not m:
            continue
        _root, d6, cp, k8 = m.groups()
        exp = f"20{d6[:2]}-{d6[2:4]}-{d6[4:]}"
        strike = int(k8) / 1000.0
        row = by_exp.setdefault(exp, {}).setdefault(strike, {"strike": strike})
        s = cp.lower()
        iv = _num(o.get("iv"))
        row[f"{s}_ltp"] = _num(o.get("last_trade_price")) or None
        row[f"{s}_bid"] = _num(o.get("bid"))
        row[f"{s}_ask"] = _num(o.get("ask"))
        row[f"{s}_oi"] = _num(o.get("open_interest"))
        row[f"{s}_volume"] = _num(o.get("volume"))
        row[f"{s}_iv"] = iv if iv and iv > 0 else None
        row[f"{s}_chg_oi"] = None
    if not by_exp:
        raise ValueError("could not read any option symbols")
    exps = sorted(by_exp)
    today = dt.date.today().isoformat()
    if expiry:
        if expiry not in by_exp:
            raise ValueError(f"expiry {expiry} not listed; available: {', '.join(exps[:12])}{' ...' if len(exps) > 12 else ''}")
        chosen = expiry
    else:
        chosen = next((e for e in exps if e >= today), exps[-1])
    rows = []
    for k in sorted(by_exp[chosen]):
        r = by_exp[chosen][k]
        for s in ("c", "p"):
            for f in SIDE_FIELDS:
                r.setdefault(f"{s}_{f}", None)
        rows.append(r)
    return {"underlying": data.get("symbol"), "spot": _num(data.get("current_price")), "expiry": chosen,
            "expiries": exps, "source": "cboe-delayed", "as_of": payload.get("timestamp"), "rows": rows}


def kite_underlyings_spot_key(name: str) -> str:
    """Kite quote key for an underlying's spot. Indices have their own names on the NSE segment."""
    idx = {"NIFTY": "NSE:NIFTY 50", "BANKNIFTY": "NSE:NIFTY BANK", "FINNIFTY": "NSE:NIFTY FIN SERVICE",
           "MIDCPNIFTY": "NSE:NIFTY MID SELECT", "SENSEX": "BSE:SENSEX"}
    return idx.get(name.upper(), f"NSE:{name.upper()}")


def kite_chain(client, name: str, expiry: Optional[str] = None, exchange: str = "NFO", spot: Optional[float] = None) -> Dict:
    """Option chain from Kite Connect: the instruments list (strikes, expiries, lot size) plus quotes (OI,
    volume, prices). Quotes need the paid Kite Connect data plan. `client` is a brokers.kite.KiteClient."""
    name = name.upper()
    inst = [i for i in client.instruments(exchange)
            if (i.get("name") or "").upper() == name and i.get("instrument_type") in ("CE", "PE")]
    if not inst:
        raise ValueError(f"no {exchange} options found for {name} in Kite's instruments list")
    exps = sorted({i["expiry"] for i in inst})
    today = dt.date.today().isoformat()
    chosen = expiry or next((e for e in exps if e >= today), exps[-1])
    if chosen not in exps:
        raise ValueError(f"expiry {chosen} not listed; available: {', '.join(exps[:8])}")
    sel = [i for i in inst if i["expiry"] == chosen]
    lot = _num(sel[0].get("lot_size"))
    quotes: Dict = {}
    keys = [f"{exchange}:{i['tradingsymbol']}" for i in sel]
    for j in range(0, len(keys), 400):
        quotes.update(client.quote(keys[j:j + 400]))
    if spot is None:
        try:
            sk = kite_underlyings_spot_key(name)
            spot = _num((client.ltp([sk]).get(sk) or {}).get("last_price"))
        except Exception:  # noqa: BLE001 - spot is optional, the caller can pass --spot
            spot = None
    rows: Dict[float, Dict] = {}
    for i in sel:
        k = _num(i["strike"])
        q = quotes.get(f"{exchange}:{i['tradingsymbol']}") or {}
        side = "c" if i["instrument_type"] == "CE" else "p"
        row = rows.setdefault(k, {"strike": k})
        depth = q.get("depth") or {}
        bid = ((depth.get("buy") or [{}])[0]).get("price")
        ask = ((depth.get("sell") or [{}])[0]).get("price")
        row[f"{side}_ltp"] = _num(q.get("last_price"))
        row[f"{side}_bid"] = _num(bid) or None
        row[f"{side}_ask"] = _num(ask) or None
        row[f"{side}_oi"] = _num(q.get("oi"))
        row[f"{side}_volume"] = _num(q.get("volume"))
        row[f"{side}_chg_oi"] = None
        row[f"{side}_iv"] = None
    out = []
    for k in sorted(rows):
        r = rows[k]
        for s in ("c", "p"):
            for f in SIDE_FIELDS:
                r.setdefault(f"{s}_{f}", None)
        out.append(r)
    return {"underlying": name, "spot": spot, "expiry": chosen, "expiries": exps, "source": "kite",
            "lot_size": lot, "rows": out}


def _sum(rows: Sequence[Dict], key: str) -> float:
    return sum(r[key] for r in rows if r.get(key))


def max_pain(rows: Sequence[Dict]) -> Optional[Dict]:
    """Strike at which option BUYERS collectively lose the most (writers pay out the least) at expiry.
    A popularly watched level, not a guarantee: price is under no obligation to settle there."""
    strikes = [r["strike"] for r in rows if r.get("c_oi") or r.get("p_oi")]
    if not strikes:
        return None
    best = None
    for K in sorted({r["strike"] for r in rows}):
        pay = sum((r.get("c_oi") or 0) * max(K - r["strike"], 0) + (r.get("p_oi") or 0) * max(r["strike"] - K, 0) for r in rows)
        if best is None or pay < best[1]:
            best = (K, pay)
    return {"strike": best[0], "payout_per_unit": best[1]}


def atm_strike(rows: Sequence[Dict], spot: float) -> float:
    return min((r["strike"] for r in rows), key=lambda k: abs(k - spot))


def chain_summary(chain: Dict, top: int = 3) -> Dict:
    """OI totals, put/call ratios, max pain, biggest OI walls, ATM straddle and implied move."""
    rows = chain["rows"]
    spot = chain.get("spot")
    c_oi, p_oi = _sum(rows, "c_oi"), _sum(rows, "p_oi")
    c_vol, p_vol = _sum(rows, "c_volume"), _sum(rows, "p_volume")
    res = {
        "underlying": chain.get("underlying"), "spot": spot, "expiry": chain.get("expiry"), "source": chain.get("source"),
        "strikes": len(rows),
        "call_oi": c_oi, "put_oi": p_oi,
        "pcr_oi": (p_oi / c_oi) if c_oi else None,
        "call_volume": c_vol, "put_volume": p_vol,
        "pcr_volume": (p_vol / c_vol) if c_vol else None,
        "max_pain": max_pain(rows),
        "call_oi_walls": [{"strike": r["strike"], "oi": r["c_oi"]} for r in sorted(rows, key=lambda r: -(r.get("c_oi") or 0))[:top] if r.get("c_oi")],
        "put_oi_walls": [{"strike": r["strike"], "oi": r["p_oi"]} for r in sorted(rows, key=lambda r: -(r.get("p_oi") or 0))[:top] if r.get("p_oi")],
    }
    if spot:
        a = atm_strike(rows, spot)
        ar = next(r for r in rows if r["strike"] == a)
        res["atm_strike"] = a

        def px(r, s):
            bid, ask, ltp = r.get(f"{s}_bid"), r.get(f"{s}_ask"), r.get(f"{s}_ltp")
            if bid and ask and ask >= bid:
                return (bid + ask) / 2
            return ltp
        c, p = px(ar, "c"), px(ar, "p")
        if c and p:
            res["atm_straddle"] = c + p
            res["implied_move_pct"] = (c + p) / spot * 100
        ivs = [v for v in (ar.get("c_iv"), ar.get("p_iv")) if v]
        res["atm_iv"] = sum(ivs) / len(ivs) if ivs else None
    return res
