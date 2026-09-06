# Sui TypeScript SDK (`@mysten/sui` v2)

Source: https://sdk.mystenlabs.com/sui · https://sdk.mystenlabs.com/typescript

Install:
```bash
npm install @mysten/sui
```

**Never** `npm install @mysten/sui.js` — frozen at v1.

All imports use subpath exports:
```ts
import { Transaction } from '@mysten/sui/transactions';
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { SuiGrpcClient } from '@mysten/sui/grpc';
```

## Clients (v2)

Three client classes, all requiring explicit `network`:

```ts
// Recommended — gRPC, best performance, typed protobuf
import { SuiGrpcClient } from '@mysten/sui/grpc';
const client = new SuiGrpcClient({
  network: 'mainnet',
  baseUrl: 'https://fullnode.mainnet.sui.io:443',
});

// Legacy — JSON-RPC, still widely deployed
import { SuiJsonRpcClient, getJsonRpcFullnodeUrl } from '@mysten/sui/jsonRpc';
const client = new SuiJsonRpcClient({
  network: 'mainnet',
  url: getJsonRpcFullnodeUrl('mainnet'),
});

// Specialized — GraphQL queries
import { SuiGraphQLClient } from '@mysten/sui/graphql';
const gql = new SuiGraphQLClient({
  network: 'mainnet',
  url: 'https://graphql.mainnet.sui.io/graphql',
});
```

### Network URLs

| Network | gRPC | GraphQL | JSON-RPC helper |
|---|---|---|---|
| Mainnet | `https://fullnode.mainnet.sui.io:443` | `https://graphql.mainnet.sui.io/graphql` | `getJsonRpcFullnodeUrl('mainnet')` |
| Testnet | `https://fullnode.testnet.sui.io:443` | `https://graphql.testnet.sui.io/graphql` | `getJsonRpcFullnodeUrl('testnet')` |
| Devnet | `https://fullnode.devnet.sui.io:443` | `https://graphql.devnet.sui.io/graphql` | `getJsonRpcFullnodeUrl('devnet')` |

### Which client to use

- **New code**: `SuiGrpcClient`. Typed protobuf, best throughput, active surface.
- **Existing v1 migration / JSON-RPC-only infra**: `SuiJsonRpcClient` (legacy — JSON-RPC is deprecated; use only when migrating from v1 or talking to infrastructure that only exposes JSON-RPC).
- **Complex relational queries**: `SuiGraphQLClient` alongside one of the above.
- **All clients share the v2 Core API.** User/application code should call top-level methods (`client.getBalance()`). The `client.core.*` accessor is for SDK/library code that accepts `ClientWithCoreApi` and must work with any transport. See `sui-ts-docs-patterns` skill for details.

### gRPC service clients (low-level)

`SuiGrpcClient` exposes typed services:

```ts
await client.transactionExecutionService.executeTransaction({ ... });
await client.ledgerService.getObject({ objectId: '0x...' });
await client.movePackageService.getFunction({
  packageId: '0x2', moduleName: 'coin', name: 'transfer',
});
await client.nameService.reverseLookupName({ address: '0x...' });
```

## Transactions

```ts
import { Transaction } from '@mysten/sui/transactions';
const tx = new Transaction();
```

Pure inputs — always typed:
```ts
tx.pure.u8(255); tx.pure.u16(n); tx.pure.u32(n); tx.pure.u64(n);
tx.pure.u128(n); tx.pure.u256(n);
tx.pure.bool(true); tx.pure.string('hello');
tx.pure.address('0x...'); tx.pure.id('0x...');
tx.pure.vector('u64', [100n, 200n]);
tx.pure.option('u64', 42n);  // null for None
```

Objects — let the SDK resolve versions:
```ts
tx.object('0x...');
tx.object.system();    // 0x5
tx.object.clock();     // 0x6
tx.object.random();    // 0x8
tx.object.denyList();  // 0x403
tx.object.option({ type: '0xpkg::m::T', value: '0x...' });
```

