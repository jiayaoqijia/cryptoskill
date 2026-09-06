# Building PTBs with the TypeScript SDK

How to construct, sign, serialize, and execute PTBs with `@mysten/sui/transactions`.

Source: https://docs.sui.io/develop/transactions/ptbs/building-ptb · https://sdk.mystenlabs.com/sui/transactions/basics

## Setup

```ts
import { Transaction, Inputs } from '@mysten/sui/transactions';
import { SuiGrpcClient } from '@mysten/sui/grpc';

const tx = new Transaction();
const client = new SuiGrpcClient({
  network: 'mainnet',
  baseUrl: 'https://fullnode.mainnet.sui.io:443',
});
```

## Inputs

### Object inputs

```ts
tx.object(objectId)                     // by string ID; SDK resolves version via RPC
tx.object(Inputs.ObjectRef({            // fully-specified (owned / immutable), offline-buildable
  objectId, version, digest,
}))
tx.object(Inputs.SharedObjectRef({      // fully-specified shared
  objectId, initialSharedVersion, mutable,
}))
tx.object(Inputs.ReceivingRef({         // fully-specified receiving
  objectId, version, digest,
}))

// System object helpers:
tx.object.system()
tx.object.clock()
tx.object.random()
tx.object.denyList()
tx.object.option({ type: '0x123::m::T', value: '0xabc' })  // helper for Option<Object>
```

**When wrapping is required:** for `moveCall` arguments that mix pure and object inputs, always wrap object IDs with `tx.object(id)` so the SDK knows which call-arg kind to emit. Many other methods accept raw string IDs directly.

### Pure inputs

Typed helpers (preferred):
```ts
tx.pure.u8(255)
tx.pure.u16(n) ; tx.pure.u32(n) ; tx.pure.u64(n) ; tx.pure.u128(n) ; tx.pure.u256(n)
tx.pure.bool(true)
tx.pure.address('0x...')
tx.pure.string('hello')
tx.pure.vector('u8', [1, 2, 3])
tx.pure.option('u64', 42)      // Option<u64> = Some(42)
tx.pure.option('u64', null)    // Option<u64> = None
```

Generic form:
```ts
tx.pure('u64', 100)
tx.pure('vector<u8>', [1, 2, 3])
tx.pure('option<u8>', 1)
```

Raw BCS:
```ts
import { bcs } from '@mysten/sui/bcs';
tx.pure(bcs.U64.serialize(100))
tx.pure(bcs.vector(bcs.U8).serialize([1, 2, 3]))
// Or raw Uint8Array — used directly:
tx.pure(new Uint8Array([0, 1, 2]))
```

### The gas coin

`tx.gas` references the `GasCoin` argument. Usage rules:
- Valid as any arg position, but **must be by reference** unless passed to `transferObjects` (value) or used as the source of `splitCoins` (mutable borrow).
- `tx.splitCoins(tx.gas, [tx.pure.u64(amount)])` — most common pattern: derive an owned `Coin<SUI>` from gas.
- `tx.mergeCoins(tx.gas, [tx.object(extra1), tx.object(extra2)])` — consolidate owned SUI into the gas coin before using it.

**`InsufficientCoinBalance` when splitting from gas:** the gas coin must cover both the split amount *and* the gas budget. If the user's gas coin has 0.5 SUI and you split 0.45 SUI, there may not be enough left for gas (~0.01 SUI). The wallet selects gas budget via dry-run, but cannot increase the coin's balance. Surface this error to users with the amount they need and suggest the faucet (testnet) or merging coins.

**Use `BigInt` for large MIST amounts.** When coin amounts come from JSON responses (e.g. a listing price fetched from chain), they parse as `number` or `string`. Always wrap with `BigInt(amount)` to avoid silent precision loss:

```ts
// ✅ Safe for any MIST value
const coins = tx.splitCoins(tx.gas, [BigInt(listing.price)]);
tx.moveCall({ target: '...::buy', arguments: [coins[0]] });

// ⚠️ Risky — JS number precision loss above 2^53
const coins = tx.splitCoins(tx.gas, [listing.price]);
```

## Commands — TS SDK signatures

