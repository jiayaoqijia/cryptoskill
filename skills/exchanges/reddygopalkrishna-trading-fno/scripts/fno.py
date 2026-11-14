#!/usr/bin/env python3
"""F&O analysis: option Greeks, implied volatility, multi-leg payoff, and option-chain OI / PCR / max pain.

Analysis only. Nothing here places an order (orders go trading-risk -> trading-broker preview -> your confirm).

Examples
  python3 scripts/fno.py greeks --spot 24500 --strike 24600 --kind call --days 7 --iv 14
  python3 scripts/fno.py iv --price 120 --spot 24500 --strike 24600 --kind call --days 7
  python3 scripts/fno.py payoff --kind call --side long --strike 24600 --premium 120 --lot-size 75
  python3 scripts/fno.py strategy --name iron-condor --strikes 24000,24200,24800,25000 --premiums 20,60,55,18 --lot-size 75
  python3 scripts/fno.py strategy --legs +1C24600@120 -1C24800@60 --lot-size 75 --chart
  python3 scripts/fno.py chain AAPL                                   # US, Cboe delayed data
  python3 scripts/fno.py chain --file nse_chain.csv --spot 24512 --expiry 2026-11-27    # NSE CSV you downloaded
  python3 scripts/fno.py chain NIFTY --kite                           # Kite instruments + quotes (needs Kite)
"""

import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import DISCLAIMER, cli, http, options  # noqa: E402

CBOE_URL = "https://cdn-api.cboe.com/api/global/delayed_quotes/options/{sym}.json"
DEFAULT_RATE = 0.05


# ------------------------------------------------------------------ helpers

def pct_to_frac(v):
    """--iv 14 and --iv 0.14 both mean 14%."""
    return None if v is None else (v / 100.0 if v > 1.5 else v)


def years(a):
    if getattr(a, "expiry", None):
        if getattr(a, "days", None) is not None:
            cli.fail("give --days or --expiry, not both")
        return options.years_to(a.expiry)
    if getattr(a, "days", None) is None:
        cli.fail("give --days (calendar days to expiry) or --expiry YYYY-MM-DD")
    return a.days / 365.0


def add_time_args(p):
    p.add_argument("--days", type=float, help="calendar days to expiry")
    p.add_argument("--expiry", help="expiry date YYYY-MM-DD (alternative to --days)")
    p.add_argument("--rate", type=float, default=DEFAULT_RATE,
                   help=f"risk-free rate, annual (default {DEFAULT_RATE:g} = {DEFAULT_RATE*100:g}%%; set your market's rate)")
    p.add_argument("--div-yield", type=float, default=0.0, help="continuous dividend yield (default 0)")


# ------------------------------------------------------------------ greeks / iv

def cmd_greeks(a):
    T, iv = years(a), pct_to_frac(a.iv)
    g = options.greeks(a.spot, a.strike, T, a.rate, iv, a.kind, a.div_yield)
    res = {"kind": options._kind(a.kind), "spot": a.spot, "strike": a.strike, "days": round(T * 365, 2), "iv": iv,
           "rate": a.rate, "model": "Black-Scholes-Merton (European)",
           "intrinsic": options.intrinsic(a.spot, a.strike, a.kind), **g}
    res["time_value"] = g["price"] - res["intrinsic"]
    if a.lot_size:
        res["per_lot"] = {"delta": g["delta"] * a.lot_size, "gamma": g["gamma"] * a.lot_size,
                          "theta_per_day": g["theta"] * a.lot_size, "vega_per_vol_pt": g["vega"] * a.lot_size}

    def md(r):
        out = [f"{r['kind'].upper()} strike {r['strike']:,.2f}, spot {r['spot']:,.2f}, {r['days']:g} days, IV {r['iv']*100:.2f}%, rate {r['rate']*100:g}%",
               f"Price {r['price']:,.2f}  (intrinsic {r['intrinsic']:,.2f} + time value {r['time_value']:,.2f})",
               f"Delta {r['delta']:+.4f}   Gamma {r['gamma']:.6f}   Theta {r['theta']:+.4f}/day   Vega {r['vega']:.4f} per 1 vol point   Rho {r['rho']:+.4f} per 1% rate"]
        if r.get("per_lot"):
            p = r["per_lot"]
            out.append(f"Per lot ({a.lot_size:g}): delta {p['delta']:+.2f}, gamma {p['gamma']:.4f}, theta {p['theta_per_day']:+.2f}/day, vega {p['vega_per_vol_pt']:.2f}/vol pt (one long lot)")
        out.append("Model note: Black-Scholes is European and assumes constant volatility; American stock options can differ.")
        return "\n".join(out)
    cli.emit(res, a.json, md)


