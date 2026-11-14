"""Portfolio trading-backtest for rule-based strategies.

Execution model (no look-ahead):
    * Rules are evaluated on the CLOSE of bar t.
    * Entries and rule-based exits fill at the OPEN of the symbol's next bar, plus slippage.
    * Stops fill at the stop price, or at the open if the bar gaps through it, plus slippage.
    * Targets fill at the target price (or the open on a favourable gap). No slippage on targets.
    * If a bar touches both stop and target, the stop is assumed to fill first (conservative).
    * The entry bar itself can stop out.
    * max_bars exits at the close of the Nth bar held.
    * Positions still open at the end are closed at the last close (flagged end_of_data).

Strategy spec (JSON) - see SPEC_DEFAULTS and skills/trading-backtest/references/strategy-spec.md
"""

from __future__ import annotations

import copy
import math
from typing import Dict, List, Optional

from . import expr, indicators as ind, metrics
from .frame import Bars

SPEC_DEFAULTS: Dict = {
    "name": "strategy",
    "side": "long",                      # long | short
    "entry": None,                       # rule (required)
    "exit": None,                        # optional rule
    "stop": {"type": "atr", "mult": 2.0, "n": 14},   # atr | pct | expr | none
    "target": None,                      # {"type": "r", "value": 2} | {"type": "pct", "value": 10} | {"type":"expr",...}
    "trail": None,                       # {"type": "atr", "mult": 3, "n": 14} | {"type": "pct", "value": 8}
    "max_bars": None,
    "sizing": {"type": "risk", "risk_pct": 1.0},     # risk | percent | fixed
    "max_positions": 5,
    "max_position_pct": 25.0,
    "rank_by": None,                     # rule; higher ranks first when slots are limited
    "initial_capital": 100000.0,
    "costs": {"commission_pct": 0.03, "commission_fixed": 0.0, "slippage_pct": 0.05},
    "lot_size": 1,
    "fractional": False,
    "periods_per_year": None,            # auto: 252 daily, 52 weekly, 12 monthly
    "oos_start": None,                   # date splitting in-sample / out-of-sample
}


class BacktestError(ValueError):
    pass


def normalize_spec(spec: Dict) -> Dict:
    s = copy.deepcopy(SPEC_DEFAULTS)
    for k, v in spec.items():
        if isinstance(v, dict) and isinstance(s.get(k), dict):
            s[k].update(v)
        else:
            s[k] = v
    if not s.get("entry"):
        raise BacktestError("spec needs an 'entry' rule")
    if s["side"] not in ("long", "short"):
        raise BacktestError("side must be long or short")
    expr.compile_expr(s["entry"])
    if s.get("exit"):
        expr.compile_expr(s["exit"])
    if s.get("rank_by"):
        expr.compile_expr(s["rank_by"])
    st = s.get("stop") or {"type": "none"}
    if isinstance(st, str):
        st = {"type": "expr", "value": st}
    s["stop"] = st
    if st["type"] == "expr":
        expr.compile_expr(st["value"])
    if st["type"] not in ("atr", "pct", "expr", "none"):
        raise BacktestError("stop.type must be atr | pct | expr | none")
    if s["sizing"]["type"] == "risk" and st["type"] == "none":
        raise BacktestError("risk-based sizing needs a stop; use sizing.type=percent or add a stop")
    tg = s.get("target")
    if tg and tg.get("type") == "expr":
        expr.compile_expr(tg["value"])
    return s


class _Sym:
    def __init__(self, bars: Bars, spec: Dict):
        self.bars = bars
        ev = expr.Evaluator(bars)
        self.entry = expr.as_bool(ev.series(spec["entry"]))
        self.exit = expr.as_bool(ev.series(spec["exit"])) if spec.get("exit") else None
        self.rank = ev.series(spec["rank_by"]) if spec.get("rank_by") else None
        st = spec["stop"]
        self.atr = None
        if st["type"] == "atr":
            self.atr = ind.atr(bars.high, bars.low, bars.close, int(st.get("n", 14)))
        self.stop_expr = ev.series(st["value"]) if st["type"] == "expr" else None
        tg = spec.get("target") or {}
        self.target_expr = ev.series(tg["value"]) if tg.get("type") == "expr" else None
        tr = spec.get("trail") or {}
        self.trail_atr = ind.atr(bars.high, bars.low, bars.close, int(tr.get("n", 14))) if tr.get("type") == "atr" else None
        self.index = {d: i for i, d in enumerate(bars.date)}


