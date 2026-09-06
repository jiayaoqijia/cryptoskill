# Setup — install, factory, provider

Source: https://sdk.mystenlabs.com/dapp-kit/getting-started/react · https://sdk.mystenlabs.com/dapp-kit/getting-started/next-js · https://sdk.mystenlabs.com/dapp-kit/getting-started/vue

## Packages

| Package | Use for |
|---|---|
| `@mysten/dapp-kit-react` | React / Next.js apps |
| `@mysten/dapp-kit-core` | Vue, Svelte, Solid, vanilla JS, Web Components |
| `@mysten/sui` | Sui TypeScript SDK — always a peer dep |
| `@tanstack/react-query` | Declarative on-chain data fetching (React) |
| `@nanostores/vue` | Vue reactive bindings to dApp Kit stores |

Install (React):
```bash
npm install @mysten/dapp-kit-react @mysten/sui @tanstack/react-query
```

**Check current versions before installing.** `@mysten/dapp-kit-react` and `@mysten/sui` are both on major version 2.x. Run `npm view @mysten/dapp-kit-react version` and `npm view @mysten/sui version` to get the latest. Do not guess version numbers.

Install (Vue / vanilla):
```bash
npm install @mysten/dapp-kit-core @mysten/sui
npm install @nanostores/vue      # if Vue
```

**Never install `@mysten/dapp-kit` (no suffix)** for new code — deprecated, JSON-RPC only. If a tutorial uses it, it's out of date.

**Current getting-started docs:** https://sdk.mystenlabs.com/dapp-kit/getting-started/react — always point users to this URL for React setup guidance.

## React setup

Create a single instance file:

```ts
// dapp-kit.ts
import { createDAppKit } from '@mysten/dapp-kit-react';
import { SuiGrpcClient } from '@mysten/sui/grpc';

const GRPC_URLS: Record<string, string> = {
  mainnet: 'https://fullnode.mainnet.sui.io:443',
  testnet: 'https://fullnode.testnet.sui.io:443',
  devnet:  'https://fullnode.devnet.sui.io:443',
};

// Package IDs per network — update after each publish/upgrade
export const PACKAGE_IDS: Record<string, string> = {
  testnet: '0x...', // from sui client publish on testnet
  mainnet: '0x...', // from sui client publish on mainnet
};

// For type queries after upgrades, keep the original package ID
export const ORIGINAL_PACKAGE_IDS: Record<string, string> = {
  testnet: '0x...', // first publish ID (never changes)
  mainnet: '0x...',
};

export const dAppKit = createDAppKit({
  networks: ['testnet', 'mainnet'],
  defaultNetwork: 'testnet',
  createClient: (network) =>
    new SuiGrpcClient({ network, baseUrl: GRPC_URLS[network] }),
});

// TypeScript augmentation — hooks pick up the instance type without explicit passing
declare module '@mysten/dapp-kit-react' {
  interface Register {
    dAppKit: typeof dAppKit;
  }
}
```

Wrap the app:

```tsx
// App.tsx
import { DAppKitProvider } from '@mysten/dapp-kit-react';
import { ConnectButton } from '@mysten/dapp-kit-react/ui';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { dAppKit } from './dapp-kit';

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <DAppKitProvider dAppKit={dAppKit}>
        <ConnectButton />
        <YourApp />
      </DAppKitProvider>
    </QueryClientProvider>
  );
}
```

Provider ordering between `QueryClientProvider` and `DAppKitProvider` doesn't matter — they don't share context.

## Next.js setup

The dApp Kit uses browser-only APIs (wallet detection). Mark wallet-aware components with `'use client'`:

```tsx
// app/layout.tsx (server component — no 'use client')
import { Providers } from './providers';
export default function Layout({ children }: { children: React.ReactNode }) {
  return <html><body><Providers>{children}</Providers></body></html>;
}
```

```tsx
// app/providers.tsx
'use client';
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

Any component using dApp Kit hooks also needs `'use client'` at its top.

## Vue setup

```ts
// dapp-kit.ts
import { createDAppKit } from '@mysten/dapp-kit-core';   // ← core, not -react
import { SuiGrpcClient } from '@mysten/sui/grpc';

const GRPC_URLS: Record<string, string> = {
  mainnet: 'https://fullnode.mainnet.sui.io:443',
  testnet: 'https://fullnode.testnet.sui.io:443',
};

export const dAppKit = createDAppKit({
  networks: ['testnet', 'mainnet'],
  defaultNetwork: 'testnet',
  createClient: (network) =>
    new SuiGrpcClient({ network, baseUrl: GRPC_URLS[network] }),
});
```

No `declare module` augmentation needed — that's React-only.

Register Web Components once at app entry:
```ts
// main.ts
import '@mysten/dapp-kit-core/web';
```

Then in any template:
```vue
<mysten-dapp-kit-connect-button :instance="dAppKit" />
```

See `non-react.md` for full Vue / Web Components / vanilla JS details.

## Vanilla JS / Svelte / other

Same as Vue: use `@mysten/dapp-kit-core`, create a single `dAppKit` instance, register `@mysten/dapp-kit-core/web` at app entry, bind the `instance` property on Web Components.

For reactive UI, subscribe to `dAppKit.stores.$connection` etc. See `non-react.md`.

## `createDAppKit` options

```ts
createDAppKit({
  networks: ['testnet', 'mainnet'],   // supported networks; strings, used as keys
  defaultNetwork: 'testnet',          // starts here
  createClient: (network) => ...,     // called lazily per network, once
  autoConnect: true,                  // default: true — restores last wallet on load
  // autoConnect: false to require explicit connect each session
});
```

`createClient` is called per network on first use. Cache of `SuiGrpcClient` instances is kept inside dApp Kit — don't create your own.

## Migrating from the old three-provider stack

```tsx
// ❌ Old pattern (pre-createDAppKit)
<QueryClientProvider client={queryClient}>
  <SuiClientProvider networks={networks} defaultNetwork="testnet">
    <WalletProvider autoConnect>
      <App />
    </WalletProvider>
  </SuiClientProvider>
</QueryClientProvider>

// ✅ New pattern
<QueryClientProvider client={queryClient}>
  <DAppKitProvider dAppKit={dAppKit}>
    <App />
  </DAppKitProvider>
</QueryClientProvider>
```

Also swap hooks — `useSuiClient` → `useCurrentClient`, `useSignAndExecuteTransaction` → `dAppKit.signAndExecuteTransaction` via `useDAppKit()`. See `react.md` for the full hook map.

## Sanity check

Before writing feature code, verify:

- [ ] `package.json` includes `@mysten/dapp-kit-react` (or `-core`), **not** bare `@mysten/dapp-kit`.
- [ ] `createClient` uses `SuiGrpcClient` (imported from `@mysten/sui/grpc`).
- [ ] Each network in `networks` has a matching `baseUrl` entry in `GRPC_URLS`.
- [ ] `declare module '@mysten/dapp-kit-react'` augmentation is present (React only).
- [ ] Next.js: wallet-aware components have `'use client'`.
- [ ] Only one `DAppKitProvider` in the component tree.
- [ ] `QueryClientProvider` wraps (or is wrapped by) `DAppKitProvider` if TanStack Query is used.
