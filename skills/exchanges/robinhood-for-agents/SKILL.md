---
name: robinhood-for-agents
description: Trade stocks, options, and crypto on Robinhood — dual mode (MCP tools or TypeScript client).
homepage: https://github.com/kevin1chun/robinhood-for-agents
allowed-tools: Bash(bun:*), Bash(bunx robinhood-for-agents:*), mcp__robinhood-for-agents__*
install:
  - kind: node
    package: robinhood-for-agents
    bins: [robinhood-for-agents]
requires:
  bins: [bun]
metadata: {"credentials":"OAuth tokens stored via TokenStore adapters: KeychainTokenStore (OS keychain, default) or EncryptedFileTokenStore (for Docker/headless). restoreSession() loads tokens, injects Bearer auth directly, and registers both proactive renewal (a pre-request hook renews ~24h before expiry) and reactive refresh (on 401). Access-token lifetime varies (~6-8.5 days observed) — never assume a fixed number. Refresh tokens are single-use and rotate on every renewal, so only one client should drive a session at a time. Renewal happens only while the client is in use: a session left idle past the refresh-token lifetime lapses and needs a new browser login.","chrome":"Google Chrome is required only for initial login (bunx robinhood-for-agents onboard) — playwright-core drives the system Chrome; there is no Brave/Chromium fallback or BROWSER_PATH override. Not needed for subsequent API calls."}
---

# robinhood-for-agents

AI-native Robinhood trading interface. **No MCP server required** — this skill works standalone via the TypeScript client API and `bun`.

## How to Use

Run Robinhood operations by executing TypeScript code with `bun`. The `robinhood-for-agents` npm package provides a full client library — just import it and call methods:

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
// call any method, print results as JSON
const holdings = await rh.buildHoldings();
console.log(JSON.stringify(holdings, null, 2));
'
```

See [client-api.md](client-api.md) for all available methods and signatures.

> **MCP users:** If you have the `robinhood-for-agents` MCP server configured, you may use MCP tools instead. See [reference.md](reference.md) for tool parameters. MCP is optional — the client API above does everything the MCP tools do. Pick **one** mode per session and stay in it: the MCP server and a `bun -e` script are two separate token-refreshing processes, and refresh tokens are single-use, so interleaving them can poison one of them. In MCP mode, `robinhood_check_session` is the session check — it probes the API rather than just reading the keychain.

## CRITICAL SAFETY RULES
1. **Always confirm before placing any order** — show order preview, get explicit "yes"
2. **Show current price** before order confirmation so user knows the cost
3. **Never place orders without user confirmation**
4. **Fund transfers and bank operations are BLOCKED** — refuse these requests
5. **Never place bulk cancel operations** — cancel orders one at a time
6. **Never turn a "sell" into a short.** `sell` closes a long; `sell_short` opens a short with unlimited loss potential. Only short when the user asked to short, and label it **SHORT SELL** when confirming. A **negative** position quantity *is* a short — close it by **buying**, never by selling more. See [trade.md](trade.md#short-selling)
7. **Name the trading session.** Outside regular hours, only limit orders execute; an order tagged to the wrong session silently queues for the next open instead of filling. Check with `robinhood_get_market_hours` / `getMarketHours()` — never infer the session from the local clock

### BLOCKED Operations (never use)
- Bulk cancel operations
- Fund transfers (withdraw/deposit)
- Bank unlinking

## Routing

| User Intent | Domain File | Example Triggers |
|---|---|---|
| Auth / login / connect | [setup.md](setup.md) | "setup robinhood", "connect to robinhood", "robinhood login" |
| Portfolio / holdings / positions | [portfolio.md](portfolio.md) | "show my portfolio", "my holdings", "account summary" |
| Stock research / analysis | [research.md](research.md) | "research AAPL", "analyze TSLA", "due diligence on NVDA" |
| Buy / sell / short / orders / cancel | [trade.md](trade.md) | "buy 10 shares of AAPL", "sell my TSLA", "short 10 SPY", "cancel my order" |
| Options / calls / puts / chains | [options.md](options.md) | "show AAPL options", "SPX calls", "0DTE options", "covered calls" |
| Watchlists / lists / "add to my list" | [watchlists.md](watchlists.md) | "my watchlists", "add NVDA to my tech list", "remove TSLA from watchlist" |
| Scanners / screeners / saved screens | [reference.md](reference.md) | "my scanners", "my saved screens", "what filters can I scan on" |
| Realized P&L / gains / "how did my trades do" | [reference.md](reference.md) | "my realized gains", "P&L this year", "how did my trades do" |
| Tax lots / cost basis per holding | [reference.md](reference.md) | "tax lots for AAPL", "cost basis of my NVDA lots", "which lots are long-term" |

Read the corresponding domain file for detailed workflow instructions.

## Authentication Prerequisite
Before any data-fetching or trading operation, verify the session actually works. `restoreSession()` only loads tokens from the store — it does **not** prove they are still valid, so probe with a real call:
```bash
bun -e '
import { getClient, AuthenticationError } from "robinhood-for-agents";
const rh = getClient();
try {
  await rh.restoreSession();
  await rh.getAccountProfile();          // the probe — this is what proves the token works
  console.log("logged_in");
} catch (e) {
  console.log(e instanceof AuthenticationError ? `expired: ${e.name}` : `unknown: ${e}`);
}
'
```
- `logged_in` → proceed.
- `expired` (`TokenExpiredError` / `AuthenticationError`) → the tokens are dead and could not be refreshed. Follow [setup.md](setup.md) to re-authenticate.
- `unknown` → a transient/network failure. The session may well be fine — **do not** send the user through a browser re-login on this; retry once first.

> **MCP mode:** call `robinhood_check_session` instead — it probes the API and returns `logged_in` / `expired` / `unknown` / `not_authenticated`. Only `expired` and `not_authenticated` warrant `robinhood_browser_login`.

## Client Methods

The client exposes 70+ async methods across auth, portfolio, research, options, orders, watchlists, scanners, P&L, and tax lots.

- [client-api.md](client-api.md) — full method reference (signatures, options, examples) and the MCP↔client mapping table
- [reference.md](reference.md) — MCP tool parameters (if using MCP mode instead of the client)

## Important Notes
- **Do NOT use `phoenix.robinhood.com`** — use `api.robinhood.com` endpoints only
- Multi-account is first-class: always ask which account when multiple exist
- Session tokens renew themselves: the client refreshes proactively (~24h before expiry) and again on a 401, so a session in regular use stays alive without a re-login. Access-token TTL varies (~6-8.5 days observed) — never quote a fixed number
- Refresh tokens are **single-use**: every renewal issues a new one and instantly kills the old (and revokes the previous access token). Run one client at a time — MCP server *or* a `bun -e` script, not both; a second process gets poisoned. It self-heals by re-reading the token store, but there is no cross-process lock
- Renewal only happens while the client is being used. A session left idle past the refresh-token lifetime lapses and needs a **new browser login** — see [setup.md](setup.md)
