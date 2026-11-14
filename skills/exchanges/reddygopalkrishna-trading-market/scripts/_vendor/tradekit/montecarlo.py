"""Monte Carlo simulators.

simulate_trades  - resample a list of R-multiples to see the range of equity
                   paths, drawdowns and risk of ruin a system can produce.
simulate_setup   - block-bootstrap the symbol's own recent bars to estimate the
                   odds that a trade hits its target before its stop.
Both are simulations of the past, not predictions.
"""

from __future__ import annotations

import math
import random
import statistics
from typing import Dict, List, Optional, Sequence

from .frame import Bars


def _pct(sorted_vals: List[float], p: float) -> float:
    if not sorted_vals:
        return float("nan")
    k = (len(sorted_vals) - 1) * p / 100
    f = math.floor(k)
    c = min(f + 1, len(sorted_vals) - 1)
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def simulate_trades(r_multiples: Sequence[float], risk_pct: float = 1.0, n_trades: Optional[int] = None,
                    n_sims: int = 10000, start_equity: float = 100000.0, ruin_dd_pct: float = 50.0,
                    dd_thresholds=(10, 20, 30), seed: Optional[int] = 7, compounding: bool = True) -> Dict:
    rs = [float(r) for r in r_multiples if r is not None]
    if len(rs) < 5:
        raise ValueError("need at least 5 trade R-multiples")
    n_trades = int(n_trades or len(rs))
    rng = random.Random(seed)
    finals: List[float] = []
    max_dds: List[float] = []
    ruined = 0
    dd_hits = {t: 0 for t in dd_thresholds}
    losing_streaks: List[int] = []
    sample_paths: List[List[float]] = []
    for sim in range(n_sims):
        eq = start_equity
        peak = eq
        mdd = 0.0
        streak = best_streak = 0
        path = [eq] if sim < 50 else None
        for _ in range(n_trades):
            r = rng.choice(rs)
            base = eq if compounding else start_equity
            eq += base * risk_pct / 100 * r
            if eq <= 0:
                eq = 0.0
            peak = max(peak, eq)
            dd = (eq / peak - 1) * 100 if peak > 0 else -100
            mdd = min(mdd, dd)
            streak = streak + 1 if r < 0 else 0
            best_streak = max(best_streak, streak)
            if path is not None:
                path.append(round(eq, 2))
            if eq == 0:
                break
        finals.append(eq)
        max_dds.append(mdd)
        losing_streaks.append(best_streak)
        if mdd <= -ruin_dd_pct:
            ruined += 1
        for t in dd_thresholds:
            if mdd <= -t:
                dd_hits[t] += 1
        if path is not None:
            sample_paths.append(path)
    finals.sort()
    max_dds.sort()
    rets = [(f / start_equity - 1) * 100 for f in finals]
    wins = [r for r in rs if r > 0]
    return {
        "inputs": {"trades_sampled_from": len(rs), "n_trades": n_trades, "n_sims": n_sims, "risk_pct": risk_pct,
                   "compounding": compounding, "avg_r": round(statistics.fmean(rs), 4),
                   "win_rate_pct": round(len(wins) / len(rs) * 100, 2)},
        "final_return_pct": {p: round(_pct(sorted(rets), p), 2) for p in (5, 25, 50, 75, 95)},
        "max_drawdown_pct": {p: round(_pct(max_dds, 100 - p), 2) for p in (5, 25, 50, 75, 95)},
        "prob_loss_pct": round(sum(1 for r in rets if r < 0) / n_sims * 100, 2),
        "prob_drawdown_pct": {f">={t}%": round(dd_hits[t] / n_sims * 100, 2) for t in dd_thresholds},
        "risk_of_ruin_pct": round(ruined / n_sims * 100, 3),
        "ruin_definition": f"drawdown of {ruin_dd_pct}% or more",
        "worst_losing_streak": {p: _pct(sorted(losing_streaks), p) for p in (50, 95)},
        "sample_paths": sample_paths[:30],
    }


