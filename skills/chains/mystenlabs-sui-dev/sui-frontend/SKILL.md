---
name: sui-frontend
description: Sui frontend dApp development with @mysten/dapp-kit-react (React) and @mysten/dapp-kit-core (Vue, vanilla JS, other frameworks). Use when building browser apps that connect to Sui wallets, query on-chain data, or execute transactions. Use alongside the sui-ts-sdk skill for PTB construction patterns.
---

# Sui Frontend Skill

This skill covers building browser-based Sui dApps using the dApp Kit SDK. The SDK has two packages:

- **`@mysten/dapp-kit-react`** — React hooks, `DAppKitProvider`, and React component wrappers
- **`@mysten/dapp-kit-core`** — Framework-agnostic core: actions, nanostores state, and Web Components for Vue, vanilla JS, Svelte, or any other framework

Both packages expose the same `createDAppKit` factory and identical action APIs (`signAndExecuteTransaction`, `signTransaction`, `signPersonalMessage`, etc.). What differs is how you access reactive state and render UI: React uses hooks and provider components; other frameworks use nanostores stores and Web Components.

For PTB construction details (splitCoins, moveCall, coinWithBalance, etc.), apply the **sui-ts-sdk** skill alongside this one — the `Transaction` API is identical in browser and Node contexts.

> **Note**: The older `@mysten/dapp-kit` package is deprecated (JSON-RPC only, no gRPC/GraphQL support). New projects must use `@mysten/dapp-kit-react` or `@mysten/dapp-kit-core`.

---

## 1. Package Installation

**React:**
```bash
npm install @mysten/dapp-kit-react @mysten/sui
# Add React Query for declarative on-chain data fetching (recommended)
npm install @tanstack/react-query
```

**Vue / vanilla JS / other frameworks:**
```bash
npm install @mysten/dapp-kit-core @mysten/sui
# For Vue reactive bindings:
npm install @nanostores/vue
```

| Package | Purpose |
|---------|---------|
| `@mysten/dapp-kit-react` | React hooks, `DAppKitProvider`, React component wrappers |
| `@mysten/dapp-kit-core` | Framework-agnostic actions, stores, Web Components |
| `@mysten/sui` | Sui TypeScript SDK (Transaction class, gRPC client) |
| `@tanstack/react-query` | Declarative on-chain data fetching (React only) |
| `@nanostores/vue` | Reactive store bindings for Vue |

---

## 2. Instance & Provider Setup (React)

