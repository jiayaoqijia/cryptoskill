# React + Bitcoin

> Connect Bitcoin wallets in React apps.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-bitcoin
```

## Configuration

```tsx
import { createAppKit } from '@reown/appkit/react'
import { BitcoinAdapter } from '@reown/appkit-adapter-bitcoin'
import { bitcoin, bitcoinTestnet, bitcoinSignet } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
const networks = [bitcoin, bitcoinTestnet, bitcoinSignet]

const bitcoinAdapter = new BitcoinAdapter({
  projectId
})

createAppKit({
  adapters: [bitcoinAdapter],
  networks,
  projectId,
  metadata: {
    name: 'My Bitcoin dApp',
    description: 'Bitcoin dApp with AppKit',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
  features: {
    analytics: true,
    email: false,
    socials: []
  }
})

export default function App() {
  return (
    <div>
      <appkit-button />
      <YourAppContent />
    </div>
  )
}
```

Note: Bitcoin adapter does **not** require `WagmiProvider` or `QueryClientProvider`. Email and social login features are not available for Bitcoin.

## Using Hooks

```tsx
import { useAppKitProvider, useAppKitAccount } from '@reown/appkit/react'

function BitcoinInteraction() {
  const { walletProvider } = useAppKitProvider<any>('bip122')
  const { address, isConnected } = useAppKitAccount()

  async function signMessage() {
    if (!walletProvider) return
    const signature = await walletProvider.signMessage({
      address,
      message: 'Hello Bitcoin!',
    })
    console.log('Signature:', signature)
  }

  async function sendBitcoin() {
    if (!walletProvider) return
    const txId = await walletProvider.sendTransfer({
      recipient: 'bc1q...',
      amount: '1000', // satoshis
    })
    console.log('TX ID:', txId)
  }

  if (!isConnected) return <appkit-button />

  return (
    <div>
      <p>Address: {address}</p>
      <button onClick={signMessage}>Sign Message</button>
      <button onClick={sendBitcoin}>Send BTC</button>
    </div>
  )
}
```