def simulate_setup(bars: Bars, entry: float, stop: float, target: float, horizon: int = 20,
                   n_sims: int = 10000, lookback: int = 250, block: int = 5, seed: Optional[int] = 7) -> Dict:
    """Bootstrap the symbol's recent bar shapes forward from `entry`.

    Each simulated bar is a block-sampled historical bar expressed relative to the
    previous close (open/high/low/close ratios), which keeps gaps, ranges and
    short-term autocorrelation. Stop is checked before target within a bar.
    """
    if len(bars) < max(30, block + 2):
        raise ValueError("need at least 30 bars of history")
    long = target > entry
    if long and not stop < entry:
        raise ValueError("long setup needs stop < entry < target")
    if not long and not stop > entry:
        raise ValueError("short setup needs target < entry < stop")
    b = bars.tail(lookback + 1)
    rel = []
    for i in range(1, len(b)):
        pc = b.close[i - 1]
        rel.append((b.open[i] / pc, b.high[i] / pc, b.low[i] / pc, b.close[i] / pc))
    rng = random.Random(seed)
    outcomes = {"target": 0, "stop": 0, "open": 0}
    bars_to: Dict[str, List[int]] = {"target": [], "stop": []}
    final_r: List[float] = []
    risk = abs(entry - stop)
    for _ in range(n_sims):
        price = entry
        hit = None
        step = 0
        while step < horizon and hit is None:
            start = rng.randrange(0, len(rel) - block + 1)
            for k in range(block):
                if step >= horizon:
                    break
                o, h, l, c = rel[start + k]
                op, hi, lo, cl = price * o, price * h, price * l, price * c
                step += 1
                if long:
                    if op <= stop or lo <= stop:
                        hit, exit_px = "stop", min(op, stop)
                    elif op >= target or hi >= target:
                        hit, exit_px = "target", max(op, target) if op >= target else target
                else:
                    if op >= stop or hi >= stop:
                        hit, exit_px = "stop", max(op, stop)
                    elif op <= target or lo <= target:
                        hit, exit_px = "target", min(op, target) if op <= target else target
                if hit:
                    bars_to[hit].append(step)
                    break
                price = cl
        if hit is None:
            outcomes["open"] += 1
            final_r.append(((price - entry) if long else (entry - price)) / risk)
        else:
            outcomes[hit] += 1
            final_r.append(((exit_px - entry) if long else (entry - exit_px)) / risk)
    rr = abs(target - entry) / risk
    p_t = outcomes["target"] / n_sims
    p_s = outcomes["stop"] / n_sims
    breakeven = 1 / (1 + rr)
    fr = sorted(final_r)
    return {
        "setup": {"side": "long" if long else "short", "entry": entry, "stop": stop, "target": target,
                  "reward_risk": round(rr, 3), "horizon_bars": horizon},
        "history": {"bars_used": len(rel), "block": block, "from": b.date[0], "to": b.date[-1]},
        "prob_target_first_pct": round(p_t * 100, 2),
        "prob_stop_first_pct": round(p_s * 100, 2),
        "prob_neither_pct": round(outcomes["open"] / n_sims * 100, 2),
        "breakeven_win_rate_pct": round(breakeven * 100, 2),
        "expected_r": round(statistics.fmean(final_r), 3),
        "r_percentiles": {p: round(_pct(fr, p), 3) for p in (5, 25, 50, 75, 95)},
        "median_bars_to_target": statistics.median(bars_to["target"]) if bars_to["target"] else None,
        "median_bars_to_stop": statistics.median(bars_to["stop"]) if bars_to["stop"] else None,
        "verdict": _verdict(p_t, p_s, breakeven, statistics.fmean(final_r)),
        "n_sims": n_sims,
    }


def _verdict(p_t: float, p_s: float, breakeven: float, exp_r: float) -> str:
    decided = p_t + p_s
    if decided == 0:
        return "inconclusive - price rarely reaches either level within the horizon"
    wr = p_t / decided
    if exp_r > 0.15 and wr > breakeven + 0.05:
        return "favourable - positive expected R and hit rate above breakeven"
    if exp_r > 0:
        return "marginal - small positive expected R; costs and slippage could erase it"
    return "unfavourable - negative expected R for this stop/target over the horizon"