> **Not using React?** Skip to the [Non-React Integration](#non-react-integration-vue--vanilla-js--svelte) section below.

The new dApp Kit uses a single `createDAppKit` factory instead of three nested providers. Create the instance once in a dedicated file, then wrap your app with `DAppKitProvider`:

```tsx
// dapp-kit.ts
import { createDAppKit } from '@mysten/dapp-kit-react';
import { SuiGrpcClient } from '@mysten/sui/grpc';

const GRPC_URLS: Record<string, string> = {
  testnet: 'https://fullnode.testnet.sui.io:443',
  mainnet: 'https://fullnode.mainnet.sui.io:443',
};

export const dAppKit = createDAppKit({
  networks: ['testnet', 'mainnet'],
  defaultNetwork: 'testnet',
  createClient: (network) =>
    new SuiGrpcClient({ network, baseUrl: GRPC_URLS[network] }),
});

// Register the instance type for TypeScript inference in hooks
declare module '@mysten/dapp-kit-react' {
  interface Register {
    dAppKit: typeof dAppKit;
  }
}
```

```tsx
// App.tsx
import { DAppKitProvider, ConnectButton } from '@mysten/dapp-kit-react';
import { dAppKit } from './dapp-kit';

export default function App() {
  return (
    <DAppKitProvider dAppKit={dAppKit}>
      <ConnectButton />
      <YourApp />
    </DAppKitProvider>
  );
}
```

The `declare module` augmentation is what makes `useDAppKit()` and other hooks return properly typed values without passing the instance explicitly. It's the recommended approach — the alternative is passing `dAppKit` directly to each hook call (e.g. `useWalletConnection({ dAppKit })`), but that's more verbose.

---

## 3. Network & Client Configuration

`createDAppKit` accepts these key options:

```tsx
createDAppKit({
  networks: ['testnet', 'mainnet'],       // which networks your app supports
  defaultNetwork: 'testnet',              // starting network
  createClient: (network) =>              // called once per network
    new SuiGrpcClient({ network, baseUrl: GRPC_URLS[network] }),
  autoConnect: true,                      // default: true — restores last wallet on reload
  // autoConnect: false,                  // disable if you want manual connect only
});
```

**Use `SuiGrpcClient` here** — unlike the deprecated `@mysten/dapp-kit`, the new package is built for gRPC. Do not pass `SuiJsonRpcClient` to `createClient`.

```tsx
// ❌ Wrong client type — belongs to the deprecated @mysten/dapp-kit era
import { SuiJsonRpcClient } from '@mysten/sui/jsonRpc';
createClient: (network) => new SuiJsonRpcClient({ ... })

// ✅ Correct
import { SuiGrpcClient } from '@mysten/sui/grpc';
createClient: (network) => new SuiGrpcClient({ network, baseUrl: GRPC_URLS[network] })
```

---

## Non-React Integration (Vue / Vanilla JS / Svelte)

Use `@mysten/dapp-kit-core` when not building with React. The `createDAppKit` call is identical — only the import path differs:

```ts
// dapp-kit.ts
import { createDAppKit } from '@mysten/dapp-kit-core';  // ← core, not -react
import { SuiGrpcClient } from '@mysten/sui/grpc';

const GRPC_URLS: Record<string, string> = {
  testnet: 'https://fullnode.testnet.sui.io:443',
  mainnet: 'https://fullnode.mainnet.sui.io:443',
};

export const dAppKit = createDAppKit({
  networks: ['testnet', 'mainnet'],
  defaultNetwork: 'testnet',
  createClient: (network) => new SuiGrpcClient({ network, baseUrl: GRPC_URLS[network] }),
});
```

No `declare module` augmentation needed — that's React-only.

All actions on the instance work identically to the React sections below: `signAndExecuteTransaction`, `signTransaction`, `signPersonalMessage`, `connectWallet`, `disconnectWallet`, `switchNetwork`, `switchAccount`.

### Web Components

Register the web components once at your app entry point, then use them in any HTML or template:

```ts
// main.ts (app entry point)
import '@mysten/dapp-kit-core/web';
```

**Connect Button** — set `instance` as a DOM property (not an HTML attribute):

```html
<mysten-dapp-kit-connect-button></mysten-dapp-kit-connect-button>

<script type="module">
  import { dAppKit } from './dapp-kit.js';
  document.querySelector('mysten-dapp-kit-connect-button').instance = dAppKit;
</script>
```

In Vue templates use property binding:

```vue
<mysten-dapp-kit-connect-button :instance="dAppKit" />
```

Supports `modalOptions.filterFn` / `modalOptions.sortFn`, same as the React `ConnectButton`.

**Connect Modal** — for custom triggers (menu items, keyboard shortcuts, programmatic open):

```html
<mysten-dapp-kit-connect-modal></mysten-dapp-kit-connect-modal>

<script type="module">
  const modal = document.querySelector('mysten-dapp-kit-connect-modal');
  modal.instance = dAppKit;
  document.getElementById('open-btn').addEventListener('click', () => modal.show());
</script>
```

Modal events: `open`, `opened`, `close`, `closed`, `cancel`.

### Reactive State (nanostores)

State is exposed as [nanostores](https://github.com/nanostores/nanostores) stores on `dAppKit.stores`:

| Store | Type | Description |
|-------|------|-------------|
| `$connection` | `{ wallet, account, status, isConnected, isConnecting, isReconnecting, isDisconnected }` | Full connection state |
| `$currentNetwork` | `string` | Active network name |
| `$currentClient` | `SuiClient` | Client for the active network |
| `$wallets` | `UiWallet[]` | Detected wallets |

**Vanilla JS** — subscribe for reactive updates:

```ts
// Read current value synchronously
const connection = dAppKit.stores.$connection.get();

// Subscribe (returns an unsubscribe function — always clean up)
const unsubscribe = dAppKit.stores.$connection.subscribe((conn) => {
  const el = document.getElementById('status');
  if (!el) return;
  if (conn.isConnected && conn.account) {
    el.textContent = `${conn.wallet?.name}: ${conn.account.address}`;
  } else {
    el.textContent = 'Not connected';
  }
});

// Unsubscribe when the view is destroyed
unsubscribe();
```

**Vue** — use `@nanostores/vue` for reactive template bindings:

```vue
<script setup lang="ts">
import { useStore } from '@nanostores/vue';
import { Transaction } from '@mysten/sui/transactions';
import { dAppKit } from './dapp-kit';

const connection = useStore(dAppKit.stores.$connection);
const network = useStore(dAppKit.stores.$currentNetwork);

async function handleTransfer() {
  if (!connection.value.account) return;

  const tx = new Transaction();
  // ... build PTB ...
  const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });

  if (result.FailedTransaction) {
    throw new Error(result.FailedTransaction.status.error?.message ?? 'Transaction failed');
  }
  console.log('Digest:', result.Transaction.digest);
}
</script>

<template>
  <mysten-dapp-kit-connect-button :instance="dAppKit" />
  <div v-if="connection.account">
    <p>Wallet: {{ connection.wallet?.name }}</p>
    <p>Address: {{ connection.account.address }}</p>
    <p>Network: {{ network }}</p>
    <button @click="handleTransfer">Send Transaction</button>
  </div>
  <p v-else>Connect your wallet to get started</p>
</template>
```

For Svelte, Solid, and other frameworks, nanostores has dedicated integrations — see the [nanostores docs](https://github.com/nanostores/nanostores).

### On-chain queries (non-React)

Outside React there's no `useCurrentClient` hook. Use the store or `getClient()` directly:

```ts
const client = dAppKit.stores.$currentClient.get();
// or equivalently:
const client = dAppKit.getClient();           // current network's client
const mainnetClient = dAppKit.getClient('mainnet'); // specific network

const connection = dAppKit.stores.$connection.get();
if (!connection.account) throw new Error('Wallet not connected');

const balance = await client.getBalance({
  owner: connection.account.address,
  coinType: '0x2::sui::SUI',
});
```

For live queries, subscribe to `$connection` and `$currentNetwork` and re-run when they change.

---

## 4. Wallet Connection

### ConnectButton

The simplest approach — renders a "Connect Wallet" button that opens a wallet selection modal:

```tsx
import { ConnectButton } from '@mysten/dapp-kit-react';

function Header() {
  return (
    <header>
      <ConnectButton />
    </header>
  );
}
```

`ConnectButton` auto-connects on page load by default (controlled by `autoConnect` in `createDAppKit`). Wallet detection happens in the browser — the component must be client-side rendered.

You can filter or sort the wallet list:

```tsx
<ConnectButton
  modalOptions={{
    filterFn: (wallet) => wallet.name !== 'ExcludedWallet',
    sortFn: (a, b) => a.name.localeCompare(b.name),
  }}
/>
```

### Supported wallets

dApp Kit auto-detects any wallet implementing the [Sui Wallet Standard](https://docs.sui.io/standards/wallet-standard). No manual registration needed — installed wallets appear automatically.

### Custom connection UI

Use `useWallets` to list wallets and `useDAppKit` for the connect/disconnect actions:

```tsx
import { useWallets, useDAppKit } from '@mysten/dapp-kit-react';

function WalletMenu() {
  const wallets = useWallets();
  const dAppKit = useDAppKit();

  return (
    <div>
      {wallets.map((wallet) => (
        <button
          key={wallet.name}
          onClick={() => dAppKit.connectWallet({ wallet })}
        >
          {wallet.name}
        </button>
      ))}
      <button onClick={() => dAppKit.disconnectWallet()}>Disconnect</button>
    </div>
  );
}
```

### Connection status

`useWalletConnection` provides the full connection state:

```tsx
import { useWalletConnection } from '@mysten/dapp-kit-react';

function ConnectionStatus() {
  const { status, wallet, account } = useWalletConnection();
  // status: 'disconnected' | 'connecting' | 'reconnecting' | 'connected'

  if (status === 'connecting' || status === 'reconnecting') return <p>Connecting...</p>;
  if (status === 'connected') return <p>Connected: {wallet?.name}</p>;
  return <p>Disconnected</p>;
}
```

---

## 5. Current Account & Wallet

`useCurrentAccount` gives you the connected address; `useCurrentWallet` gives you the wallet object (name, icon, accounts list):

```tsx
import { useCurrentAccount, useCurrentWallet } from '@mysten/dapp-kit-react';

function Profile() {
  const account = useCurrentAccount();
  const wallet = useCurrentWallet();

  if (!account) {
    return <p>No wallet connected</p>;
  }

  return (
    <div>
      <p>Wallet: {wallet?.name}</p>
      <p>Address: {account.address}</p>
      <p>Label: {account.label}</p>
    </div>
  );
}
```

Both return `null` when no wallet is connected. Always null-check before accessing their properties — TypeScript enforces this.

- `useCurrentAccount()` → `UiWalletAccount | null` — provides `address`, `label`
- `useCurrentWallet()` → `UiWallet | null` — provides `name`, `icon`, `accounts`

---

## 6. Accessing the Raw Client

`useCurrentClient` returns the `SuiClient` for the active network. Use it for imperative async calls — inside event handlers or after a transaction:

```tsx
import { useCurrentClient } from '@mysten/dapp-kit-react';

function SomeComponent() {
  const client = useCurrentClient();

  const handleSuccess = async (digest: string) => {
    // Wait for indexing before follow-up reads (see sui-ts-sdk §11)
    await client.waitForTransaction({ digest });
    // All SuiGrpcClient methods are available — see sui-ts-sdk for the full API
  };
}
```

Do not instantiate `new SuiGrpcClient(...)` inside components — use `useCurrentClient` so it stays in sync with the active network.

---

## 7. Querying On-Chain Data

`useSuiClientQuery` no longer exists in the new package. Use `useCurrentClient` with `@tanstack/react-query` directly:

```tsx
import { useCurrentClient, useCurrentAccount } from '@mysten/dapp-kit-react';
import { useQuery } from '@tanstack/react-query';

function Balance() {
  const client = useCurrentClient();
  const account = useCurrentAccount();

  const { data, isPending, error } = useQuery({
    queryKey: ['getBalance', account?.address],
    queryFn: () =>
      client.getBalance({
        owner: account!.address,
        coinType: '0x2::sui::SUI',
      }),
    enabled: !!account, // ✅ skip until wallet is connected
  });

  if (isPending) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  const sui = Number(data.totalBalance) / 1_000_000_000;
  return <p>Balance: {sui.toFixed(4)} SUI</p>;
}
```

Always wrap `@tanstack/react-query` usage in a `QueryClientProvider`:

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
const queryClient = new QueryClient();

// Wrap your DAppKitProvider (or vice versa — order doesn't matter here)
<QueryClientProvider client={queryClient}>
  <DAppKitProvider dAppKit={dAppKit}>
    <App />
  </DAppKitProvider>
</QueryClientProvider>
```

**Always pass `enabled: !!account`** for queries that require a connected wallet. Without it, the query fires immediately with an undefined owner and errors.

---

## 8. Paginated Queries

Use `useInfiniteQuery` from `@tanstack/react-query` paired with `useCurrentClient`:

```tsx
import { useCurrentClient, useCurrentAccount } from '@mysten/dapp-kit-react';
import { useInfiniteQuery } from '@tanstack/react-query';

function OwnedNFTs() {
  const client = useCurrentClient();
  const account = useCurrentAccount();

  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery({
    queryKey: ['getOwnedObjects', account?.address],
    queryFn: ({ pageParam }) =>
      client.getOwnedObjects({
        owner: account!.address,
        cursor: pageParam ?? null,
        filter: { StructType: '0xPKG::nft::NFT' },
        options: { showContent: true },
      }),
    initialPageParam: undefined,
    getNextPageParam: (lastPage) =>
      lastPage.hasNextPage ? lastPage.nextCursor : undefined,
    enabled: !!account,
  });

  const allObjects = data?.pages.flatMap((page) => page.data) ?? [];

  return (
    <div>
      {allObjects.map((obj) => (
        <NFTCard key={obj.data?.objectId} object={obj} />
      ))}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? 'Loading...' : 'Load more'}
        </button>
      )}
    </div>
  );
}
```

---

## 9. Signing and Executing Transactions

Use `useDAppKit` and call `signAndExecuteTransaction` as an async function. Build the `Transaction` exactly as you would in any other context — see **sui-ts-sdk** for PTB construction patterns:

```tsx
import { useDAppKit, useCurrentClient, useCurrentAccount } from '@mysten/dapp-kit-react';
import { Transaction } from '@mysten/sui/transactions';
import { useState } from 'react';

function ActionButton() {
  const dAppKit = useDAppKit();
  const client = useCurrentClient();
  const account = useCurrentAccount();
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAction = async () => {
    if (!account) return;
    setIsPending(true);
    setError(null);

    try {
      const tx = new Transaction();
      // ... build PTB using sui-ts-sdk patterns ...

      const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });

      if (result.FailedTransaction) {
        throw new Error(result.FailedTransaction.status.error?.message ?? 'Transaction failed');
      }

      const digest = result.Transaction.digest;
      await client.waitForTransaction({ digest });
      // now safe to re-query updated on-chain state
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setIsPending(false);
    }
  };

  return (
    <>
      <button onClick={handleAction} disabled={!account || isPending}>
        {isPending ? 'Waiting for wallet...' : 'Submit'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </>
  );
}
```

**Key differences from the old API:**
- No mutation hook — `signAndExecuteTransaction` is a plain async function on the `useDAppKit()` instance
- Result is a discriminated union: check `result.FailedTransaction` for failure; success data is at `result.Transaction.digest`
- Manage your own `isPending` / error state with `useState`

---

## 10. Signing Without Executing

When you need the user's signature but execution happens elsewhere (e.g., a sponsored flow where your backend attaches gas):

```tsx
import { useDAppKit } from '@mysten/dapp-kit-react';
import { Transaction } from '@mysten/sui/transactions';