```ts
tx.splitCoins(coin, amounts)
//   coin:    tx.gas | tx.object(id) | prior result
//   amounts: Arg[] (u64 pure or result)
//   returns: destructurable result (one coin per amount)

tx.mergeCoins(destination, sources)
//   returns: nothing meaningful

tx.transferObjects(objects, recipient)
//   objects:   Arg[]
//   recipient: Arg (address pure or result)

tx.moveCall({
  target: 'pkg::module::function',
  arguments?: Arg[],
  typeArguments?: string[],
})
//   returns: destructurable result (per Move fn signature)

tx.makeMoveVec({ type?: string, elements: Arg[] })
//   type required for empty vectors or non-object element types
//   returns: single vector value

tx.publish({ modules: number[][], dependencies: string[] })
//   returns: UpgradeCap

tx.upgrade({ modules, dependencies, packageId, ticket })
//   returns: UpgradeReceipt

tx.balance({ coinType?: string, owner?: string })
//   returns: a Balance value resolved at build time

tx.coin({ balance, type?: string })
//   wraps a Balance into a Coin object

tx.add(command)
//   appends a raw command object to the transaction
```

## Result chaining

Each command returns a destructurable/indexable result:

```ts
// Single-return: destructure
const [coin] = tx.splitCoins(tx.gas, [tx.pure.u64(100)]);
tx.transferObjects([coin], tx.pure.address(to));

// Single-return: index (equivalent)
const coins = tx.splitCoins(tx.gas, [BigInt(price)]);
tx.moveCall({ target: '...::buy', arguments: [coins[0]] });

// Multi-return: destructure
const [nft1, nft2] = tx.moveCall({ target: '0xpkg::mint::two' });
tx.transferObjects([nft1, nft2], tx.pure.address(to));

// Or index into the result
const minted = tx.moveCall({ target: '0xpkg::mint::two' });
tx.transferObjects([minted[0], minted[1]], tx.pure.address(to));

// Pass the whole result when a single value is expected
const hero = tx.moveCall({ target: '0x123::hero::mint_hero' });
const sword = tx.moveCall({ target: '0x123::hero::new_sword', arguments: [tx.pure.u64(10)] });
tx.moveCall({ target: '0x123::hero::equip_sword', arguments: [hero, sword] });
```

## Sender and gas configuration

```ts
tx.setSender(senderAddress);        // required if building offline or sending kind-only
tx.setGasPrice(gasPrice);           // default: network reference gas price
tx.setGasBudget(gasBudgetMist);     // default: auto (SDK dry-runs and picks)
tx.setGasPayment([                  // default: auto (all coins at sender not used as inputs)
  { objectId, version, digest },
  ...
]);
tx.setGasOwner(sponsorAddress);     // for sponsored txs — gas coins owned by someone else
```

### Defaults — leave them alone when a wallet signs

The SDK:
- Sets `gas price` to the network's reference gas price.
- **Dry-runs the PTB** to auto-derive `gas budget`.
- Selects gas payment coins (all SUI coins at the sender not used as inputs). Multiple coins get merged into the 0-index coin during execution; the others are deleted.

For user-signed transactions in apps, **don't set these** — let the wallet handle it. See "App ↔ wallet handoff" below.

### Batch transfers pattern

```ts
interface Transfer { to: string; amount: number }
const transfers: Transfer[] = getTransfers();

const tx = new Transaction();
const coins = tx.splitCoins(
  tx.gas,
  transfers.map(t => tx.pure.u64(t.amount)),
);
transfers.forEach((t, i) => {
  tx.transferObjects([coins[i]], tx.pure.address(t.to));
});
```

One PTB replaces N transactions — cheaper and atomic.

## Building, serializing, rehydrating

```ts
// Normal build: SDK resolves input versions via RPC
const bytes = await tx.build({ client });

// Kind-only (for sponsored flows — no gas data)
const kindBytes = await tx.build({ client, onlyTransactionKind: true });

// Offline build: all inputs must be fully-specified (Inputs.ObjectRef/SharedObjectRef/ReceivingRef)
// and gas data must be set manually. setSender is required.
const offlineBytes = await tx.build();

// Rehydrate
const tx2 = Transaction.from(bytes);           // full tx
const tx3 = Transaction.fromKind(kindBytes);   // kind-only; set sender + gas data before building
```

