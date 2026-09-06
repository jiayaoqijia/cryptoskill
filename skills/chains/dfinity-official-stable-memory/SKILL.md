---
name: stable-memory
description: "Persist canister state across upgrades. Covers StableBTreeMap and MemoryManager in Rust, persistent actor in Motoko, and upgrade hook patterns. Use when dealing with canister upgrades, data persistence, data lost after upgrade, stable storage, StableBTreeMap, pre_upgrade traps, or heap vs stable memory. Do NOT use for inter-canister calls or access control — use multi-canister or canister-security instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2, moc >= 1.7.0 for the Motoko examples (dot notation)"
metadata:
  title: "Stable Memory & Upgrades"
  category: Core
---

# Stable Memory & Canister Upgrades

## What This Is
Stable memory is persistent storage on Internet Computer that survives canister upgrades. Whether ordinary variables survive depends on the language:

- **Rust** -- heap data (`thread_local! { RefCell<T> }`, plain `static`s) is wiped on every upgrade. Any data you care about must live in stable memory, either through `ic-stable-structures` or by serializing it yourself in `pre_upgrade`/`post_upgrade`.
- **Motoko** -- enhanced orthogonal persistence is on by default, so `let` and `var` in a `persistent actor` already survive upgrades with no `stable` keyword and no upgrade hooks. Only `transient` declarations are wiped.

## Prerequisites

- For Motoko: mops with `core = "2.0.0"` in mops.toml, and `moc >= 1.7.0` (dot notation on `Map`/`List` needs it)
- For Rust: `ic-stable-structures = "0.7"` in Cargo.toml

## Canister IDs
No external canister dependencies. Stable memory is a local canister feature.

## Mistakes That Break Your Build

1. **Using `thread_local! { RefCell<T> }` for user data (Rust)** -- This is heap memory. It is wiped on every canister upgrade. All user data, balances, settings stored this way will vanish after `icp deploy`. Use `StableBTreeMap` instead.

2. **Forgetting `#[post_upgrade]` handler (Rust)** -- Without a `post_upgrade` function, the canister may silently reset state or behave unexpectedly after upgrade. Always define both `#[init]` and `#[post_upgrade]`.

3. **Using `stable` keyword in persistent actors (Motoko)** -- In mo:core `persistent actor`, all `let` and `var` declarations are automatically stable. Writing `stable let` produces warning M0218 and `stable var` is redundant. Just use `let` and `var`.

4. **Confusing heap memory limits with stable memory limits (Rust)** -- Heap (Wasm linear) memory is limited to 4GB for wasm32 and 6GB for wasm64. Stable memory can grow up to hundreds of GB (the subnet storage limit). The real danger: if you use `pre_upgrade`/`post_upgrade` hooks to serialize heap data to stable memory and deserialize it back, you are limited by the heap memory size AND by the instruction limit for upgrade hooks. Large datasets will trap during upgrade, bricking the canister. The solution is to use stable structures (`StableBTreeMap`, `StableCell`, etc.) that read/write directly to stable memory, bypassing the heap entirely. Use `MemoryManager` to partition stable memory into virtual memories so multiple structures can coexist without overwriting each other.

5. **Treating a rejected upgrade as data loss (Motoko)** -- Enhanced orthogonal persistence checks the new program against the existing state and either accepts the upgrade or rejects it *before* it takes effect. A rejected upgrade is **not** data loss: the canister keeps running the previous version with its state intact, so you fix the code and redeploy.

   Which schema changes need a migration, and how to write one, are owned by `migrating-motoko-actors` (the mops-managed migration chain); load it for the rules and syntax. The one thing to know here is the common surprise: **changing a record type that an existing persistent variable holds is an incompatible change and needs a migration**, even for an *optional* added field, and regardless of where the record lives (a top-level `var`, a `Map` value, etc.). Whether adding a *new* stable field itself needs a migration depends on the project's setup — under the enhanced migration chain a stable field is declared type-only, so a new one needs a migration; a plain `persistent actor` with an initializer on the new field does not — which is exactly why the rules live in that skill rather than as a table here. An incompatible upgrade is rejected at runtime with `RTS error: Memory-incompatible program upgrade` (the old state stays intact — it is not data loss).

   Don't discover this at deploy time. Configure `[canisters.<name>.check-stable]` in `mops.toml` so `mops check` runs the stable-compatibility check against the previous version's `.most` (load `mops-cli`): it tells you at check time whether a change is compatible or needs a migration, instead of surfacing the `RTS error` on the upgrade call.