function SponsoredMint() {
  const dAppKit = useDAppKit();

  const handleSign = async () => {
    const tx = new Transaction();
    // ... build PTB ...

    const { bytes, signature } = await dAppKit.signTransaction({ transaction: tx });
    // Send bytes + signature to backend; sponsor attaches gas and executes
    await fetch('/api/sponsor', {
      method: 'POST',
      body: JSON.stringify({ bytes, signature }),
    });
  };

  return <button onClick={handleSign}>Mint (Gasless)</button>;
}
```

For the server-side sponsored execution flow (attaching the sponsor's gas, collecting both signatures, submitting), see **sui-ts-sdk §15**.

---

## 11. Personal Message Signing

```tsx
import { useDAppKit, useCurrentAccount } from '@mysten/dapp-kit-react';

function AuthButton() {
  const dAppKit = useDAppKit();
  const account = useCurrentAccount();

  const handleAuth = async () => {
    if (!account) return;
    // In production, fetch a single-use nonce from your backend to prevent replay attacks.
    // Here we use a random client-side value for illustration only.
    const nonce = crypto.randomUUID();
    const message = new TextEncoder().encode(`Sign in to MyApp: nonce=${nonce}`);

    const { bytes, signature } = await dAppKit.signPersonalMessage({ message });
    // POST to backend for verification; backend should verify and invalidate the nonce.
    await verifyOnServer({ address: account.address, bytes, signature });
  };

  return (
    <button onClick={handleAuth} disabled={!account}>
      Sign In
    </button>
  );
}
```

The message must be a `Uint8Array` — use `TextEncoder` to convert strings. Always display message content clearly to users before signing.

---

## 12. Network Switching

Read the active network with `useCurrentNetwork`; switch it via `useDAppKit`:

```tsx
import { useCurrentNetwork, useDAppKit } from '@mysten/dapp-kit-react';

