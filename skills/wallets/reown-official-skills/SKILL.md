---
name: appkit
description: Guides developers through integrating Reown AppKit into web applications (React, Next.js, Vue, Nuxt, Svelte, vanilla JavaScript). Use when adding wallet connection, network switching, multi-chain support, or troubleshooting AppKit integration issues.
---

# Reown AppKit — Web Integration

## Goal

Help developers integrate Reown AppKit so their users can connect wallets, switch networks, and interact with EVM, Solana, and Bitcoin blockchains. AppKit provides a universal modal UI and hooks/composables for wallet management.

## When to use

- Adding wallet connection to a web app (React, Next.js, Vue, Nuxt, Svelte, JavaScript)
- Setting up multi-chain support (EVM + Solana + Bitcoin)
- Configuring blockchain adapters (Wagmi, Ethers, Solana, Bitcoin)
- Debugging AppKit initialization, modal, or connection issues
- Implementing Sign In With X (SIWX) authentication
- Choosing the right adapter for a project

## When not to use

- Building native mobile apps (use AppKit mobile SDKs — separate product)
- WalletKit integration for wallet developers (separate SDK)
- WalletConnect Pay (use the walletconnect-pay skill)

## Supported Platforms & Adapters

**Frameworks:** React, Next.js, Vue, Nuxt, Svelte, vanilla JavaScript
**Adapters:** Wagmi (EVM), Ethers v5/v6 (EVM), Solana, Bitcoin
**Networks:** All EVM chains, Solana, Bitcoin

## Choose Your Framework

| Framework | Import path | Notes |
|-----------|-------------|-------|
| React | `@reown/appkit/react` | Hooks-based |
| Next.js | `@reown/appkit/react` | SSR + cookie hydration required |
| Vue | `@reown/appkit/vue` | Composables-based |
| Nuxt | `@reown/appkit/vue` | SSR + module config required |
| Svelte | `@reown/appkit` | Stores-based |
| JavaScript | `@reown/appkit` | No framework dependency |

Jump to the right reference:
- [React + Wagmi](references/react-wagmi.md)
- [React + Ethers](references/react-ethers.md)
- [React + Solana](references/react-solana.md)
- [React + Bitcoin](references/react-bitcoin.md)
- [React + Multichain](references/react-multichain.md)
- [Next.js + Wagmi](references/nextjs-wagmi.md)
- [Next.js + Ethers](references/nextjs-ethers.md)
- [Next.js + Solana](references/nextjs-solana.md)
- [Next.js + Multichain](references/nextjs-multichain.md)
- [Vue + Wagmi](references/vue-wagmi.md)
- [Vue + Ethers](references/vue-ethers.md)
- [Vue + Solana](references/vue-solana.md)
- [Vue + Multichain](references/vue-multichain.md)
- [Nuxt + Wagmi](references/nuxt-wagmi.md)
- [Svelte + Wagmi](references/svelte-wagmi.md)
- [JavaScript + Wagmi](references/javascript-wagmi.md)
- [JavaScript + Ethers](references/javascript-ethers.md)
- [JavaScript + Solana](references/javascript-solana.md)
- [JavaScript + Multichain](references/javascript-multichain.md)

## Prerequisites

