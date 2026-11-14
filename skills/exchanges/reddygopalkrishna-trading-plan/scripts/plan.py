#!/usr/bin/env python3
"""Build a complete trade plan: entry, stop options, targets, reward:risk, position size.

Examples
  python3 scripts/plan.py AAPL                                   # long at last close, auto stop/targets
  python3 scripts/plan.py AAPL --entry 195.5 --stop 188 --target 215
  python3 scripts/plan.py NVDA --entry pivot --stop pattern       # use the best live chart pattern
  python3 scripts/plan.py TSLA --side short --stop atr:2.5 --target r:2
  python3 scripts/plan.py BTC-USD --stop pct:6 --fractional --lot 0.0001
  python3 scripts/plan.py ES=F --stop atr:1.5 --multiplier 50 --lot 1
  python3 scripts/plan.py AAPL --regime-adjust --save --setup "VCP breakout" --thesis "3rd contraction, volume dry-up"
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import analysis, cli, config, data, indicators as ind, patterns, risk  # noqa: E402
from tradekit.journal import Journal  # noqa: E402


def parse_level(spec, kind):
    if spec is None:
        return None, None
    s = str(spec).strip().lower()
    for prefix in ("atr:", "pct:", "r:"):
        if s.startswith(prefix):
            return prefix[:-1], float(s[len(prefix):])
    if s in ("swing", "pattern", "pivot", "market", "resistance", "support", "auto"):
        return s, None
    return "price", float(s)


def main():
    p = cli.parser(__doc__)
    p.add_argument("symbol", nargs="?")
    p.add_argument("--symbol", dest="symbol_opt")
    p.add_argument("--side", default="long", choices=["long", "short"])
    p.add_argument("--entry", default="market", help="price | market (last close) | pivot (pattern trigger)")
    p.add_argument("--stop", default="auto", help="price | atr:MULT | pct:N | swing | pattern | auto")
    p.add_argument("--target", default="auto", help="price | r:MULT | pct:N | resistance | auto")
    p.add_argument("--risk-pct", type=float, help="risk per trade %% (default from config)")
    p.add_argument("--equity", type=float, help="account equity (default: broker, then config)")
    p.add_argument("--lot", type=float, default=1, help="tradable increment (shares, contracts, coin units)")
    p.add_argument("--multiplier", type=float, default=1.0, help="contract point value (futures/options)")
    p.add_argument("--margin-pct", type=float, default=100.0, help="capital needed as %% of notional")
    p.add_argument("--fractional", action="store_true", help="allow fractional quantities (crypto)")
    p.add_argument("--regime-adjust", action="store_true", help="scale risk by trading-market exposure")
    p.add_argument("--benchmark", help="index for --regime-adjust (default config)")
    p.add_argument("--save", action="store_true", help="save as a planned trade in the journal")
    p.add_argument("--setup", default="")
    p.add_argument("--thesis", default="")
    data.add_data_args(p, period="2y")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    cfg = config.load()
    sym = a.symbol or a.symbol_opt
    b = data.load_bars(sym, a.csv, a.interval, a.period, a.provider, min_bars=30)
    sym = b.symbol
    long = a.side == "long"
    sign = 1 if long else -1
    last = b.close[-1]
    atr14 = ind.atr(b.high, b.low, b.close, 14)[-1]
    lv = analysis.levels(b)
    best_pat = None
    pats = patterns.scan(b) if len(b) >= 60 else []
    if pats:
        best_pat = pats[0]

    # ---------------- entry
    ek, ev = parse_level(a.entry, "entry")
    notes = []
    if ek == "price":
        entry = ev
        entry_type = "limit" if (long and entry <= last) or (not long and entry >= last) else "stop"
    elif ek == "pivot":
        if not best_pat:
            cli.fail("no live chart pattern found for --entry pivot; give a price")
        entry = best_pat["pivot"] * (1.001 if long else 0.999)
        entry_type = "stop"
        notes.append(f"entry just beyond the {best_pat['pattern']} pivot {best_pat['pivot']}")
    else:
        entry = last
        entry_type = "limit"
    # ---------------- stop candidates
    cands = {}
    if atr14:
        cands["atr_2x"] = entry - sign * 2 * atr14
        cands["atr_1.5x"] = entry - sign * 1.5 * atr14
    if long and lv["support"]:
        s0 = next((x["price"] for x in lv["support"] if x["price"] < entry * 0.995), None)
        if s0:
            cands["below_support"] = s0 - 0.25 * (atr14 or 0)
    if not long and lv["resistance"]:
        r0 = next((x["price"] for x in lv["resistance"] if x["price"] > entry * 1.005), None)
        if r0:
            cands["above_resistance"] = r0 + 0.25 * (atr14 or 0)
    recent = b.tail(10)
    cands["swing_10bar"] = (min(recent.low) - 0.1 * (atr14 or 0)) if long else (max(recent.high) + 0.1 * (atr14 or 0))
    if best_pat and long:
        cands["pattern"] = best_pat["stop"]

    sk, sv = parse_level(a.stop, "stop")
    if sk == "price":
        stop, stop_basis = sv, "manual"
    elif sk == "atr":
        if not atr14:
            cli.fail("not enough bars for ATR")
        stop, stop_basis = entry - sign * sv * atr14, f"{sv}x ATR"
    elif sk == "pct":
        stop, stop_basis = entry * (1 - sign * sv / 100), f"{sv}%"
    elif sk == "swing":
        stop, stop_basis = cands["swing_10bar"], "10-bar swing"
    elif sk == "pattern":
        if "pattern" not in cands:
            cli.fail("no pattern stop available")
        stop, stop_basis = cands["pattern"], f"{best_pat['pattern']} low"
    else:
        # auto: the structural stop if it sits within 1-3 ATR, else 2 ATR
        struct = cands.get("pattern") or cands.get("below_support") or cands.get("above_resistance") or cands["swing_10bar"]
        dist = abs(entry - struct) / atr14 if atr14 else None
        if dist is not None and 0.8 <= dist <= 3.0:
            stop, stop_basis = struct, "structure (pattern/support/swing)"
        else:
            stop, stop_basis = cands.get("atr_2x", struct), "2x ATR (structure too near/far)"
    if (long and stop >= entry) or (not long and stop <= entry):
        cli.fail(f"stop {stop:.4f} is on the wrong side of entry {entry:.4f}")
    risk_unit = abs(entry - stop)

    # ---------------- targets
    tk, tv = parse_level(a.target, "target")
    r_levels = [{"label": f"{r}R", "price": round(entry + sign * r * risk_unit, 4)} for r in (1, 2, 3)]
    struct_t = None
    if long and lv["resistance"]:
        struct_t = next((x["price"] for x in lv["resistance"] if x["price"] > entry * 1.005), None)
    if not long and lv["support"]:
        struct_t = next((x["price"] for x in lv["support"] if x["price"] < entry * 0.995), None)
    if tk == "price":
        target, target_basis = tv, "manual"
    elif tk == "r":
        target, target_basis = entry + sign * tv * risk_unit, f"{tv}R"
    elif tk == "pct":
        target, target_basis = entry * (1 + sign * tv / 100), f"{tv}%"
    elif tk == "resistance":
        if not struct_t:
            cli.fail("no resistance/support level beyond entry")
        target, target_basis = struct_t, "next level"
    else:
        if struct_t and abs(struct_t - entry) / risk_unit >= cfg["risk"]["min_reward_risk"]:
            target, target_basis = struct_t, "next resistance/support level"
        else:
            target, target_basis = entry + sign * 2 * risk_unit, "2R (no level far enough)"
            if struct_t:
                notes.append(f"nearest level {struct_t:.2f} is closer than {cfg['risk']['min_reward_risk']}R - "
                             "price may stall there")
    rr = abs(target - entry) / risk_unit

    # ---------------- sizing
    equity = a.equity
    equity_src = "argument"
    if equity is None:
        try:
            from tradekit.brokers import get_broker
            equity = float(get_broker().account()["equity"])
            equity_src = f"{cfg['broker']['name']} broker"
        except Exception:  # noqa: BLE001
            equity = float(cfg["account"]["equity"])
            equity_src = "config"
    risk_pct = a.risk_pct if a.risk_pct is not None else float(cfg["risk"]["risk_per_trade_pct"])
    regime_info = None
    if a.regime_adjust:
        bm = a.benchmark or cfg["account"].get("benchmark")
        if bm:
            try:
                rg = analysis.regime(data.get_bars(bm, "1d", "2y", min_bars=220))
                regime_info = {"index": bm, "regime": rg["regime"], "exposure_pct": rg["suggested_exposure_pct"]}
                risk_pct = risk_pct * rg["suggested_exposure_pct"] / 100
            except Exception as e:  # noqa: BLE001
                notes.append(f"regime adjust skipped: {e}")
        else:
            notes.append("regime adjust skipped: no benchmark configured")
    size = risk.position_size(equity, entry, stop, risk_pct, lot_size=a.lot, multiplier=a.multiplier,
                              max_position_pct=cfg["risk"]["max_position_pct"], fractional=a.fractional,
                              margin_pct=a.margin_pct) if risk_pct > 0 else None
    if size and size["binding_constraint"] != "risk":
        notes.append(f"size capped by {size['binding_constraint']} limit, actual risk {size['actual_risk_pct']}%")
    if atr14 and risk_unit < 0.7 * atr14:
        notes.append(f"stop is only {risk_unit / atr14:.1f}x ATR away - normal noise may hit it")
    if rr < cfg["risk"]["min_reward_risk"]:
        notes.append(f"reward:risk {rr:.2f} is below your minimum {cfg['risk']['min_reward_risk']} - gate will FAIL")

    plan = {
        "symbol": sym, "side": a.side, "date": b.date[-1], "last_price": round(last, 4),
        "entry": round(entry, 4), "entry_order": entry_type, "stop": round(stop, 4), "stop_basis": stop_basis,
        "target": round(target, 4), "target_basis": target_basis, "reward_risk": round(rr, 2),
        "risk_per_unit": round(risk_unit, 4), "atr14": round(atr14, 4) if atr14 else None,
        "stop_in_atr": round(risk_unit / atr14, 2) if atr14 else None,
        "r_levels": r_levels, "stop_candidates": {k: round(v, 4) for k, v in cands.items()},
        "pattern": {k: best_pat[k] for k in ("pattern", "score", "pivot", "stop")} if best_pat else None,
        "equity": equity, "equity_source": equity_src, "risk_pct": round(risk_pct, 4), "regime": regime_info,
        "size": size, "notes": notes,
        "invalidation": f"close {'below' if long else 'above'} {stop:.2f}",
        "next_step": "run trading-risk with these numbers, then trading-broker",
    }
    if a.save:
        j = Journal()
        t = j.plan(sym, a.side, plan["entry"], plan["stop"], plan["target"], size["qty"] if size else None,
                   setup=a.setup or (best_pat["pattern"] if best_pat else ""), thesis=a.thesis,
                   account=cfg["broker"]["name"])
        plan["journal_id"] = t["id"]
    cli.emit(plan, a.json, md)


def md(p):
    s = p["size"] or {}
    out = [f"## Trade plan: {p['side'].upper()} {p['symbol']}  (last {p['last_price']:,} on {p['date']})", ""]
    out.append("| | price | basis |\n|---|---|---|")
    out.append(f"| Entry | {p['entry']:,} | {p['entry_order']} order |")
    out.append(f"| Stop | {p['stop']:,} | {p['stop_basis']} ({p['stop_in_atr']}x ATR) |")
    out.append(f"| Target | {p['target']:,} | {p['target_basis']} |")
    out.append(f"\n**Reward:risk {p['reward_risk']}**  |  R levels: " + ", ".join(f"{r['label']} {r['price']:,}" for r in p["r_levels"]))
    if s:
        out.append(f"\n**Size: {s['qty']:g}** units -> notional {s['notional']:,.2f} ({s['position_pct']}% of equity), "
                   f"risk {s['actual_risk']:,.2f} ({s['actual_risk_pct']}%) at {p['risk_pct']}% risk on "
                   f"{p['equity']:,.2f} equity ({p['equity_source']})")
    if p.get("regime"):
        r = p["regime"]
        out.append(f"Regime {r['index']}: {r['regime']} -> risk scaled to {r['exposure_pct']}%")
    if p.get("pattern"):
        pt = p["pattern"]
        out.append(f"Live pattern: {pt['pattern']} (score {pt['score']}), pivot {pt['pivot']}, stop {pt['stop']}")
    out.append("\nStop candidates: " + ", ".join(f"{k} {v:,}" for k, v in p["stop_candidates"].items()))
    out.append(f"Invalidation: {p['invalidation']}")
    if p["notes"]:
        out.append("\n**Watch-outs:**")
        out += [f"- {n}" for n in p["notes"]]
    if p.get("journal_id"):
        out.append(f"\nSaved to journal as planned trade #{p['journal_id']}.")
    out.append(f"\nNext: {p['next_step']}.")
    return "\n".join(out)


if __name__ == "__main__":
    cli.run(main)
