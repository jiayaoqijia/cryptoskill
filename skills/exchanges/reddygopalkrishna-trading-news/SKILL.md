---
name: trading-news
description: News monitor for any market - shows only what is new on the stocks you watch since the last check, newest first, in the exchange's local time, each item tagged (earnings, analyst, deal, capital, people, legal, regulatory, halt, risk, macro), with how far each stock is from the previous close and MOVING flags. Google News for every market (US, India NSE/BSE, UK, Japan...), Yahoo Finance headlines for US tickers and SEC 8-K filings for US companies. Free, no API key. Use when the user asks "any news on X", "why is this moving", "morning briefing", "what's the news on my watchlist", "did anything break", "check the 8-Ks", or before planning a trade.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# News Monitor (`trading-news`)

A chart can look perfect and still be about to gap on results, a deal or a regulator. Before a setup
becomes a trade, read what is new on it - and only what is new.

```bash
python3 scripts/news.py AAPL RELIANCE.NS                  # what is new on these
python3 scripts/news.py --watchlist ~/my_list.txt --hours 12
python3 scripts/news.py --journal                         # tickers in open and planned trades
python3 scripts/news.py TCS.NS --all                      # include items already shown
python3 scripts/news.py NVDA --sources google,yahoo,sec --json
```

Exit code 0 = something new, 1 = nothing new. `--dry-run` shows without remembering. `--move-pct 3`
sets the MOVING flag. Symbols use Yahoo suffixes: `.NS` NSE, `.BO` BSE, `.L` London, `.T` Tokyo...

## Sources

| source | covers | notes |
|---|---|---|
| Google News RSS | every market | searched by ticker and company name in that market's edition (India edition for `.NS`/`.BO`) |
| Yahoo Finance RSS | US tickers | the ticker's own headline feed |
| SEC EDGAR 8-K / 6-K | US companies | needs `data.sec_user_agent` (trading-setup); filings marked `!` carry an important item: results (2.02), officer change (5.02), impairment (2.06), delisting notice (3.01), financials no longer reliable (4.02), bankruptcy (1.03), cyber incident (1.05) |

Indian exchange announcements (NSE/BSE corporate filings) cannot be read automatically: both sites
block programs. Results and big announcements still reach Google News within minutes; for the
filing itself, point the user to the company page on nseindia.com or bseindia.com.

## Rules

1. **Headlines are leads, not facts.** Before saying something happened, open the story or filing
   and read it. Quote the source and link it. Never summarise a paywalled story you could not read.
2. **Filings beat headlines.** If an 8-K and a headline disagree, the filing is what the company said.
3. **A move with no headline** is worth saying out loud too.
4. **No predictions.** Report what was published and how far the price is from yesterday's close.
5. **Say what it means for the setup** in one line - e.g. "results are this week: an overnight gap
   can jump past any stop".

## Steps

1. Run the check for the tickers in question (or `--journal`).
2. Read the important ones first: `!` filings, earnings / halt / legal / regulatory / risk tags,
   MOVING tickers.
3. Write a short brief per ticker: what happened, source + link, the move, why it matters to the trade.
4. If the story changes the picture (results inside the trade, an offering, a halt), say so before
   trading-entry / trading-plan. Never act on a headline alone.

During the session: `/loop 15m` the check, or schedule it before the open. Free data is delayed;
headlines can take minutes to appear.
