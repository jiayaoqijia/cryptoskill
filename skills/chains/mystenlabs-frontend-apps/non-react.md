# Vue, Vanilla JS, Web Components

Source: https://sdk.mystenlabs.com/dapp-kit/getting-started/vue

`@mysten/dapp-kit-core` exposes the same `createDAppKit` factory and the same action methods (`signAndExecuteTransaction`, `signTransaction`, `signPersonalMessage`, `connectWallet`, `disconnectWallet`, `switchNetwork`, `switchAccount`) as the React package. What differs:

- Reactive state is exposed via **nanostores** instead of React hooks.
- UI components are **Web Components** (`<mysten-dapp-kit-connect-button>`, `<mysten-dapp-kit-connect-modal>`) instead of React components.

## Setup (Vue)

```ts
// dapp-kit.ts
import { createDAppKit } from '@mysten/dapp-kit-core';
import { SuiGrpcClient } from '@mysten/sui/grpc';

const GRPC_URLS: Record<string, string> = {
  mainnet: 'https://fullnode.mainnet.sui.io:443',
  testnet: 'https://fullnode.testnet.sui.io:443',
};

export const dAppKit = createDAppKit({
  networks: ['testnet', 'mainnet'],
  defaultNetwork: 'testnet',
  createClient: (network) => new SuiGrpcClient({ network, baseUrl: GRPC_URLS[network] }),
});
```

```ts
// main.ts
import '@mysten/dapp-kit-core/web';    // registers Web Components globally
import { createApp } from 'vue';
import App from './App.vue';
createApp(App).mount('#app');
```

## Web Components

### Connect button

```vue
<template>
  <mysten-dapp-kit-connect-button :instance="dAppKit" />
</template>

<script setup lang="ts">
import { dAppKit } from './dapp-kit';
</script>
```

**Important:** `instance` is a **DOM property**, not an HTML attribute. In vanilla HTML:
```html
<mysten-dapp-kit-connect-button></mysten-dapp-kit-connect-button>
<script type="module">
  import { dAppKit } from './dapp-kit.js';
  document.querySelector('mysten-dapp-kit-connect-button').instance = dAppKit;
</script>
```

In Vue, the `:instance` property binding handles this automatically.

Accepts the same `modalOptions.filterFn` / `modalOptions.sortFn` as the React component:

```vue
<mysten-dapp-kit-connect-button
  :instance="dAppKit"
  :modal-options="{ filterFn: (w) => w.name !== 'Excluded' }"
/>
```

### Connect modal (custom trigger)

```html
<mysten-dapp-kit-connect-modal></mysten-dapp-kit-connect-modal>
<button id="open-btn">Connect</button>

<script type="module">
  const modal = document.querySelector('mysten-dapp-kit-connect-modal');
  modal.instance = dAppKit;
  document.getElementById('open-btn').onclick = () => modal.show();
</script>
```

Events: `open`, `opened`, `close`, `closed`, `cancel`.

## Reactive state (nanostores)

`dAppKit.stores` exposes nanostores stores:

| Store | Type | Contents |
|---|---|---|
| `$connection` | object | `{ wallet, account, status, isConnected, isConnecting, isReconnecting, isDisconnected }` |
| `$currentNetwork` | string | active network |
| `$currentClient` | `SuiGrpcClient` | client for active network |
| `$wallets` | `UiWallet[]` | detected wallets |

### Vanilla JS

Read synchronously, or subscribe:

```ts
// Snapshot
const conn = dAppKit.stores.$connection.get();
if (conn.isConnected) console.log(conn.account?.address);

// Subscribe (returns unsubscribe — always clean up)
const unsub = dAppKit.stores.$connection.subscribe((c) => {
  const el = document.getElementById('status');
  if (!el) return;
  el.textContent = c.isConnected
    ? `${c.wallet?.name}: ${c.account?.address}`
    : 'Not connected';
});

// Cleanup
unsub();
```

### Vue (`@nanostores/vue`)

```vue
<script setup lang="ts">
import { computed } from 'vue';
import { useStore } from '@nanostores/vue';
import { Transaction } from '@mysten/sui/transactions';
import { dAppKit } from './dapp-kit';

const connection = useStore(dAppKit.stores.$connection);
const network = useStore(dAppKit.stores.$currentNetwork);

// useStore returns a Vue ref — use .value in script code.
// Vue auto-unwraps refs in templates, so connection.account works there (no .value needed).
const address = computed(() => connection.value.account?.address);

async function handleTransfer() {
  if (!connection.value.account) return;

  const tx = new Transaction();
  // ... build PTB with @mysten/sui (see sui-sdks skill) ...

  const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });
  if (result.$kind === 'FailedTransaction') {
    throw new Error(result.FailedTransaction.status.error?.message ?? 'Failed');
  }

  const client = dAppKit.getClient();
  await client.waitForTransaction({ digest: result.Transaction.digest });
}
</script>

<template>
  <!-- Vue auto-unwraps refs in templates, so connection.account works (no .value needed) -->
  <mysten-dapp-kit-connect-button :instance="dAppKit" />
  <div v-if="connection.account">
    <p>{{ connection.wallet?.name }}: {{ connection.account.address }}</p>
    <button @click="handleTransfer">Send</button>
  </div>
</template>
```

### Svelte

```svelte
<script lang="ts">
  import { dAppKit } from './dapp-kit';
  let connection = dAppKit.stores.$connection.get();
  dAppKit.stores.$connection.subscribe((c) => connection = c);
</script>
```

For idiomatic Svelte stores, nanostores has a `@nanostores/svelte` integration.

## Accessing the client outside React

```ts
// Current network's client
const client = dAppKit.getClient();
// or equivalently:
const client = dAppKit.stores.$currentClient.get();

// Specific network (must be in the `networks` array)
const mainnetClient = dAppKit.getClient('mainnet');
```

## Actions (identical to React side)

All methods hang off the dApp Kit instance:

```ts
await dAppKit.signAndExecuteTransaction({ transaction });
await dAppKit.signTransaction({ transaction });
await dAppKit.signPersonalMessage({ message });
await dAppKit.connectWallet({ wallet });
await dAppKit.disconnectWallet();
await dAppKit.switchNetwork('mainnet');
await dAppKit.switchAccount({ account });
```

## Common mistakes

- **Setting `instance` as an HTML attribute** (`<... instance="dAppKit">`) — doesn't work; it's a DOM property.
- **Registering Web Components per component** — `import '@mysten/dapp-kit-core/web'` once at the app entry point.
- **Reading store value without `.get()` in vanilla JS** — `dAppKit.stores.$connection` is a store, not its value.
- **Forgetting to unsubscribe** — long-lived subscriptions leak memory.
- **Using `@mysten/dapp-kit-react` bindings in Vue** — wrong package; use `-core`.
