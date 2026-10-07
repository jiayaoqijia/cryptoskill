#!/usr/bin/env python3
"""QuantForge metrics: performance, tail risk, bootstrap CI, IS/OOS split.

Input CSV (one of):
  --returns FILE   column `ret` (periodic simple returns, e.g. 0.002 = 0.2%), optional `date`
  --trades  FILE   column `pnl` (per-trade P&L as a fraction of capital)
Usage:
  python metrics.py --returns r.csv --periods-per-year 252 --cost-bps 2 --oos-frac 0.3
Never feed it invented data. It reports what the file contains, nothing more.
"""
import argparse, json, sys
import numpy as np
import pandas as pd


def perf(r, ppy):
    r = np.asarray(r, dtype=float)
    n = len(r)
    if n < 2:
        return {"error": "need >= 2 observations"}
    eq = np.cumprod(1 + r)
    total = eq[-1] - 1
    years = n / ppy
    cagr = eq[-1] ** (1 / years) - 1 if years > 0 and eq[-1] > 0 else float("nan")
    vol = r.std(ddof=1) * np.sqrt(ppy)
    sharpe = r.mean() / r.std(ddof=1) * np.sqrt(ppy) if r.std(ddof=1) > 0 else float("nan")
    dn = r[r < 0]
    dd_dev = np.sqrt(np.mean(np.minimum(r, 0) ** 2))
    sortino = r.mean() / dd_dev * np.sqrt(ppy) if dd_dev > 0 else float("nan")
    peak = np.maximum.accumulate(eq)
    mdd = ((eq - peak) / peak).min()
    calmar = cagr / abs(mdd) if mdd < 0 else float("nan")
    var95 = np.percentile(r, 5)
    cvar95 = r[r <= var95].mean() if (r <= var95).any() else float("nan")
    wins, losses = r[r > 0], r[r < 0]
    pf = wins.sum() / abs(losses.sum()) if losses.sum() < 0 else float("inf")
    return {
        "n": n, "total_return": total, "cagr": cagr, "ann_vol": vol,
        "sharpe": sharpe, "sortino": sortino, "max_drawdown": mdd, "calmar": calmar,
        "win_rate": float((r > 0).mean()), "profit_factor": pf,
        "expectancy": float(r.mean()),
        "avg_win": float(wins.mean()) if len(wins) else 0.0,
        "avg_loss": float(losses.mean()) if len(losses) else 0.0,
        "skew": float(pd.Series(r).skew()), "excess_kurtosis": float(pd.Series(r).kurt()),
        "var95": float(var95), "cvar95": float(cvar95),
    }


def bootstrap_sharpe(r, ppy, n_boot=2000, block=10, seed=7):
    """Moving-block bootstrap of Sharpe; deterministic via seed."""
    rng = np.random.default_rng(seed)
    r = np.asarray(r, dtype=float)
    n = len(r)
    block = max(1, min(block, n))
    out = []
    for _ in range(n_boot):
        starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
        s = np.concatenate([r[i:i + block] for i in starts])[:n]
        sd = s.std(ddof=1)
        out.append(s.mean() / sd * np.sqrt(ppy) if sd > 0 else np.nan)
    out = np.array(out)
    lo, hi = np.nanpercentile(out, [2.5, 97.5])
    return {"sharpe_ci95": [float(lo), float(hi)], "prob_sharpe_le_0": float(np.nanmean(out <= 0))}


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--returns")
    g.add_argument("--trades")
    ap.add_argument("--periods-per-year", type=float, default=252)
    ap.add_argument("--cost-bps", type=float, default=0.0,
                    help="extra cost per observation (per trade for --trades), in bps")
    ap.add_argument("--oos-frac", type=float, default=0.3)
    a = ap.parse_args()

    if a.returns:
        df = pd.read_csv(a.returns)
        if "ret" not in df: sys.exit("DATA REQUIRED: column 'ret' missing")
        r = df["ret"].astype(float).to_numpy()
    else:
        df = pd.read_csv(a.trades)
        if "pnl" not in df: sys.exit("DATA REQUIRED: column 'pnl' missing")
        r = df["pnl"].astype(float).to_numpy()
    r = r[~np.isnan(r)]
    if len(r) < 30:
        print("WARNING: fewer than 30 observations; statistics are unreliable", file=sys.stderr)

    rc = r - a.cost_bps / 1e4
    split = int(len(rc) * (1 - a.oos_frac))
    ppy = a.periods_per_year
    report = {
        "full": perf(rc, ppy),
        "in_sample": perf(rc[:split], ppy) if split >= 2 else None,
        "out_of_sample": perf(rc[split:], ppy) if len(rc) - split >= 2 else None,
        "bootstrap": bootstrap_sharpe(rc, ppy),
        "cost_stress_2x_sharpe": perf(r - 2 * a.cost_bps / 1e4, ppy).get("sharpe"),
        "note": "OOS split is chronological and fixed; do not tune on it. Results are historical only.",
    }
    print(json.dumps(report, indent=2, default=lambda x: None if x != x else float(x)))


if __name__ == "__main__":
    main()
