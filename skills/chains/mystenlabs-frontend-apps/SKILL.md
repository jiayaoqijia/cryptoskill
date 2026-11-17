---
name: frontend-apps
description: Builds Sui browser dApps with @mysten/dapp-kit-react (React, Next.js) and @mysten/dapp-kit-core (Vue, Svelte, vanilla JS, Web Components). Use when the user asks how to connect a Sui wallet, add a ConnectButton, set up createDAppKit or DAppKitProvider, read a balance or owned objects/NFTs in a frontend, sign and execute a transaction from a React or Vue component, sponsor gas from a backend, fix a UI that is stale after a transaction, handle Next.js App Router 'use client' / SSR for Sui, migrate off the deprecated @mysten/dapp-kit package or removed hooks (useSuiClientQuery, useSuiClient, useSignAndExecuteTransaction, useConnectWallet), or review Sui frontend code. Pair with the `sui-sdks` skill for @mysten/sui Transaction construction and the `ptbs` skill for PTB semantics.
---

# Sui dApp Kit (frontend)

Use `@mysten/dapp-kit-react` (React/Next.js) or `@mysten/dapp-kit-core` (Vue, Svelte, vanilla, Web Components) with `@mysten/sui`. The bare `@mysten/dapp-kit` is the deprecated JSON-RPC-only package and `@mysten/sui.js` is the frozen v1 package — never use either in new code. Most tutorials online are v1; when unsure, fetch the docs rather than extrapolate.

## Quick start (React + Vite)

```bash
npm i @mysten/dapp-kit-react @mysten/sui @tanstack/react-query
```

```ts
// src/dapp-kit.ts
import { createDAppKit } from '@mysten/dapp-kit-react';
import { SuiGrpcClient } from '@mysten/sui/grpc';

const GRPC_URLS = {
  testnet: 'https://fullnode.testnet.sui.io',
  mainnet: 'https://fullnode.mainnet.sui.io',
} as const;

export const dAppKit = createDAppKit({
  networks: ['testnet', 'mainnet'],
  defaultNetwork: 'testnet',
  createClient: (network) => new SuiGrpcClient({ network, url: GRPC_URLS[network] }),
});

// React only: gives every hook the right types without passing the instance around.
declare module '@mysten/dapp-kit-react' {
  interface Register {
    dAppKit: typeof dAppKit;
  }
}
```

```tsx
// src/main.tsx
import { DAppKitProvider } from '@mysten/dapp-kit-react';
import '@mysten/dapp-kit-react/ui/styles.css';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { dAppKit } from './dapp-kit';

const queryClient = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <DAppKitProvider dAppKit={dAppKit}>
      <App />
    </DAppKitProvider>
  </QueryClientProvider>,
);
```

`QueryClientProvider` is only for your own TanStack queries; dApp Kit itself no longer needs it. There is no `SuiClientProvider` or `WalletProvider` anymore.

Connect UI: `import { ConnectButton } from '@mysten/dapp-kit-react/ui'` — importing it from the package root silently renders nothing.

Current hooks: `useCurrentAccount`, `useCurrentWallet`, `useCurrentNetwork`, `useCurrentClient`, `useDAppKit`, `useWallets`, `useWalletConnection`.
Removed hooks (treat any occurrence as a bug): `useSuiClientQuery`, `useSuiClientInfiniteQuery`, `useSuiClientContext`, `useSuiClient`, `useSignAndExecuteTransaction`, `useConnectWallet`, `useDisconnectWallet`.

## Reading on-chain data

Always read through `useCurrentClient()` + TanStack Query. Never construct a client inside a component (breaks network switching). Gate on the account.

```tsx
import { useCurrentAccount, useCurrentClient, useCurrentNetwork } from '@mysten/dapp-kit-react';
import { useQuery } from '@tanstack/react-query';

export function Balance() {
  const account = useCurrentAccount();
  const client = useCurrentClient();
  const network = useCurrentNetwork();

  const { data, isPending, error } = useQuery({
    queryKey: ['balances', network, account?.address],
    queryFn: () => client.core.listBalances({ owner: account!.address }),
    enabled: !!account, // useCurrentAccount() is null until a wallet connects
  });

  if (!account) return <p>Connect a wallet.</p>;
  if (isPending) return <p>Loading…</p>;
  if (error) return <p>{error.message}</p>;
  // pick the entry whose coinType is 0x2::sui::SUI
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
```

Pagination uses `useInfiniteQuery` and the v2 single nullable `cursor` (there is no `nextCursor` / `hasNextPage` on the response):