1. **Project ID** — The examples use `b56e18d47c72ab683b10814fe9495694`, a public projectId for **localhost testing only**. For production, create your own project at [dashboard.reown.com](https://dashboard.reown.com)
2. **Node 18+** and a modern bundler (Vite recommended)
3. Choose an adapter based on your chain requirements

## Universal Setup Flow (all frameworks)

Every integration follows these steps:

```
1. Install packages (appkit + adapter)
        ↓
2. Configure adapter (projectId, networks)
        ↓
3. Call createAppKit({ adapters, networks, projectId, metadata })
        ↓
4. Wrap app with required providers (framework-specific)
        ↓
5. Add <appkit-button /> or use hooks/composables to open modal
        ↓
6. Use hooks/composables for account, network, and provider access
        ↓
7. Add your domain at [dashboard.reown.com](https://dashboard.reown.com)
```

### Step 1 — Install packages

Always install `@reown/appkit` plus the adapter for your chain:

```bash
# EVM with Wagmi (most common)
npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem @tanstack/react-query

# EVM with Ethers v6
npm install @reown/appkit @reown/appkit-adapter-ethers ethers

# Solana
npm install @reown/appkit @reown/appkit-adapter-solana

# Bitcoin
npm install @reown/appkit @reown/appkit-adapter-bitcoin

```

### Step 2 — Configure and create AppKit

```typescript
import { createAppKit } from '@reown/appkit/react' // or /vue or just @reown/appkit
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // Public projectId for localhost only
const networks = [mainnet, arbitrum]

const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
})

const modal = createAppKit({
  adapters: [wagmiAdapter],
  networks,
  projectId,
  metadata: {
    name: 'My App',
    description: 'My App Description',
    url: 'https://myapp.com',      // Must match your domain
    icons: ['https://myapp.com/icon.png']
  },
  features: {
    analytics: true
  }
})
```

### Step 3 — Trigger the modal

```tsx
// Web component (works everywhere)
<appkit-button />

// React hook
import { useAppKit } from '@reown/appkit/react'
const { open } = useAppKit()
<button onClick={() => open()}>Connect</button>

// Vue composable
import { useAppKit } from '@reown/appkit/vue'
const { open } = useAppKit()
```

### Step 4 — Access account and network

```tsx
// React
import { useAppKitAccount, useAppKitNetwork } from '@reown/appkit/react'

const { address, isConnected, caipAddress } = useAppKitAccount()
const { caipNetwork, switchNetwork } = useAppKitNetwork()
```

## Key Hooks / Composables

| Hook | Returns | Purpose |
|------|---------|---------|
| `useAppKit` | `open()`, `close()` | Control modal |
| `useAppKitAccount` | `address`, `isConnected`, `caipAddress`, `status` | Account state |
| `useAppKitNetwork` | `caipNetwork`, `chainId`, `switchNetwork()` | Network state |
| `useAppKitProvider` | `walletProvider` | Raw provider access |
| `useAppKitState` | `initialized`, `loading`, `open`, `selectedNetworkId` | Modal state |
| `useDisconnect` | `disconnect()` | Disconnect wallet |
| `useAppKitBalance` | `fetchBalance()` | Token balance |
| `useWalletInfo` | `walletInfo` | Wallet metadata |

## Best Practices

### 1. Keep all AppKit package versions aligned

All `@reown/appkit*` packages must be the **same version**. Mixing versions causes subtle runtime errors (missing methods, broken state, silent failures).

```json
// package.json — correct: all versions match
{
  "@reown/appkit": "1.7.1",
  "@reown/appkit-adapter-wagmi": "1.7.1",
  "@reown/appkit-adapter-solana": "1.7.1"
}
```

When upgrading, update every `@reown/appkit*` package together.

### 2. Call `createAppKit` at module level — never inside a component

`createAppKit` must run **once** as a side-effect at module scope. Calling it inside a React component, Vue `setup()`, or Svelte component causes duplicate instances and broken state on re-renders.

```typescript
// DO — module-level (runs once on import)
import { createAppKit } from '@reown/appkit/react'
import { wagmiAdapter, projectId, networks, metadata } from './config'

createAppKit({ adapters: [wagmiAdapter], networks, projectId, metadata })

export default function App() {
  return <appkit-button />
}
```

```typescript
// DON'T — inside a component (runs on every render)
export default function App() {
  createAppKit({ adapters: [wagmiAdapter], networks, projectId, metadata }) // BUG
  return <appkit-button />
}
```

### 3. Wagmi OR Ethers — never both

Both `WagmiAdapter` and `EthersAdapter` register the EVM (`eip155`) namespace. Using both in the same project causes conflicts.

- **New projects:** use Wagmi — better React hook integration, active ecosystem, broader wallet support
- **Existing ethers.js codebase:** use Ethers to avoid rewriting provider logic

```typescript
// DO — one EVM adapter
createAppKit({ adapters: [wagmiAdapter, solanaAdapter], ... })

// DON'T — two EVM adapters
createAppKit({ adapters: [wagmiAdapter, ethersAdapter], ... }) // CONFLICT
```

## Multichain Setup

Pass multiple adapters to `createAppKit`:

```typescript
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { SolanaAdapter } from '@reown/appkit-adapter-solana'
import { mainnet, arbitrum, solana, solanaDevnet } from '@reown/appkit/networks'

const wagmiAdapter = new WagmiAdapter({ networks: [mainnet, arbitrum], projectId })
const solanaAdapter = new SolanaAdapter()

createAppKit({
  adapters: [wagmiAdapter, solanaAdapter],
  networks: [mainnet, arbitrum, solana, solanaDevnet],
  projectId,
  metadata,
})
```

## Validation checklist

- [ ] `projectId` obtained from dashboard.reown.com
- [ ] `metadata.url` matches your actual domain (wallets verify this)
- [ ] Networks imported from `@reown/appkit/networks` (not from viem/wagmi directly)
- [ ] For Next.js: SSR flag set, cookie hydration implemented, webpack externals configured
- [ ] For Wagmi: `WagmiProvider` and `QueryClientProvider` wrapping the app
- [ ] Adapter matches target chain (don't use WagmiAdapter for Solana)
- [ ] `createAppKit` called once at app initialization (not inside components)

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Project ID is required" | Missing projectId | Get one from dashboard.reown.com |
| Hydration mismatch (Next.js) | Missing SSR config | Add `ssr: true` to WagmiAdapter, use `cookieToInitialState` |
| Modal not appearing | `createAppKit` not called | Ensure it runs before app renders |
| Network not switching | Wrong network import | Use `@reown/appkit/networks`, not viem |
| Webpack error (Next.js) | Missing externals config | Add `pino-pretty`, `lokijs`, `encoding` to webpack externals |
| Provider undefined | Accessing before connection | Check `isConnected` before using provider |

## Examples

### Example 1 — React + Wagmi basic setup

```tsx
// config.ts
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'

export const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
export const networks = [mainnet, arbitrum, base]
export const wagmiAdapter = new WagmiAdapter({ networks, projectId })
export const metadata = {
  name: 'My dApp',
  description: 'My dApp description',
  url: 'https://mydapp.com',
  icons: ['https://mydapp.com/icon.png']
}

// App.tsx
import { createAppKit } from '@reown/appkit/react'
import { WagmiProvider } from 'wagmi'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { projectId, networks, wagmiAdapter, metadata } from './config'

const queryClient = new QueryClient()

createAppKit({
  adapters: [wagmiAdapter],
  networks,
  projectId,
  metadata,
  features: { analytics: true }
})

export default function App() {
  return (
    <WagmiProvider config={wagmiAdapter.wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <appkit-button />
      </QueryClientProvider>
    </WagmiProvider>
  )
}
```

### Example 2 — Vue + Ethers basic setup

```vue
<script lang="ts" setup>
import { createAppKit } from '@reown/appkit/vue'
import { EthersAdapter } from '@reown/appkit-adapter-ethers'
import { mainnet, arbitrum } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

createAppKit({
  adapters: [new EthersAdapter()],
  networks: [mainnet, arbitrum],
  projectId,
  metadata: {
    name: 'My Vue dApp',
    description: 'My Vue dApp',
    url: 'https://myapp.com',
    icons: ['https://myapp.com/icon.png']
  }
})
</script>

<template>
  <appkit-button />
</template>
```

## Evaluations

1. **Activation** — "I want to add wallet connection to my React app using Wagmi. How do I set up AppKit?"
2. **Non-activation** — "How do I build a mobile wallet with WalletConnect?" (use WalletKit, not AppKit)
3. **Edge case** — "I'm using Next.js and getting hydration mismatch errors with AppKit." (Answer: enable SSR flag, use cookieToInitialState)
4. **Framework choice** — "I have a Vue 3 app and want to support both Ethereum and Solana. What's the setup?" (Answer: Vue + Wagmi + Solana multichain)
5. **Adapter choice** — "Should I use Wagmi or Ethers for my React project?" (Answer: Wagmi recommended for most cases; Ethers if already using ethers.js)
6. **Edge case** — "My AppKit modal shows but wallet connection fails." (Answer: check projectId, metadata.url domain match, and network config)