6. **Serializing large data in pre_upgrade (Rust)** -- `pre_upgrade` has a fixed instruction limit. If you serialize a large HashMap to stable memory in pre_upgrade, it will hit the limit and trap, bricking the canister. Use `StableBTreeMap` which writes directly to stable memory and needs no serialization step.

7. **Mismatching the actor form and the `--default-persistent-actors` flag (Motoko)** -- Both plain `actor` and `persistent actor` are correct; which one compiles depends on that compiler flag. Enabling it is the recommended setup, because it keeps the code less verbose:

   ```toml
   # mops.toml — recommended; see `mops-cli`
   [moc]
   args = ["--default-persistent-actors"]
   ```

   With the flag, every actor is persistent, so write plain `actor { }`; the `persistent` keyword still compiles but is redundant (warning M0217). Without the flag, `persistent actor { }` is required, and plain `actor` fails with `[M0220] this actor or actor class should be declared persistent`. No annotation rescues it — `stable`, `transient`, and `pre_upgrade`/`post_upgrade` hooks all still fail, because the error is on the actor itself:

   ```motoko
   // without --default-persistent-actors
   actor {
     stable var users = Map.empty<Nat, Text>();   // M0220 — `stable` does not help
   };

   persistent actor {
     let users = Map.empty<Nat, Text>();          // compiles; persisted automatically
   };
   ```

   The examples below use `persistent actor`, which compiles either way.

   One trap when the flag is off: if the actor body has un-annotated `let`/`var`, moc reports `[M0219] this declaration is currently implicitly transient, please declare it explicitly transient` on those lines and M0220 never appears. Do not follow that suggestion — `transient` discards the data on upgrade, and the actor still fails M0220. The fix is `persistent` on the actor, or the flag.

## Implementation

### Motoko

With mo:core 2.0, `persistent actor` makes stable storage trivial. All `let` and `var` declarations inside the actor body are automatically persisted across upgrades.

```motoko
import Map "mo:core/Map";
import List "mo:core/List";
import Nat "mo:core/Nat";  // required: the compiler derives Map's implicit `compare` from this module
import Text "mo:core/Text";
import Time "mo:core/Time";

persistent actor {

  // Types: in the actor body (as here) or in an imported module -- but never
  // between the imports and the actor, which is M0141. See the `writing-motoko` skill.
  type User = {
    id : Nat;
    name : Text;
    created : Int;
  };

  // These survive upgrades automatically -- no "stable" keyword needed
  let users = Map.empty<Nat, User>();
  var userCounter : Nat = 0;
  let tags = List.empty<Text>();

  // Transient data -- reset to initial value on every upgrade
  transient var requestCount : Nat = 0;

  public func addUser(name : Text) : async Nat {
    let id = userCounter;
    users.add(id, {
      id;
      name;
      created = Time.now();
    });
    userCounter += 1;
    requestCount += 1;
    id
  };

  public query func getUser(id : Nat) : async ?User {
    users.get(id)
  };

  public query func getUserCount() : async Nat {
    users.size()
  };

  // requestCount resets to 0 after every upgrade
  public query func getRequestCount() : async Nat {
    requestCount
  };
}
```

Key rules for Motoko persistent actors:
- `let` for Map, List, Set, Queue -- auto-persisted, no serialization
- `var` for simple values (Nat, Text, Bool) -- auto-persisted
- `transient var` for caches, counters that should reset on upgrade
- NO `pre_upgrade` / `post_upgrade` needed -- the runtime handles it
- NO `stable` keyword -- it is redundant and produces warnings

#### mops.toml

```toml
[package]
name = "my-project"
version = "0.1.0"

[dependencies]
core = "2.0.0"

# Required. Without a [toolchain] moc pin, mops falls back to the dfx cache and
# the build dies with `dfx: not found` (see `mops-cli`).
[toolchain]
moc = "1.9.0"
```

### Rust

Rust canisters use `ic-stable-structures` for persistent storage. The `MemoryManager` partitions stable memory (up to hundreds of GB, limited by subnet storage) into virtual memories, each backing a different data structure.

#### Cargo.toml

