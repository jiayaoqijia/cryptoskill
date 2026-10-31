---
name: deepbook-move
description: >
  Guides writing, reviewing, and debugging Move smart contracts that call DeepBook V3:
  placing limit or market orders on-chain, creating pools, swapping without a
  BalanceManager, flash loans, BalanceManager/TradeCap authorization, and composing
  DeepBook calls in programmable transaction blocks. Use when the user asks about
  deepbook::pool, place_limit_order, swap_exact_base_for_quote, borrow_flashloan_base,
  FlashLoan hot potato, TradeProof, TradeCap/DepositCap/WithdrawCap, or adding
  `deepbook = { mvr = "@deepbook/core" }` to Move.toml.
---

# DeepBook V3 Move Integration

## Setup

`Move.toml`:

```toml
[dependencies]
deepbook = { mvr = "@deepbook/core" }
```

```move
use deepbook::pool::{Self, Pool};
use deepbook::balance_manager::{Self, BalanceManager, TradeProof, TradeCap};
```

Every `Pool` function is generic over `<BaseAsset, QuoteAsset>` and the type arguments must match the pool's creation order exactly: `Pool<SUI, USDC>` is a different type from `Pool<USDC, SUI>`.

## Orders (require a BalanceManager + TradeProof)

```move
public fun place_limit_order<BaseAsset, QuoteAsset>(
    self: &mut Pool<BaseAsset, QuoteAsset>,
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

`place_market_order` takes the same arguments minus `price` and `expire_timestamp`.
`cancel_order<BaseAsset, QuoteAsset>(pool, balance_manager, trade_proof, order_id, clock, ctx)`.

`order_type` constants: `0` = NO_RESTRICTION, `1` = IMMEDIATE_OR_CANCEL (IOC), `2` = FILL_OR_KILL (FOK), `3` = POST_ONLY.

Every order placement and cancellation needs a `TradeProof`, created in the same transaction:

```move
// owner of the BalanceManager
public fun generate_proof_as_owner(bm: &mut BalanceManager, ctx: &TxContext): TradeProof
// delegated trader holding a TradeCap
public fun generate_proof_as_trader(bm: &mut BalanceManager, trade_cap: &TradeCap, ctx: &TxContext): TradeProof
```

## Swaps (no BalanceManager, no TradeProof)

```move
public fun swap_exact_base_for_quote<BaseAsset, QuoteAsset>(
    self: &mut Pool<BaseAsset, QuoteAsset>,
    base_in: Coin<BaseAsset>,
    deep_in: Coin<DEEP>,
    min_quote_out: u64,
    clock: &Clock,
    ctx: &mut TxContext,
): (Coin<BaseAsset>, Coin<QuoteAsset>, Coin<DEEP>)

public fun swap_exact_quote_for_base<BaseAsset, QuoteAsset>(
    self: &mut Pool<BaseAsset, QuoteAsset>,
    quote_in: Coin<QuoteAsset>,
    deep_in: Coin<DEEP>,
    min_base_out: u64,
    clock: &Clock,
    ctx: &mut TxContext,
): (Coin<BaseAsset>, Coin<QuoteAsset>, Coin<DEEP>)
```

Both return three coins: leftover base, leftover quote, and unused DEEP. `deep_in` pays the taker fee — overestimating is safe because the unused DEEP is returned; underestimating aborts.

Simulate first:

```move
public fun get_quantity_out<BaseAsset, QuoteAsset>(
    self: &Pool<BaseAsset, QuoteAsset>,
    base_quantity: u64,
    quote_quantity: u64,
    clock: &Clock,
): (u64, u64, u64) // (base_out, quote_out, deep_required)
```

Exactly one of `base_quantity` or `quote_quantity` must be non-zero; passing both or neither is invalid.

## Flash loans

```move
public fun borrow_flashloan_base<BaseAsset, QuoteAsset>(
    self: &mut Pool<BaseAsset, QuoteAsset>, base_amount: u64, ctx: &mut TxContext,
): (Coin<BaseAsset>, FlashLoan)