### Coins and balances (recommended)

`tx.coin()` and `tx.balance()` are the **recommended** methods. They automatically draw from both coin objects and address balances, preferring address balances to avoid versioned object dependencies.

```ts
// Get a Coin<T> for transfers
tx.transferObjects([tx.coin({ balance: 1_000_000_000n })], recipient);

// Non-SUI coin type
tx.transferObjects(
  [tx.coin({ balance: 1_000_000n, type: '0xPkg::module::USDC' })],
  recipient,
);

// Get a Balance<T> for Move function arguments
tx.moveCall({
  target: '0xPkg::module::deposit',
  arguments: [tx.object('0xPool'), tx.balance({ balance: 1_000_000_000n })],
});

// Send to address balance (preferred for payments)
tx.moveCall({
  target: '0x2::balance::send_funds',
  typeArguments: ['0x2::sui::SUI'],
  arguments: [tx.balance({ balance: 1_000_000_000n }), tx.pure.address(recipient)],
});
```

Options: `{ balance: bigint, type?: string, useGasCoin?: boolean }`. Default type is SUI. Set `useGasCoin: false` for sponsored transactions.

`coinWithBalance()` is a standalone alias for `tx.coin()`:
```ts
import { coinWithBalance } from '@mysten/sui/transactions';
tx.transferObjects([coinWithBalance({ balance: 1_000_000 })], recipient);
```

`setSender` is mandatory for non-SUI types — the SDK needs the sender to resolve owned coins during build.

### Manual commands (low-level)

```ts
const [coin] = tx.splitCoins(tx.gas, [1000]);  // low-level; prefer tx.coin() above
tx.mergeCoins(tx.object('0xDest'), [tx.object('0xSrc')]);
tx.transferObjects([coin], '0x...');
tx.moveCall({
  target: '0xpkg::module::fn',
  arguments: [tx.object(poolId), coin, tx.pure.string('x')],
  typeArguments: ['0x2::sui::SUI'],
});
const vec = tx.makeMoveVec({ type: '0xpkg::m::T', elements: [tx.object('0xA')] });
const [upgradeCap] = tx.publish({ modules, dependencies });
```

For deeper PTB semantics (equivocation, hot-potato cliques, sponsored), load the `ptbs` skill.

## v2 Data Access

### Top-level methods (user/application code)

When using a concrete client like `SuiGrpcClient`, call methods directly:

```ts
await client.getObject({ objectId, include: { content: true } });
await client.getObjects({ objectIds: [...], include: { content: true } });
await client.listOwnedObjects({ owner, type: '0xpkg::nft::NFT', limit: 50 });
await client.listCoins({ owner, coinType, limit: 50 });
await client.listBalances({ owner });
await client.getBalance({ owner, coinType: '0x2::sui::SUI' });
await client.listDynamicFields({ parentId, limit: 50 });
await client.getDynamicField({ parentId, name });
await client.getCoinMetadata({ coinType });
await client.getTransaction({ digest, include: {...} });
await client.waitForTransaction({ digest, include: {...} });
await client.simulateTransaction({ transaction: tx });
await client.executeTransaction({ transaction: bytes, signatures: [...], include: {...} });
```

### Core API (SDK/library code only)

When building an SDK that must work with any transport, accept `ClientWithCoreApi` and use `client.core.*`:

```ts
import type { ClientWithCoreApi } from '@mysten/sui/client';

class MySDK {
  constructor(private client: ClientWithCoreApi) {}
  async getItem(id: string) {
    return this.client.core.getObject({ objectId: id, include: { content: true } });
  }
}
```

**Do not use `client.core.*` in documentation examples, application code, or scripts.** It is for SDK internals only.

### Pagination and include options

Pagination: `list*` methods return a single nullable `cursor`. Iterate while non-null, passing it back as the next call's `cursor`.