## App ↔ wallet handoff — use `toJSON`, not `build`

In frontend code that hands a PTB to a wallet:

```ts
// App code:
const tx = new Transaction();
tx.transferObjects([tx.object(nftId)], tx.pure.address(recipient));
await wallet.signTransaction({ transaction: tx });  // pass Transaction instance

// The wallet adapter internally does:
sendToWalletContext({ transaction: await input.transaction.toJSON() });
// And the wallet does:
const userTx = Transaction.from(input.transaction);
userTx.setSender(walletAddress);
// wallet builds bytes (picks gas, sets budget via dry-run), signs, executes.
```

**Why not `build`:** if the app calls `tx.build()` and hands bytes to the wallet, the wallet cannot do gas coin selection or budget dry-running on the caller's behalf. Use `await tx.toJSON()` (or pass the `Transaction` instance) so the wallet controls gas logic.

## Sponsored transactions

Flow:
1. **App** builds the PTB kind-only.
2. **Sponsor service** rehydrates, fills gas, signs as gas owner.
3. **User** signs as sender.
4. Either party submits the dual-signed bytes (user is safer — submitting via sponsor allows censorship).

```ts
// App:
const tx = new Transaction();
tx.moveCall({ /* ... */ });
const kindBytes = await tx.build({ client, onlyTransactionKind: true });
sendToSponsor(kindBytes);

// Sponsor:
const sponsored = Transaction.fromKind(kindBytes);
sponsored.setSender(userAddress);
sponsored.setGasOwner(sponsorAddress);
sponsored.setGasPayment(sponsorCoins);   // [{ objectId, version, digest }]
const sponsorSigned = await sponsorSigner.signTransaction(sponsored);
sendBackToUser(sponsorSigned);

// User signs (over the same TransactionData, including GasData) and submits.
```

Both parties sign over the **entire TransactionData** including `GasData`. Signing only parts lets a malicious full node substitute gas data.

**Sponsor safety note:** The sender can use `GasCoin` (which belongs to the sponsor) within the PTB — for example, splitting SUI from it or passing it to `transferObjects`. Sponsors should validate the PTB before signing to ensure the gas coin is not drained for non-gas purposes. Reject PTBs that pass `tx.gas` by value to anything other than the final transfer, or use `coinWithBalance` intents instead of raw gas coin access.

## Signing & executing

```ts
const result = await keypair.signAndExecuteTransaction({
  transaction: tx,
  client,
  include: { effects: true, balanceChanges: true, objectTypes: true },
});

if (result.$kind === 'FailedTransaction') {
  throw new Error(`Tx failed: ${result.error}`);
}

// Ensure the RPC you'll read from next has indexed these effects
await client.waitForTransaction({ digest: result.digest });
```

**Always check status.** A transaction can execute (validators accept it) but still fail at the Move level (assertion, insufficient gas budget, etc.). Check `result.$kind === 'FailedTransaction'`.

## Simulating transactions

```ts
// Simulate: full execution against current state, no signature required
const sim = await client.simulateTransaction({
  transaction: tx,
  include: { effects: true, balanceChanges: true },
});
```

Use `client.simulateTransaction` to preview effects, estimate gas, and inspect return values from a view-like Move call without publishing a custom view function.

## Checklist for a PTB ready to ship

- Inputs: either `tx.object(stringId)` (online) or `Inputs.*Ref` (offline); pure values typed.
- No shared object passed to `transferObjects`.
- Every non-`drop` result either consumed or transferred.
- `tx.gas` only by value in `transferObjects`; otherwise `splitCoins`/`mergeCoins`/borrow.
- Multi-return `moveCall` results destructured or indexed.
- For user-signed flows: no `setGasBudget`/`setGasPrice`/`setGasPayment`, no `tx.build()` before handing to wallet — use `await tx.toJSON()` or pass the `Transaction` directly.
- For sponsored flows: `build({ onlyTransactionKind: true })` → sponsor `setSender`/`setGasOwner`/`setGasPayment` → both signatures over full `TransactionData`.
- **Check `result.$kind` after execution.** A transaction can be accepted by validators but still fail at the Move level. Never treat a transfer (or any operation) as successful without checking `result.$kind === 'FailedTransaction'`.
- `waitForTransaction` before reading mutated state from the same client.