function NetworkSwitcher() {
  const network = useCurrentNetwork();
  const dAppKit = useDAppKit();

  return (
    <select value={network} onChange={(e) => dAppKit.switchNetwork(e.target.value)}>
      <option value="mainnet">Mainnet</option>
      <option value="testnet">Testnet</option>
    </select>
  );
}
```

Only networks in `createDAppKit`'s `networks` array are valid targets. `switchNetwork` executes synchronously and does not notify the wallet — it only affects the dApp's client.

---

## 13. Cache Invalidation After Transactions

After a successful transaction, invalidate React Query caches so the UI reflects updated state. Always wait for indexing first:

```tsx
import { useQueryClient } from '@tanstack/react-query';
import { useDAppKit, useCurrentClient, useCurrentAccount } from '@mysten/dapp-kit-react';

function MintButton() {
  const dAppKit = useDAppKit();
  const client = useCurrentClient();
  const account = useCurrentAccount();
  const queryClient = useQueryClient();

  const handleMint = async () => {
    const tx = new Transaction(); // import { Transaction } from '@mysten/sui/transactions'
    // ... build PTB ...

    const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });
    if (result.FailedTransaction) throw new Error('Mint failed');

    await client.waitForTransaction({ digest: result.Transaction.digest }); // ✅ wait first
    await queryClient.invalidateQueries({ queryKey: ['getBalance', account?.address] });
    await queryClient.invalidateQueries({ queryKey: ['getOwnedObjects', account?.address] });
  };

  return <button onClick={handleMint}>Mint NFT</button>;
}
```

```tsx
// ❌ Invalidating before waitForTransaction — indexer hasn't caught up yet
const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });
await queryClient.invalidateQueries(...); // stale!
await client.waitForTransaction({ digest: result.Transaction.digest });
```

---

## 14. Wallet-Gated UI

```tsx
import { useCurrentAccount, ConnectButton } from '@mysten/dapp-kit-react';

