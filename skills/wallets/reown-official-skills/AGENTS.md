# AppKit Web Examples

This repository contains example projects for integrating [Reown AppKit](https://docs.reown.com/appkit/overview) - an all-in-one SDK for Web3 wallet connections, transactions, and authentication.

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

## Project Structure

```
AGENTS.md           # This file (symlinked as CLAUDE.md)
SKILL.md            # Comprehensive integration guide
references/         # Per-framework + adapter reference docs
  react-wagmi.md
  react-ethers.md
  react-solana.md
  react-bitcoin.md
  react-multichain.md
  nextjs-wagmi.md
  nextjs-ethers.md
  nextjs-solana.md
  nextjs-multichain.md
  vue-wagmi.md
  vue-ethers.md
  vue-solana.md
  vue-multichain.md
  nuxt-wagmi.md
  svelte-wagmi.md
  javascript-wagmi.md
  javascript-ethers.md
  javascript-solana.md
  javascript-multichain.md
```

### Blockchain Adapters

| Adapter | Description | Key Package |
|---------|-------------|-------------|
| `wagmi` | Multi-chain EVM (recommended) | `@reown/appkit-adapter-wagmi` |
| `ethers` | Ethers.js v6 integration | `@reown/appkit-adapter-ethers` |
| `solana` | Solana blockchain | `@reown/appkit-adapter-solana` |
| `bitcoin` | Bitcoin blockchain | `@reown/appkit-adapter-bitcoin` |
| `multichain` | Combined wagmi + Solana | Multiple adapters |

## Features support
- Email Login
- Social logins ( Google, X, Github, Discord, Apple, Facebook, Farcaster)
- SIWX (Sign in with EVM, Solana or Bitcoin)
- Pay with Exchange
- Deposit with Exchange
- Wallet Buttons (use it with `<appkit-wallet-button  />` or `useAppKitWallet`)
- Headless (build your own modal, only for enterprise clients)

## Project ID

The examples use `b56e18d47c72ab683b10814fe9495694`, a public projectId for **localhost testing only**. For production, create your own at [dashboard.reown.com](https://dashboard.reown.com).

## Quick Start Pattern

### 1. Install Dependencies

```bash
npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem @tanstack/react-query
```

### 2. Configure AppKit

```typescript
// config/index.tsx
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // Public projectId for localhost only — get your own at https://cloud.reown.com for production

export const networks = [mainnet, arbitrum]

export const wagmiAdapter = new WagmiAdapter({
  projectId,
  networks
})
```

### 3. Initialize AppKit

```typescript
// main.tsx or App.tsx
import { createAppKit } from '@reown/appkit/react'
import { wagmiAdapter, networks } from './config'

createAppKit({
  adapters: [wagmiAdapter],
  networks,
  projectId: 'b56e18d47c72ab683b10814fe9495694', // localhost testing only
  metadata: {
    name: 'My App',
    description: 'My App Description',
    url: 'https://myapp.com',
    icons: ['https://myapp.com/icon.png']
  }
})
```

### 4. Wrap Your App

```tsx
// React
import { WagmiProvider } from 'wagmi'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

function App() {
  return (
    <WagmiProvider config={wagmiAdapter.wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <YourApp />
      </QueryClientProvider>
    </WagmiProvider>
  )
}
```

### 5. Use AppKit Components

```tsx
// Connect button (opens modal)
<appkit-button />

// Or use hooks
import { useAppKit } from '@reown/appkit/react'

function ConnectButton() {
  const { open } = useAppKit()
  return <button onClick={() => open()}>Connect Wallet</button>
}
```

## Common File Structure

```
src/
├── config/
│   └── index.tsx         # AppKit & adapter configuration
├── components/
│   ├── ActionButtonList  # Wallet action buttons
│   └── InfoList          # Display wallet info
├── App.tsx               # Main app component
└── main.tsx              # Entry point with providers
```

## Key Hooks (React/Vue)

```typescript
import { useAppKit, useAppKitAccount, useAppKitNetwork } from '@reown/appkit/react'

// Modal controls
const { open, close } = useAppKit()

// Account state
const { address, isConnected, caipAddress } = useAppKitAccount()

// Network state
const { chainId, caipNetwork } = useAppKitNetwork()
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
const modal = createAppKit({
  adapters: [wagmiAdapter],
  projectId,
  networks: [mainnet, arbitrum],
  metadata,
  features: {
    email: true, // default to true
    socials: [
      "google",
      "x",
      "github",
      "discord",
      "apple",
      "facebook",
      "farcaster",
    ],
    emailShowWallets: true, // default to true
  },
  allWallets: "SHOW", // default to SHOW
});

## Social login and email setup
You can delete or change the order for the socials.

```
const modal = createAppKit({
  adapters: [wagmiAdapter],
  projectId,
  networks: [mainnet, arbitrum],
  metadata,
  features: {
    email: true, // default to true
    socials: [
      "google",
      "x",
      "github",
      "discord",
      "apple",
      "facebook",
      "farcaster",
    ],
    emailShowWallets: true, // default to true
  },
  allWallets: "SHOW", // default to SHOW
});
```

## Framework-Specific Notes

### React
- Uses Vite for development
- Requires `WagmiProvider` + `QueryClientProvider`

### Vue
- Uses `@wagmi/vue` for Vue-specific hooks
- Uses `@tanstack/vue-query` for queries

### Next.js
- Configuration must be in a Client Component (`'use client'`)
- Uses App Router pattern with `layout.tsx` providers

### Vanilla JavaScript
- Uses `@wagmi/core` instead of React hooks
- Direct DOM manipulation for UI updates

## Environment Variables

Create `.env` or `.env.local`:

```
VITE_PROJECT_ID=b56e18d47c72ab683b10814fe9495694 # localhost testing only
# or for Next.js
NEXT_PUBLIC_PROJECT_ID=b56e18d47c72ab683b10814fe9495694 # localhost testing only
```

## Running Examples
always use pnpm if available

```bash
cd react/react-wagmi  # or any example
pnpm install
pnpm  dev
```

## Resources

- [AppKit Web Examples](https://github.com/reown-com/appkit-web-examples) — repository with working examples for every framework + adapter combination
- [AppKit Docs](https://docs.reown.com/appkit/overview)
- [React Quickstart](https://docs.reown.com/appkit/react/core/installation)
- [Next.js Quickstart](https://docs.reown.com/appkit/next/core/installation)
- [Vue Quickstart](https://docs.reown.com/appkit/vue/core/installation)
- [JavaScript Quickstart](https://docs.reown.com/appkit/javascript/core/installation)
- [Dashboard (get projectId)](https://dashboard.reown.com/)

## Supported Networks

Import networks from `@reown/appkit/networks`:

```typescript
import { mainnet, arbitrum, optimism, polygon, solana } from '@reown/appkit/networks'
```


---

## Important Reminders

1. **Call `createAppKit()` outside component render cycles** - It should be called at module level, not inside components

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

2. **Use `'use client'` directive** in Next.js for components using hooks or AppKit initialization
3. **Enable `ssr: true`** in WagmiAdapter for Next.js projects
4. **Await `headers()` call** in Next.js App Router layouts
5. **Import networks from `@reown/appkit/networks`** - not from wagmi or viem
6. **Use the typed network array pattern**: `as [AppKitNetwork, ...AppKitNetwork[]]`
7. **Never hardcode production projectIds** - always use environment variables. The projectId `b56e18d47c72ab683b10814fe9495694` is a public ID that only works on localhost — for production, get your own at dashboard.reown.com
8. **All Reown packages should be in the same version** - use the same version for all Reown packages
9. **Wagmi OR Ethers — never both** - Both register the EVM (`eip155`) namespace; using both causes conflicts

```typescript
// DO — one EVM adapter
createAppKit({ adapters: [wagmiAdapter, solanaAdapter], ... })

// DON'T — two EVM adapters
createAppKit({ adapters: [wagmiAdapter, ethersAdapter], ... }) // CONFLICT
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Project ID is required" | Missing projectId | Get one from dashboard.reown.com |
| Hydration mismatch (Next.js) | Missing SSR config | Add `ssr: true` to WagmiAdapter, use `cookieToInitialState` |
| Modal not appearing | `createAppKit` not called | Ensure it runs before app renders |
| Network not switching | Wrong network import | Use `@reown/appkit/networks`, not viem |
| Webpack error (Next.js) | Missing externals config | Add `pino-pretty`, `lokijs`, `encoding` to webpack externals |
| Provider undefined | Accessing before connection | Check `isConnected` before using provider |

## Validation Checklist

- [ ] `projectId` obtained from dashboard.reown.com
- [ ] `metadata.url` matches your actual domain (wallets verify this)
- [ ] Networks imported from `@reown/appkit/networks` (not from viem/wagmi directly)
- [ ] For Next.js: SSR flag set, cookie hydration implemented, webpack externals configured
- [ ] For Wagmi: `WagmiProvider` and `QueryClientProvider` wrapping the app
- [ ] Adapter matches target chain (don't use WagmiAdapter for Solana)
- [ ] `createAppKit` called once at app initialization (not inside components)
- [ ] Add your domain to dashboard.reown.com
