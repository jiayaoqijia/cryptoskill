#!/usr/bin/env python3
"""Insider tracker: who with inside access is buying or selling, from public filings.

  congress   US House members' trades (STOCK Act Periodic Transaction Reports), alerting once per filing
  ptr        read one House report (by DocID or a saved PDF) into clean rows
  form4      US company insiders (officers, directors, 10% owners) from SEC Form 4 (needs data.sec_user_agent)
  deals      India: NSE bulk and block deals (big buyers and sellers, published daily)
  sebi       India: company insiders (SEBI PIT disclosures) from the CSV you download on nseindia.com

Every row is a public disclosure filed days or weeks after the trade. Fast, not early.

Examples
  python3 scripts/insiders.py congress --member pelosi
  python3 scripts/insiders.py congress --new --read             # only filings not seen before, read them
  python3 scripts/insiders.py ptr 20035143
  python3 scripts/insiders.py form4 NVDA --days 90
  python3 scripts/insiders.py deals --symbol RELIANCE TATAMOTORS
  python3 scripts/insiders.py deals --min-value-cr 25
  python3 scripts/insiders.py sebi ~/Downloads/CF-Insider-Trading-equities.csv --symbol INFY
"""

import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, config, disclosures as D, http, sec  # noqa: E402


def fetch(url, cache_name=None, max_age_h=6.0):
    if cache_name:
        f = config.path("cache", "disclosures", cache_name)
        import time
        if f.exists() and (time.time() - f.stat().st_mtime) < max_age_h * 3600:
            return f.read_bytes()
    raw = http.request("GET", url, headers={"Accept": "*/*"}, timeout=40)
    if cache_name:
        config.path("cache", "disclosures", cache_name).write_bytes(raw)
    return raw


def state():
    f = config.path("state", "insiders.json")
    try:
        return json.loads(f.read_text()) if f.exists() else {"seen_ptr": []}
    except json.JSONDecodeError:
        return {"seen_ptr": []}


def save_state(st):
    config.path("state", "insiders.json").write_text(json.dumps(st, indent=1) + "\n")


def read_ptr(row_or_doc, year=None, offline=None):
    if isinstance(row_or_doc, dict):
        row = row_or_doc
    else:
        doc = str(row_or_doc)
        if doc.lower().endswith(".pdf") and Path(doc).expanduser().exists():
            return D.parse_ptr(D.pdf_text(Path(doc).expanduser().read_bytes()))
        row = {"doc_id": doc, "year": str(year or dt.date.today().year), "filed": None}
    saved = config.path("cache", "ptr-pdfs", f"{row['doc_id']}.pdf")
    if offline:
        src = Path(offline).expanduser() / f"ptr-{row['doc_id']}.pdf"
        pdf = src.read_bytes()
    elif saved.exists():
        pdf = saved.read_bytes()
    else:
        pdf = http.request("GET", D.ptr_url(row), headers={"Accept": "application/pdf"}, timeout=40)
        saved.write_bytes(pdf)
    try:
        res = D.parse_ptr(D.pdf_text(pdf), row.get("filed"))
    except ValueError as e:
        return {"doc_id": row["doc_id"], "rows": [], "error": f"{e}. Open the saved PDF directly: {saved}",
                "pdf": str(saved), "url": D.ptr_url(row)}
    res.update(pdf=str(saved), url=D.ptr_url(row))
    res.setdefault("doc_id", row["doc_id"])
    if not res["rows"]:
        res["error"] = (f"no transaction rows recognised (a paper filing is a scanned image). "
                        f"Open the PDF and read it: {saved}")
    return res


# ---------------------------------------------------------------- commands

