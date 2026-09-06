# Querying on-chain data in dApps

TanStack React Query + `useCurrentClient`. `useSuiClientQuery` / `useSuiClientInfiniteQuery` are **removed** — don't look for them.

## Basic query

```tsx
import { useCurrentClient, useCurrentAccount } from '@mysten/dapp-kit-react';
import { useQuery } from '@tanstack/react-query';

function Balance() {
  const client = useCurrentClient();
  const account = useCurrentAccount();

  const { data, isPending, error } = useQuery({
    queryKey: ['balance', account?.address, '0x2::sui::SUI'],
    queryFn: () =>
      client.core.listBalances({ owner: account!.address }),
    enabled: !!account,          // ← crucial — skip until connected
  });

  if (isPending) return <Spinner />;
  if (error) return <Error message={error.message} />;

  const sui = data.find((b) => b.coinType === '0x2::sui::SUI');
  return <p>{Number(sui?.totalBalance ?? 0n) / 1e9} SUI</p>;
}
```

**Always `enabled: !!account`** for queries that require an owner. Without it, the query fires with `undefined` and errors.

## Paginated queries

`client.core.list*` methods return a single nullable `cursor` field — iterate while it's non-null. The response shape also contains the results under a method-specific key: `objects` for `listOwnedObjects`, `coins` for `listCoins`, `dynamicFields` for `listDynamicFields`, etc. Use TanStack's `useInfiniteQuery`:

```tsx
import { useCurrentClient, useCurrentAccount } from '@mysten/dapp-kit-react';
import { useInfiniteQuery } from '@tanstack/react-query';

function OwnedNFTs() {
  const client = useCurrentClient();
  const account = useCurrentAccount();

  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery({
    queryKey: ['owned-nfts', account?.address],
    queryFn: ({ pageParam }) =>
      client.core.listOwnedObjects({
        owner: account!.address,
        cursor: pageParam,
        type: '0xPKG::nft::NFT',   // type filter — use the ORIGINAL package ID (see note below)
        include: { json: true },    // json gives parsed fields; content gives raw BCS bytes
        limit: 50,
      }),
    initialPageParam: undefined,
    // v2 returns null (not undefined) when there are no more pages; coerce to undefined so TanStack Query stops paginating.
    getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    enabled: !!account,
  });

  const all = data?.pages.flatMap((p) => p.objects) ?? [];
  return (
    <>
      {all.map((o) => <NFTCard key={o.objectId} object={o} />)}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? 'Loading…' : 'Load more'}
        </button>
      )}
    </>
  );
}
```

## Core API methods (v2) — what you'll query

All hang off `client.core`:

| Method | Returns |
|---|---|
| `getObject({ objectId, include })` | `{ object }` |
| `getObjects({ objectIds, include })` | `{ objects }` — elements can be `Object` or `Error` (see note below) |
| `listOwnedObjects({ owner, type?, cursor?, limit?, include? })` | `{ objects, cursor }` |
| `listCoins({ owner, coinType?, cursor?, limit? })` | `{ coins, cursor }` |
| `listBalances({ owner })` | `{ balances }` |
| `listDynamicFields({ parentId, cursor?, limit? })` | `{ dynamicFields, cursor }` |
| `getDynamicField({ parentId, name })` | `{ dynamicField }` |
| `getCoinMetadata({ coinType })` | `{ coinMetadata }` |
| `getTransaction({ digest, include })` | `{ Transaction, FailedTransaction }` |
| `simulateTransaction({ transaction, include })` | simulation result |

**Include options** — keys differ by method:
- **Objects**: `content`, `previousTransaction`, `json`, `objectBcs`, `display`.
- **Transactions**: `effects`, `events`, `balanceChanges`, `transaction`, `bcs`.
- **Simulate**: adds `commandResults`.

## Reading object fields

Use `include: { json: true }` to get a JSON representation of the object's Move struct fields. Access fields via `obj.json`:

```tsx
const result = await client.core.listOwnedObjects({
  owner: account!.address,
  type: `${PACKAGE_ID}::nft::NFT`,
  include: { json: true },
});

for (const obj of result.objects) {
  const json = obj.json as Record<string, string>;
  console.log(json.name, json.description, json.image_url);
}
```

Alternatively, use `include: { content: true }` to get raw BCS bytes and parse with generated types (from `@mysten/codegen`). `json` is easier for quick access; `content` is more reliable across API implementations.

### `getObjects` returns `(Object | Error)[]`

When batch-fetching with `getObjects`, individual entries can be `Error` instances (e.g. if an object was deleted or the ID is invalid). Always narrow the type before accessing fields:

```ts
const { objects } = await client.core.getObjects({
  objectIds: ids,
  include: { json: true },
});

const valid = objects
  .filter((o): o is Exclude<typeof o, Error> => !(o instanceof Error) && !!o.json)
  .map((o) => ({
    objectId: o.objectId,
    name: String((o.json as Record<string, unknown>).name ?? ''),
  }));
```

Without this guard, TypeScript will error on `o.json` and `o.objectId` because `Error` has neither property.

**Type anchoring after upgrades:** when filtering by type in `listOwnedObjects`, always use the **original** package ID where the struct was first published — not the upgraded package ID. Struct types are permanently anchored to the original package. Use the upgraded package ID only for calling functions via `moveCall`.