public fun borrow_flashloan_quote<BaseAsset, QuoteAsset>(
    self: &mut Pool<BaseAsset, QuoteAsset>, quote_amount: u64, ctx: &mut TxContext,
): (Coin<QuoteAsset>, FlashLoan)

public fun return_flashloan_base<BaseAsset, QuoteAsset>(
    self: &mut Pool<BaseAsset, QuoteAsset>, coin: Coin<BaseAsset>, flash_loan: FlashLoan,
)

public fun return_flashloan_quote<BaseAsset, QuoteAsset>(
    self: &mut Pool<BaseAsset, QuoteAsset>, coin: Coin<QuoteAsset>, flash_loan: FlashLoan,
)
```

`FlashLoan` has **no abilities** — it cannot be stored, copied, or dropped, so it must be consumed by the matching `return_flashloan_*` call in the same transaction. If it is not repaid the whole transaction reverts and no state change persists. The maximum borrowable amount is the pool's current holdings of that asset. There is no borrow fee; repay the exact borrowed amount.

## BalanceManager and delegation

A `BalanceManager` is a shared object that holds a user's balances and is reused across **all** pools — deposit once, trade everywhere. Two-tier authorization:

- **Owner** — full control: deposit, withdraw, mint and revoke caps, `generate_proof_as_owner`.
- **Cap holders** — `TradeCap` can only trade (`generate_proof_as_trader`); it **cannot deposit or withdraw**. `DepositCap` can only deposit, `WithdrawCap` can only withdraw.

```move
public fun new(ctx: &mut TxContext): BalanceManager
public fun mint_trade_cap(bm: &mut BalanceManager, ctx: &mut TxContext): TradeCap
public fun deposit<T>(bm: &mut BalanceManager, coin: Coin<T>, ctx: &mut TxContext)
public fun withdraw<T>(bm: &mut BalanceManager, amount: u64, ctx: &mut TxContext): Coin<T>
```

Limit: **1,000 total capabilities per BalanceManager** across TradeCap, DepositCap, and WithdrawCap combined. Beyond that, shard across multiple BalanceManagers.

## Rules and common mistakes

1. **Type parameter order.** `<USDC, SUI>` against a `Pool<SUI, USDC>` is a type mismatch; match the pool's base/quote order.
2. **Return the hot potato.** Forgetting `return_flashloan_*` compiles but aborts at runtime.
3. **Do not borrow from a pool and trade in that same pool in one transaction.** Borrowed funds are unavailable for settlement and the combined operations can fail; use a different pool or venue for the trade leg.
4. **`generate_proof_as_owner` only works from the owner address.** Delegated traders must call `generate_proof_as_trader` with a valid `TradeCap`.
5. **`generate_proof_as_trader` takes `ctx`** — `(bm, trade_cap, ctx: &TxContext)`; omitting it is a compile error.
6. **Use `_v2` variants where they exist** (e.g. `new_with_custom_owner_caps_v2`). The unsuffixed originals are stubs that `abort 1337`.
7. **Plan around the 1,000-cap limit** before building a system with many delegated trading accounts.

## Reference files

- `pool-api.md` — pool creation, order placement and cancellation, pool state queries, governance, constants.
- `balance-manager-api.md` — BalanceManager creation, cap minting and revocation, deposits/withdrawals, TradeProofs, events.
- `flash-loans.md` — borrow/return details, constraints, worked example.

Related skills: `deepbook-overview` (architecture, package addresses, pool IDs), `deepbook-sdk` (TypeScript), `sui-move` (Move fundamentals), `ptbs` (PTB composition).

If a signature is not above, read the reference file or `https://docs.sui.io/onchain-finance/deepbook/deepbookv3/contract-information` and the [deepbookv3 sources](https://github.com/MystenLabs/deepbookv3/tree/main/packages/deepbook/sources). Do not extrapolate from other protocols.