def run(spec: Dict, data: Dict[str, Bars], benchmark: Optional[Bars] = None) -> Dict:
    s = normalize_spec(spec)
    if not data:
        raise BacktestError("no data to backtest")
    syms = {k: _Sym(b, s) for k, b in data.items() if len(b) > 1}
    if not syms:
        raise BacktestError("every symbol has fewer than 2 bars")
    dates = sorted({d for x in syms.values() for d in x.bars.date})
    long = s["side"] == "long"
    sign = 1 if long else -1
    c = s["costs"]
    slip = float(c.get("slippage_pct", 0)) / 100
    com_pct = float(c.get("commission_pct", 0)) / 100
    com_fix = float(c.get("commission_fixed", 0))
    lot = float(s.get("lot_size") or 1)
    fractional = bool(s.get("fractional"))

    cash = float(s["initial_capital"])
    positions: Dict[str, Dict] = {}
    pending_entry: Dict[str, int] = {}
    pending_exit: Dict[str, int] = {}
    last_close: Dict[str, float] = {}
    trades: List[Dict] = []
    equity_curve: List[float] = []
    exposure_bars = 0
    skipped_slots = 0

    def fee(notional: float) -> float:
        return abs(notional) * com_pct + com_fix

    def adverse(px: float, is_entry: bool) -> float:
        # entry long buys higher; exit long sells lower; mirrored for short
        buying = (long and is_entry) or (not long and not is_entry)
        return px * (1 + slip) if buying else px * (1 - slip)

    def close_pos(sym: str, px: float, date: str, i: int, reason: str, apply_slip: bool = True):
        nonlocal cash
        p = positions.pop(sym)
        fill = adverse(px, False) if apply_slip else px
        f = fee(fill * p["qty"])
        cash += sign * p["qty"] * fill - f
        gross = (fill - p["entry_price"]) * p["qty"] * sign
        net = gross - f - p["entry_fee"]
        risk_amt = p["risk_per_unit"] * p["qty"] if p["risk_per_unit"] else None
        bars_held = i - p["entry_i"] + 1
        trades.append({
            "symbol": sym, "side": s["side"], "entry_date": p["entry_date"], "entry_price": round(p["entry_price"], 6),
            "exit_date": date, "exit_price": round(fill, 6), "qty": p["qty"],
            "initial_stop": round(p["initial_stop"], 6) if p["initial_stop"] else None,
            "pnl": round(net, 2), "return_pct": round((fill / p["entry_price"] - 1) * 100 * sign, 3),
            "r_multiple": round(net / risk_amt, 3) if risk_amt else None,
            "bars_held": bars_held, "exit_reason": reason,
            "mae_r": round(p["mae"] / p["risk_per_unit"], 3) if p["risk_per_unit"] else None,
            "mfe_r": round(p["mfe"] / p["risk_per_unit"], 3) if p["risk_per_unit"] else None,
        })

    for d in dates:
        # ---------------- 1. manage open positions on this bar
        for sym in list(positions):
            x = syms[sym]
            i = x.index.get(d)
            if i is None:
                continue
            p = positions[sym]
            o, h, l, cl = x.bars.open[i], x.bars.high[i], x.bars.low[i], x.bars.close[i]
            if i > p["entry_i"]:
                if sym in pending_exit:
                    pending_exit.pop(sym)
                    close_pos(sym, o, d, i, "exit_rule")
                    continue
            # excursions
            p["mae"] = max(p["mae"], (p["entry_price"] - l) if long else (h - p["entry_price"]))
            p["mfe"] = max(p["mfe"], (h - p["entry_price"]) if long else (p["entry_price"] - l))
            stop, target = p["stop"], p["target"]
            px = None
            reason = None
            apply_slip = True
            first_bar = i == p["entry_i"]
            if stop is not None:
                if long:
                    if not first_bar and o <= stop:
                        px, reason = o, "stop_gap"
                    elif l <= stop:
                        px, reason = stop, "stop"
                else:
                    if not first_bar and o >= stop:
                        px, reason = o, "stop_gap"
                    elif h >= stop:
                        px, reason = stop, "stop"
            if px is None and target is not None:
                if long:
                    if not first_bar and o >= target:
                        px, reason, apply_slip = o, "target_gap", False
                    elif h >= target:
                        px, reason, apply_slip = target, "target", False
                else:
                    if not first_bar and o <= target:
                        px, reason, apply_slip = o, "target_gap", False
                    elif l <= target:
                        px, reason, apply_slip = target, "target", False
            if px is not None:
                close_pos(sym, px, d, i, reason, apply_slip)
                continue
            if s.get("max_bars") and (i - p["entry_i"] + 1) >= int(s["max_bars"]):
                close_pos(sym, cl, d, i, "max_bars")
                continue
            # trailing stop update at close (applies from the next bar)
            tr = s.get("trail")
            if tr and tr.get("type"):
                if tr["type"] == "atr" and x.trail_atr and x.trail_atr[i] is not None:
                    cand = cl - sign * float(tr.get("mult", 3)) * x.trail_atr[i]
                elif tr["type"] == "pct":
                    cand = cl * (1 - sign * float(tr["value"]) / 100)
                else:
                    cand = None
                if cand is not None:
                    if p["stop"] is None:
                        p["stop"] = cand
                    else:
                        p["stop"] = max(p["stop"], cand) if long else min(p["stop"], cand)

        # ---------------- 2. new entries at this bar's open (signals from previous bar)
        cands = []
        for sym, sig_i in list(pending_entry.items()):
            x = syms[sym]
            i = x.index.get(d)
            if i is None:
                continue
            pending_entry.pop(sym)
            if i != sig_i + 1 or sym in positions:
                continue
            rank = x.rank[sig_i] if x.rank else 0.0
            cands.append((rank if rank is not None else -math.inf, sym, i, sig_i))
        cands.sort(key=lambda t: t[0], reverse=True)
        for _, sym, i, sig_i in cands:
            if len(positions) >= int(s["max_positions"]):
                skipped_slots += 1
                continue
            x = syms[sym]
            o = x.bars.open[i]
            entry_px = adverse(o, True)
            st = s["stop"]
            stop = None
            if st["type"] == "atr":
                a = x.atr[sig_i]
                if a is None:
                    continue
                stop = entry_px - sign * float(st.get("mult", 2)) * a
            elif st["type"] == "pct":
                stop = entry_px * (1 - sign * float(st["value"]) / 100)
            elif st["type"] == "expr":
                stop = x.stop_expr[sig_i]
                if stop is None:
                    continue
            if stop is not None and ((long and stop >= entry_px) or (not long and stop <= entry_px)):
                continue  # invalid stop (e.g. gapped through) - skip trade
            equity_now = cash + sum(sign * q["qty"] * last_close.get(k, q["entry_price"]) for k, q in positions.items())
            sz = s["sizing"]
            if sz["type"] == "risk":
                budget = equity_now * float(sz.get("risk_pct", 1)) / 100
                units = budget / abs(entry_px - stop)
            elif sz["type"] == "percent":
                units = equity_now * float(sz.get("pct", 10)) / 100 / entry_px
            elif sz["type"] == "fixed":
                units = float(sz["amount"]) / entry_px
            else:
                raise BacktestError("sizing.type must be risk | percent | fixed")
            cap = equity_now * float(s.get("max_position_pct") or 100) / 100 / entry_px
            units = min(units, cap)
            if long:
                units = min(units, max(cash, 0) / (entry_px * (1 + com_pct)))
            units = math.floor(units / lot + 1e-9) * lot if not fractional else units
            if units <= 0:
                continue
            target = None
            tg = s.get("target") or {}
            if tg.get("type") == "r" and stop is not None:
                target = entry_px + sign * float(tg["value"]) * abs(entry_px - stop)
            elif tg.get("type") == "pct":
                target = entry_px * (1 + sign * float(tg["value"]) / 100)
            elif tg.get("type") == "expr":
                target = x.target_expr[sig_i]
            f = fee(entry_px * units)
            cash -= sign * units * entry_px + f
            positions[sym] = {"qty": units, "entry_price": entry_px, "entry_i": i, "entry_date": d,
                              "stop": stop, "initial_stop": stop, "target": target, "entry_fee": f,
                              "risk_per_unit": abs(entry_px - stop) if stop is not None else None,
                              "mae": 0.0, "mfe": 0.0}
            # same-bar stop/target check after entry
            h, l = x.bars.high[i], x.bars.low[i]
            p = positions[sym]
            p["mae"] = max(0.0, (entry_px - l) if long else (h - entry_px))
            p["mfe"] = max(0.0, (h - entry_px) if long else (entry_px - l))
            if stop is not None and ((long and l <= stop) or (not long and h >= stop)):
                close_pos(sym, stop, d, i, "stop")
            elif target is not None and ((long and h >= target) or (not long and l <= target)):
                close_pos(sym, target, d, i, "target", apply_slip=False)

        # ---------------- 3. mark to market
        for sym, x in syms.items():
            i = x.index.get(d)
            if i is not None:
                last_close[sym] = x.bars.close[i]
        eq = cash + sum(sign * p["qty"] * last_close.get(k, p["entry_price"]) for k, p in positions.items())
        equity_curve.append(eq)
        if positions:
            exposure_bars += 1

        # ---------------- 4. signals at this close for the next bar
        for sym, x in syms.items():
            i = x.index.get(d)
            if i is None:
                continue
            if sym in positions:
                if x.exit and x.exit[i]:
                    pending_exit[sym] = i
            elif x.entry[i] and i + 1 < len(x.bars):
                pending_entry[sym] = i

    # close anything still open
    for sym in list(positions):
        x = syms[sym]
        close_pos(sym, x.bars.close[-1], x.bars.date[-1], len(x.bars) - 1, "end_of_data", apply_slip=True)
    if positions == {} and equity_curve:
        equity_curve[-1] = cash

    ppy = s.get("periods_per_year") or _ppy(next(iter(data.values())).interval)
    eq_stats = metrics.equity_stats(equity_curve, dates, ppy)
    tr_stats = metrics.trade_stats(trades)
    result = {
        "name": s["name"], "spec": s, "symbols": sorted(syms),
        "metrics": {**eq_stats, **tr_stats,
                    "exposure_pct": round(exposure_bars / len(dates) * 100, 2) if dates else 0,
                    "skipped_for_slots": skipped_slots},
        "trades": trades,
        "equity": [[d, round(v, 2)] for d, v in zip(dates, equity_curve)],
        "warnings": _warnings(s, trades, data),
    }
    if s.get("oos_start"):
        result["in_sample"] = _segment(dates, equity_curve, trades, None, s["oos_start"], ppy)
        result["out_of_sample"] = _segment(dates, equity_curve, trades, s["oos_start"], None, ppy)
    bm = _benchmark(benchmark, data, dates, float(s["initial_capital"]), ppy)
    if bm:
        result["benchmark"] = bm
    return result


