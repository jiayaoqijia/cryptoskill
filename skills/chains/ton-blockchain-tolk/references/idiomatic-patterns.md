# Idiomatic Tolk Contract Patterns

Use this reference for implementing or reviewing Tolk contract code.

## Table of Contents

- Project layout
- Storage
- Message schemas
- Internal messages
- Bounced messages
- External messages
- Outgoing messages and deployment
- Getters
- Maps
- Serialization boundaries
- Standard contract families

## Project Layout

Prefer a small set of focused files:

- `contracts/errors.tolk`: error constants or enums.
- `contracts/messages.tolk`: incoming and outgoing message structs, opcodes, payload aliases, and union types.
- `contracts/storage.tolk`: persistent storage structs and `load/save` helpers.
- `contracts/*-contract.tolk`: entrypoints, getters, validation, state transitions, and sends.
- `tests/*`: integration tests and helper wrappers according to the project's framework.
- `scripts/*`: deployment or operational flows if the project already uses scripts.

Keep shared message/storage types importable without importing an entrypoint file. This avoids duplicate reserved entrypoint definitions in tests, wrappers, or multi-contract projects.

## Storage

Use persistent storage as a struct and wrap raw data access:

```tolk
struct Storage {
    ownerAddress: address
    seqno: uint32
    balance: coins
}

fun Storage.load() {
    return Storage.fromCell(contract.getData())
}

fun Storage.save(self) {
    contract.setData(self.toCell())
}
```

Use `lazy Storage.load()` when only a subset of fields is needed:

```tolk
get fun currentOwner(): address {
    val storage = lazy Storage.load();
    return storage.ownerAddress;
}
```

For storage with multiple valid shapes, model the shapes explicitly. Start from a loader struct or slice, inspect remaining bits/refs, then parse the exact shape:

```tolk
struct ItemStorage {
    itemIndex: uint64
    collectionAddress: address
    ownerAddress: address
    content: cell
}

struct ItemStorageNotInitialized {
    itemIndex: uint64
    collectionAddress: address
}

struct ItemStorageLoader {
    itemIndex: uint64
    collectionAddress: address
    private rest: RemainingBitsAndRefs
}

fun ItemStorage.startLoading() {
    return ItemStorageLoader.fromCell(contract.getData())
}

fun ItemStorageLoader.isInitialized(self) {
    return !self.rest.isEmpty()
}

fun ItemStorageLoader.endLoading(mutate self): ItemStorage {
    return {
        itemIndex: self.itemIndex,
        collectionAddress: self.collectionAddress,
        ownerAddress: self.rest.loadAny(),
        content: self.rest.loadAny(),
    }
}
```

## Message Schemas

Represent message bodies as structs. Use 32-bit prefixes for opcode-bearing messages:

```tolk
struct (0x12345678) Increment {
    queryId: uint64
    amount: uint32
}

struct (0x23456789) Reset {
    queryId: uint64
    value: uint32
}

type AllowedMessage = Increment | Reset
```

Use the narrowest correct types:

- `address` for required internal addresses.
- `address?` for optional internal addresses.
- `any_address` or `any_address?` when the contract intentionally accepts broader address encodings.
- `Cell<T>` when the payload is a typed ref.
- `cell` when a ref is intentionally opaque.
- `RemainingBitsAndRefs` when the schema includes "the rest of the slice".
- Fixed-width `intN`/`uintN` or `coins` inside serialized structs, not unbounded `int`.

Use custom serializers for domain encodings that do not fit built-in types:

```tolk
type MetadataTail = slice

fun MetadataTail.unpackFromSlice(mutate s: slice) {
    val rest = s;
    s = createEmptySlice();
    return rest
}

fun MetadataTail.packToBuilder(self, mutate b: builder) {
    b.storeSlice(self)
}
```

## Internal Messages

Use `InMessage`, lazy union parsing, and `match`:

```tolk
fun onInternalMessage(in: InMessage) {
    val msg = lazy AllowedMessage.fromSlice(in.body);

    match (msg) {
        Increment => {
            var storage = lazy Storage.load();
            assert (in.senderAddress == storage.ownerAddress) throw ERR_NOT_OWNER;
            storage.balance += msg.amount;
            storage.save();
        }
        Reset => {
            var storage = lazy Storage.load();
            assert (in.senderAddress == storage.ownerAddress) throw ERR_NOT_OWNER;
            storage.balance = msg.value;
            storage.save();
        }
        else => {
            assert (in.body.isEmpty()) throw 0xFFFF
        }
    }
}
```

Choose the unknown-message policy deliberately. Empty internal messages are commonly balance top-ups; non-empty unknown messages are usually rejected.

## Bounced Messages

Use `onBouncedMessage` for bounce-specific state repair:

```tolk
type BounceableMessage = TransferOut | MintOut

fun onBouncedMessage(in: InMessageBounced) {
    in.bouncedBody.skipBouncedPrefix();
    val msg = lazy BounceableMessage.fromSlice(in.bouncedBody);

    match (msg) {
        TransferOut => {
            var storage = lazy Storage.load();
            storage.balance += msg.amount;
            storage.save();
        }
        else => {}
    }
}
```

Pick one bounce mode family where possible:

