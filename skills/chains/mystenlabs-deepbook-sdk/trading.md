# Orders, Swaps, and Order Lifecycle

## Placing limit orders

Limit orders require a BalanceManager with deposited funds. Prices and quantities must respect the pool's tick size and lot size.

### Maker order (POST_ONLY)

A `POST_ONLY` order guarantees the order rests on the book as a maker. If it would cross the spread and fill immediately, it is silently rejected — no order is placed and no error is thrown.

```typescript
import { OrderType, SelfMatchingOptions } from "@mysten/deepbook-v3";

const tx = new Transaction();
client.deepbook.deepBook.placeLimitOrder({
  poolKey: "DEEP_SUI",
  balanceManagerKey: "MANAGER_1",
  clientOrderId: "123",         // must be numeric string
  price: 0.03,                  // below market for a bid
  quantity: 100,                // in base asset units
  isBid: true,
  orderType: OrderType.POST_ONLY,
  selfMatchingOption: SelfMatchingOptions.CANCEL_TAKER,
})(tx);

await signAndExecute(tx);
```

### Taker order (NO_RESTRICTION)

A `NO_RESTRICTION` order fills what it can immediately and rests the remainder.

```typescript
const tx = new Transaction();
client.deepbook.deepBook.placeLimitOrder({
  poolKey: "DEEP_SUI",
  balanceManagerKey: "MANAGER_1",
  clientOrderId: "124",
  price: 0.05,                  // at or above market for a bid to cross
  quantity: 50,
  isBid: true,
  orderType: OrderType.NO_RESTRICTION,
})(tx);

await signAndExecute(tx);
```

### Order type options

| Type | Behavior |
|------|----------|
| `NO_RESTRICTION` | Fills what it can, rests the remainder |
| `POST_ONLY` | Must rest entirely — silently rejected if it would cross |
| `IMMEDIATE_OR_CANCEL` | Fills what it can immediately, cancels the rest |
| `FILL_OR_KILL` | Must fill entirely or the whole order is rejected |

### Pool constraints

Each pool has minimum size, tick size, and lot size constraints. For example, DEEP/SUI has tick=0.00001, lot=1, minimum=10 DEEP. Orders that don't align are rejected.

## Placing market orders

Market orders fill against existing liquidity. On localnet/sandbox, the market maker has a ~15-second rebalance cycle where liquidity temporarily disappears. Use retry logic:

```typescript
const tx = new Transaction();
client.deepbook.deepBook.placeMarketOrder({
  poolKey: "DEEP_SUI",
  balanceManagerKey: "MANAGER_1",
  clientOrderId: "125",
  quantity: 10,
  isBid: true,
  selfMatchingOption: SelfMatchingOptions.CANCEL_TAKER,
})(tx);

// Retry pattern for sandbox market maker rebalance window
const maxRetries = 3;
for (let attempt = 0; attempt < maxRetries; attempt++) {
  try {
    await signAndExecute(tx);
    break;
  } catch (e) {
    if (attempt < maxRetries - 1) {
      await new Promise((r) => setTimeout(r, 5000));
    }
  }
}
```

Market order fills are proven by BalanceManager balance deltas, not just transaction digests.

## Swaps

Swaps operate directly on wallet `Coin` objects without a BalanceManager. They provide an AMM-like interface on top of the order book.

### Simple swap (no BalanceManager)

```typescript
const tx = new Transaction();
const [baseCoin, quoteCoin, deepCoin] = tx.add(
  client.deepbook.deepBook.swapExactQuoteForBase({
    poolKey: "DEEP_SUI",
    amount: 1,            // quote amount (SUI)
    deepAmount: 0.1,      // DEEP for fees (overestimate — unused is returned)
    minOut: 0,            // minimum base received
  })
);

// Transfer returned coins back to sender — required or coins are destroyed
tx.transferObjects([baseCoin, quoteCoin, deepCoin], keypair.toSuiAddress());
await signAndExecute(tx);
```

### Swap rules

