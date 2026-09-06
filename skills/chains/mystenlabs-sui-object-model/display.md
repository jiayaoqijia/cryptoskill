# Object Display (V2)

Object Display defines how objects render in wallets, explorers, and apps. It is a template system that maps struct field names to display properties like name, description, image URL, and links.

**Display V2 is the current standard.** It replaces the legacy V1 event-discovery model with a registry-backed model where each type has one deterministic `Display<T>` derived from the global `DisplayRegistry` and the type. V1 displays were automatically migrated to V2 via a system snapshot migration.

## Creating a Display

Use the `sui::display_registry` module (not the legacy `sui::display`). There are two creation paths.

`DisplayRegistry` is a shared system object at address `0xd`. Both creation functions take a `&mut DisplayRegistry` as their first argument. Each returns a `(Display<T>, DisplayCap<T>)` pair — the display has a deterministic derived ID, and the capability authorizes future updates.

### Publisher path — `new_with_publisher`

Requires a `Publisher` object, which is obtained during the module's `init` function using `package::claim(otw, ctx)`. Use this when you already have a Publisher and are setting up Display at publish time.

```move
use sui::display_registry;
use sui::package;

public struct MY_NFT has drop {}

public struct GameItem has key, store {
    id: UID,
    name: String,
    image_id: u64,
    rarity: String,
}

fun init(otw: MY_NFT, ctx: &mut TxContext) {
    let publisher = package::claim(otw, ctx);

    // registry is the shared DisplayRegistry at 0xd
    let (mut d, cap) = display_registry::new_with_publisher<GameItem>(
        registry,
        &publisher,
        ctx,
    );
    display_registry::set(&mut d, &cap, b"name".to_string(), b"{name}".to_string());
    display_registry::set(&mut d, &cap, b"description".to_string(), b"A {rarity} game item".to_string());
    display_registry::set(&mut d, &cap, b"image_url".to_string(), b"https://example.com/items/{image_id}.png".to_string());
    display_registry::share(d);

    transfer::public_transfer(cap, ctx.sender());
    transfer::public_transfer(publisher, ctx.sender());
}
```

### Permit path — `new`

Uses `internal::Permit<T>` instead of a Publisher. Simpler because it does not require a One-Time Witness or a Publisher object — it works in any function, not just `init`.

```move
use sui::display_registry;
use sui::internal;

public struct GameItem has key, store {
    id: UID,
    name: String,
    image_id: u64,
    rarity: String,
}

// Can be called from any function — no OTW or Publisher needed
public fun setup_display(registry: &mut DisplayRegistry, ctx: &mut TxContext) {
    let (mut d, cap) = display_registry::new<GameItem>(
        registry,
        internal::permit<GameItem>(),
        ctx,
    );
    display_registry::set(&mut d, &cap, b"name".to_string(), b"{name}".to_string());
    display_registry::set(&mut d, &cap, b"image_url".to_string(), b"https://example.com/items/{image_id}.png".to_string());
    display_registry::share(d);

    transfer::public_transfer(cap, ctx.sender());
}
```

### Retroactive Display via upgrades

Because the Permit path does not require a Publisher (and therefore no OTW claimed in `init`), you can add Display to an already-published package via a compatible upgrade. Add a new public function that calls `display_registry::new<T>` with `internal::permit<T>()`, publish the upgrade, then call that function. This is useful when the original package did not set up Display at all.

## V2 API

| Function | Purpose |
|---|---|
| `display_registry::new_with_publisher<T>(registry, publisher, ctx)` | Create `Display<T>` + `DisplayCap<T>` — requires Publisher |
| `display_registry::new<T>(registry, permit, ctx)` | Create `Display<T>` + `DisplayCap<T>` — uses `internal::Permit<T>`, no Publisher needed |
| `display_registry::set<T>(display, cap, name, value)` | Set a display field |
| `display_registry::unset<T>(display, cap, name)` | Remove a display field |
| `display_registry::clear<T>(display, cap)` | Clear all display fields |
| `display_registry::share(display)` | Share the display object so it can be discovered |

## Template syntax

Display templates use `{field_name}` syntax. The placeholder is replaced with the actual field value from the object at display time. V2 supports nested field access with `{field.nested}` syntax. You can combine static text with field interpolation:

- `{name}` — replaced with the object's `name` field
- `A {rarity} game item` — combines static text with the `rarity` field
- `https://example.com/{image_id}.png` — constructs a URL from a field value
- `{metadata.description}` — nested field access (V2 feature)

## Common display properties

| Property | Purpose |
|---|---|
| `name` | The object's display name |
| `description` | A human-readable description |
| `image_url` | URL to the object's image |
| `thumbnail_url` | URL to a smaller thumbnail image |
| `link` | URL to the object's page in an app |
| `project_url` | URL to the project's website |
| `creator` | The creator's name or identifier |

## What changed from V1 to V2

| V1 (legacy `sui::display`) | V2 (`sui::display_registry`) |
|---|---|
| `display::new<T>(&publisher, ctx)` | `display_registry::new_with_publisher<T>(registry, publisher, ctx)` returns `(Display<T>, DisplayCap<T>)` |
| `d.add(key, value)` / `d.edit(key, value)` | `display_registry::set(display, cap, name, value)` |
| `d.remove(key)` | `display_registry::unset(display, cap, name)` |
| `d.update_version()` required to publish changes | No `update_version` needed |
| Event-based discovery (RPCs scan for `VersionUpdated` events) | Registry-backed with deterministic derived IDs |
| Multiple `Display<T>` per type allowed | One `Display<T>` per type (deterministic) |
| `Publisher` for access control | `DisplayCap<T>` for access control |

## Migrating from V1

Existing V1 displays were migrated to V2 in a system snapshot migration. If you need to manage a migrated display, use `migrate_v1_to_v2` only if the display was not already migrated by the snapshot. After migration, claim the `DisplayCap<T>` to update the display.

## Display-mixin pattern

For off-chain-primary behaviors like expiration, dependencies, or thresholds, prefer Display-field conventions over type wrappers. For example, use an `expires_at` Display field rather than wrapping objects in a `WithExpiry<T>` type:

```move
// Prefer: set an expires_at Display field
display_registry::set(&mut d, &cap, b"expires_at".to_string(), b"{expires_at}".to_string());

// Avoid: generic type wrappers for off-chain concerns
// public struct WithExpiry<T> { inner: T, expires_at: u64 }
// These interact badly with type resolution and don't compose well.
```

Type wrappers like `WithExpiry<T>` break type resolution (clients must know the wrapper to query the inner type) and do not compose well when multiple behaviors are needed (e.g., `WithExpiry<WithThreshold<T>>`). Use Display fields when the behavior is informational / off-chain. Use typed helpers only when on-chain enforcement is needed (e.g., a hot potato that forces expiry checks in Move).

## Key rules

- Each type has exactly one `Display<T>` with a deterministic derived ID from the global `DisplayRegistry`.
- Two creation paths: `new_with_publisher` (requires Publisher + OTW) and `new` (requires `internal::Permit<T>`, no OTW needed).
- The `DisplayCap<T>` is the access control mechanism for updating the display. The `Publisher` is used only at creation time (and only with the Publisher path).
- After setting fields, call `display_registry::share(display)` to make the display discoverable.
- Do not use the legacy `sui::display` module for new code. Use `sui::display_registry`.
