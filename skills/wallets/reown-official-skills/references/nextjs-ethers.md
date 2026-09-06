# Next.js + Ethers v6

> Use when you prefer ethers.js over Wagmi in a Next.js app.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-ethers ethers
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

## Step 2 — Context Provider

```tsx
// context/index.tsx
'use client'

import { createAppKit } from '@reown/appkit/react'
import { EthersAdapter } from '@reown/appkit-adapter-ethers'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'
import React, { type ReactNode } from 'react'

const projectId = process.env.NEXT_PUBLIC_PROJECT_ID || 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

createAppKit({
  adapters: [new EthersAdapter()],
  networks: [mainnet, arbitrum, base],
  projectId,
  metadata: {
    name: 'My Next.js dApp',
    description: 'Next.js dApp with Ethers',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
  features: {
    analytics: true
  }
})

export default function ContextProvider({ children }: { children: ReactNode }) {
  return <>{children}</>
}
```

Note: Ethers adapter does **not** require `WagmiProvider`, `QueryClientProvider`, or cookie hydration. SSR setup is simpler.

## Step 3 — Root Layout

```tsx
// app/layout.tsx
import ContextProvider from '@/context'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <ContextProvider>{children}</ContextProvider>
      </body>
    </html>
  )
}
```

## Step 4 — Page Component

```tsx
// app/page.tsx
'use client'

import { useAppKitProvider, useAppKitAccount } from '@reown/appkit/react'
import { BrowserProvider, Contract, formatEther } from 'ethers'
import type { Provider } from '@reown/appkit/react'

export default function Home() {
  const { walletProvider } = useAppKitProvider<Provider>('eip155')
  const { address, isConnected } = useAppKitAccount()

  async function getBalance() {
    if (!walletProvider) return
    const provider = new BrowserProvider(walletProvider)
    const balance = await provider.getBalance(address!)
    console.log(formatEther(balance))
  }

  return (
    <main>
      <appkit-button />
      {isConnected && (
        <button onClick={getBalance}>Get Balance</button>
      )}
    </main>
  )
}
```

## Key Differences from Next.js + Wagmi

| Aspect | Wagmi | Ethers |
|--------|-------|--------|
| Cookie hydration | Required | Not needed |
| Providers | `WagmiProvider` + `QueryClientProvider` | None |
| SSR config | `ssr: true` + `cookieToInitialState` | Just webpack externals |
| Contract interaction | Wagmi hooks | Manual `BrowserProvider` + `Contract` |