def cmd_iv(a):
    T = years(a)
    iv = options.implied_vol(a.price, a.spot, a.strike, T, a.rate, a.kind, a.div_yield)
    if iv is None:
        cli.fail("no implied volatility fits that price: it is below the option's minimum value (discounted intrinsic), "
                 "above its maximum, or the option has expired. Check spot, strike, kind, days and price.")
    g = options.greeks(a.spot, a.strike, T, a.rate, iv, a.kind, a.div_yield)
    res = {"iv": iv, "iv_pct": iv * 100, "price": a.price, "kind": options._kind(a.kind), "spot": a.spot,
           "strike": a.strike, "days": round(T * 365, 2), "rate": a.rate, "delta": g["delta"], "vega": g["vega"]}
    cli.emit(res, a.json, lambda r: f"Implied volatility {r['iv_pct']:.2f}%  ({r['kind']} {r['strike']:,.2f}, price {r['price']:,.2f}, "
                                    f"spot {r['spot']:,.2f}, {r['days']:g} days, rate {r['rate']*100:g}%)  delta {r['delta']:+.3f}")


# ------------------------------------------------------------------ payoff / strategy

def fill_premiums(legs, a):
    """Legs without a premium get a Black-Scholes price if spot, iv and time were given."""
    missing = [l for l in legs if l["kind"] != "stock" and not l.get("premium_known")]
    if not missing:
        return []
    if not (a.spot and a.iv is not None and (a.days is not None or a.expiry)):
        cli.fail("some legs have no premium: give it (+1C100@2.5) or give --spot, --iv and --days/--expiry to price it with Black-Scholes")
    T, iv = years(a), pct_to_frac(a.iv)
    notes = []
    for l in missing:
        l["premium"] = round(options.bs_price(a.spot, l["strike"], T, a.rate, iv, l["kind"], a.div_yield), 2)
        notes.append(f"{l['side']} {l['kind']} {l['strike']:g}: premium {l['premium']:g} (Black-Scholes at IV {iv*100:g}%)")
    return notes


def run_position(legs, a, label):
    notes = fill_premiums(legs, a)
    lot = a.lot_size or 1.0
    an = options.analyze(legs, lot)
    strikes = [l["strike"] for l in legs]
    lo = a.low if a.low is not None else (a.spot * 0.85 if a.spot else min(strikes) * 0.85)
    hi = a.high if a.high is not None else (a.spot * 1.15 if a.spot else max(strikes) * 1.15)
    rows = options.payoff_table(legs, lo, hi, a.steps, lot)
    res = {"strategy": label, "lot_size": lot, "legs": [{k: v for k, v in l.items() if k != "premium_known"} for l in legs],
           "analysis": an, "table": rows, "notes": notes, "spot": a.spot,
           "assumptions": "P&L at expiry, before brokerage, taxes and margin cost; premiums as given."}
    if a.spot:
        res["pnl_at_spot_now"] = options.payoff_at(legs, a.spot, lot)
    return res


def md_position(r):
    an = r["analysis"]
    out = [f"{r['strategy']}  (lot size {r['lot_size']:g}; P&L at expiry)"]
    for l in r["legs"]:
        k = f"{l['kind']} {l['strike']:g}" if l["kind"] != "stock" else f"underlying @ {l['strike']:g}"
        out.append(f"  {l['side'].upper():5} {l['qty']:g} x {k}" + (f" @ premium {l['premium']:g}" if l["kind"] != "stock" else ""))
    for n in r["notes"]:
        out.append("  note: " + n)
    cr = an["net_credit"]
    out.append(f"Net {'credit received' if cr > 0 else 'debit paid'}: {abs(cr):,.2f}")
    out.append("Max profit: " + ("UNLIMITED" if an["max_profit_unlimited"] else f"{an['max_profit']:,.2f}"))
    out.append("Max loss:   " + ("UNLIMITED" if an["max_loss_unlimited"] else f"{an['max_loss']:,.2f}"))
    out.append("Breakeven(s): " + (", ".join(f"{b:,.2f}" for b in an["breakevens"]) or "none"))
    if "pnl_at_spot_now" in r:
        out.append(f"P&L at expiry if spot stays at {r['spot']:,.2f}: {r['pnl_at_spot_now']:+,.2f}")
    out.append("")
    out.append(cli.md_table([{"spot": x["spot"], "pnl": x["pnl"]} for x in r["table"]], ["spot", "pnl"], ["Spot at expiry", "P&L"]))
    if r.get("chart"):
        out += ["", r["chart"]]
    out.append("\n" + r["assumptions"])
    return "\n".join(out)


