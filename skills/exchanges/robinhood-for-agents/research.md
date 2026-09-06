# Research — Stock Analysis

`restoreSession()` loads tokens but does not validate them — a `TokenExpiredError` from any call below means the session is dead and automatic refresh could not recover it; re-authenticate via [setup.md](setup.md) rather than retrying. (In a parallel `Promise.all`, one expired session fails every branch at once — that is one auth failure, not seven.)

### Fetch Data (parallel)

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();

const [quotes, fundamentals, news, ratings, earnings, historicals, shortInterest] = await Promise.all([
  rh.getQuotes("AAPL"),
  rh.getFundamentals("AAPL"),
  rh.getNews("AAPL"),
  rh.getRatings("AAPL"),
  rh.getEarnings("AAPL"),
  rh.getStockHistoricals("AAPL", { interval: "day", span: "year" }),
  rh.getShortInterest("AAPL"),
]);
console.log(JSON.stringify({ quotes, fundamentals, news, ratings, earnings, historicals, shortInterest }, null, 2));
'
```

To search by keyword: `await rh.findInstruments("artificial intelligence")`

Index symbols (SPX, NDX, VIX, RUT, XSP) also work with `getQuotes()` — returns the current index value.

## Key Data Fields
- **Quote**: `last_trade_price`, `bid_price`, `ask_price`, `previous_close`, `pe_ratio`
- **Fundamentals**: `market_cap`, `pe_ratio`, `pb_ratio`, `float`, `dividend_yield`, dividend schedule (`dividend_per_share`, `ex_dividend_date`), `high_52_weeks`, `low_52_weeks`, `description`, `ceo`, `sector`
- **Ratings**: `summary.num_buy_ratings`, `summary.num_hold_ratings`, `summary.num_sell_ratings`
- **Earnings**: `eps.estimate`, `eps.actual`, `year`, `quarter`
- **Historicals**: Array of `{ begins_at, open_price, close_price, high_price, low_price, volume }`
- **Short interest** (`getShortInterest`): `daily_data[]` of `{ date, shares_short, pc_freefloat }` (+ upper/lower bounds). Modeled DAILY estimate, not the official FINRA figure; `pc_freefloat` is a percent. History begins ~mid-2025

## Output Structure
1. **Company Overview**: Name, sector, industry, market cap, description
2. **Price Data**: Current price, 52-week range, position within range
3. **Valuation**: P/E ratio, P/B ratio, dividend yield
4. **Analyst Ratings**: Buy/Hold/Sell consensus
5. **Recent Earnings**: Last 4 quarters EPS (estimate vs actual)
6. **News**: Top 5 recent headlines
7. **Price Trend**: Summary of recent price action from historicals

For all client methods, see [client-api.md](client-api.md).
