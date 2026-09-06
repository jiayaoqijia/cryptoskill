# Portfolio — Holdings, P&L, Account Summary

`restoreSession()` loads tokens but does not validate them — a `TokenExpiredError` from any call below means the session is dead and automatic refresh could not recover it; re-authenticate via [setup.md](setup.md) rather than retrying.

### Fetch Portfolio Data

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();

const [holdings, accounts, crypto] = await Promise.all([
  rh.buildHoldings(),
  rh.getAccounts(),
  rh.getCryptoPositions(),
]);
console.log(JSON.stringify({ holdings, accounts, crypto }, null, 2));
'
```

### Enrich (Optional)
For crypto positions, get current prices:
```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
const btc = await rh.getCryptoQuote("BTC");
console.log(JSON.stringify(btc, null, 2));
'
```

## Multi-Account Support
`getAccounts()` returns all accounts. To get portfolio for a specific account:
```typescript
rh.buildHoldings({ accountNumber: "ACCT_ID" })
```

**Caveat:** for `robinhood_get_portfolio` / `getUnifiedPortfolio(accountNumber)`, only Robinhood's *default* account returns a populated `unified` snapshot — any other real, valid account_number gets `unified: null` (bonfire's unified-portfolio endpoint 404s for non-default accounts). Holdings, cash, and buying power are unaffected either way; only the bonfire-sourced parity fields (`total_equity`, `total_market_value`, `portfolio_equity`, `options_buying_power`, `uninvested_cash`, `withdrawable_cash`) are missing when scoped to a non-default account. Don't treat a `null` `unified` as a failure.

## Output Format
Present results as a formatted table:
- Account summary: account number, type, portfolio value, cash, buying power
- Per-holding: Symbol, Name, Shares, Price, Avg Cost, Equity, P&L %, Allocation %
- Separate sections for stocks and crypto
- Summary line: Total holdings value, day change

## Short Positions
A **negative `quantity`** is a short position, not bad data — the account owes those shares. Report it as "short N shares", never as a holding of N.

Its P&L runs the opposite way: the position gains when the price falls and loses when it rises, with no upper bound on the loss. Closing it means **buying** the absolute value back (`side: "buy"`), not selling — see [trade.md](trade.md#short-selling). If a user asks to "sell" a short position, they almost certainly mean cover it; confirm before acting, because a `sell_short` would double the exposure instead.

## Key Response Fields
**`holdings`** — per ticker: `price`, `quantity` (negative = short), `average_buy_price`, `equity`, `percent_change`, `intraday_percent_change`, `equity_change`, `name`

**`summary`**: `equity`, `market_value`, `cash`, `buying_power`, `crypto_buying_power`, `cash_available_for_withdrawal`

For all client methods, see [client-api.md](client-api.md).
