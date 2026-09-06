# Next.js + Solana

> Connect Solana wallets in Next.js apps.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-solana
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
import { SolanaAdapter } from '@reown/appkit-adapter-solana/react'
import { solana, solanaTestnet, solanaDevnet } from '@reown/appkit/networks'
import React, { type ReactNode } from 'react'

const projectId = process.env.NEXT_PUBLIC_PROJECT_ID || 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

const solanaAdapter = new SolanaAdapter()

createAppKit({
  adapters: [solanaAdapter],
  networks: [solana, solanaTestnet, solanaDevnet],
  projectId,
  metadata: {
    name: 'My Solana dApp',
    description: 'Next.js Solana dApp',
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

## Step 3 — Root Layout

```tsx
// app/layout.tsx
import ContextProvider from '@/context'

export default function RootLayout({ children }: { children: React.ReactNode }) {
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
import { Connection, PublicKey, LAMPORTS_PER_SOL } from '@solana/web3.js'

export default function Home() {
  const { walletProvider } = useAppKitProvider<any>('solana')
  const { address, isConnected } = useAppKitAccount()

  async function getBalance() {
    if (!address) return
    const connection = new Connection('https://api.mainnet-beta.solana.com')
    const balance = await connection.getBalance(new PublicKey(address))
    console.log('Balance:', balance / LAMPORTS_PER_SOL, 'SOL')
  }

  return (
    <main>
      <appkit-button />
      {isConnected && <button onClick={getBalance}>Get Balance</button>}
    </main>
  )
}
```

Note: Solana adapter does not require cookie hydration or `WagmiProvider`. The webpack externals are still needed for AppKit internals.
