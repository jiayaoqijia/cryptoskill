# Next.js + Multichain

> Support EVM + Solana + Bitcoin in a single Next.js app with SSR.

## Installation

```bash
# EVM + Solana
npm install @reown/appkit @reown/appkit-adapter-wagmi @reown/appkit-adapter-solana wagmi viem @tanstack/react-query

# EVM + Bitcoin
npm install @reown/appkit @reown/appkit-adapter-wagmi @reown/appkit-adapter-bitcoin wagmi viem @tanstack/react-query
```

## Step 1 — Webpack Config

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    config.externals.push('pino-pretty', 'lokijs', 'encoding')
    return config
  },
}

module.exports = nextConfig
```

## Step 2 — Config

```tsx
// config/index.tsx
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import {
  mainnet, arbitrum, base,
  solana, solanaTestnet, solanaDevnet
} from '@reown/appkit/networks'
import type { AppKitNetwork } from '@reown/appkit/networks'

export const projectId = process.env.NEXT_PUBLIC_PROJECT_ID || 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

export const networks: [AppKitNetwork, ...AppKitNetwork[]] = [
  mainnet, arbitrum, base, solana, solanaTestnet, solanaDevnet
]

export const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
  ssr: true,
})

export const metadata = {
  name: 'My Multichain dApp',
  description: 'Next.js Multichain dApp',
  url: 'https://mydapp.com',
  icons: ['https://mydapp.com/icon.png']
}
```

## Step 3 — Context Provider

```tsx
// context/index.tsx
'use client'

import { createAppKit } from '@reown/appkit/react'
import { SolanaAdapter } from '@reown/appkit-adapter-solana/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React, { type ReactNode } from 'react'
import { cookieToInitialState, WagmiProvider, type Config } from 'wagmi'
import { projectId, networks, wagmiAdapter, metadata } from '@/config'

const queryClient = new QueryClient()
const solanaAdapter = new SolanaAdapter()

createAppKit({
  adapters: [wagmiAdapter, solanaAdapter],
  networks,
  projectId,
  metadata,
  features: {
    analytics: true
  }
})

export default function ContextProvider({
  children,
  cookies,
}: {
  children: ReactNode
  cookies: string | null
}) {
  const initialState = cookieToInitialState(
    wagmiAdapter.wagmiConfig as Config,
    cookies
  )

  return (
    <WagmiProvider
      config={wagmiAdapter.wagmiConfig as Config}
      initialState={initialState}
    >
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  )
}
```

## Step 4 — Root Layout

```tsx
// app/layout.tsx
import { headers } from 'next/headers'
import ContextProvider from '@/context'

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const headersList = await headers()
  const cookies = headersList.get('cookie')

  return (
    <html lang="en">
      <body>
        <ContextProvider cookies={cookies}>
          {children}
        </ContextProvider>
      </body>
    </html>
  )
}
```

## Adding Bitcoin

```tsx
// Add to context/index.tsx
import { BitcoinAdapter } from '@reown/appkit-adapter-bitcoin'
import { bitcoin, bitcoinTestnet } from '@reown/appkit/networks'

const bitcoinAdapter = new BitcoinAdapter({ projectId })

createAppKit({
  adapters: [wagmiAdapter, solanaAdapter, bitcoinAdapter],
  networks: [...networks, bitcoin, bitcoinTestnet],
  // ...rest
})
```