```toml
[package]
name = "stable_memory_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-cdk = "0.19"
ic-stable-structures = "0.7"
candid = "0.10"
serde = { version = "1", features = ["derive"] }
ciborium = "0.2"
```

#### Single Stable Structure (Simple Case)

```rust
use ic_stable_structures::{
    memory_manager::{MemoryId, MemoryManager, VirtualMemory},
    storable::{Bound, Storable},
    DefaultMemoryImpl, StableBTreeMap,
};
use ic_cdk::{init, post_upgrade, query, update};
use candid::CandidType;
use serde::{Deserialize, Serialize};
use std::borrow::Cow;
use std::cell::RefCell;

type Memory = VirtualMemory<DefaultMemoryImpl>;

// -- Implement Storable for custom types --
// StableBTreeMap keys need Storable + Ord, values need Storable.
// Storable defines how a type is serialized to/from bytes in stable memory.
// Use CBOR (via ciborium) for serialization -- compact binary format, faster than candid.

#[derive(CandidType, Serialize, Deserialize, Clone)]
struct User {
    id: u64,
    name: String,
    created: u64,
}

impl Storable for User {
    // Recommended: prefer Unbounded to avoid backwards compatibility issues when adding new fields.
    // Bounded requires a fixed max_size -- adding a field that increases the size will break existing data.
    const BOUND: Bound = Bound::Unbounded;

    fn to_bytes(&self) -> Cow<'_, [u8]> {
        let mut buf = vec![];
        ciborium::into_writer(self, &mut buf).expect("Failed to encode User");
        Cow::Owned(buf)
    }

    fn into_bytes(self) -> Vec<u8> {
        let mut buf = vec![];
        ciborium::into_writer(&self, &mut buf).expect("Failed to encode User");
        buf
    }

    fn from_bytes(bytes: Cow<'_, [u8]>) -> Self {
        ciborium::from_reader(bytes.as_ref()).expect("Failed to decode User")
    }
}
// Bound::Bounded { max_size, is_fixed_size: true } exists for fixed-size types but is NOT
// recommended -- adding a new field later will exceed max_size and break deserialization.

// Stable storage -- survives upgrades
thread_local! {
    static MEMORY_MANAGER: RefCell<MemoryManager<DefaultMemoryImpl>> =
        RefCell::new(MemoryManager::init(DefaultMemoryImpl::default()));

    static USERS: RefCell<StableBTreeMap<u64, User, Memory>> =
        RefCell::new(StableBTreeMap::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(MemoryId::new(0)))
        ));

    // Counter stored in stable memory via StableCell
    static COUNTER: RefCell<ic_stable_structures::StableCell<u64, Memory>> =
        RefCell::new(ic_stable_structures::StableCell::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(MemoryId::new(1))),
            0u64,
        ));
}

#[init]
fn init() {
    // Any one-time initialization
}

#[post_upgrade]
fn post_upgrade() {
    // Stable structures auto-restore -- no deserialization needed
    // Re-init timers or other transient state here
}

#[update]
fn add_user(name: String) -> u64 {
    let id = COUNTER.with(|c| {
        let mut cell = c.borrow_mut();
        let current = *cell.get();
        cell.set(current + 1);
        current
    });

    let user = User {
        id,
        name,
        created: ic_cdk::api::time(),
    };

    USERS.with(|users| {
        users.borrow_mut().insert(id, user);
    });

    id
}

#[query]
fn get_user(id: u64) -> Option<User> {
    USERS.with(|users| users.borrow().get(&id))
}

#[query]
fn get_user_count() -> u64 {
    USERS.with(|users| users.borrow().len())
}

ic_cdk::export_candid!();
```

#### Multiple Stable Structures with MemoryManager

