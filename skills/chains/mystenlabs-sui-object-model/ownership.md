# Ownership Types and Versioning

Every object on Sui has one of five ownership types. The ownership type determines who can use the object, whether it goes through consensus, and how it behaves in transactions.

## Address-owned objects

Owned by a specific 32-byte address. Only that address can use the object as a transaction input. Created through `transfer::transfer()` or `transfer::public_transfer()`.

Every Sui transaction, including one that touches only address-owned objects, is sequenced by consensus before it executes. Address-owned inputs are referenced at a fixed version, so they need no version assignment from consensus and are not subject to shared-object congestion. Transactions that touch disjoint owned objects execute in parallel. Most transactions on Sui (transfers, personal asset management, single-player game moves) touch only owned objects.

The tradeoff: only one address can use the object, and each transaction must reference the object's current version. If two transactions use the same version, only the first in consensus order executes; the others are rejected and must be rebuilt against the new version. If multiple users need access, use a shared object. If a single owner needs multiple inflight transactions against the same object, use a party object.

> **Current recommendation:** For most new use cases, prefer party objects over address-owned objects. Address-owned objects require the sender to track the current version and allow only one inflight transaction per version, which needs offchain coordination when several transactions or senders use the same object. Party objects let consensus assign versions while still restricting access to a single owner.

## Party objects

Party objects are an ownership form that combines single-address ownership with consensus sequencing. The underlying mechanism is called consensus-address-owned (also called party objects). APIs expose this ownership with a `ConsensusAddressOwner` owner variant.

Party objects are the public Move-facing way to create this ownership form. They are created using `sui::transfer::party_transfer` or `sui::transfer::public_party_transfer`, and use the `sui::party::Party` type (currently restricted to `party::single_owner` for single-address ownership).

Key differences from address-owned:
- **Multiple inflight transactions.** Unlike address-owned objects, which only allow a single inflight transaction per object version, party objects can be used by multiple inflight transactions at the same time. This makes them useful for pipelining multiple transactions against the same object.
- **Consensus-assigned versions.** Consensus assigns the object's version when a transaction uses it, as for shared objects, so the transaction is subject to shared-object scheduling and congestion control.

Key differences from shared objects:
- **Single-address ownership.** Only the owning address can use the object — unlike shared objects which are accessible to anyone.
- **Can be transferred and wrapped.** Party objects can be transferred to and from other ownership types and wrapped inside other objects. Shared objects cannot.
- **Transfer-to-object not supported.** You cannot transfer an object to a party object whose owning address corresponds to an object ID. Transfer-to-object (Receiving) is not supported for party objects.

Use party objects when you want single-owner access control with consensus sequencing, for example to allow multiple inflight transactions against the same logical object without tracking its version. If an object is only used with other party or shared objects, converting it to a party object has no additional performance cost.

## Shared objects

Accessible to any address on the network. Created through `transfer::share_object()` or `transfer::public_share_object()`. Once shared, an object cannot be unshared or converted back to address-owned.

Consensus assigns the versions of shared objects that a transaction uses, and transactions that write the same shared object are serialized and subject to congestion control. Use shared objects when multiple users or modules need to read or write the same state (registries, pools, marketplaces, shared game state).

**Access mode optimization:** When a function takes a shared object by immutable reference (`&`), the system marks it as `mutable: false` and can schedule multiple read-only transactions on that shared object in parallel. When taken by mutable reference (`&mut`) or by value, the system marks it as `mutable: true` and consensus must sequence those transactions. Prefer immutable references on shared objects whenever mutation is not needed.

**Frontend access:** To use a shared object in a transaction from a frontend or CLI, you reference it by its object ID as a transaction input. There is no need to "fetch" or "get" the shared object before including it in a programmable transaction block. Anyone on the network can reference a shared object by ID. Implement access control within your Move functions if needed.

## Immutable (frozen) objects

Cannot be changed, transferred, or deleted. Anyone can read them. Created through `transfer::freeze_object()` or `transfer::public_freeze_object()`. Freezing is permanent and irreversible.

Immutable objects need no version assignment and cannot conflict, since nothing can modify them. For mutable state, the current recommendation is to prefer party objects over address-owned objects for most new use cases. Use immutable objects for reference data, published packages, and constants that never change.

## Wrapped objects

An object stored as a field inside another object. Wrapped objects are not directly accessible by ID; they can only be reached through their parent. While wrapped, the object cannot be passed as a transaction input, even if you know its ID.

When unwrapped, the object regains direct access and retains its original ID.

Wrapping requires the child object to have the `store` ability (so it can be stored inside the parent).

**Same-transaction wrapping and unwrapping:** wrapping and unwrapping can happen within the same transaction. A PTB can wrap an object into a parent and later unwrap it, all atomically.

Use wrapping for tight coupling: when a child should only be accessible through its parent (equipment inside a character, items inside a chest).

## Object versioning

Object versions use Lamport timestamps. When a transaction touches multiple objects, all of them receive the same new version: `1 + max(version of all input objects)`.

Example: if a transaction modifies an object at version 5 using a gas coin at version 3, both the object and the gas coin become version 6.

Only the most recent version is accessible to active transactions. Historical versions are available through versioned ID queries. Each object has a linear version history: exactly one transaction modifies it per version.

### Versioning and ownership

- **Address-owned / immutable objects:** The transaction must use the exact current version as input, and consensus does not assign it. Only one inflight transaction per object version is allowed: if several use the same version, the first in consensus order executes and the rest are rejected. **For most new use cases, prefer party objects** over address-owned objects to avoid the need for offchain coordination.
- **Shared / party objects:** Consensus assigns the version. Enables concurrent access — multiple inflight transactions can touch the same object without tracking its version. Party objects are recommended over address-owned objects for single-owner mutable state.
- **Wrapped objects:** Version increments when the parent is modified, maintaining unique (ID, version) pairs. While wrapped, the object is not directly accessible by version.
- **Dynamic fields:** Version increments when the field is modified, following Lamport timestamps like regular objects.
