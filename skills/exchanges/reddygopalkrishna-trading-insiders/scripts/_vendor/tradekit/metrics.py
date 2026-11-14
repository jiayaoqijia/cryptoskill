"""Performance statistics for equity curves and trade lists."""

from __future__ import annotations

import datetime as dt
import math
import statistics
from typing import Dict, List, Optional, Sequence


def _years(dates: Sequence[str]) -> float:
    if len(dates) < 2:
        return 0.0
    a = dt.date.fromisoformat(dates[0][:10])
    b = dt.date.fromisoformat(dates[-1][:10])
    return max((b - a).days / 365.25, 1e-9)


def drawdown_series(equity: Sequence[float]) -> List[float]:
    peak = -math.inf
    out = []
    for v in equity:
        peak = max(peak, v)
        out.append((v / peak - 1) * 100 if peak > 0 else 0.0)
    return out


def max_drawdown(equity: Sequence[float], dates: Optional[Sequence[str]] = None) -> Dict:
    if not equity:
        return {"max_drawdown_pct": 0.0}
    dd = drawdown_series(equity)
    i = min(range(len(dd)), key=dd.__getitem__)
    peak_i = max(range(i + 1), key=lambda k: equity[k]) if i else 0
    rec_i = next((k for k in range(i, len(equity)) if equity[k] >= equity[peak_i]), None)
    out = {"max_drawdown_pct": round(dd[i], 3)}
    if dates:
        out.update({"peak_date": dates[peak_i], "trough_date": dates[i],
                    "recovery_date": dates[rec_i] if rec_i is not None and rec_i > i else None})
        # longest time under water in bars
    longest = cur = 0
    for v in dd:
        cur = cur + 1 if v < 0 else 0
        longest = max(longest, cur)
    out["longest_underwater_bars"] = longest
    return out


def equity_stats(equity: Sequence[float], dates: Sequence[str], periods_per_year: int = 252,
                 risk_free_pct: float = 0.0) -> Dict:
    if len(equity) < 2:
        return {}
    rets = [equity[i] / equity[i - 1] - 1 for i in range(1, len(equity)) if equity[i - 1] > 0]
    total = equity[-1] / equity[0] - 1
    yrs = _years(dates)
    cagr = (equity[-1] / equity[0]) ** (1 / yrs) - 1 if yrs > 0 and equity[-1] > 0 else None
    rf = risk_free_pct / 100 / periods_per_year
    ex = [r - rf for r in rets]
    sd = statistics.pstdev(ex) if len(ex) > 1 else 0.0
    downside = [min(0.0, r) for r in ex]
    dsd = math.sqrt(sum(d * d for d in downside) / len(downside)) if downside else 0.0
    mean = statistics.fmean(ex) if ex else 0.0
    sharpe = mean / sd * math.sqrt(periods_per_year) if sd > 0 else None
    sortino = mean / dsd * math.sqrt(periods_per_year) if dsd > 0 else None
    mdd = max_drawdown(equity, dates)
    calmar = (cagr * 100 / abs(mdd["max_drawdown_pct"])) if cagr is not None and mdd["max_drawdown_pct"] < 0 else None
    return {
        "start": dates[0], "end": dates[-1], "years": round(yrs, 2),
        "start_equity": round(equity[0], 2), "end_equity": round(equity[-1], 2),
        "total_return_pct": round(total * 100, 3),
        "cagr_pct": round(cagr * 100, 3) if cagr is not None else None,
        "volatility_pct": round(statistics.pstdev(rets) * math.sqrt(periods_per_year) * 100, 3) if len(rets) > 1 else None,
        "sharpe": round(sharpe, 3) if sharpe is not None else None,
        "sortino": round(sortino, 3) if sortino is not None else None,
        "calmar": round(calmar, 3) if calmar is not None else None,
        **mdd,
    }


def trade_stats(trades: Sequence[Dict]) -> Dict:
    """trades need 'pnl'; optional 'r_multiple', 'bars_held'/'hold_days'."""
    closed = [t for t in trades if t.get("pnl") is not None]
    n = len(closed)
    if n == 0:
        return {"trades": 0}
    pnl = [float(t["pnl"]) for t in closed]
    wins = [p for p in pnl if p > 0]
    losses = [p for p in pnl if p < 0]
    rs = [float(t["r_multiple"]) for t in closed if t.get("r_multiple") is not None]
    gross_win = sum(wins)
    gross_loss = -sum(losses)
    win_rate = len(wins) / n
    avg_win = gross_win / len(wins) if wins else 0.0
    avg_loss = gross_loss / len(losses) if losses else 0.0
    streak_w = streak_l = cur_w = cur_l = 0
    for p in pnl:
        if p > 0:
            cur_w += 1
            cur_l = 0
        elif p < 0:
            cur_l += 1
            cur_w = 0
        streak_w = max(streak_w, cur_w)
        streak_l = max(streak_l, cur_l)
    out = {
        "trades": n, "wins": len(wins), "losses": len(losses),
        "win_rate_pct": round(win_rate * 100, 2),
        "net_pnl": round(sum(pnl), 2), "gross_profit": round(gross_win, 2), "gross_loss": round(-gross_loss, 2),
        "avg_win": round(avg_win, 2), "avg_loss": round(-avg_loss, 2),
        "payoff_ratio": round(avg_win / avg_loss, 3) if avg_loss else None,
        "profit_factor": round(gross_win / gross_loss, 3) if gross_loss else None,
        "expectancy": round(sum(pnl) / n, 2),
        "best_trade": round(max(pnl), 2), "worst_trade": round(min(pnl), 2),
        "max_consecutive_wins": streak_w, "max_consecutive_losses": streak_l,
    }
    if rs:
        mean_r = statistics.fmean(rs)
        sd_r = statistics.pstdev(rs) if len(rs) > 1 else 0.0
        out.update({
            "avg_r": round(mean_r, 3), "median_r": round(statistics.median(rs), 3),
            "total_r": round(sum(rs), 2),
            "sqn": round(mean_r / sd_r * math.sqrt(min(len(rs), 100)), 3) if sd_r > 0 else None,
            "r_trades": len(rs),
        })
    holds = [t.get("bars_held") or t.get("hold_days") for t in closed if (t.get("bars_held") or t.get("hold_days")) is not None]
    if holds:
        out["avg_hold"] = round(statistics.fmean(holds), 2)
        win_h = [t.get("bars_held") or t.get("hold_days") for t in closed if t["pnl"] > 0 and (t.get("bars_held") or t.get("hold_days")) is not None]
        loss_h = [t.get("bars_held") or t.get("hold_days") for t in closed if t["pnl"] < 0 and (t.get("bars_held") or t.get("hold_days")) is not None]
        out["avg_hold_winners"] = round(statistics.fmean(win_h), 2) if win_h else None
        out["avg_hold_losers"] = round(statistics.fmean(loss_h), 2) if loss_h else None
    return out


def histogram(values: Sequence[float], bins: int = 12) -> List[Dict]:
    if not values:
        return []
    lo, hi = min(values), max(values)
    if lo == hi:
        return [{"lo": lo, "hi": hi, "count": len(values)}]
    w = (hi - lo) / bins
    counts = [0] * bins
    for v in values:
        counts[min(bins - 1, int((v - lo) / w))] += 1
    return [{"lo": round(lo + i * w, 4), "hi": round(lo + (i + 1) * w, 4), "count": c} for i, c in enumerate(counts)]
