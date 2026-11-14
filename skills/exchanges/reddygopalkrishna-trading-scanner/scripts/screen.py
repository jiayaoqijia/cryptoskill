#!/usr/bin/env python3
"""Screen a universe with a rule (or preset), rank the matches, show key columns.

Examples
  python3 scripts/screen.py --presets
  python3 scripts/screen.py --universe watchlist.txt --preset trend-template
  python3 scripts/screen.py --universe AAPL,MSFT,NVDA,AMZN --rule "close > sma(200) and rsi(2) < 10" --rank "-rsi(2)"
  python3 scripts/screen.py --universe list.txt --rule "rel_volume(50) > 2 and close > shift(high, 1)" --min-price 5
  python3 scripts/screen.py --universe list.txt --preset squeeze --json --save hits.txt
  python3 scripts/screen.py --check "cross_above(ema(20), ema(50))"
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, data, expr  # noqa: E402

PRESETS = {
    "trend-template": {
        "rule": "close > sma(150) and close > sma(200) and sma(150) > sma(200) and sma(200) > shift(sma(200), 21) "
                "and sma(50) > sma(150) and close > sma(50) and pct_from_low(252) >= 30 and pct_from_high(252) >= -25",
        "rank": "roc(126)", "about": "Minervini stage-2 trend template (all 8 criteria)"},
    "momentum-leaders": {
        "rule": "close > sma(50) and sma(50) > sma(200) and roc(126) > 20",
        "rank": "roc(126)", "about": "Strong 6-month momentum in a confirmed uptrend"},
    "breakout-volume": {
        "rule": "close > shift(highest(high, 20), 1) and rel_volume(50) >= 1.5",
        "rank": "rel_volume(50)", "about": "Closed above the prior 20-bar high on 1.5x+ volume"},
    "near-52w-high": {
        "rule": "pct_from_high(252) >= -3 and close > sma(50)",
        "rank": "pct_from_high(252)", "about": "Within 3% of the 52-week high"},
    "oversold-in-uptrend": {
        "rule": "close > sma(200) and rsi(2) < 10",
        "rank": "-rsi(2)", "about": "Short-term washout inside a long-term uptrend (Connors RSI-2)"},
    "pullback-to-ema": {
        "rule": "close > sma(200) and low <= ema(21) and close > ema(21) and adx(14) > 20",
        "rank": "adx(14)", "about": "Trending stock tagging its 21-EMA and holding"},
    "squeeze": {
        "rule": "percentile(bb_width(20), 120) <= 10 and close > sma(50)",
        "rank": "-bb_width(20)", "about": "Bollinger width in the bottom 10% of 6 months, above the 50-SMA"},
    "golden-cross": {
        "rule": "cross_above(sma(50), sma(200))", "rank": "roc(63)", "about": "50-SMA crossed above 200-SMA today"},
    "death-cross": {
        "rule": "cross_below(sma(50), sma(200))", "rank": "-roc(63)", "about": "50-SMA crossed below 200-SMA today"},
    "macd-bull-cross": {
        "rule": "cross_above(macd(), macd_signal()) and close > sma(200)",
        "rank": "roc(63)", "about": "MACD crossed above its signal line, above the 200-SMA"},
    "supertrend-flip-up": {
        "rule": "supertrend_dir(10, 3) == 1 and shift(supertrend_dir(10, 3), 1) == -1",
        "rank": "rel_volume(50)", "about": "Supertrend turned up today"},
    "gap-up-volume": {
        "rule": "open > shift(high, 1) * 1.02 and rel_volume(50) >= 2 and close > open",
        "rank": "rel_volume(50)", "about": "2%+ gap above yesterday's high on 2x volume, held into the close"},
    "oversold-bounce": {
        "rule": "rsi(14) < 35 and close > open and close > shift(close, 1) and low <= lowest(low, 20)",
        "rank": "-rsi(14)", "about": "Reversal day from a 20-bar low with RSI under 35"},
    "high-adx-trend": {
        "rule": "adx(14) > 30 and plus_di(14) > minus_di(14) and close > ema(21)",
        "rank": "adx(14)", "about": "Strong, established uptrend (ADX > 30)"},
}

COLUMNS = {
    "close": "close",
    "chg_1d_%": "pct_change(close, 1)",
    "rsi14": "rsi(14)",
    "roc_3m_%": "roc(63)",
    "rel_vol": "rel_volume(50)",
    "from_high_%": "pct_from_high(252)",
    "atr_%": "atr_pct(14)",
}


def md(r):
    head = f"## Screen: {r['label']} - {len(r['matches'])} of {r['scanned']} matched"
    out = [head, f"Rule: `{r['rule']}`" + (f"  |  rank by `{r['rank']}`" if r.get("rank") else ""), ""]
    if r["matches"]:
        cols = ["symbol"] + (["rank"] if r.get("rank") else []) + list(COLUMNS)
        out.append(cli.md_table(r["matches"][: r["limit"]], cols))
    else:
        out.append("No matches. Loosen the rule or widen the universe.")
    if r["errors"]:
        out.append("")
        out.append(f"Skipped {len(r['errors'])} symbols: " + "; ".join(f"{k} ({v[:60]})" for k, v in list(r["errors"].items())[:8]))
    if r.get("saved"):
        out.append(f"\nSaved matches to `{r['saved']}`")
    out.append("\n_A screen finds candidates, not trades. Check each with trading-chart / trading-patterns._")
    return "\n".join(out)


def main():
    p = cli.parser(__doc__)
    p.add_argument("symbols", nargs="*")
    p.add_argument("--universe", help="file (one symbol per line or CSV with a symbol column) or comma list")
    p.add_argument("--preset", choices=sorted(PRESETS))
    p.add_argument("--rule", help="rule expression (see references/rule-language.md)")
    p.add_argument("--rank", help="expression to sort matches by (descending)")
    p.add_argument("--min-price", type=float)
    p.add_argument("--min-avg-volume", type=float, help="minimum 50-bar average volume (shares/units)")
    p.add_argument("--min-dollar-volume", type=float, help="minimum 50-bar average close*volume")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--save", help="write matching symbols to this file")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--interval", default="1d", choices=data.INTERVALS)
    p.add_argument("--period", default="2y", choices=data.PERIODS)
    p.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    p.add_argument("--presets", action="store_true", help="list presets")
    p.add_argument("--check", metavar="RULE", help="validate a rule and exit")
    p.add_argument("--functions", action="store_true", help="list rule functions")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.presets:
        cli.emit(PRESETS, a.json, lambda d: "\n".join(f"- **{k}** - {v['about']}\n  `{v['rule']}`" for k, v in d.items()))
        return
    if a.functions:
        print(expr.help_text())
        return
    if a.check:
        expr.compile_expr(a.check)
        print(f"OK: {a.check}")
        return

    if a.preset:
        rule = PRESETS[a.preset]["rule"]
        rank = a.rank or PRESETS[a.preset]["rank"]
        label = a.preset
    elif a.rule:
        rule, rank, label = a.rule, a.rank, "custom"
    else:
        cli.fail("give --preset NAME or --rule EXPR (see --presets)")
    filters = []
    if a.min_price:
        filters.append(f"close >= {a.min_price}")
    if a.min_avg_volume:
        filters.append(f"sma(volume, 50) >= {a.min_avg_volume}")
    if a.min_dollar_volume:
        filters.append(f"sma(close * volume, 50) >= {a.min_dollar_volume}")
    full_rule = " and ".join([f"({rule})"] + filters) if filters else rule
    tree = expr.compile_expr(full_rule)
    rank_tree = expr.compile_expr(rank) if rank else None
    col_trees = {k: expr.compile_expr(v) for k, v in COLUMNS.items()}

    syms = data.load_universe(a.universe, a.symbols)
    if not syms:
        cli.fail("no symbols: pass --universe FILE|A,B,C or symbols")
    series, errors = data.get_many(syms, a.interval, a.period, a.provider, workers=a.workers)
    matches = []
    for sym, b in series.items():
        if len(b) < 2:
            errors[sym] = "not enough bars"
            continue
        ev = expr.Evaluator(b)
        try:
            ok = ev.last(tree)
        except expr.ExprError:
            raise
        except Exception as e:  # noqa: BLE001
            errors[sym] = f"eval failed: {e}"
            continue
        if not ok:
            continue
        row = {"symbol": sym, "date": b.date[-1]}
        if rank_tree is not None:
            v = ev.last(rank_tree)
            row["rank"] = round(v, 4) if isinstance(v, (int, float)) and not isinstance(v, bool) else v
        for k, t in col_trees.items():
            v = ev.last(t)
            row[k] = round(v, 2) if isinstance(v, float) else v
        matches.append(row)
    if rank_tree is not None:
        matches.sort(key=lambda r: (r.get("rank") is None, -(r.get("rank") or 0)))
    saved = None
    if a.save and matches:
        with open(a.save, "w") as fh:
            fh.write("\n".join(m["symbol"] for m in matches) + "\n")
        saved = os.path.abspath(a.save)
    cli.emit({"label": label, "rule": full_rule, "rank": rank, "scanned": len(series), "matches": matches,
              "errors": errors, "limit": a.limit, "saved": saved}, a.json, md)


if __name__ == "__main__":
    cli.run(main)
