# Svelte (SvelteKit) + Wagmi

> EVM wallet connection in SvelteKit apps.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem
```

For contract interactions, also install:
```bash
npm install @wagmi/core
```

## Configuration

```typescript
// src/lib/appkit.ts
import { browser } from '$app/environment'
import { createAppKit } from '@reown/appkit'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'

let appKit: ReturnType<typeof createAppKit> | undefined = undefined

if (browser) {
  const projectId = import.meta.env.VITE_PROJECT_ID
  if (!projectId) {
    throw new Error('VITE_PROJECT_ID is not set')
  }

  const networks = [mainnet, arbitrum, base]

  const wagmiAdapter = new WagmiAdapter({
    networks,
    projectId,
  })

  appKit = createAppKit({
    adapters: [wagmiAdapter],
    networks,
    defaultNetwork: mainnet,
    projectId,
    metadata: {
      name: 'My SvelteKit dApp',
      description: 'SvelteKit dApp with AppKit',
      url: 'https://mydapp.com',
      icons: ['https://mydapp.com/icon.png']
    },
  })
}

export { appKit }
```

Note: Import from `@reown/appkit` (not `/react` or `/vue`). The `if (browser)` guard prevents SSR issues.

## Layout

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  import '$lib/appkit';
</script>

<slot />
```

## Environment Variables

```bash
# .env
VITE_PROJECT_ID=b56e18d47c72ab683b10814fe9495694 # localhost testing only
```

## Triggering the Modal

### Web Component

```svelte
<appkit-button />
```

Other components: `<appkit-connect-button />`, `<appkit-account-button />`, `<appkit-network-button />`

### Programmatic

```svelte
<script lang="ts">
  import { appKit } from '$lib/appkit';

  function openModal() {
    appKit?.open();
  }

  function openConnectModal() {
    appKit?.open({ view: 'Connect' });
  }

  function openNetworkModal() {
    appKit?.open({ view: 'Networks' });
  }
</script>

<button on:click={openModal}>Open Modal</button>
<button on:click={openConnectModal}>Connect Wallet</button>
<button on:click={openNetworkModal}>Switch Network</button>
```

## Subscribe to State

```svelte
<script lang="ts">
  import { appKit } from '$lib/appkit';
  import { onMount } from 'svelte';

  let address = '';
  let isConnected = false;
  let networkName = '';

  onMount(() => {
    appKit?.subscribeAccount((account) => {
      address = account.address || '';
      isConnected = account.isConnected;
    });

    appKit?.subscribeNetwork((network) => {
      networkName = network.caipNetwork?.name || '';
    });
  });
</script>

{#if isConnected}
  <p>Address: {address}</p>
  <p>Network: {networkName}</p>
{:else}
  <appkit-button />
{/if}
```

## Svelte-Specific Notes

- SvelteKit v5 recommended
- All initialization wrapped in `if (browser)` from `$app/environment`
- `appKit` is `undefined` on the server — always use optional chaining (`appKit?.`)
- No hooks/composables — use `subscribeAccount()` and `subscribeNetwork()` for reactivity
- Env vars use Vite convention: `VITE_` prefix, accessed via `import.meta.env`

## Ethers Variant

```typescript
// src/lib/appkit.ts
import { browser } from '$app/environment'
import { createAppKit } from '@reown/appkit'
import { EthersAdapter } from '@reown/appkit-adapter-ethers'
import { mainnet, arbitrum } from '@reown/appkit/networks'

let appKit: ReturnType<typeof createAppKit> | undefined = undefined

if (browser) {
  appKit = createAppKit({
    adapters: [new EthersAdapter()],
    networks: [mainnet, arbitrum],
    projectId: import.meta.env.VITE_PROJECT_ID,
    metadata: { name: 'My dApp', description: 'SvelteKit + Ethers', url: 'https://mydapp.com', icons: [] },
  })
}

export { appKit }
```

## Solana Variant

```typescript
import { SolanaAdapter } from '@reown/appkit-adapter-solana'
import { solana, solanaTestnet, solanaDevnet } from '@reown/appkit/networks'

const solanaAdapter = new SolanaAdapter()

appKit = createAppKit({
  adapters: [solanaAdapter],
  networks: [solana, solanaTestnet, solanaDevnet],
  // ...
})
```
