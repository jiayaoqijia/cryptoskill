# Core Kiosk Operations

Kiosk is a decentralized system for commerce applications on Sui. Kiosks are shared objects that store assets with built-in trading functionality, including custom trade mechanisms like auctions.

## Key guarantees

- Ownership retention until purchase completion
- Creator-defined policy enforcement across all trades
- Marketplace event indexing capability

## Kiosk creation

`kiosk::default` creates and shares a Kiosk, then transfers the `KioskOwnerCap` to the creator. The KioskOwnerCap grants full control over the Kiosk contents.

## Access control

Ownership is represented by the `KioskOwnerCap`. Only the cap owner can place, take, list, borrow, or modify assets in the Kiosk.

## Asset states

Items in a Kiosk exist in one of four states:

| State | Withdrawable | Mutable borrow | Immutable borrow | Listable |
|-------|-------------|----------------|------------------|----------|
| **PLACED** | Yes | Yes | Yes | Yes |
| **LOCKED** | No | Yes | Yes | Yes |
| **LISTED** | No | No | Yes | No (can delist) |
| **LISTED EXCLUSIVELY** | No | No | No | Extension-managed |

- **PLACED**: Set via `kiosk::place`. Items are withdrawable, borrowable (mutable and immutable), and listable.
- **LOCKED**: Set via `kiosk::lock`. Items are non-withdrawable but mutable-borrowable and listable. Requires an associated TransferPolicy.
- **LISTED**: Set via `kiosk::list`. Items are immutably borrowable only. Modifications are prohibited. Can be delisted.
- **LISTED EXCLUSIVELY**: Extension-managed via `kiosk::list_with_purchase_cap`.

## Placing items

`kiosk::place` requires the `KioskOwnerCap` and the item to place. The item enters the PLACED state.

## Taking items

`kiosk::take` returns the asset to the owner. Unavailable for listed items.

## Locking items

`kiosk::lock` requires showing the associated `TransferPolicy`. Locked items cannot be withdrawn -- they can only leave the Kiosk through a sale.

## Listing and delisting

`kiosk::list` accepts an item ID and a price in MIST (1 SUI = 10^9 MIST). Emits an `ItemListed` event.

`kiosk::delist` removes a listing. Emits an `ItemDelisted` event.

## TransferPolicy and purchase flow

For an asset type `T` to be tradeable, it must have an associated shared `TransferPolicy`. Without one, items of type `T` cannot be traded (storage via `kiosk::place` is still possible).

### Purchase process

1. Buyer calls `kiosk::purchase` specifying the item and the list price
2. The function returns the purchased asset and a `TransferRequest`
3. The buyer must satisfy all `TransferPolicy` terms to complete the transaction

Policy changes apply instantly and globally across all platform trades.

## Borrowing

Three borrowing patterns are available:

### Immutable borrow (`kiosk::borrow`)

Always available for PLACED, LOCKED, and LISTED items. Requires a Move module.

```move
module examples::immutable_borrow;
use sui::kiosk::{Self, Kiosk, KioskOwnerCap};

public fun immutable_borrow_example<T>(self: &Kiosk, cap: &KioskOwnerCap, item_id: ID): &T {
    self.borrow(cap, item_id)
}
```

### Mutable borrow (`kiosk::borrow_mut`)

Available for PLACED and LOCKED items. Unavailable for LISTED items. Requires a Move module.

```move
module examples::mutable_borrow;
use sui::kiosk::{Self, Kiosk, KioskOwnerCap};

public fun mutable_borrow_example<T>(
    self: &mut Kiosk, cap: &KioskOwnerCap, item_id: ID
): &mut T {
    self.borrow_mut(cap, item_id)
}
```

### PTB-friendly mutable borrow (`kiosk::borrow_val`)

Uses the hot potato pattern. The borrowed value must be returned via `kiosk::return_val` in the same transaction or the transaction aborts.

## Withdrawal

`kiosk::withdraw` accesses sale proceeds from completed purchases. Uses `Option<u64>` for the amount parameter.