def cmd_congress(a):
    year = a.year or dt.date.today().year
    years = [year]
    if a.new and dt.date.today().month == 1 and not a.year:
        years.insert(0, year - 1)
    rows = []
    for y in years:
        if a.offline:
            raw = (Path(a.offline).expanduser() / f"house-{y}FD-excerpt.zip").read_bytes()
        else:
            raw = fetch(D.HOUSE_INDEX_URL.format(year=y), f"house-{y}FD.zip", max_age_h=3)
        rows += D.parse_house_index(raw)
    if a.type:
        rows = [r for r in rows if r["type"] == a.type]
    if a.member:
        rows = [r for r in rows if any(D.member_matches(r, m) for m in a.member)]
    if a.since:
        rows = [r for r in rows if (r["filed"] or "") >= a.since]
    rows.sort(key=lambda r: (r["filed"] or "", r["doc_id"]), reverse=True)
    st = state()
    if a.new:
        first_run = not st["seen_ptr"]
        cut = (dt.date.today() - dt.timedelta(days=45)).isoformat()
        rows = [r for r in rows if r["doc_id"] not in st["seen_ptr"] and (not first_run or (r["filed"] or "") >= cut)]
    rows = rows[: a.limit]
    if a.read:
        for r in rows:
            r["report"] = read_ptr(r, offline=a.offline)
    if a.new and not a.dry_run:
        st["seen_ptr"] = sorted(set(st["seen_ptr"]) | {r["doc_id"] for r in rows})[-5000:]
        save_state(st)
    out = {"kind": "congress", "years": years, "filings": rows,
           "note": "Public STOCK Act filings, due within 45 days of the trade: fast, not early. "
                   "Senate: search efdsearch.senate.gov yourself (it asks you to accept terms) and paste the table."}
    cli.emit(out, a.json, md_congress)
    if a.new and not rows:
        sys.exit(1)


def md_rows(rep):
    lines = []
    for x in rep.get("rows", []):
        opt = x.get("option")
        what = (f"{opt['contracts']} {opt['kind']} options, strike {opt['strike']:g}, expires {opt['expires']}"
                if opt else x["asset_type"])
        late = " LATE" if x.get("late") else ""
        days = f", disclosed {x['days_to_disclose']} days later{late}" if x.get("days_to_disclose") is not None else ""
        lines.append(f"  - {x['owner']} {x['type']}: {x['asset']} ({what}), {x['amount']}, traded {x['trade_date']}{days}"
                     + (f"\n    {x['description']}" if x.get("description") and not opt else ""))
    if rep.get("error"):
        lines.append(f"  - {rep['error']}")
    return lines


def md_congress(out):
    if not out["filings"]:
        return "No matching filings." + (" Nothing new since the last check." if out.get("new") else "")
    lines = [f"House financial disclosures ({', '.join(map(str, out['years']))}), newest first:"]
    for r in out["filings"]:
        lines.append(f"- {r['filed']}  {r['name']} ({r['district']})  {D.FILING_TYPES.get(r['type'], r['type'])}  "
                     f"doc {r['doc_id']}  {D.ptr_url(r) if r['type'] == 'P' else ''}")
        if r.get("report"):
            lines += md_rows(r["report"])
    lines.append("\n" + out["note"])
    lines.append("Amounts are ranges, never exact figures. SP = spouse, JT = joint, DC = dependent child.")
    return "\n".join(lines)


def cmd_ptr(a):
    rep = read_ptr(a.doc, a.year, a.offline)
    def md(r):
        head = f"{r.get('member', '?')} ({r.get('district', '?')}), filed {r.get('filed')}, doc {r.get('doc_id')}"
        return "\n".join([head] + md_rows(r) + ["", "A public disclosure filed after the trade: it says what was "
                                                   "bought or sold then, not what anyone will do next."])
    cli.emit(rep, a.json, md)