```tsx
const q = useInfiniteQuery({
  queryKey: ['nfts', network, account?.address],
  queryFn: ({ pageParam }) =>
    client.core.listOwnedObjects({
      owner: account!.address,
      type: '0xPKG::nft::NFT',
      cursor: pageParam,
    }),
  initialPageParam: null as string | null,
  getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
  enabled: !!account,
});

const nfts = q.data?.pages.flatMap((page) => page.objects) ?? [];

<button onClick={() => q.fetchNextPage()} disabled={!q.hasNextPage || q.isFetchingNextPage}>
  {q.isFetchingNextPage ? 'Loading…' : 'Load more'}
</button>
```

## Sending a transaction

Checklist — follow in this order, the ordering is what breaks:

1. Build a `Transaction` with typed pure helpers (`tx.pure.u64`, `tx.pure.address`, `tx.pure.string`). Never `tx.pure(v)`.
2. Do **not** call `tx.build()`, `setGasBudget`, `setGasPrice` or `setGasPayment` — the wallet selects gas and dry-runs for budget.
3. `const result = await useDAppKit().signAndExecuteTransaction({ transaction: tx })` — imperatively, in the event handler. The parameter is `transaction`, not `transactionBlock`.
4. Check `result.$kind === 'FailedTransaction'` (or `result.FailedTransaction`) before reading anything. Success digest lives at `result.Transaction.digest`.
5. `await client.waitForTransaction({ digest })` — fullnodes index asynchronously.
6. Then `queryClient.invalidateQueries(...)`. Invalidating first refetches stale data.

```tsx
import { useCurrentClient, useDAppKit } from '@mysten/dapp-kit-react';
import { useQueryClient } from '@tanstack/react-query';
import { Transaction } from '@mysten/sui/transactions';
import { useState } from 'react';

const RECIPIENT = '0xRECIPIENT';

export function SendButton() {
  const dAppKit = useDAppKit();
  const client = useCurrentClient();
  const queryClient = useQueryClient();
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onClick() {
    setIsPending(true);
    setError(null);
    try {
      const tx = new Transaction();
      const [coin] = tx.splitCoins(tx.gas, [tx.pure.u64(500_000_000n)]); // 0.5 SUI
      tx.transferObjects([coin], tx.pure.address(RECIPIENT));

      const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });
      if (result.$kind === 'FailedTransaction') throw new Error('Transaction failed on chain');

      await client.waitForTransaction({ digest: result.Transaction.digest });
      await queryClient.invalidateQueries({ queryKey: ['balances'] });
    } catch (e) {
      // also catches wallet rejection
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setIsPending(false);
    }
  }

  return (
    <>
      <button onClick={onClick} disabled={isPending}>{isPending ? 'Sending…' : 'Send 0.5 SUI'}</button>
      {error && <p role="alert">{error}</p>}
    </>
  );
}
```

There is no mutation hook — manage `isPending` / `error` with `useState`.

## Sponsored gas (wallet signs, backend pays and submits)

```tsx
const { bytes, signature } = await dAppKit.signTransaction({ transaction: tx });

const { digest } = await fetch('/api/sponsor', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ bytes, signature }),
}).then((r) => r.json());

await client.waitForTransaction({ digest }); // then invalidate queries
```

The backend sets the gas owner, gas payment and sponsor signature and executes. The frontend sets no gas fields and holds no keys. See `transactions.md` and the `ptbs` skill for the sponsor side.

## Next.js App Router

Wallet detection uses browser-only APIs, so dApp Kit must render client-side — but keep `layout.tsx` a server component:

```tsx
// app/providers.tsx
'use client';
// …QueryClientProvider + DAppKitProvider exactly as in the quick start, wrapping {children}
```
```tsx
// app/layout.tsx — no 'use client'
import { Providers } from './providers';
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html><body><Providers>{children}</Providers></body></html>;
}
```
Every leaf component that calls a dApp Kit hook or renders `ConnectButton` also needs `'use client'`. Do not mark the whole layout `'use client'` — you lose RSC.

## Vue / non-React (`@mysten/dapp-kit-core`)

```bash
npm i @mysten/dapp-kit-core @mysten/sui @nanostores/vue
```

```ts
// src/dapp-kit.ts — identical to the React instance, but import createDAppKit from '@mysten/dapp-kit-core'
// and omit the `declare module` augmentation (React-only).

// src/main.ts
import '@mysten/dapp-kit-core/web'; // registers the Web Components once, at app entry
import { createApp } from 'vue';
import App from './App.vue';
createApp(App).mount('#app');
```