- **Base to quote:** `base_in` must be positive; `quote_in` must be zero
- **Quote to base:** `quote_in` must be positive; `base_in` must be zero
- A `deep_in` amount is necessary to cover trading fees — overestimating is safe since unused DEEP is returned
- Whitelisted pools (DEEP/SUI, DEEP/USDC) have 0% fees, so `deep_in` can be 0

### Swap with BalanceManager

```typescript
const tx = new Transaction();
const [baseCoin, quoteCoin, deepCoin] = tx.add(
  client.deepbook.deepBook.swapExactBaseForQuote({
    poolKey: "DEEP_SUI",
    balanceManagerKey: "MANAGER_1",
    amount: 100,          // base amount
    deepAmount: 1,
    minOut: 0,
  })
);

// Transfer returned coins back to sender
tx.transferObjects([baseCoin, quoteCoin, deepCoin], keypair.toSuiAddress());
await signAndExecute(tx);
```

### Simulating swaps

Use `getQuantityOut` to simulate a swap and determine the exact DEEP required for fees before executing:

```typescript
const result = await client.deepbook.deepBook.getQuantityOut({
  poolKey: "DEEP_SUI",
  baseQuantity: 100,
  quoteQuantity: 0,
});
```

## Querying the order book

### Order book depth

```typescript
const { bid_prices, bid_quantities, ask_prices, ask_quantities } =
  await client.deepbook.getLevel2TicksFromMid("DEEP_SUI", 100); // depth: number of ticks from mid
```

### Mid price calculation

Calculate mid price from the best bid and ask:

```typescript
const { bid_prices, ask_prices } =
  await client.deepbook.getLevel2TicksFromMid("DEEP_SUI", 1); // depth of 1 for best bid/ask

if (bid_prices.length > 0 && ask_prices.length > 0) {
  const bestBid = bid_prices[0];
  const bestAsk = ask_prices[0];
  const midPrice = (bestBid + bestAsk) / 2;
}
```

## Order management

### Querying open orders

```typescript
const orders = await client.deepbook.deepBook.accountOpenOrders({
  poolKey: "DEEP_SUI",
  balanceManagerKey: "MANAGER_1",
});
// Returns array of order IDs
```

### Getting order details

```typescript
const details = await client.deepbook.deepBook.getAccountOrderDetails({
  poolKey: "DEEP_SUI",
  balanceManagerKey: "MANAGER_1",
});
// Returns: order_id, client_order_id, quantity, filled_quantity, status, fee_is_deep
```

### Canceling orders

Cancel a specific order by ID:

```typescript
const tx = new Transaction();
client.deepbook.deepBook.cancelOrder({
  poolKey: "DEEP_SUI",
  balanceManagerKey: "MANAGER_1",
  orderId: "123456",
})(tx);

await signAndExecute(tx);
```

Cancel all open orders:

```typescript
const tx = new Transaction();
client.deepbook.deepBook.cancelAllOrders({
  poolKey: "DEEP_SUI",
  balanceManagerKey: "MANAGER_1",
})(tx);

await signAndExecute(tx);
```

## Complete order lifecycle

A typical spot trading session follows this flow:

1. **Create or reuse BalanceManager** — see `client-setup.md`
2. **Deposit funds** — deposit base/quote assets and DEEP for fees
3. **Place orders** — limit or market orders against the pool
4. **Monitor orders** — query `accountOpenOrders()` or `getAccountOrderDetails()`
5. **Cancel if needed** — cancel resting orders to unlock funds
6. **Withdraw** — call `withdrawAllFromManager()` to move settled balances back to wallet

Fills move funds into settled balances within the BalanceManager. Settled balances are available for withdrawal or further trading.

## Self-matching behavior

| Option | Behavior |
|--------|----------|
| `SelfMatchingOptions.SELF_MATCHING_ALLOWED` (default) | Allows self-trades — taker fills against own resting orders |
| `SelfMatchingOptions.CANCEL_TAKER` | Cancels the incoming taker order on self-match |
| `SelfMatchingOptions.CANCEL_MAKER` | Cancels the resting maker order on self-match |

The SDK defaults to `SelfMatchingOptions.SELF_MATCHING_ALLOWED`. Set explicitly to avoid unintended self-fills when the same account has resting orders on both sides.
