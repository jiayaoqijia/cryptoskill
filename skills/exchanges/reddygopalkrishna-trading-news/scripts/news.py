#!/usr/bin/env python3
"""News monitor: what is new on the stocks you watch, any market, newest first, tagged.

Sources (free, no keys): Google News for every market, Yahoo Finance headlines for US tickers,
SEC 8-K filings for US companies (needs data.sec_user_agent). Shows only what is new since the
last check, plus how far each stock is from the previous close.

Examples
  python3 scripts/news.py AAPL RELIANCE.NS                 # what is new on these two
  python3 scripts/news.py --watchlist ~/my_list.txt --hours 12
  python3 scripts/news.py --journal                        # stocks in open and planned trades
  python3 scripts/news.py TCS.NS --all --json              # include items already shown
"""

import datetime as dt
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, data, feeds, sec  # noqa: E402
from tradekit.journal import Journal  # noqa: E402


def local_time(iso_utc, gmtoff):
    if not iso_utc:
        return "?"
    t = dt.datetime.strptime(iso_utc, "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(seconds=int(gmtoff or 0))
    return t.strftime("%m-%d %H:%M")


def offline_file(folder, name):
    if not folder:
        return None
    p = Path(folder).expanduser() / name
    return p if p.exists() else None


def gather(sym, a, now):
    out = {"symbol": sym, "items": [], "notes": [], "errors": []}
    # price and name
    try:
        q = data.live_quote(sym, a.provider, a.offline)
        q.pop("bars", None)
        out.update(name=q["name"], price=q["price"], previous_close=q["previous_close"], currency=q["currency"],
                   exchange=q["exchange"], timezone=q["timezone"], gmtoffset=q["gmtoffset"], market_time=q["market_time"])
        if q["previous_close"]:
            out["change_pct"] = round((q["price"] / q["previous_close"] - 1) * 100, 2)
            out["moving"] = abs(out["change_pct"]) >= a.move_pct
    except Exception as e:  # noqa: BLE001 - news still useful without a price
        out["errors"].append(f"price: {e}")
    name = out.get("name")
    items = []
    # Google News: every market
    try:
        f = offline_file(a.offline, f"google-news-{sym}.xml")
        g = feeds.parse_rss(f.read_text(), "google") if f else feeds.fetch(feeds.google_url(sym, name, max(1, round(a.hours / 24 + 0.5))), "google")
        items += [i for i in g if feeds.relevant(i, sym, name)]
    except Exception as e:  # noqa: BLE001
        out["errors"].append(f"google news: {e}")
    # Yahoo headlines: US tickers
    if feeds.is_us(sym) and "yahoo" in a.sources:
        try:
            f = offline_file(a.offline, f"yahoo-news-{sym}.xml")
            items += feeds.parse_rss(f.read_text(), "yahoo") if f else feeds.fetch(feeds.yahoo_url(sym), "yahoo")
        except Exception as e:  # noqa: BLE001
            out["errors"].append(f"yahoo news: {e}")
    # SEC filings: US companies
    if feeds.is_us(sym) and "sec" in a.sources and not a.offline:
        if not sec.user_agent():
            out["notes"].append("SEC filings skipped: set data.sec_user_agent (trading-setup) to include 8-Ks")
        else:
            try:
                info = sec.cik_for(sym)
                since = (now - dt.timedelta(hours=max(a.hours, 24))).date().isoformat()
                for fl in sec.recent_filings(sec.submissions(info["cik"]), a.forms.split(","), since):
                    flag = "! " if fl["important"] else ""
                    what = ", ".join(fl["important"] or fl["items"]) or fl["form"]
                    items.append({"id": f"sec:{fl['accession']}", "title": f"{flag}{fl['form']} filed: {what}",
                                  "link": fl["url"], "published": (fl["accepted"] or fl["filed"] + "T00:00:00Z")[:19] + "Z",
                                  "summary": "", "publisher": "SEC EDGAR", "source": "sec",
                                  "important": bool(fl["important"])})
            except Exception as e:  # noqa: BLE001
                out["errors"].append(f"sec: {e}")
    items = feeds.dedupe(feeds.within(items, a.hours, now))
    seen = feeds.load_seen()
    for it in items:
        it["tags"] = feeds.tag_text(it["title"] + " " + it.get("summary", ""))
        if it["source"] == "sec" and "earnings results" in it["title"]:
            it["tags"] = sorted(set(it["tags"]) | {"earnings"})
        it["new"] = feeds.item_key(it) not in seen
    out["total"] = len(items)
    out["items"] = (items if a.all else [i for i in items if i["new"]])[: a.limit]
    return out


def md(res):
    lines = [f"News check {res['checked_at']} UTC, last {res['hours']:g}h. Headlines are leads, not facts: "
             "open the story or filing before saying something happened."]
    for t in res["tickers"]:
        head = f"\n## {t['symbol']}" + (f" - {t['name']}" if t.get("name") else "")
        lines.append(head)
        if t.get("price") is not None and t.get("change_pct") is not None:
            mv = "  MOVING" if t.get("moving") else ""
            lines.append(f"{t['price']:,.2f} {t.get('currency') or ''} ({t['change_pct']:+.2f}% vs previous close "
                         f"{t['previous_close']:,.2f}) at {(t.get('market_time') or '')[11:16]} {t.get('timezone') or ''} "
                         f"(free data, delayed){mv}")
        if not t["items"]:
            lines.append(f"Nothing new ({t['total']} item(s) in the window already shown)." if t["total"]
                         else "No news in this window.")
            if t.get("moving"):
                lines.append("It is moving with no headline: worth saying out loud, and worth checking the exchange's announcements.")
        for i in t["items"]:
            tags = f" [{', '.join(i['tags'])}]" if i.get("tags") else ""
            pub = f" - {i['publisher']}" if i.get("publisher") else ""
            lines.append(f"- {local_time(i.get('published'), t.get('gmtoffset'))} {i['title']}{tags}{pub}\n  {i['link']}")
        for n in t["notes"]:
            lines.append(f"_note: {n}_")
        for e in t["errors"]:
            lines.append(f"_could not read {e}_")
    if res["new_items"] == 0:
        lines.append("\nNothing new since the last check.")
    lines.append("\nTimes are the exchange's local time. Never trade on a headline alone.")
    return "\n".join(lines)


def main():
    p = cli.parser(__doc__)
    p.add_argument("symbols", nargs="*", help="tickers, e.g. AAPL RELIANCE.NS SHEL.L")
    p.add_argument("--watchlist", help="file or comma list of tickers")
    p.add_argument("--journal", action="store_true", help="add the tickers of open and planned trades")
    p.add_argument("--hours", type=float, default=24, help="look back this many hours (default 24)")
    p.add_argument("--all", action="store_true", help="show items already shown before")
    p.add_argument("--limit", type=int, default=12, help="max items per ticker")
    p.add_argument("--move-pct", type=float, default=3.0, help="flag MOVING at this %% from previous close")
    p.add_argument("--sources", default="google,yahoo,sec", help="google,yahoo,sec")
    p.add_argument("--forms", default="8-K,6-K", help="SEC forms to include (US)")
    p.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    p.add_argument("--offline", help="folder of saved feeds and charts (tests, replays)")
    p.add_argument("--now", help="pin the clock, UTC 'YYYY-MM-DDTHH:MM'")
    p.add_argument("--dry-run", action="store_true", help="do not remember what was shown")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    syms = data.load_universe(a.watchlist, a.symbols)
    if a.journal:
        j = Journal()
        syms = data.load_universe(None, syms + [t["symbol"] for st in ("open", "planned") for t in j.list(status=st)])
    if not syms:
        cli.fail("give tickers, --watchlist FILE or --journal")
    now = dt.datetime.fromisoformat(a.now).replace(tzinfo=dt.timezone.utc) if a.now else dt.datetime.now(dt.timezone.utc)
    res = {"checked_at": now.strftime("%Y-%m-%d %H:%M"), "hours": a.hours, "tickers": []}
    shown = []
    for s in syms:
        t = gather(s, a, now)
        res["tickers"].append(t)
        shown += [i for i in t["items"] if i["new"]]
    res["new_items"] = len(shown)
    if not a.dry_run:
        feeds.mark_seen(shown, now=now)
    cli.emit(res, a.json, md)
    sys.exit(0 if shown else 1)


if __name__ == "__main__":
    cli.run(main)