**Include options** (replaces v1's `options: { show*: true }`). Keys differ by method:
- Object reads (`getObject`, `getObjects`, `listOwnedObjects`): `content`, `previousTransaction`, `json`, `objectBcs`, `display`.
- Transaction reads (`getTransaction`, `waitForTransaction`): `effects`, `events`, `balanceChanges`, `transaction`, `bcs`.
- Simulation (`simulateTransaction`): adds `commandResults`.

## Execution

```ts
const result = await client.signAndExecuteTransaction({
  signer: keypair,
  transaction: tx,
});

// Wait BEFORE error handling to ensure finality
await client.waitForTransaction(result);

if (result.$kind === 'FailedTransaction') {
  // Onchain, gas charged, Move execution aborted. Do NOT retry.
  throw new Error(`Failed: ${result.FailedTransaction.effects.status.error}`);
}

// Success — safe to query updated state
```

Execution response shape uses a `$kind` discriminant: `'Transaction' | 'FailedTransaction'`. **Do not** rely on v1's `result.effects?.status?.status`.

A `FailedTransaction` **is** onchain — the sender was charged gas and the tx has effects. It is NOT the same as "never seen by network." Always distinguish:
1. `Transaction` — succeeded with intended effects
2. `FailedTransaction` — onchain, gas charged, Move execution aborted
3. Exception/not found — transaction never seen by the network

For sponsored or multi-sig, split sign and execute:

```ts
const { bytes, signature } = await tx.sign({ client, signer: keypair });
const result = await client.executeTransaction({
  transaction: bytes,
  signatures: [signature],
  include: { effects: true },
});
```

## Keypairs

```ts
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { Secp256k1Keypair } from '@mysten/sui/keypairs/secp256k1';
import { Secp256r1Keypair } from '@mysten/sui/keypairs/secp256r1';

const kp = new Ed25519Keypair();
const kp2 = Ed25519Keypair.deriveKeypair('mnemonic words ...');
const kp3 = Ed25519Keypair.fromSecretKey(secretKeyBytes);
const addr = kp.toSuiAddress();
```

## Extensions — `client.$extend(...)` (v2)

Ecosystem packages integrate via `$extend`:

```ts
import { SuiGrpcClient } from '@mysten/sui/grpc';
import { suins } from '@mysten/suins';
import { deepbook } from '@mysten/deepbook-v3';

const client = new SuiGrpcClient({
  network: 'mainnet',
  baseUrl: 'https://fullnode.mainnet.sui.io:443',
}).$extend(suins(), deepbook({ address: myAddress }));

await client.suins.getNameRecord('example.sui');
await client.deepbook.checkManagerBalance(manager, asset);
```

Known extensions: `@mysten/suins`, `@mysten/deepbook-v3`, `@mysten/kiosk`, `@mysten/walrus`, `@mysten/seal`, `@mysten/zksend`.

**Not** an extension: `@mysten/dapp-kit` (React-only frontend framework — see `frontend-apps` skill).

## Offline building

```ts
import { Transaction, Inputs } from '@mysten/sui/transactions';

const tx = new Transaction();
tx.object(Inputs.ObjectRef({ objectId, version, digest }));
tx.object(Inputs.SharedObjectRef({ objectId, initialSharedVersion, mutable: true }));
tx.object(Inputs.ReceivingRef({ objectId, version, digest }));

tx.setSender('0x...');
tx.setGasPrice(1000);
tx.setGasBudget(10_000_000);
tx.setGasPayment([{ objectId, version, digest }]);

const bytes = await tx.build();
```

## v1 → v2 migration (abridged)

Full migration guide: fetch `https://sdk.mystenlabs.com/sui/migrations/sui-2.0/llms.txt` for the complete list.

**Migration rule:** when migrating a v1 snippet, do not migrate only the lines visible. v1 codebases almost always also use the execution / waiting / status APIs even if not shown. Surface the full set of likely-related migrations (signing, waiting, status check, options→include) alongside the migrated snippet so the user can update the rest of their file in one pass. A "complete" migration that leaves `signAndExecuteTransactionBlock` or `result.effects?.status?.status` intact elsewhere in the project is a half-migration that will break.

| v1 | v2 |
|---|---|
| `@mysten/sui.js` | `@mysten/sui` |
| `TransactionBlock` | `Transaction` |
| `SuiClient` + `getFullnodeUrl` | `SuiGrpcClient` + `baseUrl` (or `SuiJsonRpcClient` + `getJsonRpcFullnodeUrl`) |
| `client.getObject({ id, options: {...} })` | `client.getObject({ objectId, include: {...} })` |
| `client.getOwnedObjects` | `client.listOwnedObjects` |
| `client.getCoins` | `client.listCoins` |
| `client.getDynamicFields` | `client.listDynamicFields` |
| `client.signAndExecuteTransactionBlock` | `client.signAndExecuteTransaction` |
| `client.waitForTransactionBlock` | `client.waitForTransaction` |
| `client.devInspectTransactionBlock` | `client.simulateTransaction` |
| `client.executeTransactionBlock` | `client.executeTransaction` |
| `options: { showEffects: true }` | `include: { effects: true }` (always show this pattern explicitly — do not omit it by saying effects are returned by default) |
| `result.effects?.status?.status === 'success'` | `result.$kind !== 'FailedTransaction'` |
| `txb.pure(value)` untyped | `tx.pure.u64(value)` / typed helpers |
| `tx.serialize()` | `await tx.toJSON()` |
| `namedPackagesPlugin` | built-in (MVR auto-resolution) |
| direct `new SuinsClient(...)` | `client.$extend(suins())` |
| `Commands` | `TransactionCommands` |
| `graphql/schemas/latest` | `graphql/schema` |

### ESM required

All `@mysten/*` packages are ESM-only:
```json
// package.json
{ "type": "module" }

// tsconfig.json
{ "compilerOptions": { "moduleResolution": "NodeNext", "module": "NodeNext" } }
```

## Common mistakes

### v1 holdovers

| Wrong | Right |
|---|---|
| `import { ... } from '@mysten/sui.js'` | `import { ... } from '@mysten/sui'` |
| `new TransactionBlock()` | `new Transaction()` |
| `client.signAndExecuteTransactionBlock(...)` | `client.signAndExecuteTransaction(...)` |
| `SuiClient` | `SuiGrpcClient` (or `SuiJsonRpcClient`) |
| Hardcoding `tx.object(Inputs.ObjectRef({ version, digest }))` for online code | `tx.object('0x...')` — let SDK resolve |
| `tx.pure(100)` untyped | `tx.pure.u64(100)` |
| Not checking `result.$kind` | Always check for `'FailedTransaction'` |
| `coinWithBalance(type=non-SUI)` without `tx.setSender` | Always call `tx.setSender(addr)` first for non-SUI |

### v2 mistakes

| Wrong | Right |
|---|---|
| `client.core.getBalance(...)` in user code | `client.getBalance(...)` — `.core` is for SDK internals only |
| `tx.splitCoins(tx.gas, [amount])` + `tx.transferObjects` | `tx.coin({ balance: amount })` or `tx.balance({ balance: amount })` |
| `new Ed25519Keypair()` then signing transactions | `Ed25519Keypair.fromSecretKey(process.env.KEY!)` — random keys are unfunded |
| Error handling before `waitForTransaction` | Call `waitForTransaction(result)` first, then check `$kind` |
| `TransactionDataBuilder.fromBytes(bytes)` | `Transaction.from(bytes)` — `TransactionDataBuilder` is internal |
| `sponsor.signAndExecuteTransaction({ signature })` | Parameter is `userSignature`, not `signature` |
| Treating `FailedTransaction` as "not onchain" | It IS onchain, gas was charged, has effects. Do not retry. |
| `splitCoins(tx.gas, ...)` in sponsored tx | Use `tx.coin({ balance, useGasCoin: false })` |