def add_range_args(p):
    p.add_argument("--spot", type=float, help="current spot (sets the chart range, marks 'now', and prices legs with no premium)")
    p.add_argument("--iv", type=float, help="volatility used to price legs without a premium (14 or 0.14)")
    p.add_argument("--lot-size", type=float, default=1.0, help="units per lot from the exchange / broker (default 1 = per unit)")
    p.add_argument("--low", type=float, help="table range low (default spot -15%%)")
    p.add_argument("--high", type=float, help="table range high (default spot +15%%)")
    p.add_argument("--steps", type=int, default=21)
    p.add_argument("--chart", action="store_true", help="add an ASCII payoff chart")
    add_time_args(p)


def finish_position(res, a):
    if a.chart:
        wide = options.payoff_table([dict(l, premium_known=True) for l in res["legs"]],
                                    res["table"][0]["spot"], res["table"][-1]["spot"], 61, res["lot_size"])
        res["chart"] = options.ascii_payoff(wide, spot=res.get("spot"))
    cli.emit(res, a.json, md_position)


def cmd_payoff(a):
    l = options.leg(a.kind, a.side, a.strike, a.premium or 0.0, a.qty)
    l["premium_known"] = a.premium is not None or l["kind"] == "stock"
    finish_position(run_position([l], a, f"{a.side} {a.kind} {a.strike:g}"), a)


def cmd_strategy(a):
    if a.name:
        if not a.strikes:
            cli.fail("--name needs --strikes low,to,high (see 'strategies' for each shape)")
        strikes = [float(x) for x in a.strikes.split(",")]
        prem = [float(x) if x.strip() not in ("", "?") else None for x in a.premiums.split(",")] if a.premiums else None
        legs = options.build_strategy(a.name, strikes, prem, a.qty)
        label = a.name
    elif a.legs:
        legs = [options.parse_leg(s) for s in a.legs]
        label = f"custom ({len(legs)} legs)"
    else:
        cli.fail("give --name with --strikes, or --legs like +1C24600@120 -1C24800@60")
    finish_position(run_position(legs, a, label), a)


def cmd_strategies(a):
    rows = [{"name": k, "strikes": v[0], "what": v[1]} for k, v in sorted(options.STRATEGIES.items())]
    cli.emit(rows, a.json, lambda r: cli.md_table(r, ["name", "strikes", "what"], ["Strategy", "Strikes", "Shape"]))


# ------------------------------------------------------------------ chain

def load_chain(a):
    if a.file:
        with open(os.path.expanduser(a.file), encoding="utf-8-sig", newline="") as f:
            text = f.read()
        ch = options.parse_nse_csv(text, a.spot, a.expiry, a.symbol)
        if not a.spot:
            ch["warnings"] = ["No --spot given: the NSE CSV does not contain it, so ATM, implied move and the table window are skipped."]
        return ch
    if not a.symbol:
        cli.fail("give a symbol (AAPL, NIFTY) or --file nse_chain.csv")
    if a.kite:
        from tradekit.brokers.kite import KiteClient  # imported late: needs credentials only here
        from tradekit.brokers.base import BrokerError
        try:
            ch = options.kite_chain(KiteClient(), a.symbol, a.expiry, a.exchange, a.spot)
        except BrokerError as e:
            cli.fail(f"Kite is not usable: {e}. Without Kite, download the option chain CSV from nseindia.com "
                     "(Option Chain page -> Download) and run: chain --file FILE --spot PRICE --expiry YYYY-MM-DD")
        if not ch.get("spot"):
            ch["warnings"] = ["Spot not available from Kite; pass --spot."]
        return ch
    sym = a.symbol.upper().lstrip("^")
    if a.symbol.startswith("^"):
        sym = "_" + sym
    if sym.endswith((".NS", ".BO")):
        cli.fail("NSE/BSE options have no free automated feed here (nseindia.com blocks programs and this tool does not bypass that). "
                 "Use --file with the option-chain CSV you download from nseindia.com, or --kite if Kite Connect is configured.")
    try:
        payload = http.get_json(CBOE_URL.format(sym=sym), retries=1)
    except http.HTTPError as e:
        if e.status in (403, 404):
            cli.fail(f"no US option chain for {sym} from Cboe's delayed data (HTTP {e.status}). Check the ticker, "
                     "or use --file with a chain CSV. Yahoo's options endpoint needs a cookie/crumb session and is not used.")
        cli.fail(f"Cboe delayed data request failed: {e}")
    ch = options.parse_cboe(payload, a.expiry)
    ch["warnings"] = ["Cboe delayed data (about 15 minutes), unofficial public endpoint that can change or be withdrawn. "
                      "IV is Cboe's; 'ltp' is the last trade, which can be stale for illiquid strikes."]
    return ch