```vue
<script setup lang="ts">
import { computed } from 'vue';
import { useStore } from '@nanostores/vue';
import { dAppKit } from './dapp-kit';

const connection = useStore(dAppKit.stores.$connection); // a Vue ref
const address = computed(() => connection.value.account?.address);
</script>

<template>
  <mysten-dapp-kit-connect-button :instance="dAppKit" />
  <p v-if="connection.account">Connected: {{ connection.account.address }}</p>
</template>
```

`:instance` must be a property binding — a plain string attribute will not pass the instance. Use `.value` in script, auto-unwrapped in templates. Other stores: `dAppKit.stores.$wallets`, etc. Actions (`signAndExecuteTransaction`, `signTransaction`, `switchNetwork`, `connectWallet`, `disconnectWallet`) are identical to React.

## Reviewing code / "is this tutorial current?"

Walk the whole list and report **every** match — v1-tutorial code usually stacks 5–10 issues in one component. If you found fewer than 5 in a multi-line snippet, re-read it.

- `@mysten/sui.js` → `@mysten/sui`; `@mysten/dapp-kit` (no suffix) → `@mysten/dapp-kit-react` / `-core`.
- `ConnectButton` / `ConnectModal` from the package root → `@mysten/dapp-kit-react/ui`.
- `SuiClient` (removed in v2) → `SuiGrpcClient` from `@mysten/sui/grpc`, or `useCurrentClient()` in components.
- `TransactionBlock` → `Transaction`.
- Any removed hook → `useCurrentClient()` + `useQuery`/`useInfiniteQuery`, or `useDAppKit()` imperative actions.
- `SuiClientProvider` + `WalletProvider` → `createDAppKit` + `<DAppKitProvider>` (`QueryClientProvider` stays).
- `new SuiClient(...)` / `new SuiGrpcClient(...)` in a component body → `useCurrentClient()`.
- Wallet-dependent query missing `enabled: !!account`.
- Untyped `tx.pure(v)`; `tx.build()` or gas settings in app code.
- `signAndExecuteTransactionBlock` / `{ transactionBlock: tx }` → `signAndExecuteTransaction` / `{ transaction: tx }`.
- `result.effects?.status?.status` → `$kind` discriminant; bare `result.digest` → `result.Transaction.digest`.
- `invalidateQueries` not preceded by `await client.waitForTransaction({ digest })`.
- Wallet-aware Next.js component missing `'use client'`.
- Returning a `Transaction` from a `queryFn`; calling `window.navigator.wallets` directly (use `useWallets()` / `$wallets`); instantiating `SuinsClient` / `DeepBookClient` instead of `client.$extend(suins(), deepbook({ address }))`; `autoConnect: true` without pending/reconnecting states; network URLs hardcoded in several places instead of one `GRPC_URLS` map; any secret or private key in browser code.

Output format — one bullet per issue, what's wrong then the replacement:

> - `useSuiClientQuery` — removed in v2. Use `useCurrentClient()` with TanStack `useQuery`.
> - `{ transactionBlock: tx }` — the parameter is now `{ transaction: tx }`.
> - `invalidateQueries` fires immediately — `await client.waitForTransaction({ digest: result.Transaction.digest })` first.

When the user asks whether an old tutorial is current, say plainly that it is not, name the deprecated package and each removed API, give the replacement, and link the current getting-started docs.

## Reference files and docs

| File | Load when |
|------|-----------|
| `setup.md` | scaffolding, `createDAppKit`, providers, TS augmentation, migrating off the three-provider stack |
| `react.md` | React hooks, `ConnectButton`, wallet-gated UI |
| `non-react.md` | Vue/Svelte/vanilla, nanostores, Web Components |
| `queries.md` | balances, owned objects, coins, dynamic fields, pagination, invalidation |
| `transactions.md` | sign/execute, `$kind` results, sponsored flows, `signPersonalMessage`, wallet UX failures |
| `limitations.md` | SSR, auto-connect, backend-only features, secrets |

Full code review → all six. PTB construction → `sui-sdks` / `ptbs` skills.

Docs: https://sdk.mystenlabs.com/dapp-kit and its `/getting-started/react`, `/getting-started/next-js`, `/getting-started/vue` pages; https://docs.sui.io/standards/wallet-standard. MCP tool when available: `https://sui.mcp.kapa.ai`.
