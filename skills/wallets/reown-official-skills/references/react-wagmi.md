# React + Wagmi

> Most common setup for EVM dApps with React.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem @tanstack/react-query
```

## Configuration

```tsx
// config.ts
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum, base, optimism, polygon } from '@reown/appkit/networks'
import type { AppKitNetwork } from '@reown/appkit/networks'

export const projectId = process.env.NEXT_PUBLIC_PROJECT_ID || 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

export const networks: [AppKitNetwork, ...AppKitNetwork[]] = [
  mainnet, arbitrum, base, optimism, polygon
]

export const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
})

export const metadata = {
  name: 'My dApp',
  description: 'My dApp description',
  url: 'https://mydapp.com',       // Must match your domain
  icons: ['https://mydapp.com/icon.png']
}
```

```tsx
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

## Using Hooks

```tsx
import { useAppKit, useAppKitAccount, useAppKitNetwork } from '@reown/appkit/react'
import { useDisconnect } from '@reown/appkit/react'

function WalletInfo() {
  const { open } = useAppKit()
  const { address, isConnected, caipAddress } = useAppKitAccount()
  const { caipNetwork, chainId, switchNetwork } = useAppKitNetwork()
  const { disconnect } = useDisconnect()

  if (!isConnected) {
    return <button onClick={() => open()}>Connect Wallet</button>
  }

  return (
    <div>
      <p>Address: {address}</p>
      <p>Chain: {caipNetwork?.name} ({chainId})</p>
      <button onClick={() => open({ view: 'Networks' })}>Switch Network</button>
      <button onClick={() => disconnect()}>Disconnect</button>
    </div>
  )
}
```

## Smart Contract Interaction (Wagmi hooks)

```tsx
import { useReadContract, useWriteContract, useWaitForTransactionReceipt } from 'wagmi'

function ContractInteraction() {
  // Read
  const { data: balance } = useReadContract({
    address: '0x...',
    abi: erc20Abi,
    functionName: 'balanceOf',
    args: ['0x...'],
  })

  // Write
  const { writeContract, data: hash } = useWriteContract()
  const { isLoading, isSuccess } = useWaitForTransactionReceipt({ hash })

  const handleTransfer = () => {
    writeContract({
      address: '0x...',
      abi: erc20Abi,
      functionName: 'transfer',
      args: ['0x...', parseEther('1')],
    })
  }

  return (
    <div>
      <p>Balance: {balance?.toString()}</p>
      <button onClick={handleTransfer} disabled={isLoading}>
        {isLoading ? 'Confirming...' : 'Transfer'}
      </button>
      {isSuccess && <p>Transaction confirmed!</p>}
    </div>
  )
}
```

## Sign Message

```tsx
import { useSignMessage } from 'wagmi'

function SignMessage() {
  const { signMessage, data: signature } = useSignMessage()

  return (
    <div>
      <button onClick={() => signMessage({ message: 'Hello AppKit!' })}>
        Sign Message
      </button>
      {signature && <p>Signature: {signature}</p>}
    </div>
  )
}
```

## Send Transaction

```tsx
import { useSendTransaction } from 'wagmi'
import { parseEther } from 'viem'

function SendTransaction() {
  const { sendTransaction, data: hash } = useSendTransaction()

  return (
    <button onClick={() => sendTransaction({
      to: '0x...',
      value: parseEther('0.01'),
    })}>
      Send 0.01 ETH
    </button>
  )
}
```
