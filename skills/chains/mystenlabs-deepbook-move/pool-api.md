# Pool and Order Functions

## Move dependency

Add DeepBook to your `Move.toml`:

```toml
[dependencies]
deepbook = { mvr = "@deepbook/core" }
```

Then import the pool module in your Move code:

```move
use deepbook::pool::Pool;
```

## Pool creation

Pools are created through the `Registry` to prevent duplicates. Each pool manages a single market (base/quote pair). Pool creation requires a fee of 500 DEEP.

Key pool parameters set at creation:

- **Tick size** — minimum price increment
- **Lot size** — minimum quantity increment
- **Min size** — minimum order quantity

## Placing limit orders

The `place_limit_order` function places an order on the book. It requires a mutable reference to the Pool, a reference to the BalanceManager, a TradeProof, and order parameters.

```move
public fun place_limit_order<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    balance_manager: &mut BalanceManager,
    trade_proof: &TradeProof,
    client_order_id: u64,
    order_type: u8,
    self_matching_option: u8,
    price: u64,
    quantity: u64,
    is_bid: bool,
    pay_with_deep: bool,
    expire_timestamp: u64,
    clock: &Clock,
    ctx: &mut TxContext,
): OrderInfo
```

**Parameters:**
- `client_order_id` — user-defined order identifier (u64)
- `order_type` — `0` (NO_RESTRICTION), `1` (IMMEDIATE_OR_CANCEL), `2` (FILL_OR_KILL), `3` (POST_ONLY)
- `self_matching_option` — `0` (SELF_MATCHING_ALLOWED), `1` (CANCEL_TAKER), `2` (CANCEL_MAKER)
- `price` — scaled by the pool's price scaling factor
- `quantity` — scaled by the pool's quantity scaling factor
- `is_bid` — `true` for buy, `false` for sell
- `pay_with_deep` — `true` to pay fees in DEEP, `false` for input token (25% premium)
- `expire_timestamp` — order expiration in milliseconds (0 for no expiration)

Returns an `OrderInfo` struct with the order's lifecycle data including fills.

## Placing market orders

```move
public fun place_market_order<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    balance_manager: &mut BalanceManager,
    trade_proof: &TradeProof,
    client_order_id: u64,
    self_matching_option: u8,
    quantity: u64,
    is_bid: bool,
    pay_with_deep: bool,
    clock: &Clock,
    ctx: &mut TxContext,
): OrderInfo
```

Market orders fill immediately against existing liquidity. They do not rest on the book.

## Canceling orders

```move
public fun cancel_order<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    balance_manager: &mut BalanceManager,
    trade_proof: &TradeProof,
    order_id: u128,
    clock: &Clock,
    ctx: &mut TxContext,
)
```

Cancel all open orders for an account:

```move
public fun cancel_all_orders<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    balance_manager: &mut BalanceManager,
    trade_proof: &TradeProof,
    clock: &Clock,
    ctx: &mut TxContext,
)
```

Canceled orders return locked funds to settled balances in the BalanceManager.

## Swap functions

Swaps provide an AMM-like interface on top of the order book. They can operate directly on `Coin` objects without a BalanceManager.

### Direct swaps (no BalanceManager)

```move
public fun swap_exact_base_for_quote<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    base_in: Coin<BaseAsset>,
    deep_in: Coin<DEEP>,
    min_quote_out: u64,
    clock: &Clock,
    ctx: &mut TxContext,
): (Coin<BaseAsset>, Coin<QuoteAsset>, Coin<DEEP>)
```

Returns three coins: remaining base, received quote, and remaining DEEP. The `deep_in` amount covers fees — overestimate is safe since unused DEEP is returned.

```move
public fun swap_exact_quote_for_base<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    quote_in: Coin<QuoteAsset>,
    deep_in: Coin<DEEP>,
    min_base_out: u64,
    clock: &Clock,
    ctx: &mut TxContext,
): (Coin<BaseAsset>, Coin<QuoteAsset>, Coin<DEEP>)
```

### Swaps with BalanceManager

```move
public fun swap_exact_base_for_quote_with_manager<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    balance_manager: &mut BalanceManager,
    trade_cap: &TradeCap,
    deposit_cap: &DepositCap,
    withdraw_cap: &WithdrawCap,
    base_in: Coin<BaseAsset>,
    min_quote_out: u64,
    clock: &Clock,
    ctx: &mut TxContext,
): (Coin<BaseAsset>, Coin<QuoteAsset>)
```

```move
public fun swap_exact_quote_for_base_with_manager<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    balance_manager: &mut BalanceManager,
    trade_cap: &TradeCap,
    deposit_cap: &DepositCap,
    withdraw_cap: &WithdrawCap,
    quote_in: Coin<QuoteAsset>,
    min_base_out: u64,
    clock: &Clock,
    ctx: &mut TxContext,
): (Coin<BaseAsset>, Coin<QuoteAsset>)
```

The `_with_manager` swap variants take three capability references (`TradeCap`, `DepositCap`, `WithdrawCap`) instead of a `TradeProof` and do not require a separate `deep_in` coin — fees are handled through the BalanceManager.

### Swap simulation

```move
public fun get_quantity_out<BaseAsset, QuoteAsset>(
    pool: &Pool<BaseAsset, QuoteAsset>,
    base_quantity: u64,
    quote_quantity: u64,
    clock: &Clock,
): (u64, u64, u64)
```

Returns `(base_out, quote_out, deep_required)`. Use this to determine the exact DEEP needed before executing a swap. Exactly one of `base_quantity` or `quote_quantity` must be non-zero.

## Pool state queries

### Order book queries

```move
public fun get_level2_ticks_from_mid<BaseAsset, QuoteAsset>(
    pool: &Pool<BaseAsset, QuoteAsset>,
    ticks: u64,
    clock: &Clock,
): (vector<u64>, vector<u64>, vector<u64>, vector<u64>)
```

Returns bid prices, bid quantities, ask prices, and ask quantities for the specified number of ticks from mid price.

### Account queries

```move
public fun account_open_orders<BaseAsset, QuoteAsset>(
    pool: &Pool<BaseAsset, QuoteAsset>,
    balance_manager: &BalanceManager,
): vector<u128>
```

Returns a vector of order IDs for the account's open orders in this pool.

## Constants

Key protocol constants from the Move source:

| Constant | Value | Description |
|----------|-------|-------------|
| Pool creation fee | 500 DEEP | Cost to create a new pool |
| Version | 8 | Current package version |
| NO_RESTRICTION | 0 | Order fills and rests remainder |
| IMMEDIATE_OR_CANCEL | 1 | Fill or cancel remainder |
| FILL_OR_KILL | 2 | Fill entirely or reject |
| POST_ONLY | 3 | Must rest entirely |
| SELF_MATCHING_ALLOWED | 0 | Default self-matching |
| CANCEL_TAKER | 1 | Cancel taker on self-match |
| CANCEL_MAKER | 2 | Cancel maker on self-match |

## Governance functions

Users with DEEP stake can participate in pool governance:

- **Propose parameter changes** — modify taker fee, maker fee, or stake requirement
- **Vote on proposals** — voting power combines linear and square-root components (capped at 100,000 DEEP)
- **Quorum requirement** — 50% of active stake must vote for a proposal to pass
- **Effect timing** — approved proposals take effect the following epoch
