# Data sources and fallbacks

Contents
1. Choosing a data path
2. Path A: fetch_data.py (yfinance)
3. Path B: user-uploaded price file
4. Path C: build a CSV from a fetched history page
5. Path D: web search only (limited technicals)
6. sources.md format
7. Search recipes per analyst
8. Market specifics (IDX, US, crypto, others)
9. Backtest mode (past analysis dates)

---

## 1. Choosing a data path

Try them in order and stop at the first that works. Combine freely: prices
from A/B/C, news and sentiment from web search.

| Path | When it works | Technical quality |
|---|---|---|
| A. `fetch_data.py` | Claude Code / local machine, or claude.ai with Yahoo hosts allowed | Full |
| B. User uploads CSV | Any environment | Full |
| C. Fetch a history page → CSV | Web fetch available and the page shows a price table | Partial history (SMA200 may be missing) |
| D. Web search only | Always | Limited: no computed indicators |

Never stall the analysis for data. If A fails and there is no upload, go
to C or D, run the analysis, flag the limitation in the report, and mention
at the end how to unlock full technicals (upload a CSV, or allow the Yahoo
hosts).

## 2. Path A: fetch_data.py

```bash
pip install yfinance            # add --break-system-packages on claude.ai
python scripts/fetch_data.py BBCA.JK --date 2026-09-29 --outdir <run_dir>
```
Exit 0 → read `fetch_report.json`, then `technical.md`, `fundamentals.json`,
`news.json`. Exit 2 → network blocked (claude.ai's sandbox and Claude Code
cloud sessions on the default **Trusted** network level block Yahoo). The
JSON lists `hosts_to_allow`: `query1/query2.finance.yahoo.com`,
`fc.yahoo.com`, `finance.yahoo.com`, `guce.yahoo.com`, `consent.yahoo.com`
(`*.yahoo.com` covers all). The user adds them in their network settings
(cloud sessions: environment → Network access **Custom** → Allowed domains,
then a new session); otherwise continue with B to D. Exit 3 → wrong ticker;
fix the suffix.

Yahoo often lacks depth for IDX fundamentals and returns few headlines for
small caps; supplement with web search regardless.

## 3. Path B: user-uploaded price file

Any daily OHLCV export works: Yahoo Finance, Investing.com (English or
Indonesian headers), TradingView, Nasdaq.com, broker apps. The parser handles
newest-first order, `dd/mm/yyyy` vs `mm/dd/yyyy`, Indonesian number format
(`9.875` = 9875, `1,5M`), `$`/`Rp` signs and volume suffixes.

```bash
python scripts/indicators.py --csv /path/upload.csv --ticker BBCA.JK --date 2026-09-29 \
    --out <run_dir>/technical.json --md <run_dir>/technical.md \
    [--benchmark-csv /path/ihsg.csv] [--locale id]
```
Check the first lines of the output: bar count, first/last date and last
price must look right. If the last price is off by ×1000, rerun with
`--locale id` or `--locale en`. Ask for about 1 to 2 years of daily data so
SMA200 and 1-year stats exist; a benchmark file (IHSG `^JKSE`, `SPY`,
`BTC-USD`) enables beta and relative strength.

## 4. Path C: build a CSV from a fetched history page

1. Search `"<TICKER> historical prices"` (e.g. `BBCA.JK historical data`).
2. Fetch a history page from the results (Yahoo Finance `/history`,
   Investing.com historical data, or similar).
3. Transcribe the table rows exactly into `<run_dir>/prices_web.csv` with
   columns `Date,Open,High,Low,Close,Volume`. Copy numbers, never interpolate
   missing days.
4. Run `indicators.py` on it. Expect partial history; the snapshot's
   warnings say which indicators are missing.
5. Add the page to `sources.md`.

## 5. Path D: web search only

Record in `sources.md`: last price and date, day change, 52-week range,
market cap, volume, and any indicator readings published by a reputable page
(with its date). The Technical Analyst marks the report **"limited: no
computed indicators"** and keeps conclusions proportionate.

## 6. sources.md format

One line per fact source, numbered so agents can cite `[src#n]`:
```
[src#1] price | 2026-09-29 | Yahoo Finance | BBCA.JK quote | https://... | close 9,800; 52w 8,900 to 10,950
[src#2] news  | 2026-09-25 | Kontan | "BCA ... kredit tumbuh" | https://... | Q3 loan growth guidance 8 to 10%
[src#3] sentiment | 2026-09-28 | X/Stockbit | retail thread summary | https://... | mostly positive, dividend focus
```
Tag each line with the analyst it serves: `price`, `fund`, `news`, `macro`,
`sentiment`. Each analyst reads only its own tags (plus `price` for context).