def cmd_form4(a):
    info = sec.cik_for(a.ticker)
    since = (dt.date.today() - dt.timedelta(days=a.days)).isoformat()
    filings = sec.recent_filings(sec.submissions(info["cik"]), ["4", "4/A"], since)[: a.limit]
    rows = []
    for f in filings:
        try:
            doc = sec.fetch_form4(info["cik"], f)
        except Exception as e:  # noqa: BLE001
            rows.append({"filed": f["filed"], "error": str(e), "url": f["index_url"]})
            continue
        owner = doc["owners"][0] if doc["owners"] else {"name": "?", "roles": []}
        for t in doc["transactions"]:
            if a.buys_sells and t["code"] not in ("P", "S"):
                continue
            rows.append({"filed": f["filed"], "insider": owner["name"], "roles": ", ".join(owner["roles"]), **t,
                         "url": f["index_url"]})
    buys = sum(r.get("value") or 0 for r in rows if r.get("code") == "P")
    sells = sum(r.get("value") or 0 for r in rows if r.get("code") == "S")
    out = {"kind": "form4", "ticker": info["ticker"], "company": info["name"], "since": since,
           "filings": len(filings), "transactions": rows, "open_market_buys_usd": round(buys, 2),
           "open_market_sales_usd": round(sells, 2)}

    def md(o):
        lines = [f"{o['company']} ({o['ticker']}): {o['filings']} Form 4 filings since {o['since']}. "
                 f"Open-market buys ${o['open_market_buys_usd']:,.0f}, sales ${o['open_market_sales_usd']:,.0f}."]
        for r in o["transactions"]:
            if r.get("error"):
                lines.append(f"- {r['filed']} could not read: {r['error']} {r['url']}")
                continue
            val = f" = ${r['value']:,.0f}" if r.get("value") else ""
            px = f" @ {r['price']:,.2f}" if r.get("price") else ""
            lines.append(f"- {r['date']} {r['insider']} ({r['roles']}): {r['meaning']} {r['shares'] or 0:,.0f} "
                         f"{r['security']}{px}{val}")
        lines.append("Open-market buys (code P) are the signal people watch; grants, option exercises and tax "
                     "withholding are routine pay, and many sales are pre-planned (10b5-1).")
        return "\n".join(lines)
    cli.emit(out, a.json, md)


def cmd_deals(a):
    rows = []
    for kind in (["bulk", "block"] if a.kind == "both" else [a.kind]):
        if a.offline:
            files = sorted(Path(a.offline).expanduser().glob(f"nse-{kind}-*.csv"))
            text = files[-1].read_text() if files else ""
        else:
            text = fetch(D.NSE_BULK_URL if kind == "bulk" else D.NSE_BLOCK_URL, f"nse-{kind}.csv", 1).decode("utf-8", "replace")
        rows += D.parse_nse_deals(text, kind)
    want = {s.upper().replace(".NS", "") for s in (a.symbol or [])}
    if a.watchlist:
        from tradekit import data
        want |= {s.upper().replace(".NS", "").replace(".BO", "") for s in data.load_universe(a.watchlist)}
    if want:
        rows = [r for r in rows if r["symbol"].upper() in want]
    if a.min_value_cr:
        rows = [r for r in rows if r["value"] >= a.min_value_cr * 1e7]
    rows.sort(key=lambda r: r["value"], reverse=True)
    out = {"kind": "deals", "date": rows[0]["date"] if rows else None, "deals": rows[: a.limit], "total": len(rows)}

    def md(o):
        if not o["deals"]:
            return "No matching bulk or block deals in NSE's latest file."
        lines = [f"NSE bulk/block deals for {o['date']} ({o['total']} matching), biggest first:"]
        for r in o["deals"]:
            lines.append(f"- {r['kind']:5} {r['side']:4} {r['symbol']:12} {r['client'][:42]:42} {r['qty']:>12,.0f} @ "
                         f"{r['price']:,.2f} = {D.crore(r['value'])}")
        lines.append("A bulk deal is a client trading over 0.5% of a company's shares in a day; a block deal is one big "
                     "trade in the block window. Many are arbitrage or market-making firms, not long-term investors.")
        return "\n".join(lines)
    cli.emit(out, a.json, md)


