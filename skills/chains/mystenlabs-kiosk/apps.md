# Kiosk Apps and Extensions

Kiosk supports two levels of app integration: basic apps using dynamic fields on the Kiosk's UID, and permissioned apps using the `kiosk_extension` module for restricted actions without owner involvement.

## Basic apps

Basic apps use the Kiosk's `id: UID` field to attach custom metadata through dynamic fields.

`uid_mut_as_owner` enables kiosk owners to mutably access the UID for adding or modifying dynamic fields.

### Kiosk Name app example

```move
module examples::kiosk_name_ext;

use std::string::String;
use sui::dynamic_field as df;
use sui::kiosk::{Self, Kiosk, KioskOwnerCap};

struct KioskName has copy, store, drop {}

public fun add(self: &mut Kiosk, cap: &KioskOwnerCap, name: String) {
    let uid_mut = self.uid_mut_as_owner(cap);
    df::add(uid_mut, KioskName {}, name)
}

public fun name(self: &Kiosk): Option<String> {
    if (df::exists_(self.uid(), KioskName {})) {
        option::some(*df::borrow(self.uid(), KioskName {}))
    } else {
        option::none()
    }
}
```

## Permissioned apps (Kiosk Apps API)

Permissioned apps use the `kiosk_extension` module for restricted actions without requiring direct owner involvement on every operation.

### App lifecycle

1. **Installation**: Requires an explicit `kiosk_extension` module call
2. **Disable**: Owners can disable apps via the `disable` function
3. **Re-enable**: Owners can re-enable via the `enable` function
4. **Removal**: App removal requires empty storage

### Adding an app

```move
module examples::letterbox_ext;
use sui::kiosk_extension;

const PERMISSIONS: u128 = 1;
struct Extension has drop {}

public fun add(kiosk: &mut Kiosk, cap: &KioskOwnerCap, ctx: &mut TxContext) {
    kiosk_extension::add(Extension {}, kiosk, cap, PERMISSIONS, ctx)
}
```

## Permissions bitmap

Permissions are represented as a `u128` bitmap:

| Bit pattern | Decimal | Permission |
|-------------|---------|------------|
| 0000 | 0 | No permissions |
| 0001 | 1 | Place |
| 0010 | 2 | Place and lock |
| 0011 | 3 | Place and lock |

### Protected functions

These functions require the appropriate permission bit set:

- `place<Ext, T>(Ext, &mut Kiosk, T, &TransferPolicy<T>)` -- requires place permission
- `lock<Ext, T>(Ext, &mut Kiosk, T, &TransferPolicy<T>)` -- requires lock permission

### Permission checking

- `can_place<Ext>(kiosk: &Kiosk): bool` -- checks if the extension has place permission
- `can_lock<Ext>(kiosk: &Kiosk): bool` -- checks if the extension has lock permission

## App storage

Each installed app receives isolated bag-type storage, accessible via a witness token.

- `storage(_ext: Extension {}, kiosk: &Kiosk): Bag` -- immutable access
- `storage_mut(_ext: Extension {}, kiosk: &mut Kiosk): &mut Bag` -- mutable access
