# Ownership Types and Versioning

Every object on Sui has one of five ownership types. The ownership type determines who can use the object, whether it goes through consensus, and how it behaves in transactions.

## Address-owned objects

Owned by a specific 32-byte address. Only that address can use the object as a transaction input. Created through `transfer::transfer()` or `transfer::public_transfer()`.

Transactions touching only address-owned objects use a **fastpath that does not require consensus ordering** — validators can certify them directly because only one address can use the object, so there are no ordering conflicts. This gives owned-object transactions the lowest latency and highest throughput. Most transactions on Sui (transfers, personal asset management, single-player game moves) touch only owned objects and execute in parallel.

The tradeoff: only one address can use the object, and only one inflight transaction per object version is allowed. If multiple users need access, use a shared object. If a single owner needs multiple inflight transactions against the same object, use a party object.

> **Current recommendation:** For most new use cases, prefer party objects over fastpath address-owned objects. Fastpath objects carry equivocation risk (if two transactions try to use the same owned object concurrently, the object can be locked) and require offchain coordination for concurrent access by multiple senders. Party objects avoid these issues by going through consensus while still restricting access to a single owner.

## Party objects

Party objects are an ownership form that combines single-address ownership with consensus sequencing. The underlying mechanism is called consensus-address-owned (also called party objects). APIs expose this ownership with a `ConsensusAddressOwner` owner variant.

Party objects are the public Move-facing way to create this ownership form. They are created using `sui::transfer::party_transfer` or `sui::transfer::public_party_transfer`, and use the `sui::party::Party` type (currently restricted to `party::single_owner` for single-address ownership).

Key differences from address-owned:
- **Multiple inflight transactions.** Unlike address-owned objects, which only allow a single inflight transaction per object version, party objects can be used by multiple inflight transactions at the same time. This makes them useful for pipelining multiple transactions against the same object.
- **Consensus sequencing.** Transactions are ordered through consensus, not the fastpath. This adds latency compared to address-owned objects.

Key differences from shared objects:
- **Single-address ownership.** Only the owning address can use the object — unlike shared objects which are accessible to anyone.
- **Can be transferred and wrapped.** Party objects can be transferred to and from other ownership types and wrapped inside other objects. Shared objects cannot.
- **Transfer-to-object not supported.** You cannot transfer an object to a party object whose owning address corresponds to an object ID. Transfer-to-object (Receiving) is not supported for party objects.

Use party objects when you want single-owner access control with consensus sequencing, for example to allow multiple inflight transactions against the same logical object without fastpath version locking. If an object is only used with other party or shared objects, converting it to a party object has no additional performance cost.

## Shared objects

Accessible to any address on the network. Created through `transfer::share_object()` or `transfer::public_share_object()`. Once shared, an object cannot be unshared or converted back to address-owned.

Shared objects require consensus ordering through Mysticeti. This adds latency and gas cost compared to owned objects. Use shared objects when multiple users or modules need to read or write the same state (registries, pools, marketplaces, shared game state).

**Access mode optimization:** When a function takes a shared object by immutable reference (`&`), the system marks it as `mutable: false` and can schedule multiple read-only transactions on that shared object in parallel. When taken by mutable reference (`&mut`) or by value, the system marks it as `mutable: true` and consensus must sequence those transactions. Prefer immutable references on shared objects whenever mutation is not needed.

**Frontend access:** To use a shared object in a transaction from a frontend or CLI, you reference it by its object ID as a transaction input. There is no need to "fetch" or "get" the shared object before including it in a programmable transaction block. Anyone on the network can reference a shared object by ID. Implement access control within your Move functions if needed.

## Immutable (frozen) objects

Cannot be changed, transferred, or deleted. Anyone can read them. Created through `transfer::freeze_object()` or `transfer::public_freeze_object()`. Freezing is permanent and irreversible.

Immutable objects also skip consensus (like owned objects). However, for mutable state, the current recommendation is to prefer party objects over fastpath address-owned objects for most new use cases. Use immutable objects for reference data, published packages, and constants that never change.

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

- **Address-owned / immutable objects:** Skip consensus entirely (fastpath). The transaction must use the exact current version as input, and only one inflight transaction per object version is allowed. **For most new use cases, prefer party objects** over fastpath address-owned objects to avoid equivocation risk and the need for offchain coordination.
- **Shared / party objects:** Sequenced through full consensus ordering. Enables concurrent access — multiple inflight transactions can touch the same object without version locking issues. Party objects are recommended over fastpath for single-owner mutable state.
- **Wrapped objects:** Version increments when the parent is modified, maintaining unique (ID, version) pairs. While wrapped, the object is not directly accessible by version.
- **Dynamic fields:** Version increments when the field is modified, following Lamport timestamps like regular objects.