```ts
// ✅ Correct — original package ID for type queries
const ORIGINAL_PACKAGE_ID = '0x1234...';  // first publish
const UPGRADED_PACKAGE_ID = '0x5678...';  // after sui client upgrade

// Query uses original ID
client.core.listOwnedObjects({ owner, type: `${ORIGINAL_PACKAGE_ID}::nft::NFT` });

// Function calls use upgraded ID
tx.moveCall({ target: `${UPGRADED_PACKAGE_ID}::nft::mint`, ... });
```

## `getDynamicField` requires BCS-encoded name bytes (gRPC)

The gRPC `getDynamicField` does **not** accept plain JSON values for the `name` parameter — unlike the deprecated JSON-RPC `getDynamicFieldObject` which takes `{ type, value }`. The gRPC API requires BCS-serialized bytes.

**Pattern:** serialize the name with `bcs`, pass `{ type, bcs: bytes }`, then parse the BCS response value.

```ts
import { bcs } from '@mysten/sui/bcs';

// ── Serialize the dynamic field name ──────────────────────────────
// The serializer must match the Move type used as the DF key.

// address key
const addressBytes = bcs.Address.serialize('0xABC...').toBytes();
const name = { type: 'address', bcs: addressBytes };

// string key (std::string::String)
const stringBytes = bcs.string().serialize('my_key').toBytes();
const nameStr = { type: '0x1::string::String', bcs: stringBytes };

// u64 key
const u64Bytes = bcs.u64().serialize(42n).toBytes();
const nameU64 = { type: 'u64', bcs: u64Bytes };

// ── Call getDynamicField ──────────────────────────────────────────
const result = await client.core.getDynamicField({
  parentId: '0xPARENT...',
  name,                         // { type, bcs }
  include: { json: true },      // or { content: true } for raw BCS
});

// ── Parse the result ──────────────────────────────────────────────
// With include.json, read fields directly:
const value = result.dynamicField?.json;

// With include.content (BCS bytes), deserialize manually:
// const raw = result.dynamicField?.content;
// const parsed = bcs.u64().parse(Uint8Array.from(raw));
```

**JSON-RPC difference:** the deprecated `SuiJsonRpcClient.getDynamicFieldObject` accepts `{ type: 'address', value: '0xABC...' }` — plain JSON, no serialization. If you're migrating from JSON-RPC to gRPC, this is the key change.

## Cache invalidation after transactions

```tsx
import { useQueryClient } from '@tanstack/react-query';
import { useDAppKit, useCurrentClient, useCurrentAccount } from '@mysten/dapp-kit-react';
import { Transaction } from '@mysten/sui/transactions';

function MintButton() {
  const dAppKit = useDAppKit();
  const client = useCurrentClient();
  const account = useCurrentAccount();
  const queryClient = useQueryClient();

  async function handleMint() {
    const tx = new Transaction();
    // ... build PTB (see sui-sdks / ptbs) ...

    const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });
    if (result.$kind === 'FailedTransaction') throw new Error('Mint failed');

    // ✅ Wait for indexing BEFORE invalidating
    await client.core.waitForTransaction({ digest: result.Transaction.digest });

    await queryClient.invalidateQueries({ queryKey: ['balance', account?.address] });
    await queryClient.invalidateQueries({ queryKey: ['owned-nfts', account?.address] });
  }

  return <button onClick={handleMint}>Mint</button>;
}
```

Do **not** invalidate before `waitForTransaction` — the refetch will see stale data.

## Query keys

Include every input that can change the result:
- owner address
- coin type / object type filter
- network (if the query reads across networks)
- cursor / page params

```ts
queryKey: ['owned-nfts', account?.address, network, typeFilter]
```

Too loose a key causes cross-account data leakage when switching wallets. Too tight causes unnecessary refetches.

## Stale-while-revalidate defaults

TanStack Query aggressively refetches on window focus / reconnect. For rapidly-changing on-chain data (balances, orderbook state) this is often right. For immutable data (a specific tx digest, a past object version) it's wasteful — tune `staleTime`:

```ts
useQuery({
  queryKey: ['tx', digest],
  queryFn: () => client.core.getTransaction({ digest, include: { effects: true } }),
  staleTime: Infinity,   // transactions don't change once finalized
});
```

## Derivations

Prefer to derive in the component, not in the query:

```tsx
const { data: balances } = useQuery({ queryKey: ['balances', addr], queryFn: ... });
const sui = balances?.find((b) => b.coinType === '0x2::sui::SUI');  // derive here
const suiAmount = Number(sui?.totalBalance ?? 0n) / 1e9;
```

Don't transform inside `queryFn` — TanStack's dedupe / cache works on the raw return, and double-transforming confuses invalidation.

## Don't use `queryFn` to run transactions

Queries should be pure reads. Transactions go in event handlers / mutations:

```tsx
// ❌ Don't do this
useQuery({ queryFn: () => dAppKit.signAndExecuteTransaction(...) });

// ✅ Do this — imperative in an event handler
async function onClick() {
  const result = await dAppKit.signAndExecuteTransaction(...);
}
```

If you want a mutation hook pattern, use TanStack's `useMutation` + `dAppKit.signAndExecuteTransaction` — dApp Kit no longer exports its own mutation hook.
