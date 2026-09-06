# React + Multichain

> Support EVM + Solana + Bitcoin (or any combination) in a single React app.

## Installation

Install AppKit plus all adapters you need:

```bash
# EVM + Solana
npm install @reown/appkit @reown/appkit-adapter-wagmi @reown/appkit-adapter-solana wagmi viem @tanstack/react-query

# EVM + Bitcoin
npm install @reown/appkit @reown/appkit-adapter-wagmi @reown/appkit-adapter-bitcoin wagmi viem @tanstack/react-query

# EVM + Solana + Bitcoin (all three)
npm install @reown/appkit @reown/appkit-adapter-wagmi @reown/appkit-adapter-solana @reown/appkit-adapter-bitcoin wagmi viem @tanstack/react-query
```

## Configuration — EVM + Solana

```tsx
import { createAppKit } from '@reown/appkit/react'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { SolanaAdapter } from '@reown/appkit-adapter-solana/react'
import { WagmiProvider } from 'wagmi'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  mainnet, arbitrum, base, optimism, polygon,
  solana, solanaTestnet, solanaDevnet
} from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
const queryClient = new QueryClient()

const networks = [mainnet, arbitrum, base, optimism, polygon, solana, solanaTestnet, solanaDevnet]

const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
})

const solanaAdapter = new SolanaAdapter()

createAppKit({
  adapters: [wagmiAdapter, solanaAdapter],
  networks,
  projectId,
  metadata: {
    name: 'My Multichain dApp',
    description: 'EVM + Solana dApp',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
  features: {
    analytics: true
  }
})

export default function App() {
  return (
    <WagmiProvider config={wagmiAdapter.wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <appkit-button />
        <YourAppContent />
      </QueryClientProvider>
    </WagmiProvider>
  )
}
```

## Configuration — EVM + Bitcoin

```tsx
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { BitcoinAdapter } from '@reown/appkit-adapter-bitcoin'
import {
  mainnet, arbitrum, base,
  bitcoin, bitcoinTestnet
} from '@reown/appkit/networks'

const wagmiAdapter = new WagmiAdapter({
  networks: [mainnet, arbitrum, base],
  projectId,
})

const bitcoinAdapter = new BitcoinAdapter({ projectId })

createAppKit({
  adapters: [wagmiAdapter, bitcoinAdapter],
  networks: [mainnet, arbitrum, base, bitcoin, bitcoinTestnet],
  projectId,
  metadata,
})
```

## Configuration — EVM + Solana + Bitcoin

```tsx
const wagmiAdapter = new WagmiAdapter({ networks: [mainnet, arbitrum, base], projectId })
const solanaAdapter = new SolanaAdapter()
const bitcoinAdapter = new BitcoinAdapter({ projectId })

createAppKit({
  adapters: [wagmiAdapter, solanaAdapter, bitcoinAdapter],
  networks: [mainnet, arbitrum, base, solana, bitcoin],
  projectId,
  metadata,
})
```

## Using Chain-Specific Providers

```tsx
import { useAppKitProvider, useAppKitAccount, useAppKitNetwork } from '@reown/appkit/react'

function MultichainInteraction() {
  const { address, isConnected } = useAppKitAccount()
  const { caipNetwork } = useAppKitNetwork()

  // EVM provider
  const { walletProvider: evmProvider } = useAppKitProvider<any>('eip155')
  // Solana provider
  const { walletProvider: solanaProvider } = useAppKitProvider<any>('solana')
  // Bitcoin provider
  const { walletProvider: btcProvider } = useAppKitProvider<any>('bip122')

  // Determine active chain namespace
  const activeNamespace = caipNetwork?.chainNamespace // 'eip155' | 'solana' | 'bip122'

  return (
    <div>
      <appkit-button />
      {isConnected && (
        <div>
          <p>Connected to: {caipNetwork?.name}</p>
          <p>Address: {address}</p>
          <p>Namespace: {activeNamespace}</p>
        </div>
      )}
    </div>
  )
}
```

## Important Notes

- `WagmiProvider` and `QueryClientProvider` are still required when using the Wagmi adapter, even in multichain setups
- The modal automatically shows all supported networks and lets users switch between chains
- Each adapter handles its own chain namespace independently
- `useAppKitAccount` returns the currently active account regardless of chain