- `BounceMode.NoBounce` for messages that should not return on failure.
- `BounceMode.Only256BitsOfBody` for low-cost bounce recovery when the needed fields fit.
- `BounceMode.RichBounce` or `RichBounceOnlyRootCell` when recovery needs richer failure data.

## External Messages

External messages originate off-chain and have limited initial gas. Validate signatures, expiration, replay state, and message shape before accepting external gas:

```tolk
fun onExternalMessage(inMsg: slice) {
    val request = lazy SignedRequest.fromSlice(inMsg);
    assert (request.validUntil > blockchain.now()) throw ERR_EXPIRED;
    assert (checkSignature(request)) throw ERR_BAD_SIGNATURE;

    acceptExternalMessage();

    var storage = lazy Storage.load();
    assert (request.seqno == storage.seqno) throw ERR_INVALID_SEQNO;
    storage.seqno += 1;
    storage.save();
}
```

For replay-sensitive flows, persist replay state before sending outbound actions when the design requires it.

## Outgoing Messages And Deployment

Prefer `createMessage({ ... })` and pass typed bodies directly:

```tolk
val reply = createMessage({
    bounce: BounceMode.NoBounce,
    dest: in.senderAddress,
    value: 0,
    body: Reset {
        queryId: msg.queryId,
        value: 0,
    }
});
reply.send(SEND_MODE_CARRY_ALL_REMAINING_MESSAGE_VALUE);
```

Do not convert a typed body to a cell unless the receiving format specifically requires a ref:

```tolk
// Prefer this.
body: SomeMessage { queryId }

// Use this only when the schema requires a cell body/ref.
body: SomeMessage { queryId }.toCell()
```

Extract deploy address/state construction into a helper:

```tolk
fun calcDeployedChild(ownerAddress: address, childCode: cell): AutoDeployAddress {
    val initialStorage: ChildStorage = {
        ownerAddress,
        value: 0,
    };

    return {
        stateInit: {
            code: childCode,
            data: initialStorage.toCell(),
        }
    }
}
```

For shard-sensitive deployments, use `toShard` with a documented reason:

```tolk
dest: {
    stateInit: { code, data },
    toShard: {
        closeTo: ownerAddress,
        fixedPrefixLength: 8,
    }
}
```

Use `UnsafeBodyNoRef` only when direct inline-body encoding is required and the body is known to fit.

## Getters

Prefer explicit return types. Use standard getter names when a standard defines them; otherwise use camelCase.

```tolk
struct ContractDataReply {
    ownerAddress: address
    balance: coins
    code: cell
}

get fun contractData(): ContractDataReply {
    val storage = lazy Storage.load();
    return {
        ownerAddress: storage.ownerAddress,
        balance: storage.balance,
        code: contract.getCode(),
    }
}
```

Getter reply structs make wrappers and off-chain clients easier to audit.

## Maps

Use typed maps instead of low-level dictionary operations in core logic:

```tolk
type ReplayMap = map<uint64, bool>

struct Storage {
    processed: ReplayMap = []
}

fun Storage.markProcessed(mutate self, queryId: uint64) {
    assert (!self.processed.exists(queryId)) throw ERR_REPLAY;
    self.processed.set(queryId, true);
}
```

Map lookup returns a result object:

```tolk
val r = storage.records.get(key);
if (r.isFound) {
    val record = r.loadValue();
}
```

Do not check map lookup with `== null`. Use `isFound`, `mustGet`, `exists`, `isEmpty`, and iteration helpers such as `findFirst` and `iterateNext`.

When a low-level dictionary enters from a boundary API, convert once:

```tolk
val records = createMapFromLowLevelDict<uint256, Cell<Record>>(rawDict);
```

## Serialization Boundaries

Use auto-serialization first. Reach for manual builders/slices only for:

- custom TL-B shapes not expressible with built-in types;
- validation of a raw external payload;
- precise inline/ref control;
- opaque pass-through data;
- low-level blockchain configuration or proof structures.

Common checks:

- Serialized structs must fit 1023 bits or split large/infrequent fields into `Cell<T>`.
- Optional values carry explicit markers; do not use nullable fields to represent absent trailing fields.
- `fromSlice` asserts end by default. Disable end assertion only when a remainder is intentionally accepted.
- `bitsN`/`bytesN` are useful for fixed-size binary data.

## Standard Contract Families

When implementing standard interfaces, read the standard first and preserve its public shape:

- Jettons: `https://docs.ton.org/standard/tokens/jettons/api`
- NFTs: `https://docs.ton.org/standard/tokens/nft/api`
- Wallet V5: `https://docs.ton.org/standard/wallets/v5-api`
- Vesting: `https://docs.ton.org/standard/vesting`

Typical family-specific patterns:

- Jettons: separate minter/wallet storage, wallet address calculation helper, typed transfer/burn/notification/excess messages, bounce restoration for supply or balances, forward payload as a remainder type.
- NFTs: collection/item split, explicit uninitialized item storage, royalty/getter reply structs, batch deploy map iteration with action-list limits.
- Wallets: external signature validation, expiration, replay state, action validation, and commit/persist ordering.
- Vesting/multisig/policy contracts: typed allowlists as maps, clear authorization methods, explicit time and seqno checks.
