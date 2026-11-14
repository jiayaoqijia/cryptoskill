#!/usr/bin/env python3
"""Earnings analyst: quarterly results for any listed company and what changed.

Revenue, gross / operating / net margin, net income and diluted EPS, quarter by quarter, each
against the same quarter a year earlier, with the trailing twelve months and plain-words notes.

Sources: Yahoo Finance fundamentals (any market, no key, about 5 quarters) and, for US companies,
SEC EDGAR XBRL facts (the numbers the company filed, years deep; needs data.sec_user_agent).

Examples
  python3 scripts/earnings.py AAPL                      # SEC if configured, else Yahoo
  python3 scripts/earnings.py RELIANCE.NS TCS.NS INFY.NS
  python3 scripts/earnings.py MSFT --source sec --quarters 8
  python3 scripts/earnings.py SHEL.L --json
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, feeds, fundamentals, sec  # noqa: E402


def money(v, cur):
    if v is None:
        return "-"
    if cur == "INR":
        return f"Rs {v / 1e7:,.0f} cr"
    sym = {"USD": "$", "GBP": "£", "EUR": "€", "JPY": "¥"}.get(cur or "", (cur or "") + " ")
    a = abs(v)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if a >= div:
            return f"{'-' if v < 0 else ''}{sym}{a / div:,.2f}{suf}"
    return f"{sym}{v:,.0f}"


def pct(v):
    return "-" if v is None else f"{v:+.1f}%"


def mpct(v):
    return "-" if v is None else f"{v:.1f}%"


def one(sym, a):
    src = a.source
    if src == "auto":
        src = "sec" if feeds.is_us(sym) and sec.user_agent() and not a.offline else "yahoo"
    if src == "sec":
        if not feeds.is_us(sym):
            raise ValueError(f"{sym}: SEC covers US-listed companies only; use --source yahoo")
        info = sec.cik_for(sym)
        rows = sec.quarters_from_facts(sec.company_facts(info["cik"]), limit=max(a.quarters, 8))
        res = fundamentals.analyse(rows, sym, "SEC EDGAR XBRL (company filings)", info["name"])
        subs = sec.submissions(info["cik"])
        er = [f for f in sec.recent_filings(subs, ["8-K"]) if "2.02" in f["items"]][:1]
        tenq = sec.recent_filings(subs, ["10-Q", "10-K"])[:1]
        res["links"] = {"latest_earnings_8k": er[0]["index_url"] if er else None,
                        "latest_10q_10k": tenq[0]["url"] if tenq else None,
                        "latest_10q_10k_filed": tenq[0]["filed"] if tenq else None}
        if tenq and res.get("latest") and tenq[0]["report_date"] and tenq[0]["report_date"] > res["latest"]["period_end"]:
            res["notes"].append(f"SEC's facts trail the newest {tenq[0]['form']} (period {tenq[0]['report_date']}): "
                                "read that filing for the newest quarter")
    else:
        if a.offline:
            import json
            f = Path(a.offline).expanduser() / f"fundamentals-{sym}.json"
            rows = fundamentals.parse_yahoo(json.loads(f.read_text()))
        else:
            rows = fundamentals.yahoo_quarters(sym)
        res = fundamentals.analyse(rows, sym, "Yahoo Finance fundamentals (free, unofficial)")
    res["quarters"] = res["quarters"][-a.quarters:]
    return res


def md(out):
    lines = []
    for r in out["companies"]:
        if r.get("error"):
            lines.append(f"## {r['symbol']}\nCould not read results: {r['error']}\n")
            continue
        q = r["quarters"]
        cur = q[-1].get("currency") if q else None
        lines.append(f"## {r['symbol']}" + (f" - {r['name']}" if r.get("name") else "") + f"  ({r['source']})")
        if not q:
            lines.append("No quarterly results found.\n")
            continue
        lines.append("| quarter end | revenue | rev YoY | gross % | op % | net % | net income | NI YoY | EPS | EPS YoY |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for x in q:
            d = " (derived)" if x.get("derived") else ""
            eps = "-" if x.get("eps") is None else f"{x['eps']:.2f}"
            lines.append(f"| {x['period_end']}{d} | {money(x.get('revenue'), cur)} | {pct(x.get('revenue_yoy_pct'))} | "
                         f"{mpct(x.get('gross_margin_pct'))} | {mpct(x.get('operating_margin_pct'))} | "
                         f"{mpct(x.get('net_margin_pct'))} | {money(x.get('net_income'), cur)} | "
                         f"{pct(x.get('net_income_yoy_pct'))} | {eps} | {pct(x.get('eps_yoy_pct'))} |")
        if r.get("ttm"):
            t = r["ttm"]
            eps = "-" if t.get("eps") is None else f"{t['eps']:.2f}"
            lines.append(f"\nLast four quarters: revenue {money(t.get('revenue'), cur)}, net income "
                         f"{money(t.get('net_income'), cur)}, EPS {eps}.")
        for k, v in (r.get("links") or {}).items():
            if v and k != "latest_10q_10k_filed":
                lines.append(f"- {k.replace('_', ' ')}: {v}")
        for n in r["notes"]:
            lines.append(f"- note: {n}")
        lines.append("")
    lines.append("Numbers as reported by the source; growth is against the same quarter a year earlier. "
                 "The next report date is not in this data: check trading-news or the company's results page.")
    return "\n".join(lines)


def main():
    p = cli.parser(__doc__)
    p.add_argument("symbols", nargs="+", help="tickers, e.g. AAPL RELIANCE.NS")
    p.add_argument("--source", default="auto", choices=["auto", "yahoo", "sec"])
    p.add_argument("--quarters", type=int, default=6)
    p.add_argument("--offline", help="folder of saved fundamentals-<SYMBOL>.json (tests)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    out = {"companies": []}
    for s in a.symbols:
        try:
            out["companies"].append(one(s, a))
        except Exception as e:  # noqa: BLE001 - one bad ticker must not hide the rest
            out["companies"].append({"symbol": s, "error": str(e)})
    cli.emit(out, a.json, md)
    if all(c.get("error") for c in out["companies"]):
        sys.exit(2)


if __name__ == "__main__":
    cli.run(main)