def _ppy(interval: str) -> int:
    return {"1wk": 52, "1mo": 12}.get(interval, 252)


def _segment(dates, equity, trades, start, end, ppy) -> Dict:
    idx = [k for k, d in enumerate(dates) if (start is None or d >= start) and (end is None or d < end)]
    if len(idx) < 2:
        return {"note": "not enough bars in segment"}
    eq = [equity[k] for k in idx]
    ds = [dates[k] for k in idx]
    tr = [t for t in trades if (start is None or t["entry_date"] >= start) and (end is None or t["entry_date"] < end)]
    return {**metrics.equity_stats(eq, ds, ppy), **metrics.trade_stats(tr)}


def _benchmark(bm: Optional[Bars], data: Dict[str, Bars], dates: List[str], capital: float, ppy: int) -> Optional[Dict]:
    if bm is not None and len(bm) > 1:
        series = bm.since(dates[0]).until(dates[-1])
        if len(series) > 1:
            eq = [capital * c / series.close[0] for c in series.close]
            st = metrics.equity_stats(eq, series.date, ppy)
            return {"symbol": bm.symbol, "total_return_pct": st.get("total_return_pct"), "cagr_pct": st.get("cagr_pct"),
                    "max_drawdown_pct": st.get("max_drawdown_pct"), "sharpe": st.get("sharpe"),
                    "equity": [[d, round(v, 2)] for d, v in zip(series.date, eq)]}
    # equal-weight buy & hold of the universe
    rets = []
    for b in data.values():
        if len(b) > 1:
            rets.append(b.close[-1] / b.close[0] - 1)
    if not rets:
        return None
    return {"symbol": "equal_weight_universe", "total_return_pct": round(sum(rets) / len(rets) * 100, 3)}


def _warnings(s: Dict, trades: List[Dict], data: Dict[str, Bars]) -> List[str]:
    w = []
    n = len(trades)
    if n < 30:
        w.append(f"Only {n} trades - results are not statistically meaningful (aim for 100+).")
    if any(not b.meta.get("adjusted", True) for b in data.values()):
        w.append("Some data is unadjusted for splits/dividends - long-history results may be distorted.")
    w.append("Universe chosen today has survivorship bias (delisted losers are missing). Treat results as optimistic.")
    if float(s["costs"].get("slippage_pct", 0)) == 0 and float(s["costs"].get("commission_pct", 0)) == 0:
        w.append("Zero costs assumed - real results will be worse.")
    if not s.get("oos_start"):
        w.append("No out-of-sample split. Set oos_start to check the rules hold on unseen data.")
    return w
