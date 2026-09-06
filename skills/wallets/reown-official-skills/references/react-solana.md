# React + Solana

> Connect Solana wallets (Phantom, Solflare, etc.) in React apps.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-solana
```

## Configuration

```tsx
import { createAppKit } from '@reown/appkit/react'
import { SolanaAdapter } from '@reown/appkit-adapter-solana/react'
import { solana, solanaTestnet, solanaDevnet } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

const solanaAdapter = new SolanaAdapter()

createAppKit({
  adapters: [solanaAdapter],
  networks: [solana, solanaTestnet, solanaDevnet],
  projectId,
  metadata: {
    name: 'My Solana dApp',
    description: 'Solana dApp with AppKit',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
  features: {
    analytics: true
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

Note: Solana adapter does **not** require `WagmiProvider` or `QueryClientProvider`.

## Adapter Options

```tsx
import { HuobiWalletAdapter } from '@solana/wallet-adapter-wallets'

const solanaAdapter = new SolanaAdapter({
  // Register WalletConnect as a Wallet Standard option
  registerWalletStandard: true,
  // Add custom wallet adapters
  wallets: [new HuobiWalletAdapter()]
})
```

## Using Hooks

```tsx
import { useAppKitProvider, useAppKitAccount, useAppKitConnection } from '@reown/appkit/react'
import { Connection, PublicKey, SystemProgram, Transaction, LAMPORTS_PER_SOL } from '@solana/web3.js'

function SolanaInteraction() {
  const { walletProvider } = useAppKitProvider<any>('solana')
  const { address, isConnected } = useAppKitAccount()

  async function getBalance() {
    if (!address) return
    const connection = new Connection('https://api.mainnet-beta.solana.com')
    const pubkey = new PublicKey(address)
    const balance = await connection.getBalance(pubkey)
    console.log('Balance:', balance / LAMPORTS_PER_SOL, 'SOL')
  }

  async function signMessage() {
    if (!walletProvider) return
    const encodedMessage = new TextEncoder().encode('Hello Solana!')
    const signature = await walletProvider.signMessage(encodedMessage)
    console.log('Signature:', signature)
  }

  async function sendTransaction() {
    if (!walletProvider || !address) return
    const connection = new Connection('https://api.mainnet-beta.solana.com')
    const pubkey = new PublicKey(address)

    const transaction = new Transaction().add(
      SystemProgram.transfer({
        fromPubkey: pubkey,
        toPubkey: new PublicKey('RECIPIENT_ADDRESS'),
        lamports: 0.01 * LAMPORTS_PER_SOL,
      })
    )

    transaction.feePayer = pubkey
    transaction.recentBlockhash = (
      await connection.getLatestBlockhash()
    ).blockhash

    const signedTx = await walletProvider.signTransaction(transaction)
    const txId = await connection.sendRawTransaction(signedTx.serialize())
    console.log('TX ID:', txId)
  }

  if (!isConnected) return <appkit-button />

  return (
    <div>
      <button onClick={getBalance}>Get Balance</button>
      <button onClick={signMessage}>Sign Message</button>
      <button onClick={sendTransaction}>Send SOL</button>
    </div>
  )
}
```