```rust
use ic_stable_structures::{
    memory_manager::{MemoryId, MemoryManager, VirtualMemory},
    DefaultMemoryImpl, StableBTreeMap, StableCell, StableLog,
};
use std::cell::RefCell;

type Memory = VirtualMemory<DefaultMemoryImpl>;

// Each structure gets its own MemoryId -- NEVER reuse IDs
const USERS_MEM_ID: MemoryId = MemoryId::new(0);
const POSTS_MEM_ID: MemoryId = MemoryId::new(1);
const COUNTER_MEM_ID: MemoryId = MemoryId::new(2);
const LOG_INDEX_MEM_ID: MemoryId = MemoryId::new(3);
const LOG_DATA_MEM_ID: MemoryId = MemoryId::new(4);

thread_local! {
    static MEMORY_MANAGER: RefCell<MemoryManager<DefaultMemoryImpl>> =
        RefCell::new(MemoryManager::init(DefaultMemoryImpl::default()));

    static USERS: RefCell<StableBTreeMap<u64, Vec<u8>, Memory>> =
        RefCell::new(StableBTreeMap::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(USERS_MEM_ID))
        ));

    static POSTS: RefCell<StableBTreeMap<u64, Vec<u8>, Memory>> =
        RefCell::new(StableBTreeMap::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(POSTS_MEM_ID))
        ));

    static COUNTER: RefCell<StableCell<u64, Memory>> =
        RefCell::new(StableCell::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(COUNTER_MEM_ID)),
            0u64,
        ));

    static AUDIT_LOG: RefCell<StableLog<Vec<u8>, Memory, Memory>> =
        RefCell::new(StableLog::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(LOG_INDEX_MEM_ID)),
            MEMORY_MANAGER.with(|m| m.borrow().get(LOG_DATA_MEM_ID)),
        ));
}
```

Key rules for Rust stable structures:
- `MemoryManager` partitions stable memory -- each structure gets a unique `MemoryId`
- NEVER reuse a `MemoryId` for two different structures -- they will corrupt each other
- `StableBTreeMap` keys must implement `Storable` + `Ord`, values must implement `Storable`
- Implement `Storable` for custom types: define `BOUND`, `to_bytes`, `into_bytes`, and `from_bytes`. Use `ciborium::into_writer`/`ciborium::from_reader` for CBOR serialization (compact, fast). Prefer `Bound::Unbounded` -- it avoids backwards compatibility breakage when adding new fields. `Bound::Bounded` exists but is not recommended because exceeding `max_size` after a schema change breaks deserialization
- Primitive types (`u64`, `bool`, `f64`, etc.), `String`, `Vec<u8>`, and `Principal` already implement `Storable` -- no manual impl needed
- `StableCell` for single values (counters, config)
- `StableLog` for append-only logs (needs two memory regions: index + data)
- `thread_local! { RefCell<StableBTreeMap<...>> }` is the correct pattern -- the RefCell wraps the stable structure, not a heap HashMap
- No `pre_upgrade`/`post_upgrade` serialization needed -- data is already in stable memory

## Deploy & Test

### Motoko: Verify Persistence Across Upgrades

```bash
# Start local replica
icp network start -d

# Deploy
icp deploy backend

# Add data
icp canister call backend addUser '("Alice")'
# Expected: (0 : nat)

icp canister call backend addUser '("Bob")'
# Expected: (1 : nat)

# Verify data exists
icp canister call backend getUserCount '()'
# Expected: (2 : nat)

icp canister call backend getUser '(0)'
# Expected: (opt record { id = 0 : nat; name = "Alice"; created = ... })

# Now upgrade the canister (simulates code change + redeploy)
icp deploy backend

# Verify data survived the upgrade
icp canister call backend getUserCount '()'
# Expected: (2 : nat) -- STILL 2, not 0

icp canister call backend getUser '(1)'
# Expected: (opt record { id = 1 : nat; name = "Bob"; created = ... })
```

### Rust: Verify Persistence Across Upgrades

```bash
icp network start -d

icp deploy backend

icp canister call backend add_user '("Alice")'
# Expected: (0 : nat64)

icp canister call backend get_user_count '()'
# Expected: (1 : nat64)

# Upgrade
icp deploy backend

# Verify persistence
icp canister call backend get_user_count '()'
# Expected: (1 : nat64) -- data survived

icp canister call backend get_user '(0)'
# Expected: (opt record { id = 0 : nat64; name = "Alice"; created = ... })
```

## Verify It Works

The definitive test for stable memory: data survives upgrade.

```bash
# 1. Deploy and add data
icp deploy backend
icp canister call backend addUser '("TestUser")'

# 2. Record the count
icp canister call backend getUserCount '()'
# Note the number

# 3. Upgrade (redeploy)
icp deploy backend

# 4. Check count again -- must be identical
icp canister call backend getUserCount '()'
# Must match step 2

# 5. Verify transient data DID reset
icp canister call backend getRequestCount '()'
# Expected: (0 : nat) -- transient var resets on upgrade
```

If the count drops to 0 after step 3, your data is NOT in stable memory. Review your storage declarations.
