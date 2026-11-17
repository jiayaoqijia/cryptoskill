---
name: generate-sui-agent-config
description: >
  Current Sui dApp Kit APIs for React, Vue, and Next.js apps, and generation of a
  CLAUDE.md or AGENT.md config for Sui projects. Use when the user asks to build,
  review, modernize, or debug Sui frontend code — connect wallet, read SUI balance,
  list owned objects or NFTs, send or sponsor a transaction — or mentions
  @mysten/dapp-kit, dapp-kit-react, dapp-kit-core, @mysten/sui, @mysten/sui.js,
  createDAppKit, DAppKitProvider, SuiClientProvider, useSuiClientQuery, a Sui tutorial
  that may be out of date, "CLAUDE.md", "AGENT.md", or "agent config".
---

# Sui agent config and current dApp Kit APIs

> **MCP tool:** when the Sui docs MCP server (`https://sui.mcp.kapa.ai`) is available, query it to verify APIs and fill gaps. Include a directive to use it in any config file you generate.

## Use the current API, never the legacy one

| Legacy / removed | Use instead |
| --- | --- |
| `@mysten/sui.js` | `@mysten/sui` |
| `@mysten/dapp-kit` (no suffix) | `@mysten/dapp-kit-react` (React) or `@mysten/dapp-kit-core` (everything else) |
| `SuiClient`, `SuiJsonRpcClient` | `SuiGrpcClient` from `@mysten/sui/grpc` |
| `SuiClientProvider` + `WalletProvider` + `QueryClientProvider` stack | `createDAppKit()` + `<DAppKitProvider>`, still inside `QueryClientProvider` |
| `useSuiClient` | `useCurrentClient()` |
| `useSuiClientQuery`, `useSuiClientInfiniteQuery` | `useCurrentClient()` + TanStack `useQuery` / `useInfiniteQuery` |
| `useSignAndExecuteTransaction` (mutation hook), `useConnectWallet` | `useDAppKit()` → `instance.signAndExecuteTransaction(...)` |
| `TransactionBlock` | `Transaction` from `@mysten/sui/transactions` |
| `tx.pure('n')` | typed helpers: `tx.pure.u64(n)`, `tx.pure.address(a)`, `tx.pure.string(s)` |
| `{ transactionBlock: tx }` | `{ transaction: tx }` |
| `result.effects?.status?.status` | `result.$kind` / `result.FailedTransaction` discriminant |
| `client.getBalance`, `client.getAllBalances` | `client.core.listBalances` |
| `client.getOwnedObjects` | `client.core.listOwnedObjects` |
| `nextCursor` + `hasNextPage` | single nullable `cursor` on the page result |

Never say the legacy pattern still works. When a user shows legacy code, name each
issue and give the replacement.

## React setup

```sh
npm install @mysten/dapp-kit-react @mysten/sui @tanstack/react-query
```

```ts
// src/dapp-kit.ts
import { createDAppKit } from '@mysten/dapp-kit-react';
import { SuiGrpcClient } from '@mysten/sui/grpc';

export const dAppKit = createDAppKit({
  networks: ['testnet', 'mainnet'],
  defaultNetwork: 'testnet',
  createClient: (network) => new SuiGrpcClient({ network }), // add `url` for a custom endpoint
});

declare module '@mysten/dapp-kit-react' {
  interface Register {
    dAppKit: typeof dAppKit;
  }
}
```

```tsx
// src/providers.tsx
import { DAppKitProvider } from '@mysten/dapp-kit-react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { dAppKit } from './dapp-kit';

const queryClient = new QueryClient();

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <DAppKitProvider dAppKit={dAppKit}>{children}</DAppKitProvider>
    </QueryClientProvider>
  );
}
```

The `declare module` augmentation is React-only; omit it for `@mysten/dapp-kit-core`.

## Reading chain data

```tsx
const account = useCurrentAccount();
const client = useCurrentClient();

const { data } = useQuery({
  queryKey: ['balances', account?.address],
  enabled: !!account,
  queryFn: () => client.core.listBalances({ address: account!.address }),
});
```

Paginated owned objects / NFTs:

