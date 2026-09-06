# Options — Chain Analysis & Index Options

`restoreSession()` loads tokens but does not validate them — a `TokenExpiredError` from any call below means the session is dead and automatic refresh could not recover it; re-authenticate via [setup.md](setup.md) rather than retrying.

## Fetching Options Data

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();

const chain = await rh.getChains("AAPL");
console.log("Expirations:", chain.expiration_dates);

const options = await rh.findTradableOptions("AAPL", { expirationDate: "2026-04-17", optionType: "call" });
console.log(JSON.stringify(options.map(o => ({ strike: o.strike_price, exp: o.expiration_date, type: o.type })), null, 2));
'
```

For greeks and pricing:
```typescript
const data = await rh.getOptionMarketData("AAPL", "2026-04-17", 200, "call");
// => [{ adjusted_mark_price, delta, gamma, theta, vega, implied_volatility, open_interest, volume }]
```

## Common Workflows

### View Available Expirations
```typescript
const chain = await rh.getChains("AAPL");
// chain.expiration_dates => ["2026-04-17", "2026-05-15", ...]
```

### Full Chain for a Date
```typescript
const options = await rh.findTradableOptions("AAPL", { expirationDate: "2026-04-17" });
```

### Specific Option with Greeks
```typescript
const data = await rh.getOptionMarketData("AAPL", "2026-04-17", 200, "call");
```

### Covered Call Screening
1. Get holdings: `await rh.buildHoldings()`
2. For each stock with 100+ shares, fetch OTM calls 30-45 DTE
3. Calculate annualized premium yield from market data

### Open Option Positions
```typescript
const positions = await rh.getOptionPositions();          // per-leg
const strategies = await rh.getOptionAggregatePositions(); // grouped by strategy (spreads, condors)
```

## Index Options (SPX, NDX, VIX, RUT, XSP)

Index options work the same — just pass the index symbol (e.g. `"SPX"`). The client auto-detects index symbols.

**Chain selection**: Indexes like SPX have two chains:
- **SPXW** — daily expirations (0DTE, 1DTE, weeklies), PM-settled
- **SPX** — monthly expirations only (3rd Friday), AM-settled

The client auto-selects based on `expirationDate`. SPXW (more expirations) is default.

**Index value**:
```typescript
const spx = await rh.getIndexValue("SPX");
// => { value: "5700.00", symbol: "SPX" }
```

**Key differences**: European-style (exercise at expiration only), cash-settled (no stock delivery).

## Key Data Fields

**Option instrument**: `strike_price`, `expiration_date`, `type` (call/put), `state`, `tradability`

**Market data (greeks)**: `adjusted_mark_price`, `delta`, `gamma`, `theta`, `vega`, `rho`, `implied_volatility`, `open_interest`, `volume`, `bid_size`, `ask_size`, `chance_of_profit_long`, `chance_of_profit_short`

## Placing Option Orders
Before placing, get accounts and ask which to use. See [trade.md](trade.md) for the full option order flow.

## Output Format
Present as a table: Strike | Type | Bid | Ask | Last | Delta | IV | Volume | OI | Prob Profit

For all client methods, see [client-api.md](client-api.md).
