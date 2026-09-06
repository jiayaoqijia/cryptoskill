# Next.js + Wagmi

> Most common setup for Next.js dApps. Requires SSR-specific configuration.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem @tanstack/react-query
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

## Step 2 — AppKit Config (no 'use client')

```tsx
// config/index.tsx
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'
import type { AppKitNetwork } from '@reown/appkit/networks'

export const projectId = process.env.NEXT_PUBLIC_PROJECT_ID || 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

export const networks: [AppKitNetwork, ...AppKitNetwork[]] = [
  mainnet, arbitrum, base
]

export const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
  ssr: true,  // Required for Next.js
})

export const metadata = {
  name: 'My Next.js dApp',
  description: 'Next.js dApp with AppKit',
  url: 'https://mydapp.com',       // Must match your domain
  icons: ['https://mydapp.com/icon.png']
}
```

## Step 3 — Context Provider

```tsx
// context/index.tsx
'use client'

import { createAppKit } from '@reown/appkit/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React, { type ReactNode } from 'react'
import { cookieToInitialState, WagmiProvider, type Config } from 'wagmi'
import { projectId, networks, wagmiAdapter, metadata } from '@/config'

const queryClient = new QueryClient()

const modal = createAppKit({
  adapters: [wagmiAdapter],
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

## Step 5 — Page Component

```tsx
// app/page.tsx
'use client'

import { useAppKit, useAppKitAccount, useAppKitNetwork } from '@reown/appkit/react'

export default function Home() {
  const { open } = useAppKit()
  const { address, isConnected } = useAppKitAccount()
  const { caipNetwork } = useAppKitNetwork()

  return (
    <main>
      <appkit-button />
      {isConnected && (
        <div>
          <p>Address: {address}</p>
          <p>Network: {caipNetwork?.name}</p>
        </div>
      )}
    </main>
  )
}
```

## SSR Checklist

- [ ] `ssr: true` in WagmiAdapter constructor
- [ ] `cookieToInitialState` used in the context provider
- [ ] Cookies passed from server layout to client provider
- [ ] Webpack externals configured for `pino-pretty`, `lokijs`, `encoding`
- [ ] Config file does NOT have `'use client'` directive
- [ ] Context provider file has `'use client'` directive
- [ ] `metadata.url` matches your deployment domain

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_PROJECT_ID=b56e18d47c72ab683b10814fe9495694 # localhost testing only
```

## Smart Contract Interaction

Same as React + Wagmi — use Wagmi hooks (`useReadContract`, `useWriteContract`, etc.) in client components.
