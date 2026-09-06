# Flash Loan Pattern

Flash loans are uncollateralized loans that you borrow and repay within the same programmable transaction block. DeepBook V3 pools expose flash loan endpoints for both base and quote assets.

## How it works

The system uses a **hot potato pattern** — the `FlashLoan` struct has no abilities (`key`, `store`, `copy`, `drop`). It cannot be stored, transferred, or silently discarded. It must be consumed by returning the borrowed assets before the transaction completes. If the assets are not returned, the transaction fails.

## Borrowing

### Borrow base assets

```move
public fun borrow_flashloan_base<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    base_amount: u64,
    ctx: &mut TxContext,
): (Coin<BaseAsset>, FlashLoan)
```

Returns the borrowed coins and a `FlashLoan` hot potato that must be returned.

### Borrow quote assets

```move
public fun borrow_flashloan_quote<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    quote_amount: u64,
    ctx: &mut TxContext,
): (Coin<QuoteAsset>, FlashLoan)
```

## Returning

### Return base assets

```move
public fun return_flashloan_base<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    base_coin: Coin<BaseAsset>,
    flash_loan: FlashLoan,
)
```

The `FlashLoan` object is unwrapped only if the full borrowed amount is returned. The transaction fails otherwise.

### Return quote assets

```move
public fun return_flashloan_quote<BaseAsset, QuoteAsset>(
    pool: &mut Pool<BaseAsset, QuoteAsset>,
    quote_coin: Coin<QuoteAsset>,
    flash_loan: FlashLoan,
)
```

## Borrowing limits

The maximum borrowable amount equals the pool's current holdings of that asset. Since pools hold all deposited and settled funds, liquid pools can provide substantial flash loan amounts.

## Constraints

1. **Same-transaction repayment.** The `FlashLoan` hot potato must be consumed in the same PTB. There is no multi-transaction borrowing.

2. **No same-pool trading.** Borrowing from a pool and trading in the same pool within one transaction can fail because the borrowed funds are locked in the `FlashLoan` object and unavailable for order settlement. Use a different pool for trading if you need to use the borrowed funds.

3. **Match borrow and return types.** If you borrow base assets, you must return base assets (not quote). The `FlashLoan` tracks which asset was borrowed.

4. **Full repayment required.** You must return at least the borrowed amount. The `FlashLoan` records the borrowed quantity and the return function verifies the coin value matches.

## Worked example

A flash loan strategy that borrows from one pool and trades on another:

```move
// Step 1: Borrow SUI from the SUI/USDC pool
let (borrowed_sui, flash_loan) = pool_sui_usdc.borrow_flashloan_base<SUI, USDC>(
    1000_000_000_000, // 1000 SUI
    ctx,
);

// Step 2: Use the borrowed SUI in another operation
// (e.g., arbitrage on a different pool, liquidation, etc.)
let profit_sui = do_something_profitable(borrowed_sui);

// Step 3: Return the borrowed amount to the original pool
pool_sui_usdc.return_flashloan_base<SUI, USDC>(
    profit_sui, // must contain at least the borrowed amount
    flash_loan, // consumes the hot potato
);
```

If any step fails or the returned coin has less value than borrowed, the entire transaction reverts atomically — the pool never loses funds.