function ProtectedPage() {
  const account = useCurrentAccount();

  if (!account) {
    return (
      <div>
        <p>Connect your wallet to continue.</p>
        <ConnectButton />
      </div>
    );
  }

  return <Dashboard address={account.address} />;
}
```

Reusable guard:

```tsx
function WalletGuard({ children }: { children: React.ReactNode }) {
  const account = useCurrentAccount();
  if (!account) return <ConnectButton />;
  return <>{children}</>;
}
```

---

## 15. What dApp Kit is NOT

| Mistake | Correct approach |
|---------|-----------------|
| Using `@mysten/dapp-kit` in new projects | That package is deprecated; use `@mysten/dapp-kit-react` (React) or `@mysten/dapp-kit-core` (Vue, vanilla JS, other frameworks) |
| Using `SuiJsonRpcClient` in `createClient` | The new dApp Kit uses `SuiGrpcClient` — pass it to `createDAppKit`'s `createClient` |
| Three-provider setup (`QueryClientProvider` + `SuiClientProvider` + `WalletProvider`) | Use `createDAppKit` + `DAppKitProvider` — the old provider pattern is gone |
| Omitting the `declare module` augmentation | Without it, `useDAppKit()` and hooks lose TypeScript type inference |
| `useSignAndExecuteTransaction`, `useConnectWallet`, `useDisconnectWallet` | These mutation hooks no longer exist; use `useDAppKit()` instance methods instead |
| `useSuiClient` | Renamed to `useCurrentClient` |
| `useSuiClientContext` | Replaced by `useCurrentNetwork` (read) + `useDAppKit().switchNetwork()` (write) |
| `useSuiClientQuery` / `useSuiClientInfiniteQuery` | Removed; use `useCurrentClient` + `useQuery`/`useInfiniteQuery` from `@tanstack/react-query` |
| Checking `result.digest` after `signAndExecuteTransaction` | Result is a discriminated union: use `result.Transaction.digest` (success) or `result.FailedTransaction` (failure) |
| Reading `account.address` without null check | `useCurrentAccount()` returns `null` before connection; always guard |
| `enabled: !!account` omitted from queries | Without it, the query fires with an undefined owner and errors immediately |
| Invalidating queries before `waitForTransaction` | Indexer may not have processed the tx yet; always wait first |
| `ConnectButton` in SSR without client-side guard | Wallet detection is browser-only; ensure client-side rendering for wallet components |