def cmd_sebi(a):
    path = Path(a.csv).expanduser()
    if not path.exists():
        cli.fail(f"{path} not found. Download it first: {D.NSE_PIT_PAGE} -> filter by company or date -> "
                 "'Download (.csv)', then pass the file here")
    rows = D.parse_nse_pit_csv(path.read_text(encoding="utf-8", errors="replace"))
    if a.symbol:
        want = {s.upper().replace(".NS", "") for s in a.symbol}
        rows = [r for r in rows if r["symbol"].upper() in want]
    if a.market_only:
        rows = [r for r in rows if "market" in (r["mode"] or "").lower()]
    rows.sort(key=lambda r: (r["intimated"] or r["date_to"] or ""), reverse=True)
    buys = sum(r["value"] or 0 for r in rows if r["side"] == "buy")
    sells = sum(r["value"] or 0 for r in rows if r["side"] == "sell")
    out = {"kind": "sebi", "file": str(path), "trades": rows[: a.limit], "total": len(rows),
           "buy_value_inr": buys, "sell_value_inr": sells}

    def md(o):
        lines = [f"{o['total']} insider disclosures in {Path(o['file']).name}. Buys {D.crore(o['buy_value_inr'])}, "
                 f"sells {D.crore(o['sell_value_inr'])}."]
        for r in o["trades"]:
            val = D.crore(r["value"]) if r["value"] else "-"
            lines.append(f"- {r['date_to'] or r['date_from']} {r['symbol']} {r['person']} ({r['category']}): {r['side']} "
                         f"{(r['qty'] or 0):,.0f} shares, {val}, {r['mode']}")
        lines.append("Promoter and director buys in the open market are the ones people watch; pledges, ESOPs and "
                     "inter-se transfers between promoters are routine.")
        return "\n".join(lines)
    cli.emit(out, a.json, md)


def main():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("congress", help="US House members' trade filings")
    c.add_argument("--member", action="append", help="last name or 'First Last' (repeatable)")
    c.add_argument("--since", help="filed on or after YYYY-MM-DD")
    c.add_argument("--year", type=int)
    c.add_argument("--type", default="P", help="filing type (P = periodic transaction report; '' = all)")
    c.add_argument("--new", action="store_true", help="only filings not shown before (first run: last 45 days)")
    c.add_argument("--read", action="store_true", help="download and read each report")
    c.add_argument("--limit", type=int, default=25)
    c.add_argument("--dry-run", action="store_true")
    c.add_argument("--offline")
    c.add_argument("--json", action="store_true")
    r = sub.add_parser("ptr", help="read one House report")
    r.add_argument("doc", help="DocID (e.g. 20035143) or a saved PDF file")
    r.add_argument("--year", type=int)
    r.add_argument("--offline")
    r.add_argument("--json", action="store_true")
    f = sub.add_parser("form4", help="US company insiders (SEC Form 4)")
    f.add_argument("ticker")
    f.add_argument("--days", type=int, default=90)
    f.add_argument("--limit", type=int, default=20, help="max filings to read")
    f.add_argument("--buys-sells", action="store_true", help="only open-market buys and sales")
    f.add_argument("--json", action="store_true")
    d = sub.add_parser("deals", help="India: NSE bulk and block deals")
    d.add_argument("--kind", default="both", choices=["bulk", "block", "both"])
    d.add_argument("--symbol", nargs="*", help="NSE symbols (RELIANCE or RELIANCE.NS)")
    d.add_argument("--watchlist")
    d.add_argument("--min-value-cr", type=float, help="only deals worth at least this many crore rupees")
    d.add_argument("--limit", type=int, default=30)
    d.add_argument("--offline")
    d.add_argument("--json", action="store_true")
    s = sub.add_parser("sebi", help="India: insider trades from NSE's downloaded CSV")
    s.add_argument("csv", help="the CSV downloaded from nseindia.com (corporate filings > insider trading)")
    s.add_argument("--symbol", nargs="*")
    s.add_argument("--market-only", action="store_true", help="only market purchases / sales")
    s.add_argument("--limit", type=int, default=40)
    s.add_argument("--json", action="store_true")
    a = p.parse_args()
    {"congress": cmd_congress, "ptr": cmd_ptr, "form4": cmd_form4, "deals": cmd_deals, "sebi": cmd_sebi}[a.cmd](a)


if __name__ == "__main__":
    cli.run(main)