def cmd_chain(a):
    ch = load_chain(a)
    summ = options.chain_summary(ch, a.top)
    rows = ch["rows"]
    spot = ch.get("spot")
    if spot:
        atm = options.atm_strike(rows, spot)
        idx = next(i for i, r in enumerate(rows) if r["strike"] == atm)
        window = rows[max(0, idx - a.window): idx + a.window + 1]
    else:
        window = rows
    summ["window"] = window
    summ["lot_size"] = ch.get("lot_size") or a.lot_size
    summ["available_expiries"] = ch.get("expiries")
    summ["as_of"] = ch.get("as_of")
    summ["warnings"] = ch.get("warnings", [])
    if a.lot_size and ch.get("lot_size") and a.lot_size != ch["lot_size"]:
        summ["warnings"].append(f"--lot-size {a.lot_size:g} differs from the exchange lot size {ch['lot_size']:g} in Kite's instruments")
    if not summ["lot_size"]:
        if ch.get("source") == "cboe-delayed":
            summ["warnings"].append("Premiums are per share. Standard US equity options cover 100 shares per contract, but adjusted "
                                    "series differ: confirm in your broker before using --lot-size.")
        else:
            summ["warnings"].append("Lot size unknown: take it from the exchange circular or Kite instruments and pass --lot-size.")
    if a.export:
        cli_rows = ch["rows"]
        import csv
        cols = ["strike"] + [f"{s}_{f}" for s in ("c", "p") for f in options.SIDE_FIELDS]
        with open(os.path.expanduser(a.export), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in cli_rows:
                w.writerow({k: r.get(k) for k in cols})
        summ["exported"] = a.export
    cli.emit(summ, a.json, md_chain)


def md_chain(r):
    def n(v, d=0):
        return "-" if v is None else f"{v:,.{d}f}"
    out = [f"{r.get('underlying') or '?'} option chain  expiry {r.get('expiry') or '?'}  spot {n(r.get('spot'), 2)}  source {r['source']}"
           + (f"  as of {r['as_of']}" if r.get("as_of") else "")]
    out.append(f"Call OI {n(r['call_oi'])}   Put OI {n(r['put_oi'])}   PCR (OI) {n(r['pcr_oi'], 2)}   PCR (volume) {n(r['pcr_volume'], 2)}")
    mp = r.get("max_pain")
    if mp:
        out.append(f"Max pain {mp['strike']:,.2f}  (the strike where option buyers lose most at expiry; a level people watch, not a forecast)")
    if r.get("atm_strike") is not None:
        s = f"ATM strike {r['atm_strike']:,.2f}"
        if r.get("atm_straddle"):
            s += f"   ATM straddle {r['atm_straddle']:,.2f}  = implied move about +/-{r['implied_move_pct']:.1f}% to expiry"
        if r.get("atm_iv"):
            s += f"   ATM IV {r['atm_iv']*100:.1f}%"
        out.append(s)
    out.append("Biggest call OI (resistance-like): " + (", ".join(f"{w['strike']:g} ({w['oi']:,.0f})" for w in r["call_oi_walls"]) or "-"))
    out.append("Biggest put OI (support-like):     " + (", ".join(f"{w['strike']:g} ({w['oi']:,.0f})" for w in r["put_oi_walls"]) or "-"))
    if r.get("lot_size"):
        out.append(f"Lot size: {r['lot_size']:g}")
    tab = []
    for w in r["window"]:
        tab.append({"c_oi": n(w.get("c_oi")), "c_vol": n(w.get("c_volume")), "c_iv": n(w["c_iv"] * 100, 1) if w.get("c_iv") else "-",
                    "c_ltp": n(w.get("c_ltp"), 2), "strike": f"{w['strike']:g}", "p_ltp": n(w.get("p_ltp"), 2),
                    "p_iv": n(w["p_iv"] * 100, 1) if w.get("p_iv") else "-", "p_vol": n(w.get("p_volume")), "p_oi": n(w.get("p_oi"))})
    out += ["", cli.md_table(tab, ["c_oi", "c_vol", "c_iv", "c_ltp", "strike", "p_ltp", "p_iv", "p_vol", "p_oi"],
                             ["Call OI", "Vol", "IV%", "LTP", "STRIKE", "LTP", "IV%", "Vol", "Put OI"])]
    for w in r.get("warnings", []):
        out.append("Note: " + w)
    if r.get("available_expiries"):
        out.append("Expiries: " + ", ".join(r["available_expiries"][:10]))
    out.append("Analysis only - no order was placed. " + DISCLAIMER)
    return "\n".join(out)


# ------------------------------------------------------------------ main

def build_parser():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("greeks", help="Black-Scholes price and Greeks")
    g.add_argument("--spot", type=float, required=True)
    g.add_argument("--strike", type=float, required=True)
    g.add_argument("--kind", required=True, choices=["call", "put", "c", "p", "ce", "pe"])
    g.add_argument("--iv", type=float, required=True, help="volatility, 14 or 0.14")
    g.add_argument("--lot-size", type=float, help="also show Greeks per lot")
    add_time_args(g)
    cli.add_json_flag(g)
    g.set_defaults(fn=cmd_greeks)

    i = sub.add_parser("iv", help="implied volatility from an option price (bisection)")
    i.add_argument("--price", type=float, required=True)
    i.add_argument("--spot", type=float, required=True)
    i.add_argument("--strike", type=float, required=True)
    i.add_argument("--kind", required=True, choices=["call", "put", "c", "p", "ce", "pe"])
    add_time_args(i)
    cli.add_json_flag(i)
    i.set_defaults(fn=cmd_iv)

    o = sub.add_parser("payoff", help="payoff of one option leg at expiry")
    o.add_argument("--kind", required=True, choices=["call", "put", "c", "p", "ce", "pe"])
    o.add_argument("--side", required=True, choices=["long", "short"])
    o.add_argument("--strike", type=float, required=True)
    o.add_argument("--premium", type=float, help="price per unit (omit to price with --spot --iv --days)")
    o.add_argument("--qty", type=float, default=1.0, help="number of lots (multiplies lot size)")
    add_range_args(o)
    cli.add_json_flag(o)
    o.set_defaults(fn=cmd_payoff)

    s = sub.add_parser("strategy", help="multi-leg payoff, breakevens, max profit/loss")
    s.add_argument("--name", help="named strategy (see the 'strategies' command)")
    s.add_argument("--strikes", help="comma list, low to high")
    s.add_argument("--premiums", help="comma list in leg order; '?' = price that leg with Black-Scholes")
    s.add_argument("--legs", nargs="+", help="custom legs, e.g. +1C24600@120 -1C24800@60 (+/- qty C|P|S strike @premium)")
    s.add_argument("--qty", type=float, default=1.0, help="lots per leg for --name")
    add_range_args(s)
    cli.add_json_flag(s)
    s.set_defaults(fn=cmd_strategy)

    t = sub.add_parser("strategies", help="list the named strategies")
    cli.add_json_flag(t)
    t.set_defaults(fn=cmd_strategies)

    c = sub.add_parser("chain", help="OI, PCR, max pain, ATM straddle from a chain")
    c.add_argument("symbol", nargs="?", help="US ticker (AAPL, SPY, ^SPX) or, with --kite, an NFO name (NIFTY, RELIANCE)")
    c.add_argument("--file", help="NSE option-chain CSV downloaded from nseindia.com")
    c.add_argument("--kite", action="store_true", help="use Kite instruments + quotes (Kite Connect plan with market data)")
    c.add_argument("--exchange", default="NFO", help="Kite exchange segment (default NFO)")
    c.add_argument("--spot", type=float, help="spot price (required with --file)")
    c.add_argument("--expiry", help="expiry YYYY-MM-DD (nearest if omitted for US/Kite; label only for --file)")
    c.add_argument("--lot-size", type=float, help="exchange lot size, if you know it (Kite supplies it)")
    c.add_argument("--window", type=int, default=8, help="strikes shown each side of ATM")
    c.add_argument("--top", type=int, default=3, help="how many OI walls to list")
    c.add_argument("--export", help="write the full normalized chain to this CSV")
    cli.add_json_flag(c)
    c.set_defaults(fn=cmd_chain)
    return p


def main():
    a = build_parser().parse_args()
    a.fn(a)


if __name__ == "__main__":
    cli.run(main)