## 7. Search recipes per analyst

Keep queries short; run several narrow ones rather than one broad one. For
IDX names, search in Indonesian and English.

**Fundamentals**
- `<TICKER> laporan keuangan kuartal III 2026` / `<company> Q2 2026 results`
- `<company> annual report 2025`, `<company> investor presentation`
- Banks: `<bank> NIM NPL 2026`; miners: `<company> cash cost production 2026`
- US: SEC EDGAR 10-Q/10-K, earnings press release, call transcript summary.
- Crypto: `<token> tokenomics unlock schedule`, DefiLlama (TVL, fees),
  CoinGecko (supply, market cap).

**News & macro**
- `<TICKER> berita`, `<company> news`, `<company> rights issue / buyback / dividen`
- IDX disclosures: `<TICKER> keterbukaan informasi`
- Macro ID: `BI rate`, `rupiah hari ini`, `IHSG asing net sell`, relevant
  commodity (`harga batu bara`, `harga CPO`, `harga nikel`).
- Macro US: `Fed rate decision`, `CPI`, `10-year Treasury yield`.
- Crypto: `bitcoin ETF flows`, `crypto regulation`, `<token> hack / upgrade`.
- Upcoming: `<company> earnings date`, `<TICKER> cum date dividen`.

**Sentiment**
- `<TICKER> stockbit`, `<TICKER> saham diskusi`, `$<TICKER> stocktwits`,
  `<company> reddit`, `<TICKER> X/Twitter`
- `<company> analyst upgrade downgrade target price`,
  `<TICKER> target harga analis`
- IDX: `<TICKER> net buy asing`, `<TICKER> broker summary`
- US: `<TICKER> short interest`; crypto: `<token> funding rate open interest`.

Useful outlets. Indonesia: idx.co.id, company IR sites, Kontan, Bisnis.com,
CNBC Indonesia, Investor.id, Bloomberg Technoz. Global: Reuters, company IR,
SEC EDGAR, Bloomberg/FT headlines. Crypto: CoinGecko, DefiLlama, CoinGlass,
ETF-flow trackers.

## 8. Market specifics

| Market | Ticker format | Benchmark | Notes |
|---|---|---|---|
| Indonesia (IDX) | `BBCA.JK` | `^JKSE` (IHSG) | Lot 100 shares; tick sizes; ARA/ARB limits; foreign flow matters |
| US | `AAPL` | `SPY` | Earnings seasons; pre/after-market gaps |
| Crypto | `BTC-USD`, `ETH-USD` | `BTC-USD` | 24/7; annualise with 365; weekend gaps |
| Hong Kong / Japan / UK / India / China | `0700.HK`, `7203.T`, `AZN.L`, `RELIANCE.NS`, `600519.SS` | `^HSI`, `^N225`, `^FTSE`, `^NSEI`, `000001.SS` | Currency and trading-hour differences |

**IDX details worth checking each time**
- Price ticks (fraksi harga): below 200 → 1; 200 to 499 → 2; 500 to 1,999 → 5;
  2,000 to 4,999 → 10; 5,000 and above → 25. `risk_tools.py` rounds to these.
- Auto-rejection limits (ARA/ARB) cap daily moves; a stock locked at ARB may
  be impossible to exit that day. The percentages have changed several times,
  so search for the current rule if it matters to the plan.
- Special notations (notasi khusus) and the full-call-auction / watchlist
  board signal elevated risk (losses, low liquidity, suspension history);
  check the stock's status on idx.co.id or recent news for small caps.
- Foreign flow (net buy/sell asing), MSCI/FTSE rebalancing and dividend
  cum/ex dates often drive large caps.
- Liquidity: average daily traded value below roughly Rp1 miliar means
  meaningful slippage; `indicators.py` flags it.

**Crypto details**: no earnings; use network and flow data instead of
statements; funding rates and open interest describe leverage; major
unlocks and exchange incidents are event risks.

## 9. Backtest mode (past analysis dates)

- `fetch_data.py` and `indicators.py` cut prices at the date and drop
  statements for quarters ending within 45 days of it (reporting lag).
- Yahoo profile ratios and headlines are *current* → recompute or discard.
- Web search: keep only sources clearly dated on or before the analysis date.
  If a source is undated, leave it out.
- Social sentiment cannot be reconstructed reliably; weight it down and say so.
- To score the call afterwards, compare with the price N days later
  (`decision_log.py review`).