```tsx
const q = useInfiniteQuery({
  queryKey: ['nfts', account?.address],
  enabled: !!account,
  initialPageParam: null as string | null,
  queryFn: ({ pageParam }) =>
    client.core.listOwnedObjects({
      address: account!.address,
      type: '0xPKG::nft::NFT',
      cursor: pageParam,
    }),
  getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
});

const items = q.data?.pages.flatMap((p) => p.objects) ?? [];
// <button onClick={() => q.fetchNextPage()} disabled={q.isFetchingNextPage || !q.hasNextPage}>
```

## Sending a transaction

Order matters: build → sign+execute → check `$kind` → `waitForTransaction` → invalidate.

```tsx
const dAppKit = useDAppKit();
const client = useCurrentClient();
const queryClient = useQueryClient();
const [isPending, setIsPending] = useState(false);
const [error, setError] = useState<Error | null>(null);

async function onClick() {
  setIsPending(true);
  setError(null);
  try {
    const tx = new Transaction();
    const [coin] = tx.splitCoins(tx.gas, [tx.pure.u64(500_000_000n)]);
    tx.transferObjects([coin], tx.pure.address(RECIPIENT));

    const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });
    if (result.$kind === 'FailedTransaction') throw new Error('Transaction failed');

    await client.waitForTransaction({ digest: result.digest });
    await queryClient.invalidateQueries({ queryKey: ['balances'] });
  } catch (e) {
    setError(e as Error);
  } finally {
    setIsPending(false);
  }
}
```

- Pass the `Transaction` instance itself; do not call `tx.build()` in app code.
- Never call `tx.setGasBudget`, `tx.setGasPrice`, or `tx.setGasPayment` — the wallet handles gas.
- There is no mutation hook; track `isPending` / `error` with `useState`.

## Sign without executing (backend-sponsored gas)

```tsx
const { bytes, signature } = await dAppKit.signTransaction({ transaction: tx });
const res = await fetch('/api/sponsor', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ bytes, signature }),
});
const { digest } = await res.json();
await client.waitForTransaction({ digest });
```

The backend sets the gas owner, gas payment, and sponsor signature, then submits. The
frontend sets none of those.

## Vue / non-React

Use `@mysten/dapp-kit-core` with the same `createDAppKit` + `SuiGrpcClient` config, no
`declare module`. Register the Web Components once at the app entry:

```ts
// main.ts
import '@mysten/dapp-kit-core/web';
```

```vue
<script setup lang="ts">
import { useStore } from '@nanostores/vue';
import { dAppKit } from './dapp-kit';
const connection = useStore(dAppKit.stores.$connection);
</script>

<template>
  <mysten-dapp-kit-connect-button :instance="dAppKit" />
  <p v-if="connection.account">{{ connection.account.address }}</p>
</template>
```

Bind `:instance` as a property, never as a string attribute.

## Next.js App Router

dApp Kit needs the browser (wallet detection), so keep `layout.tsx` a server component
and put the providers in a separate `app/providers.tsx` whose first line is
`'use client'`, then render `<Providers>` inside the layout body. Any leaf component
that calls a dApp Kit hook also needs `'use client'`. Do not mark the whole layout
`'use client'`.

## Generating the config file

Write `CLAUDE.md` in the project root (use `AGENT.md` only if the user asks). Include:

````markdown
## Sui Development Skills

Install community-maintained skills for Sui development:

```sh
npx skills https://github.com/MystenLabs/skills
```

## Sui SDK Reference

Every `@mysten/*` package ships LLM documentation in its `docs/` directory. Find it via
`docs/llms-index.md` inside `node_modules/@mysten/*/`. Read the index first, then the page.

## Official Resources

When unsure about Move patterns or Sui APIs, consult these sources. Do not guess or
extrapolate from other blockchains.

- Sui docs MCP server: https://sui.mcp.kapa.ai
- Move Book: https://move-book.com (use https://move-book.com/llms.txt)
- Sui Docs: https://docs.sui.io (use https://docs.sui.io/llms.txt)
- Sui Move examples: https://github.com/MystenLabs/sui/tree/main/examples/move
````

Then add the legacy→current table above as a "Current APIs" section, and a
`## Project Structure` section only if the repo has multiple top-level directories.

Rules: the install command is exactly `npx skills https://github.com/MystenLabs/skills`;
the SDK docs path is exactly `node_modules/@mysten/*/docs/`; include the SDK Reference
section only when the project uses `@mysten/*` npm packages.
