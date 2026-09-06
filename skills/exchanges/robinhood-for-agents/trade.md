# Trade — Order Placement & Management

**CRITICAL: Safety rules in SKILL.md apply to ALL operations below. Always confirm with the user before placing any order.**

**Session first.** Verify the session per [SKILL.md](SKILL.md#authentication-prerequisite) *before* Step 1 — `restoreSession()` succeeds on dead tokens, so an unverified session fails partway through the flow instead of up front. If any step throws `TokenExpiredError`, **stop**: re-authenticate via [setup.md](setup.md), then restart from Step 3 (re-review) — never place an order against a review taken before a re-login. Run one client at a time during an order flow; refresh tokens are single-use and a competing process can invalidate the session mid-order.

## Order Flow

### Step 1: Resolve Account
```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
const accounts = await rh.getAccounts();
console.log(JSON.stringify(accounts, null, 2));
'
```
If multiple accounts, **ask the user which account to use**. Never pick on their behalf.

### Step 2: Parse the Request
Extract from the user's message:
- Symbol (e.g., AAPL, BTC)
- Side — `buy`, `sell`, or `sell_short`. "Sell" means **close a long**; only open a short when the user asked for a **short**, and say so explicitly when you confirm (see [Short selling](#short-selling))
- Quantity or dollar amount
- Order type (market/limit/stop) and prices
- Trading session — regular hours, extended hours, or the 24 Hour Market. **Do not guess from the clock** — call `robinhood_get_market_hours` (or `rh.getMarketHours()`) to see which session is live; local time is wrong across time zones, weekends, and holidays. If the user didn't say and the market is closed, ask which session they want: a regular-hours order placed after the close queues for the next open instead of executing, and only limit orders execute outside regular hours
- Asset type (stock/option/crypto)

### Step 3: Review the order (pre-trade simulation — places nothing)
**Always run the review first.** It simulates the order over read-only endpoints: it attaches the live quote and reproduces Robinhood's price collar, which catches a mis-priced (fat-fingered) limit/stop order.

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
const review = await rh.reviewEquityOrder({ symbol: "AAPL", side: "buy", quantity: 10, limitPrice: 150.0, accountNumber: "ACCT" });
console.log(JSON.stringify(review, null, 2));
'
```
- `order_checks` with an `alert_type` → a price-collar alert (e.g. the limit is far off the market). **Stop and re-confirm the price with the user.**
- `order_checks` is `{}` **and** `evaluated_checks` is non-empty → the collar ran clean. If `evaluated_checks` is empty (see `not_evaluated_checks`), the collar could not run — do **not** read `{}` as "all clear".
- Options: use `reviewOptionOrder({ symbol, legs, price, quantity, direction, accountNumber })` — returns per-leg market data + required collateral.

### Step 4: Show the review to the user and confirm
Present the review output — this is a **stop, not an internal step**. Never chain review→place silently.
```
Order Preview (simulated — nothing placed yet):
  Action: BUY 10 shares of AAPL @ $150.00 limit
  Current price: $150.00   Estimated cost: ~$1,500.00
  Session: regular hours
  Price-collar check: OK (or: ⚠️ EXTREMELY_MARKETABLE_LIMIT_PRICE — price looks far off market)
  Account: <account_number>

Proceed? (yes/no)
```
Wait for the user to explicitly confirm. If the quote in the review has since gone stale, re-run the review before placing.

State the session in the preview whenever it isn't regular hours, and say plainly what it means — "extended hours: limit orders only" or "queues for the next open". A short must be labelled **SHORT SELL**, never just "sell".

### Step 5: Place Order (after user confirms)

If the place call fails with `TokenExpiredError`, the order was **not** placed — the request never reached Robinhood. Re-authenticate ([setup.md](setup.md)), then re-run Step 3 and re-confirm with the user before trying again; do not blind-retry the place call.

## Stock Orders

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
const order = await rh.orderStock("AAPL", "buy", 10, { limitPrice: 150.0, timeInForce: "gfd", marketHours: "regular_hours", accountNumber: "ACCT" });
console.log(JSON.stringify(order, null, 2));
'
```

Options: `{ limitPrice, stopPrice, trailAmount, trailType, accountNumber, timeInForce, marketHours, extendedHours }`

- Market order: omit `limitPrice` and `stopPrice`
- Limit order: set `limitPrice`
- Stop-limit: set both `stopPrice` and `limitPrice`
- Trailing stop: set `trailAmount` + `trailType` (`"percentage"` or `"amount"` — `"amount"` is a dollar trail; anything else is treated as a percentage)
- Trading session: `marketHours` is `"regular_hours"`, `"extended_hours"`, or `"all_day_hours"` (the 24 Hour Market). **Always pass it explicitly** — the MCP tool requires it, and the client library falls back to regular hours when it is omitted, which after the close means the order queues for the next open instead of executing. Only **limit** orders execute outside regular hours; a market, stop, or trailing order tagged to another session is rejected.

### Short selling

`side: "sell"` only closes a long position — selling stock the account does not hold fails with `Not enough shares to sell.` Opening a short is a different side:

| Intent | Side |
|---|---|
| Open a short | `sell_short` |
| Cover a short | `buy` (there is no separate cover side) |

```typescript
// Open
await rh.orderStock("AAPL", "sell_short", 10, { limitPrice: 150.0, timeInForce: "gfd", marketHours: "regular_hours", accountNumber: "ACCT" });
// Cover
await rh.orderStock("AAPL", "buy", 10, { limitPrice: 145.0, timeInForce: "gfd", marketHours: "regular_hours", accountNumber: "ACCT" });
```

Requirements and failure modes:

| Condition | Rejected by | What you will see |
|---|---|---|
| Whole shares — no fractional shorts | client, before sending | `Short sales must be whole shares — fractional short selling is not supported` |
| Good-for-day only (`gtc` not allowed) | client, before sending | `Short sales must be good-for-day — timeInForce "gtc" is not accepted` |
| **Not available in the 24 Hour Market** | client, before sending | `Short selling is not available during the 24 Hour Market (all_day_hours)` |
| Margin-enabled account required | Robinhood | `You need to have margin investing enabled to short.` |
| Outside regular hours, pass `marketHours: "extended_hours"` | Robinhood | `It's after market close. To place this short sell order, change your trading session to extended hours.` |
| Symbol must be shortable | Robinhood | varies — check `short_selling_tradability` via `robinhood_get_equity_tradability` first |

The client-side rejections throw before any order is attempted, so nothing was placed. The Robinhood ones come back as an `APIError`.

**After placing.** An accepted short first shows `state: "locate_completed"` — Robinhood found shares to borrow. That is success, not an error; it proceeds to `filled` like any other order.

**A short position shows as a NEGATIVE quantity.** After a short fills, `robinhood_get_equity_positions` reports e.g. `quantity: "-10"`. Never read that as a data error or as something to "fix" by selling more — selling more *increases* the short. Cover with a `buy` of the absolute value.

**Diagnosing a rejection.** Robinhood validates in order and returns only the first failure, so a rejection can hide another one behind it. Most notably, the **session is checked before the account type**: a short attempted after hours on a cash account reports `It's after market close…`, *not* the margin error — the account may be ineligible too. Fix the reported problem, then re-try to see whether another is behind it.

**Confirm shorts explicitly.** A short has unlimited loss potential and is easy to conflate with selling a holding. Before placing, verify the user asked to *open a short* — if they said "sell my AAPL" and the account holds AAPL, that is a `sell`, not a `sell_short`. Label it **SHORT SELL** in the confirmation, and state that closing it requires buying the shares back.

## Option Orders

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
const order = await rh.orderOption("AAPL", [
  { expirationDate: "2026-04-17", strike: 200, optionType: "call", side: "buy", positionEffect: "open" }
], 3.50, 1, "debit", { accountNumber: "ACCT" });
console.log(JSON.stringify(order, null, 2));
'
```

For spreads, pass multiple legs. `direction` is "debit" for net-buy, "credit" for net-sell.

## Crypto Orders

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
// Buy 0.5 BTC
const order = await rh.orderCrypto("BTC", "buy", 0.5);
// Buy $100 of BTC
const order2 = await rh.orderCrypto("BTC", "buy", 100, { amountIn: "price" });
console.log(JSON.stringify(order, null, 2));
'
```

Options: `{ amountIn?: "quantity" | "price"; limitPrice?: number }`

## Order Management

### View Orders
```typescript
const allOrders = await rh.getAllStockOrders();
const openOrders = await rh.getOpenStockOrders();
// Also: getAllOptionOrders(), getOpenOptionOrders(), getAllCryptoOrders(), getOpenCryptoOrders()
```

### Cancel Order
```typescript
await rh.cancelStockOrder("order-uuid");
// Also: cancelOptionOrder(), cancelCryptoOrder()
```

### Monitor Order
```typescript
const order = await rh.getStockOrder("order-uuid");
// Also: getOptionOrder(), getCryptoOrder()
```

**Reading `state`.** Do not report an order as failed just because it is not `filled` — most states mean "working":

| `state` | Meaning |
|---|---|
| `unconfirmed` / `queued` / `confirmed` | Accepted and working. Not yet executed |
| `locate_completed` | **Short sale accepted** — Robinhood located shares to borrow. This is a normal, successful state on the way to a fill; it is not an error |
| `partially_filled` | Some shares executed; the rest is still working |
| `filled` | Fully executed — terminal |
| `cancelled` / `rejected` / `failed` | Terminal, nothing more will execute. Check `reject_reason` |

Only `filled`, `cancelled`, `rejected`, and `failed` are terminal. When polling, keep going until one of those; report the others as still working, and always quote `cumulative_quantity` — a cancelled order may still have partially filled before it was cancelled.

Also useful on the order object: `cumulative_quantity` (shares actually executed), `average_price` (fill price), `cancel` (non-null means it can still be cancelled), and `position_effect` (`open` / `close` — Robinhood's own view of whether the order opened or closed a position).

For all client methods, see [client-api.md](client-api.md).
