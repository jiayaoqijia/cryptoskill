#!/usr/bin/env python3
"""Fetch prices, benchmark, fundamentals and headlines for one ticker via yfinance,
then build the technical snapshot. Everything lands in one run directory that
serves as the single source of truth for all agents.

Usage:
  python fetch_data.py BBCA.JK --date 2026-09-29 --outdir ta_runs/BBCA.JK_2026-09-29

Outputs (in --outdir):
  prices.csv, benchmark.csv        daily OHLCV up to --date (no look-ahead)
  technical.json / technical.md    from indicators.py
  fundamentals.json                company profile, ratios, statements (lag-filtered)
  news.json                        headlines published on/before --date
  fetch_report.json                what worked, what failed, look-ahead caveats

Exit codes: 0 ok, 2 network blocked / yfinance unavailable (use the fallback
path in references/data-sources.md), 3 ticker returned no data.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import detect_market  # noqa: E402

REPORTING_LAG_DAYS = 45  # statements for a quarter are assumed public ~45 days after period end

INFO_FIELDS = [
    "longName", "shortName", "sector", "industry", "country", "currency", "financialCurrency",
    "marketCap", "enterpriseValue", "sharesOutstanding", "floatShares", "heldPercentInsiders",
    "heldPercentInstitutions", "trailingPE", "forwardPE", "priceToBook", "priceToSalesTrailing12Months",
    "enterpriseToEbitda", "enterpriseToRevenue", "pegRatio", "trailingEps", "forwardEps", "bookValue",
    "dividendYield", "trailingAnnualDividendYield", "payoutRatio", "exDividendDate",
    "returnOnEquity", "returnOnAssets", "profitMargins", "operatingMargins", "grossMargins",
    "ebitdaMargins", "revenueGrowth", "earningsGrowth", "earningsQuarterlyGrowth",
    "totalRevenue", "ebitda", "netIncomeToCommon", "totalCash", "totalDebt", "debtToEquity",
    "currentRatio", "quickRatio", "freeCashflow", "operatingCashflow", "beta",
    "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "targetMeanPrice", "targetHighPrice", "targetLowPrice",
    "recommendationKey", "numberOfAnalystOpinions", "longBusinessSummary",
    # crypto-specific
    "circulatingSupply", "maxSupply", "volume24Hr", "startDate", "description",
]

STATEMENT_ROWS = {
    "income": ["Total Revenue", "Gross Profit", "Operating Income", "EBITDA", "Net Income",
               "Net Income Common Stockholders", "Diluted EPS", "Basic EPS", "Interest Expense",
               "Net Interest Income"],
    "balance": ["Total Assets", "Total Liabilities Net Minority Interest", "Stockholders Equity",
                "Total Debt", "Net Debt", "Cash And Cash Equivalents", "Current Assets",
                "Current Liabilities", "Inventory", "Accounts Receivable"],
    "cashflow": ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow",
                 "Cash Dividends Paid", "Repurchase Of Capital Stock"],
}


# Hosts yfinance contacts: chart/quote APIs, cookie + crumb, and the consent flow it
# falls back to when the cookie fetch fails.
YAHOO_HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com", "fc.yahoo.com",
               "finance.yahoo.com", "guce.yahoo.com", "consent.yahoo.com"]


def blocked(msg: str):
    print(json.dumps({"status": "network_blocked", "detail": msg,
                      "hosts_to_allow": YAHOO_HOSTS,
                      "how_to_allow": "Add these hosts (or *.yahoo.com) to the network allowlist of the "
                                      "sandbox or cloud environment, then start a new session.",
                      "next_step": "Use the fallback path in references/data-sources.md "
                                   "(web search and/or user-uploaded CSV + indicators.py)."}, indent=2))
    sys.exit(2)


def to_py(v):
    try:
        import numpy as np
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.floating,)):
            f = float(v)
            return None if f != f else f
    except ImportError:
        pass
    if isinstance(v, float) and v != v:
        return None
    return v


def statements(tkr, analysis_date: date, report: dict) -> dict:
    out = {}
    cutoff = analysis_date - timedelta(days=REPORTING_LAG_DAYS)
    sources = {
        "income_quarterly": "quarterly_income_stmt", "income_annual": "income_stmt",
        "balance_quarterly": "quarterly_balance_sheet", "balance_annual": "balance_sheet",
        "cashflow_quarterly": "quarterly_cashflow", "cashflow_annual": "cashflow",
    }
    for key, attr in sources.items():
        try:
            df = getattr(tkr, attr)
            if df is None or df.empty:
                continue
            kind = key.split("_")[0]
            cols = [c for c in df.columns if hasattr(c, "date") and c.date() <= cutoff]
            dropped = len(df.columns) - len(cols)
            if dropped:
                report["lookahead_filtered"].append(f"{key}: dropped {dropped} period(s) ending after {cutoff}")
            rows = [r for r in STATEMENT_ROWS[kind] if r in df.index]
            block = {}
            for c in sorted(cols, reverse=True)[:8 if "quarterly" in key else 4]:
                block[c.strftime("%Y-%m-%d")] = {r: to_py(df.at[r, c]) for r in rows}
            if block:
                out[key] = block
        except Exception as e:  # noqa: BLE001
            report["errors"].append(f"{key}: {e}")
    return out


def headlines(tkr, analysis_date: date, report: dict) -> list:
    items = []
    try:
        raw = tkr.news or []
    except Exception as e:  # noqa: BLE001
        report["errors"].append(f"news: {e}")
        return items
    end = datetime.combine(analysis_date, datetime.max.time()).replace(tzinfo=timezone.utc)
    for n in raw:
        c = n.get("content", n)
        title = c.get("title")
        pub = c.get("pubDate") or c.get("displayTime") or n.get("providerPublishTime")
        try:
            if isinstance(pub, (int, float)):
                ts = datetime.fromtimestamp(pub, tz=timezone.utc)
            else:
                ts = datetime.fromisoformat(str(pub).replace("Z", "+00:00"))
        except Exception:  # noqa: BLE001
            ts = None
        if ts and ts > end:
            continue
        provider = c.get("provider", {})
        url = (c.get("canonicalUrl") or {}).get("url") if isinstance(c.get("canonicalUrl"), dict) else n.get("link")
        items.append({"title": title, "published": ts.isoformat() if ts else None,
                      "publisher": (provider.get("displayName") if isinstance(provider, dict) and provider
                                    else n.get("publisher")),
                      "summary": c.get("summary"), "url": url})
    return items


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--lookback-days", type=int, default=800)
    ap.add_argument("--benchmark", help="override benchmark ticker ('none' to skip)")
    a = ap.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        blocked("yfinance not installed. Try: pip install yfinance (add --break-system-packages if needed).")

    ticker = a.ticker.upper()
    ad = date.fromisoformat(a.date)
    mkt = detect_market(ticker)
    bench = mkt["benchmark"] if a.benchmark is None else (None if a.benchmark.lower() == "none" else a.benchmark)
    os.makedirs(a.outdir, exist_ok=True)
    report = {"ticker": ticker, "analysis_date": a.date, "market": mkt, "files": [],
              "errors": [], "lookahead_filtered": [], "caveats": []}

    start = ad - timedelta(days=a.lookback_days)
    end = ad + timedelta(days=1)  # yfinance end is exclusive

    def download(sym):
        df = yf.download(sym, start=start.isoformat(), end=end.isoformat(), auto_adjust=False,
                         progress=False, threads=False)
        if df is None or df.empty:
            return None
        if hasattr(df.columns, "levels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)
        df = df.reset_index().rename(columns={"index": "Date"})
        return df

    try:
        prices = download(ticker)
    except Exception as e:  # noqa: BLE001
        if "allowlist" in str(e).lower() or "403" in str(e) or "resolve" in str(e).lower():
            blocked(str(e))
        prices = None
        report["errors"].append(f"prices: {e}")
    if prices is None:
        # yfinance swallows HTTP errors; probe once to tell "blocked" from "bad ticker"
        try:
            import requests
            r = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=5d&interval=1d",
                             timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 403 or "allowlist" in r.text.lower():
                blocked(f"Yahoo Finance host blocked: {r.status_code} {r.text[:160]}")
        except Exception as e:  # noqa: BLE001
            blocked(f"Cannot reach Yahoo Finance: {e}")
        print(json.dumps({"status": "no_data", "ticker": ticker,
                          "hint": "Check the ticker suffix (e.g. .JK for IDX, -USD for crypto)."}, indent=2))
        sys.exit(3)

    p_csv = os.path.join(a.outdir, "prices.csv")
    prices.to_csv(p_csv, index=False)
    report["files"].append("prices.csv")

    b_csv = None
    if bench:
        try:
            bdf = download(bench)
            if bdf is not None:
                b_csv = os.path.join(a.outdir, "benchmark.csv")
                bdf.to_csv(b_csv, index=False)
                report["files"].append("benchmark.csv")
                report["benchmark"] = bench
        except Exception as e:  # noqa: BLE001
            report["errors"].append(f"benchmark {bench}: {e}")

    # technical snapshot
    import pandas as pd
    import indicators as ind
    warnings: list = []
    df = ind.load_prices(p_csv, "en", warnings)
    bdf = ind.load_prices(b_csv, "en") if b_csv else None
    snap = ind.build_snapshot(df, ticker, pd.Timestamp(ad), bdf, warnings)
    with open(os.path.join(a.outdir, "technical.json"), "w") as fh:
        json.dump(snap, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(a.outdir, "technical.md"), "w") as fh:
        fh.write(ind.to_markdown(snap))
    report["files"] += ["technical.json", "technical.md"]

    # fundamentals
    tkr = yf.Ticker(ticker)
    fund = {"as_of_note": "Profile/ratio fields come from Yahoo's CURRENT snapshot, not the analysis date."}
    try:
        info = tkr.info or {}
        fund["profile_and_ratios"] = {k: to_py(info.get(k)) for k in INFO_FIELDS if info.get(k) is not None}
    except Exception as e:  # noqa: BLE001
        report["errors"].append(f"info: {e}")
    fund["statements"] = statements(tkr, ad, report)
    try:
        divs = tkr.dividends
        if divs is not None and len(divs):
            divs = divs[[d.date() <= ad for d in divs.index]]
            fund["dividends_last_8"] = {d.strftime("%Y-%m-%d"): float(v) for d, v in divs.tail(8).items()}
    except Exception as e:  # noqa: BLE001
        report["errors"].append(f"dividends: {e}")
    try:
        cal = tkr.calendar
        if cal:
            fund["calendar"] = {k: str(v) for k, v in dict(cal).items()}
    except Exception:  # noqa: BLE001
        pass
    with open(os.path.join(a.outdir, "fundamentals.json"), "w") as fh:
        json.dump(fund, fh, indent=2, ensure_ascii=False, default=str)
    report["files"].append("fundamentals.json")

    news = headlines(tkr, ad, report)
    with open(os.path.join(a.outdir, "news.json"), "w") as fh:
        json.dump(news, fh, indent=2, ensure_ascii=False)
    report["files"].append("news.json")

    days_back = (date.today() - ad).days
    if days_back > 7:
        report["caveats"].append(
            f"Analysis date is {days_back} days in the past (backtest mode). Prices and statements are "
            "cut off at the date, but profile ratios are today's values and Yahoo only returns recent "
            "headlines. Use web search restricted to sources dated on/before the analysis date.")
    if len(news) < 3:
        report["caveats"].append("Few headlines returned; supplement the News and Sentiment analysts with web search.")
    report["status"] = "ok"
    with open(os.path.join(a.outdir, "fetch_report.json"), "w") as fh:
        json.dump(report, fh, indent=2, default=str)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
