---
name: trading-insiders
description: Insider tracker from public filings - US Congress members' stock trades (House STOCK Act reports, e.g. Nancy Pelosi, read from the PDF into owner, ticker, buy or sell, options strike and expiry, amount range and days to disclose, alerting once per new filing), US company insiders from SEC Form 4, India NSE bulk and block deals, and India company insiders (SEBI PIT disclosures) from the CSV the user downloads on nseindia.com. Free, no API key. Use when the user asks "what is Pelosi buying", "Congress trades", "politician stock trades", "insider buying in NVDA", "who bought TCS shares", "bulk deals today", "block deals", "promoter buying", or "alert me when Pelosi files".
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Insider Tracker (`trading-insiders`)

People close to a company - or to the laws that shape it - must disclose their trades. This skill
reads those public filings quickly. **It is fast, not early:** every filing arrives days or weeks after
the trade. There is no inside information here. Say that every time.

```bash
python3 scripts/insiders.py congress --member pelosi              # her reports this year
python3 scripts/insiders.py congress --new --read                 # filings not seen before, read them
python3 scripts/insiders.py congress --since 2026-11-01           # every member
python3 scripts/insiders.py ptr 20035143                          # one report -> rows
python3 scripts/insiders.py form4 NVDA --days 90 --buys-sells     # US company insiders (SEC)
python3 scripts/insiders.py deals --min-value-cr 25               # India: NSE bulk + block deals
python3 scripts/insiders.py deals --symbol RELIANCE TATAMOTORS
python3 scripts/insiders.py sebi ~/Downloads/insider.csv --symbol INFY   # India: SEBI PIT, downloaded CSV
```

## Sources

| command | market | source | how fresh |
|---|---|---|---|
| `congress`, `ptr` | US | House Clerk index + PTR PDFs (read with the standard library; no installs) | due within 45 days of the trade |
| `form4` | US | SEC EDGAR Form 4 XML; needs `data.sec_user_agent` | within 2 business days |
| `deals` | India | NSE's daily bulk-deal and block-deal files | same evening |
| `sebi` | India | SEBI PIT disclosures: NSE blocks programs, so the user downloads the CSV (nseindia.com > Companies > Corporate filings > Insider trading > Download .csv) | within 2 trading days |

**US Senate:** efdsearch.senate.gov asks each visitor to accept terms of use. That is the user's
agreement to make: never click or automate it. Ask the user to search there (report type "Periodic
Transactions"), then paste the table and write it up in the same shape as House rows.

## Rules

1. **Quote the filing, not a tracker.** Rows come from the official document, with its link.
2. **Amounts are ranges** for Congress ("$1,000,001 - $5,000,000"), never "$3 million".
3. **Owner matters:** SP spouse, JT joint, DC dependent child, blank = the member.
4. **Say the delay:** days from trade to disclosure; over 45 is flagged LATE.
5. **Options are options:** a call with a strike and expiry is not a share purchase.
6. **Not every insider trade is a signal.** Form 4 grants, exercises and tax withholding are pay;
   many sales are pre-planned. Many NSE bulk deals are arbitrage or market-making firms buying and
   selling the same day. Say so.
7. **Never imply anyone had inside information, and never claim copying them beats the market.**

## Steps

1. Run the command for what the user asked. For "alert me when X files", run `congress --member X
   --new --read` on a schedule (hourly on weekdays is plenty: the Clerk rebuilds the index about once
   a day). Exit code 1 means nothing new.
2. Write each row up plainly: who, owner, what, buy or sell, when, how much (range), days to disclose.
3. If the user wants to act, it goes the long way: a disclosure is a reason to look at a chart, not a
   setup. trading-chart / trading-entry decide if there is a trade today; then trading-plan, trading-risk,
   and trading-broker only after the user's explicit confirmation.
4. If a PTR cannot be read (a scanned paper filing), the tool says so and saves the PDF: open it and
   read it directly.
