---
name: trading-earnings
description: Earnings analyst for any listed company - quarterly revenue, gross, operating and net margins, net income and diluted EPS, each quarter against the same quarter a year earlier, trailing twelve months, and plain-words notes (one-off gains, derived quarters, data that lags). Yahoo Finance fundamentals for every market (US, India NSE/BSE, UK, Europe, Japan...) and SEC EDGAR XBRL filings for US companies, free with no API key. Use when the user asks "how were the results", "analyze TCS earnings", "is revenue growing", "compare margins", "what changed this quarter", "check the 10-Q", "sum up the call", or before trading a stock around its results.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Earnings Analyst (`trading-earnings`)

Results move stocks more than anything else on the calendar, and the press release puts the best
number first. This skill lines up what the company reported, quarter by quarter, and says plainly
what changed.

```bash
python3 scripts/earnings.py AAPL                         # SEC filings if configured, else Yahoo
python3 scripts/earnings.py RELIANCE.NS TCS.NS INFY.NS
python3 scripts/earnings.py MSFT --source sec --quarters 8
python3 scripts/earnings.py SHEL.L --json
```

## Sources

| source | covers | depth |
|---|---|---|
| `yahoo` | any market Yahoo covers | about the last 5 quarters, in the company's currency (Indian companies shown in Rs crore) |
| `sec` | US companies | the XBRL numbers the company filed, years deep; Q4 = 10-K year minus three quarters (marked derived); links to the latest earnings 8-K and 10-Q/10-K. Needs `data.sec_user_agent` |

`auto` (default) uses SEC for US tickers when the SEC user agent is set, Yahoo otherwise.

## Rules

1. **Compare like with like.** Growth is against the same quarter a year earlier; many businesses
   are seasonal. Say so when a year-ago quarter is missing.
2. **Say where each number came from** - the table's source, the press release, the call.
3. **Flag one-offs.** Net income above operating income means gains outside the business are in it.
4. **Never call a stock cheap, expensive, a buy or a sell.** Report what was filed.
5. **Earnings calls:** the tool does not fetch transcripts. If the user pastes one, sum up guidance,
   margins, demand and what management declined to answer.

## Steps

1. Run it for the tickers in question.
2. When numbers need context, open the latest results filing (the 8-K link for US companies, the
   company's results page or exchange filing for others) and read it.
3. Write: one line on the quarter (revenue, EPS, growth), one on margins, one on anything unusual,
   the links.
4. If the next report falls inside the planned trade, say it before trading-plan sets a stop: a stop
   does not protect against a gap. The next date is not in this data: check trading-news.
